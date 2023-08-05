import os
import time
import shutil
from collections import OrderedDict, Counter

import copy

from conans.client import packager
from conans.client.client_cache import ClientCache
from conans.client.deps_builder import DepsGraphBuilder
from conans.client.detect import detected_os
from conans.client.export import export_conanfile, load_export_conanfile
from conans.client.generators import write_generators
from conans.client.generators.text import TXTGenerator
from conans.client.importer import run_imports, undo_imports
from conans.client.installer import ConanInstaller, BuildMode
from conans.client.loader import ConanFileLoader
from conans.client.manifest_manager import ManifestManager
from conans.client.output import ScopedOutput, Color
from conans.client.package_copier import PackageCopier
from conans.client.printer import Printer
from conans.client.profile_loader import read_conaninfo_profile
from conans.client.proxy import ConanProxy
from conans.client.remote_registry import RemoteRegistry
from conans.client.remover import ConanRemover
from conans.client.require_resolver import RequireResolver
from conans.client.source import config_source, config_source_local
from conans.client.uploader import ConanUploader
from conans.client.userio import UserIO
from conans.errors import NotFoundException, ConanException, conanfile_exception_formatter
from conans.model.ref import ConanFileReference, PackageReference
from conans.paths import CONANFILE, CONANINFO, CONANFILE_TXT, CONAN_MANIFEST, BUILD_INFO
from conans.tools import environment_append
from conans.util.files import save,  rmdir, normalize, mkdir, load
from conans.util.log import logger
from conans.model.manifest import FileTreeManifest
from conans.client.loader_parse import load_conanfile_class
from conans.client.build_requires import BuildRequires
from conans.client.linter import conan_linter
from conans.search.search import filter_outdated


class ConanManager(object):
    """ Manage all the commands logic  The main entry point for all the client
    business logic
    """
    def __init__(self, client_cache, user_io, runner, remote_manager, search_manager,
                 settings_preprocessor):
        assert isinstance(user_io, UserIO)
        assert isinstance(client_cache, ClientCache)
        self._client_cache = client_cache
        self._user_io = user_io
        self._runner = runner
        self._remote_manager = remote_manager
        self._current_scopes = None
        self._search_manager = search_manager
        self._settings_preprocessor = settings_preprocessor

    def load_consumer_conanfile(self, conanfile_path, current_path, output, reference=None,
                                deps_cpp_info_required=False):

        profile = read_conaninfo_profile(current_path) or self._client_cache.default_profile
        loader = self.get_loader(profile)
        if conanfile_path.endswith(".py"):
            consumer = not reference
            conanfile = loader.load_conan(conanfile_path, output, consumer, reference)
        else:
            conanfile = loader.load_conan_txt(conanfile_path, output)
        if deps_cpp_info_required is not None:
            _load_deps_cpp_info(current_path, conanfile, required=deps_cpp_info_required)
        return conanfile

    def get_loader(self, profile):
        return ConanFileLoader(self._runner, self._get_settings(profile),
                               self._profile_with_defaults(profile))

    def _get_settings(self, profile):
        self._client_cache.settings.values = self._profile_with_defaults(profile).settings_values
        # Settings preprocessor
        self._settings_preprocessor.preprocess(self._client_cache.settings)
        return self._client_cache.settings

    def _profile_with_defaults(self, profile):
        # Get the defaults, and apply on it the profile
        tmp_profile = copy.copy(self._client_cache.default_profile)
        tmp_profile.update(profile)
        return tmp_profile

    def export(self, user, channel, conan_file_path, keep_source=False, filename=None, name=None,
               version=None):
        """ Export the conans
        param conanfile_path: the original source directory of the user containing a
                           conanfile.py
        param user: user under this package will be exported
        param channel: string (stable, testing,...)
        """
        assert conan_file_path
        logger.debug("Exporting %s" % conan_file_path)

        src_folder = conan_file_path
        conanfile_name = filename or CONANFILE
        conan_file_path = os.path.join(conan_file_path, conanfile_name)
        if ((os.path.exists(conan_file_path) and conanfile_name not in os.listdir(src_folder)) or
                (conanfile_name != "conanfile.py" and conanfile_name.lower() == "conanfile.py")):
            raise ConanException("Wrong '%s' case" % conanfile_name)
        conan_linter(conan_file_path, self._user_io.out)
        conanfile = load_export_conanfile(conan_file_path, self._user_io.out, name, version)
        conan_ref = ConanFileReference(conanfile.name, conanfile.version, user, channel)
        conan_ref_str = str(conan_ref)
        # Maybe a platform check could be added, but depends on disk partition
        refs = self._search_manager.search(conan_ref_str, ignorecase=True)
        if refs and conan_ref not in refs:
            raise ConanException("Cannot export package with same name but different case\n"
                                 "You exported '%s' but already existing '%s'"
                                 % (conan_ref_str, " ".join(str(s) for s in refs)))
        output = ScopedOutput(str(conan_ref), self._user_io.out)
        export_conanfile(output, self._client_cache, conanfile, src_folder, conan_ref, keep_source,
                         filename)

    def package_files(self, reference, source_folder, build_folder, package_folder, profile,
                      force):
        """ Bundle pre-existing binaries
        @param reference: ConanFileReference
        """
        conan_file_path = self._client_cache.conanfile(reference)
        if not os.path.exists(conan_file_path):
            raise ConanException("Package recipe '%s' does not exist" % str(reference))

        current_path = package_folder
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager,
                                  remote_name=None, update=False, check_updates=False,
                                  manifest_manager=None)

        loader = self.get_loader(profile)
        conanfile = loader.load_virtual([reference], current_path)
        graph_builder = self._get_graph_builder(loader, False, remote_proxy)
        deps_graph = graph_builder.load(conanfile)

        # this is a bit tricky, but works. The loading of a cache package makes the referenced
        # one, the first of the first level, always existing
        nodes = deps_graph.direct_requires()
        _, conanfile = nodes[0]
        pkg_id = conanfile.info.package_id()
        self._user_io.out.info("Packaging to %s" % pkg_id)
        pkg_reference = PackageReference(reference, pkg_id)
        dest_package_folder = self._client_cache.package(pkg_reference,
                                                         short_paths=conanfile.short_paths)

        if os.path.exists(dest_package_folder):
            if force:
                rmdir(dest_package_folder)
            else:
                raise ConanException("Package already exists. Please use --force, -f to overwrite it")

        recipe_hash = self._client_cache.load_manifest(reference).summary_hash
        conanfile.info.recipe_hash = recipe_hash
        if source_folder or build_folder:
            package_output = ScopedOutput(str(reference), self._user_io.out)
            packager.create_package(conanfile, source_folder, build_folder, dest_package_folder,
                                    package_output, local=True)
        else:  # we are specifying a final package
            shutil.copytree(package_folder, dest_package_folder, symlinks=True)
            save(os.path.join(dest_package_folder, CONANINFO), conanfile.info.dumps())
            # Create the digest for the package
            digest = FileTreeManifest.create(dest_package_folder)
            save(os.path.join(dest_package_folder, CONAN_MANIFEST), str(digest))

    def download(self, reference, package_ids, remote=None):
        """ Download conanfile and specified packages to local repository
        @param reference: ConanFileReference
        @param package_ids: Package ids or empty for download all
        @param remote: install only from that remote
        """
        assert(isinstance(reference, ConanFileReference))
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)

        package = remote_proxy.search(reference, None)
        if not package:  # Search the reference first, and raise if it doesn't exist
            raise ConanException("'%s' not found in remote" % str(reference))

        if package_ids:
            remote_proxy.download_packages(reference, package_ids)
        else:
            packages_props = remote_proxy.search_packages(reference, None)
            if not packages_props:
                output = ScopedOutput(str(reference), self._user_io.out)
                output.warn("No remote binary packages found in remote")
            else:
                remote_proxy.download_packages(reference, list(packages_props.keys()))

    def _get_conanfile_object(self, loader, reference_or_path, conanfile_filename, current_path):
        if isinstance(reference_or_path, ConanFileReference):
            conanfile = loader.load_virtual([reference_or_path], current_path)
        else:
            output = ScopedOutput("PROJECT", self._user_io.out)
            try:
                if conanfile_filename and conanfile_filename.endswith(".txt"):
                    raise NotFoundException("")
                conan_file_path = os.path.join(reference_or_path, conanfile_filename or CONANFILE)
                conanfile = loader.load_conan(conan_file_path, output, consumer=True)
            except NotFoundException:  # Load conanfile.txt
                conan_path = os.path.join(reference_or_path, conanfile_filename or CONANFILE_TXT)
                conanfile = loader.load_conan_txt(conan_path, output)

        return conanfile

    def _inject_require(self, conanfile, inject_require):
        """ test_package functionality requires injecting the tested package as requirement
        before running the install
        """
        require = conanfile.requires.get(inject_require.name)
        if require:
            require.conan_reference = require.range_reference = inject_require
        else:
            conanfile.requires(str(inject_require))

    def _get_graph_builder(self, loader, update, remote_proxy):
        local_search = None if update else self._search_manager
        resolver = RequireResolver(self._user_io.out, local_search, remote_proxy)
        graph_builder = DepsGraphBuilder(remote_proxy, self._user_io.out, loader, resolver)
        return graph_builder

    def _get_deps_graph(self, reference, profile, filename, current_path, remote_proxy):
        loader = self.get_loader(profile)
        conanfile = self._get_conanfile_object(loader, reference, filename, current_path)
        graph_builder = self._get_graph_builder(loader, False, remote_proxy)
        deps_graph = graph_builder.load(conanfile)
        return deps_graph, graph_builder, conanfile

    def info_build_order(self, reference, profile, filename, build_order, remote, check_updates, cwd):
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote,
                                  update=False, check_updates=check_updates)
        deps_graph, _, _ = self._get_deps_graph(reference, profile, filename, cwd, remote_proxy)
        result = deps_graph.build_order(build_order)
        return result

    def info_nodes_to_build(self, reference, profile, filename, build_modes, remote, check_updates, cwd):
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote,
                                  update=False, check_updates=check_updates)
        deps_graph, _, conanfile = self._get_deps_graph(reference, profile, filename, cwd, remote_proxy)
        build_mode = BuildMode(build_modes, self._user_io.out)
        installer = ConanInstaller(self._client_cache, self._user_io.out, remote_proxy, build_mode,
                                   None)
        nodes = installer.nodes_to_build(deps_graph)
        counter = Counter(ref.conan.name for ref, _ in nodes)
        ret = [ref if counter[ref.conan.name] > 1 else str(ref.conan) for ref, _ in nodes]
        return ret, self._get_project_reference(reference, conanfile)

    def _get_project_reference(self, reference, conanfile):
        if isinstance(reference, ConanFileReference):
            project_reference = None
        else:
            project_reference = str(conanfile)

        return project_reference

    def info_get_graph(self, reference, current_path, profile, remote=None, filename=None, check_updates=False):
        """ Fetch and build all dependencies for the given reference
        @param reference: ConanFileReference or path to user space conanfile
        @param current_path: where the output files will be saved
        @param remote: install only from that remote
        @param profile: Profile object with both the -s introduced options and profile readed values
        @param build_modes: List of build_modes specified
        @param filename: Optional filename of the conanfile
        """

        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote,
                                  update=False, check_updates=check_updates)

        deps_graph, graph_builder, conanfile = self._get_deps_graph(reference, profile, filename,
                                                                    current_path, remote_proxy)

        if check_updates:
            graph_updates_info = graph_builder.get_graph_updates_info(deps_graph)
        else:
            graph_updates_info = {}

        return deps_graph, graph_updates_info, self._get_project_reference(reference, conanfile)

    def install(self, reference, current_path, profile, remote=None,
                build_modes=None, filename=None, update=False,
                manifest_folder=None, manifest_verify=False, manifest_interactive=False,
                generators=None, no_imports=False, inject_require=None):
        """ Fetch and build all dependencies for the given reference
        @param reference: ConanFileReference or path to user space conanfile
        @param current_path: where the output files will be saved
        @param remote: install only from that remote
        @param profile: Profile object with both the -s introduced options and profile readed values
        @param build_modes: List of build_modes specified
        @param filename: Optional filename of the conanfile
        @param update: Check for updated in the upstream remotes (and update)
        @param manifest_folder: Folder to install the manifests
        @param manifest_verify: Verify dependencies manifests against stored ones
        @param manifest_interactive: Install deps manifests in folder for later verify, asking user for confirmation
        @param generators: List of generators from command line
        @param no_imports: Install specified packages but avoid running imports
        """
        generators = generators or []
        manifest_manager = ManifestManager(manifest_folder, user_io=self._user_io,
                                           client_cache=self._client_cache,
                                           verify=manifest_verify,
                                           interactive=manifest_interactive) if manifest_folder else None
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote,
                                  update=update, check_updates=False, manifest_manager=manifest_manager)

        loader = self.get_loader(profile)
        conanfile = self._get_conanfile_object(loader, reference, filename, current_path)
        if inject_require:
            self._inject_require(conanfile, inject_require)
        graph_builder = self._get_graph_builder(loader, update, remote_proxy)
        deps_graph = graph_builder.load(conanfile)

        # This line is so the conaninfo stores the correct complete info
        conanfile.info.scope = profile.scopes

        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)

        if inject_require:
            output = ScopedOutput("%s test package" % str(inject_require), self._user_io.out)
            output.info("Installing dependencies")
        else:
            if not isinstance(reference, ConanFileReference):
                output = ScopedOutput("PROJECT", self._user_io.out)
                output.highlight("Installing %s" % reference)
            else:
                output = ScopedOutput(str(reference), self._user_io.out)
                output.highlight("Installing package")
            Printer(self._user_io.out).print_graph(deps_graph, registry)

        try:
            if loader._settings.os and detected_os() != loader._settings.os:
                message = "Cross-platform from '%s' to '%s'" % (detected_os(), loader._settings.os)
                self._user_io.out.writeln(message, Color.BRIGHT_MAGENTA)
        except ConanException:  # Setting os doesn't exist
            pass

        build_mode = BuildMode(build_modes, self._user_io.out)
        build_requires = BuildRequires(loader, graph_builder, registry, output,
                                       profile.build_requires)
        installer = ConanInstaller(self._client_cache, output, remote_proxy, build_mode,
                                   build_requires)

        # Apply build_requires to consumer conanfile
        if not isinstance(reference, ConanFileReference):
            build_requires.install("", conanfile, installer)

        installer.install(deps_graph, current_path)
        build_mode.report_matches()

        # Write generators
        tmp = list(conanfile.generators)  # Add the command line specified generators
        tmp.extend([g for g in generators if g not in tmp])
        conanfile.generators = tmp
        write_generators(conanfile, current_path, output)

        if not isinstance(reference, ConanFileReference):
            content = normalize(conanfile.info.dumps())
            save(os.path.join(current_path, CONANINFO), content)
            output.info("Generated %s" % CONANINFO)
            if not no_imports:
                run_imports(conanfile, current_path, output)
            installer.call_system_requirements(conanfile, output)

        if manifest_manager:
            manifest_manager.print_log()

    def source(self, current_path, reference, force):
        if not isinstance(reference, ConanFileReference):
            output = ScopedOutput("PROJECT", self._user_io.out)
            conanfile_path = os.path.join(reference, CONANFILE)
            conanfile = self.load_consumer_conanfile(conanfile_path, current_path,
                                                     output, deps_cpp_info_required=None)
            config_source_local(current_path, conanfile, output)
        else:
            output = ScopedOutput(str(reference), self._user_io.out)
            conanfile_path = self._client_cache.conanfile(reference)
            conanfile = self.load_consumer_conanfile(conanfile_path, current_path,
                                                     output, reference=reference,
                                                     deps_cpp_info_required=None)
            src_folder = self._client_cache.source(reference, conanfile.short_paths)
            export_folder = self._client_cache.export(reference)
            export_src_folder = self._client_cache.export_sources(reference, conanfile.short_paths)
            config_source(export_folder, export_src_folder, src_folder, conanfile, output, force)

    def imports_undo(self, current_path):
        undo_imports(current_path, self._user_io.out)

    def imports(self, current_path, reference, conan_file_path, dest_folder):
        if not isinstance(reference, ConanFileReference):
            output = ScopedOutput("PROJECT", self._user_io.out)
            if not conan_file_path:
                conan_file_path = os.path.join(reference, CONANFILE)
                if not os.path.exists(conan_file_path):
                    conan_file_path = os.path.join(reference, CONANFILE_TXT)
            elif not os.path.isabs(conan_file_path):
                conan_file_path = os.path.abspath(os.path.join(reference, conan_file_path))
            reference = None
        else:
            output = ScopedOutput(str(reference), self._user_io.out)
            conan_file_path = self._client_cache.conanfile(reference)

        conanfile = self.load_consumer_conanfile(conan_file_path, current_path,
                                                 output, reference=reference,
                                                 deps_cpp_info_required=True)

        if dest_folder:
            if not os.path.isabs(dest_folder):
                dest_folder = os.path.normpath(os.path.join(current_path, dest_folder))
            mkdir(dest_folder)
        else:
            dest_folder = current_path
        run_imports(conanfile, dest_folder, output)

    def local_package(self, package_folder, recipe_folder, build_folder, source_folder):
        if package_folder == build_folder:
            raise ConanException("Cannot 'conan package' to the build folder. "
                                 "--build_folder and package folder can't be the same")
        output = ScopedOutput("PROJECT", self._user_io.out)
        conan_file_path = os.path.join(recipe_folder, CONANFILE)
        conanfile = self.load_consumer_conanfile(conan_file_path, build_folder, output)
        packager.create_package(conanfile, source_folder, build_folder, package_folder, output,
                                local=True, copy_info=True)

    def package(self, reference, package_id):
        # Package paths
        conan_file_path = self._client_cache.conanfile(reference)
        if not os.path.exists(conan_file_path):
            raise ConanException("Package recipe '%s' does not exist" % str(reference))

        conanfile = load_conanfile_class(conan_file_path)
        if hasattr(conanfile, "build_id"):
            raise ConanException("package command does not support recipes with 'build_id'\n"
                                 "To repackage them use 'conan install'")

        if not package_id:
            packages = [PackageReference(reference, packid)
                        for packid in self._client_cache.conan_builds(reference)]
            if not packages:
                raise NotFoundException("%s: Package has not been built in local cache\n"
                                        "Please read the 'conan package' command help\n"
                                        "Use 'conan install' or 'conan test_package' to build and "
                                        "create binaries" % str(reference))
        else:
            packages = [PackageReference(reference, package_id)]

        package_source_folder = self._client_cache.source(reference, conanfile.short_paths)
        for package_reference in packages:
            build_folder = self._client_cache.build(package_reference, short_paths=None)
            if not os.path.exists(build_folder):
                raise NotFoundException("%s: Package binary '%s' folder doesn't exist\n"
                                        "Please read the 'conan package' command help\n"
                                        "Use 'conan install' or 'conan test_package' to build and "
                                        "create binaries"
                                        % (str(reference), package_reference.package_id))
            # The package already exist, we can use short_paths if they were defined
            package_folder = self._client_cache.package(package_reference, short_paths=None)
            # Will read current conaninfo with specified options and load conanfile with them
            output = ScopedOutput(str(reference), self._user_io.out)
            output.info("Re-packaging %s" % package_reference.package_id)
            conanfile = self.load_consumer_conanfile(conan_file_path, build_folder,
                                                     output, reference=reference)
            rmdir(package_folder)
            if getattr(conanfile, 'no_copy_source', False):
                source_folder = package_source_folder
            else:
                source_folder = build_folder
            with environment_append(conanfile.env):
                packager.create_package(conanfile, source_folder, build_folder, package_folder,
                                        output, copy_info=True)

    def build(self, conanfile_path, source_folder, build_folder, package_folder, test=False):
        """ Call to build() method saved on the conanfile.py
        param conanfile_path: the original source directory of the user containing a
                            conanfile.py
        """
        logger.debug("Building in %s" % build_folder)
        logger.debug("Conanfile in %s" % conanfile_path)

        try:
            # Append env_vars to execution environment and clear when block code ends
            output = ScopedOutput(("%s test package" % test) if test else "Project",
                                  self._user_io.out)
            conan_file = self.load_consumer_conanfile(conanfile_path, build_folder, output)
        except NotFoundException:
            # TODO: Auto generate conanfile from requirements file
            raise ConanException("'%s' file is needed for build.\n"
                                 "Create a '%s' and move manually the "
                                 "requirements and generators from '%s' file"
                                 % (CONANFILE, CONANFILE, CONANFILE_TXT))

        if test:
            try:
                conan_file.requires.add(test)
            except ConanException:
                pass

        try:
            os.chdir(build_folder)
            conan_file._conanfile_directory = source_folder
            conan_file.build_folder = build_folder
            conan_file.source_folder = source_folder
            conan_file.package_folder = package_folder
            with environment_append(conan_file.env):
                output.highlight("Running build()")
                with conanfile_exception_formatter(str(conan_file), "build"):
                    conan_file.build()
                if test:
                    output.highlight("Running test()")
                    with conanfile_exception_formatter(str(conan_file), "test"):
                        conan_file.test()
        except ConanException:
            raise  # Raise but not let to reach the Exception except (not print traceback)
        except Exception:
            import traceback
            trace = traceback.format_exc().split('\n')
            raise ConanException("Unable to build it successfully\n%s" % '\n'.join(trace[3:]))

    def upload(self, conan_reference_or_pattern, package_id=None, remote=None, all_packages=None,
               force=False, confirm=False, retry=0, retry_wait=0, skip_upload=False,
               integrity_check=False):
        """If package_id is provided, conan_reference_or_pattern is a ConanFileReference"""
        t1 = time.time()
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager,
                                  remote)
        uploader = ConanUploader(self._client_cache, self._user_io, remote_proxy,
                                 self._search_manager)

        if package_id:  # Upload package
            ref = ConanFileReference.loads(conan_reference_or_pattern)
            uploader.check_reference(ref)
            uploader.upload_package(PackageReference(ref, package_id), retry=retry,
                                    retry_wait=retry_wait, skip_upload=skip_upload,
                                    integrity_check=integrity_check)
        else:  # Upload conans
            uploader.upload(conan_reference_or_pattern, all_packages=all_packages,
                            force=force, confirm=confirm,
                            retry=retry, retry_wait=retry_wait, skip_upload=skip_upload,
                            integrity_check=integrity_check)

        logger.debug("====> Time manager upload: %f" % (time.time() - t1))

    def _get_search_adapter(self, remote):
        if remote:
            remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)
            adapter = remote_proxy
        else:
            adapter = self._search_manager

        return adapter

    def search_recipes(self, pattern, remote, ignorecase):
        references = self._get_search_adapter(remote).search(pattern, ignorecase)
        return references

    def search_packages(self, reference=None, remote=None, packages_query=None, outdated=False):
        """ Return the single information saved in conan.vars about all the packages
            or the packages which match with a pattern

            Attributes:
                pattern = string to match packages
                remote = search on another origin to get packages info
                packages_pattern = String query with binary
                                   packages properties: "arch=x86 AND os=Windows"
        """
        packages_props = self._get_search_adapter(remote).search_packages(reference, packages_query)
        ordered_packages = OrderedDict(sorted(packages_props.items()))
        if remote:
            remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)
            remote = remote_proxy.registry.remote(remote)
            manifest = self._remote_manager.get_conan_digest(reference, remote)
            recipe_hash = manifest.summary_hash
        else:
            try:
                recipe_hash = self._client_cache.load_manifest(reference).summary_hash
            except IOError:  # It could not exist in local
                recipe_hash = None
        if outdated and recipe_hash:
            ordered_packages = filter_outdated(ordered_packages, recipe_hash)

        return ordered_packages, reference, recipe_hash, packages_query

    def copy(self, reference, package_ids, username, channel, force=False):
        """ Copy or move conanfile (exported) and packages to another user and or channel
        @param reference: ConanFileReference containing the packages to be moved
        @param package_ids: list of ids or [] for all list
        @param username: Destination username
        @param channel: Destination channel
        @param remote: install only from that remote
        """
        # It is necessary to make sure the sources are complete before proceeding
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, None)

        # Now we can actually copy
        conan_file_path = self._client_cache.conanfile(reference)
        conanfile = load_conanfile_class(conan_file_path)
        remote_proxy.complete_recipe_sources(reference, short_paths=conanfile.short_paths)
        copier = PackageCopier(self._client_cache, self._user_io, conanfile.short_paths)
        if not package_ids:
            packages = self._client_cache.packages(reference)
            if os.path.exists(packages):
                package_ids = os.listdir(packages)
            else:
                package_ids = []
        copier.copy(reference, package_ids, username, channel, force)

    def remove(self, pattern, src=False, build_ids=None, package_ids_filter=None, force=False,
               remote=None, packages_query=None, outdated=False):
        """ Remove conans and/or packages
        @param pattern: string to match packages
        @param src: Remove src folder
        @param package_ids_filter: list of ids or [] for all list
        @param build_ids: list of ids or [] for all list
        @param remote: search on another origin to get packages info
        @param force: if True, it will be deleted without requesting anything
        @param packages_query: Only if src is a reference. Query settings and options
        """
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)
        remover = ConanRemover(self._client_cache, self._search_manager, self._user_io,
                               remote_proxy)
        remover.remove(pattern, src, build_ids, package_ids_filter, force=force,
                       packages_query=packages_query, outdated=outdated)

    def user(self, remote=None, name=None, password=None):
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)
        return remote_proxy.authenticate(name, password)

    def get_path(self, reference, package_id=None, path=None, remote=None):
        remote_proxy = ConanProxy(self._client_cache, self._user_io, self._remote_manager, remote)
        if not path and not package_id:
            path = "conanfile.py"
        elif not path and package_id:
            path = "conaninfo.txt"
        return remote_proxy.get_path(reference, package_id, path), path

    def export_alias(self, reference, target_reference):

        conanfile = """
from conans import ConanFile

class AliasConanfile(ConanFile):
    alias = "%s"
""" % str(target_reference)

        export_path = self._client_cache.export(reference)
        mkdir(export_path)
        save(os.path.join(export_path, CONANFILE), conanfile)
        mkdir(self._client_cache.export_sources(reference))
        digest = FileTreeManifest.create(export_path)
        save(os.path.join(export_path, CONAN_MANIFEST), str(digest))


def _load_deps_cpp_info(current_path, conanfile, required):

    def get_forbidden_access_object(field_name):
        class InfoObjectNotDefined(object):
            def __getitem__(self, item):
                raise ConanException("self.%s not defined. If you need it for a "
                                     "local command run 'conan install -g txt'" % field_name)
            __getattr__ = __getitem__

        return InfoObjectNotDefined()

    if not current_path:
        return
    info_file_path = os.path.join(current_path, BUILD_INFO)
    try:
        deps_cpp_info, deps_user_info = TXTGenerator.loads(load(info_file_path))
        conanfile.deps_cpp_info = deps_cpp_info
        conanfile.deps_user_info = deps_user_info
    except IOError:
        if required:
            raise ConanException("%s file not found in %s\nIt is required for this command\n"
                                 "You can generate it using 'conan install -g txt'"
                                 % (BUILD_INFO, current_path))
        conanfile.deps_cpp_info = get_forbidden_access_object("deps_cpp_info")
        conanfile.deps_user_info = get_forbidden_access_object("deps_user_info")
    except ConanException:
        raise ConanException("Parse error in '%s' file in %s" % (BUILD_INFO, current_path))