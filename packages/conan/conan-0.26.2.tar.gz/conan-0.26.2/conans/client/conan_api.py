import hashlib
import os
import sys
from collections import defaultdict, OrderedDict

import requests

import conans
from conans import __version__ as CLIENT_VERSION, tools
from conans.client.client_cache import ClientCache
from conans.client.conf import MIN_SERVER_COMPATIBLE_VERSION, ConanClientConfigParser
from conans.client.detect import detect_defaults_settings
from conans.client.manager import ConanManager
from conans.client.migrations import ClientMigrator
from conans.client.output import ConanOutput, ScopedOutput
from conans.client.profile_loader import read_profile, get_profile_path
from conans.client.remote_manager import RemoteManager
from conans.client.remote_registry import RemoteRegistry
from conans.client.rest.auth_manager import ConanApiAuthManager
from conans.client.rest.rest_client import RestApiClient
from conans.client.rest.version_checker import VersionCheckerRequester
from conans.client.runner import ConanRunner
from conans.client.store.localdb import LocalDB
from conans.client.userio import UserIO
from conans.errors import ConanException
from conans.model.env_info import EnvValues
from conans.model.options import OptionsValues
from conans.model.profile import Profile
from conans.model.ref import ConanFileReference, is_a_reference
from conans.model.scope import Scopes
from conans.model.version import Version
from conans.paths import CONANFILE, get_conan_user_home
from conans.search.search import DiskSearchManager, DiskSearchAdapter
from conans.util.env_reader import get_env
from conans.util.files import rmdir, save_files, exception_message_safe, save
from conans.util.log import configure_logger
from conans.util.tracer import log_command, log_exception
from conans.client.loader_parse import load_conanfile_class
from conans.client import settings_preprocessor

default_manifest_folder = '.conan_manifests'


def get_basic_requester(client_cache):
    requester = requests.Session()
    requester.proxies = client_cache.conan_config.proxies
    return requester


def api_method(f):
    def wrapper(*args, **kwargs):
        the_self = args[0]
        try:
            log_command(f.__name__, kwargs)
            with tools.environment_append(the_self._client_cache.conan_config.env_vars):
                # Patch the globals in tools
                return f(*args, **kwargs)
        except Exception as exc:
            msg = exception_message_safe(exc)
            try:
                log_exception(exc, msg)
            except:
                pass
            raise

    return wrapper


def prepare_cwd(cwd):
    if cwd:
        if os.path.isabs(cwd):
            return cwd
        else:
            return os.path.abspath(cwd)
    else:
        return os.getcwd()


class ConanAPIV1(object):

    @staticmethod
    def factory():
        """Factory"""

        def instance_remote_manager(client_cache):
            requester = get_basic_requester(client_cache)
            # Verify client version against remotes
            version_checker_requester = VersionCheckerRequester(requester, Version(CLIENT_VERSION),
                                                                Version(MIN_SERVER_COMPATIBLE_VERSION),
                                                                out)
            # To handle remote connections
            put_headers = client_cache.read_put_headers()
            rest_api_client = RestApiClient(out, requester=version_checker_requester, put_headers=put_headers)
            # To store user and token
            localdb = LocalDB(client_cache.localdb)
            # Wraps RestApiClient to add authentication support (same interface)
            auth_manager = ConanApiAuthManager(rest_api_client, user_io, localdb)
            # Handle remote connections
            remote_manager = RemoteManager(client_cache, auth_manager, out)
            return remote_manager

        use_color = get_env("CONAN_COLOR_DISPLAY", 1)
        if use_color and hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            import colorama
            colorama.init()
            color = True
        else:
            color = False
        out = ConanOutput(sys.stdout, color)
        user_io = UserIO(out=out)

        try:
            client_cache = migrate_and_get_client_cache(get_conan_user_home(), out)
        except Exception as e:
            out.error(str(e))
            raise

        with tools.environment_append(client_cache.conan_config.env_vars):
            # Adjust CONAN_LOGGING_LEVEL with the env readed
            conans.util.log.logger = configure_logger()

            # Get the new command instance after migrations have been done
            remote_manager = instance_remote_manager(client_cache)

            # Get a search manager
            search_adapter = DiskSearchAdapter()
            search_manager = DiskSearchManager(client_cache, search_adapter)

            # Settings preprocessor
            conan = Conan(client_cache, user_io, get_conan_runner(), remote_manager, search_manager,
                          settings_preprocessor)

        return conan

    def __init__(self, client_cache, user_io, runner, remote_manager, search_manager,
                 settings_preprocessor):
        assert isinstance(user_io, UserIO)
        assert isinstance(client_cache, ClientCache)
        self._client_cache = client_cache
        self._user_io = user_io
        self._runner = runner
        self._manager = ConanManager(client_cache, user_io, runner, remote_manager, search_manager,
                                     settings_preprocessor)
        # Patch the tools module with a good requester and user_io
        tools._global_requester = get_basic_requester(self._client_cache)
        tools._global_output = self._user_io.out

    @api_method
    def new(self, name, header=False, pure_c=False, test=False, exports_sources=False, bare=False, cwd=None,
            visual_versions=None, linux_gcc_versions=None, linux_clang_versions=None, osx_clang_versions=None,
            shared=None, upload_url=None, gitignore=None, gitlab_gcc_versions=None, gitlab_clang_versions=None):
        from conans.client.new import get_files
        cwd = prepare_cwd(cwd)
        files = get_files(name, header=header, pure_c=pure_c, test=test,
                          exports_sources=exports_sources, bare=bare,
                          visual_versions=visual_versions,
                          linux_gcc_versions=linux_gcc_versions,
                          linux_clang_versions=linux_clang_versions,
                          osx_clang_versions=osx_clang_versions, shared=shared,
                          upload_url=upload_url, gitignore=gitignore,
                          gitlab_gcc_versions=gitlab_gcc_versions,
                          gitlab_clang_versions=gitlab_clang_versions)

        save_files(cwd, files)
        for f in sorted(files):
            self._user_io.out.success("File saved: %s" % f)

    @api_method
    def test_package(self, profile_name=None, settings=None, options=None, env=None,
                     scope=None, test_folder=None, not_export=False, build=None, keep_source=False,
                     verify=default_manifest_folder, manifests=default_manifest_folder,
                     manifests_interactive=default_manifest_folder,
                     remote=None, update=False, cwd=None, user=None, channel=None, name=None,
                     version=None):
        settings = settings or []
        options = options or []
        env = env or []
        cwd = prepare_cwd(cwd)

        if name and version:
            package_name = name
            package_version = version
        else:
            conanfile_path = os.path.join(cwd, "conanfile.py")
            conanfile = load_conanfile_class(conanfile_path)
            package_name = getattr(conanfile, "name", None)
            package_version = getattr(conanfile, "version", None)
        if not package_name or not package_version:
            raise ConanException("conanfile.py doesn't declare package name or version")

        test_folders = [test_folder] if test_folder else ["test_package", "test"]
        for test_folder_name in test_folders:
            test_folder = os.path.join(cwd, test_folder_name)
            test_conanfile_path = os.path.join(test_folder, "conanfile.py")
            if os.path.exists(test_conanfile_path):
                break
        else:
            raise ConanException("test folder '%s' not available, "
                                 "or it doesn't have a conanfile.py" % test_folder_name)

        sha = hashlib.sha1("".join(options + settings).encode()).hexdigest()
        build_folder = os.path.join(test_folder, "build", sha)
        rmdir(build_folder)
        # shutil.copytree(test_folder, build_folder)

        profile = profile_from_args(profile_name, settings, options, env, scope, cwd,
                                    self._client_cache.profiles_path)

        loader = self._manager.get_loader(profile)
        test_conanfile = loader.load_conan(test_conanfile_path, self._user_io.out, consumer=True)

        try:
            if hasattr(test_conanfile, "requirements"):
                test_conanfile.requirements()
        except Exception as e:
            raise ConanException("Error in test_package/conanfile.py requirements(). %s" % str(e))

        requirement = test_conanfile.requires.get(package_name)
        if requirement:
            if requirement.conan_reference.version != package_version:
                raise ConanException("package version is '%s', but test_package/conanfile "
                                     "is requiring version '%s'\n"
                                     "You can remove this requirement and use "
                                     "'conan test_package user/channel' instead"
                                     % (package_version, requirement.conan_reference.version))
            user = user or requirement.conan_reference.user
            channel = channel or requirement.conan_reference.channel

        if not user or not channel:
            raise ConanException("Please specify user and channel")
        conanfile_reference = ConanFileReference(package_name, package_version, user, channel)

        # Forcing an export!
        if not not_export:
            self._user_io.out.info("Exporting package recipe")
            self._manager.export(user, channel, cwd, keep_source=keep_source)

        if build is None:  # Not specified, force build the tested library
            build = [package_name]

        manifests = _parse_manifests_arguments(verify, manifests, manifests_interactive, cwd)
        manifest_folder, manifest_interactive, manifest_verify = manifests
        self._manager.install(inject_require=conanfile_reference,
                              reference=test_folder,
                              current_path=build_folder,
                              manifest_folder=manifest_folder,
                              manifest_verify=manifest_verify,
                              manifest_interactive=manifest_interactive,
                              remote=remote,
                              profile=profile,
                              build_modes=build,
                              update=update,
                              generators=["txt"]
                              )

        test_conanfile = os.path.join(test_folder, CONANFILE)
        self._manager.build(test_conanfile, test_folder, build_folder, package_folder=None,
                            test=str(conanfile_reference))

    @api_method
    def create(self, profile_name=None, settings=None,
               options=None, env=None, scope=None, test_folder=None, not_export=False, build=None,
               keep_source=False, verify=default_manifest_folder,
               manifests=default_manifest_folder, manifests_interactive=default_manifest_folder,
               remote=None, update=False, cwd=None,
               user=None, channel=None, name=None, version=None):

        settings = settings or []
        options = options or []
        env = env or []
        cwd = prepare_cwd(cwd)

        if not name or not version:
            conanfile_path = os.path.join(cwd, "conanfile.py")
            conanfile = load_conanfile_class(conanfile_path)
            name, version = conanfile.name, conanfile.version
            if not name or not version:
                raise ConanException("conanfile.py doesn't declare package name or version")

        reference = ConanFileReference(name, version, user, channel)
        scoped_output = ScopedOutput(str(reference), self._user_io.out)
        # Forcing an export!
        if not not_export:
            scoped_output.highlight("Exporting package recipe")
            self._manager.export(user, channel, cwd, keep_source=keep_source, name=name,
                                 version=version)

        if build is None:  # Not specified, force build the tested library
            build = [name]

        manifests = _parse_manifests_arguments(verify, manifests, manifests_interactive, cwd)
        manifest_folder, manifest_interactive, manifest_verify = manifests
        profile = profile_from_args(profile_name, settings, options, env, scope,
                                    cwd, self._client_cache.profiles_path)
        self._manager.install(reference=reference,
                              current_path=cwd,
                              manifest_folder=manifest_folder,
                              manifest_verify=manifest_verify,
                              manifest_interactive=manifest_interactive,
                              remote=remote,
                              profile=profile,
                              build_modes=build,
                              update=update
                              )

        test_folders = [test_folder] if test_folder else ["test_package", "test"]
        for test_folder_name in test_folders:
            test_folder = os.path.join(cwd, test_folder_name)
            test_conanfile_path = os.path.join(test_folder, "conanfile.py")
            if os.path.exists(test_conanfile_path):
                break
        else:
            self._user_io.out.warn("test package folder not available, or it doesn't have "
                                   "a conanfile.py\nIt is recommended to set a 'test_package' "
                                   "while creating packages")
            return

        scoped_output.highlight("Testing with 'test_package'")
        sha = hashlib.sha1("".join(options + settings).encode()).hexdigest()
        build_folder = os.path.join(test_folder, "build", sha)
        rmdir(build_folder)

        test_conanfile = os.path.join(test_folder, CONANFILE)
        self._manager.install(inject_require=reference,
                              reference=test_folder,
                              current_path=build_folder,
                              manifest_folder=manifest_folder,
                              manifest_verify=manifest_verify,
                              manifest_interactive=manifest_interactive,
                              remote=remote,
                              profile=profile,
                              update=update,
                              generators=["txt"]
                              )
        self._manager.build(test_conanfile, test_folder, build_folder, package_folder=None,
                            test=str(reference))

    @api_method
    def package_files(self, reference, source_folder=None, build_folder=None, package_folder=None,
                      profile_name=None, force=False, settings=None, options=None, cwd=None):

        cwd = prepare_cwd(cwd)

        reference = ConanFileReference.loads(reference)
        profile = profile_from_args(profile_name, settings, options, env=None, scope=None, cwd=cwd,
                                    default_folder=self._client_cache.profiles_path)
        package_folder = package_folder or cwd
        if not source_folder and build_folder:
            source_folder = build_folder
        if not os.path.isabs(package_folder):
            package_folder = os.path.join(cwd, package_folder)
        if source_folder and not os.path.isabs(source_folder):
            source_folder = os.path.normpath(os.path.join(cwd, source_folder))
        if build_folder and not os.path.isabs(build_folder):
            build_folder = os.path.normpath(os.path.join(cwd, build_folder))
        self._manager.package_files(reference=reference, source_folder=source_folder,
                                    build_folder=build_folder, package_folder=package_folder,
                                    profile=profile, force=force)

    @api_method
    def install(self, reference="", package=None, settings=None, options=None, env=None, scope=None, all=False,
                remote=None, werror=False, verify=default_manifest_folder, manifests=default_manifest_folder,
                manifests_interactive=default_manifest_folder, build=None, profile_name=None,
                update=False, generator=None, no_imports=False, filename=None, cwd=None):

        self._user_io.out.werror_active = werror
        cwd = prepare_cwd(cwd)

        try:
            ref = ConanFileReference.loads(reference)
        except:
            ref = os.path.normpath(os.path.join(cwd, reference))

        if all or package:  # Install packages without settings (fixed ids or all)
            if all:
                package = []
            if not reference or not isinstance(ref, ConanFileReference):
                raise ConanException("Invalid package recipe reference. "
                                     "e.g., MyPackage/1.2@user/channel")
            self._manager.download(ref, package, remote=remote)
        else:  # Classic install, package chosen with settings and options
            manifests = _parse_manifests_arguments(verify, manifests, manifests_interactive, cwd)
            manifest_folder, manifest_interactive, manifest_verify = manifests

            profile = profile_from_args(profile_name, settings, options, env, scope, cwd,
                                        self._client_cache.profiles_path)

            self._manager.install(reference=ref,
                                  current_path=cwd,
                                  remote=remote,
                                  profile=profile,
                                  build_modes=build,
                                  filename=filename,
                                  update=update,
                                  manifest_folder=manifest_folder,
                                  manifest_verify=manifest_verify,
                                  manifest_interactive=manifest_interactive,
                                  generators=generator,
                                  no_imports=no_imports)

    @api_method
    def config_get(self, item):
        config_parser = ConanClientConfigParser(self._client_cache.conan_conf_path)
        self._user_io.out.info(config_parser.get_item(item))
        return config_parser.get_item(item)

    @api_method
    def config_set(self, item, value):
        config_parser = ConanClientConfigParser(self._client_cache.conan_conf_path)
        config_parser.set_item(item, value)

    @api_method
    def config_rm(self, item):
        config_parser = ConanClientConfigParser(self._client_cache.conan_conf_path)
        config_parser.rm_item(item)

    @api_method
    def info_build_order(self, reference, settings=None, options=None, env=None, scope=None, profile_name=None,
                         filename=None, remote=None, build_order=None, check_updates=None, cwd=None):

        current_path = prepare_cwd(cwd)
        try:
            reference = ConanFileReference.loads(reference)
        except:
            reference = os.path.normpath(os.path.join(current_path, reference))

        profile = profile_from_args(profile_name, settings, options, env, scope, cwd, self._client_cache.profiles_path)
        graph = self._manager.info_build_order(reference, profile, filename, build_order, remote, check_updates, cwd=cwd)
        return graph

    @api_method
    def info_nodes_to_build(self, reference, build_modes, settings=None, options=None, env=None, scope=None,
                            profile_name=None, filename=None, remote=None, check_updates=None, cwd=None):

        current_path = prepare_cwd(cwd)
        try:
            reference = ConanFileReference.loads(reference)
        except:
            reference = os.path.normpath(os.path.join(current_path, reference))

        profile = profile_from_args(profile_name, settings, options, env, scope, cwd, self._client_cache.profiles_path)
        ret = self._manager.info_nodes_to_build(reference, profile, filename, build_modes, remote, check_updates, cwd)
        ref_list, project_reference = ret
        return ref_list, project_reference

    @api_method
    def info_get_graph(self, reference, remote=None, settings=None, options=None, env=None, scope=None,
                       profile_name=None, update=False, filename=None, cwd=None):

        current_path = prepare_cwd(cwd)
        try:
            reference = ConanFileReference.loads(reference)
        except:
            reference = os.path.normpath(os.path.join(current_path, reference))

        profile = profile_from_args(profile_name, settings, options, env, scope, current_path,
                                    self._client_cache.profiles_path)
        ret = self._manager.info_get_graph(reference=reference, current_path=current_path, remote=remote,
                                           profile=profile, check_updates=update, filename=filename)
        deps_graph, graph_updates_info, project_reference = ret
        return deps_graph, graph_updates_info, project_reference

    @api_method
    def build(self, path="", source_folder=None, package_folder=None, filename=None, cwd=None):

        current_path = prepare_cwd(cwd)
        if path:
            root_path = os.path.abspath(path)
        else:
            root_path = current_path

        build_folder = current_path
        source_folder = source_folder or root_path
        if not os.path.isabs(source_folder):
            source_folder = os.path.normpath(os.path.join(current_path, source_folder))

        if package_folder and not os.path.isabs(package_folder):
            package_folder = os.path.normpath(os.path.join(current_path, package_folder))

        if filename and filename.endswith(".txt"):
            raise ConanException("A conanfile.py is needed to call 'conan build'")
        conanfile_path = os.path.join(root_path, filename or CONANFILE)
        self._manager.build(conanfile_path, source_folder, build_folder, package_folder)

    @api_method
    def package(self, reference="", package_id=None, build_folder=None, source_folder=None,
                cwd=None):
        try:
            ref = ConanFileReference.loads(reference)
        except:
            if "@" in reference:
                raise
            ref = None

        if ref:  # cache packaging
            # TODO: other args are unused. Either raise, or split API in two methods
            self._manager.package(ref, package_id)
        else:  # local packaging
            current_path = prepare_cwd(cwd)
            recipe_folder = reference
            if not os.path.isabs(recipe_folder):
                recipe_folder = os.path.join(current_path, recipe_folder)
            recipe_folder = os.path.normpath(recipe_folder)
            build_folder = build_folder or recipe_folder
            if not os.path.isabs(build_folder):
                build_folder = os.path.join(current_path, build_folder)
            build_folder = os.path.normpath(build_folder)
            package_folder = current_path
            source_folder = source_folder or recipe_folder
            self._manager.local_package(package_folder, recipe_folder, build_folder, source_folder)

    @api_method
    def source(self, reference, force=False, cwd=None):
        cwd = prepare_cwd(cwd)
        current_path, reference = _get_reference(reference, cwd)
        self._manager.source(current_path, reference, force)

    @api_method
    def imports(self, reference, undo=False, dest=None, filename=None, cwd=None):
        cwd = prepare_cwd(cwd)

        if undo:
            if not os.path.isabs(reference):
                current_path = os.path.normpath(os.path.join(cwd, reference))
            else:
                current_path = reference
            self._manager.imports_undo(current_path)
        else:
            cwd = prepare_cwd(cwd)
            current_path, reference = _get_reference(reference, cwd)
            self._manager.imports(current_path, reference, filename, dest)

    @api_method
    def export(self, user, channel, path=None, keep_source=False, filename=None, cwd=None,
               name=None, version=None):
        cwd = prepare_cwd(cwd)
        current_path = os.path.abspath(path or cwd)
        self._manager.export(user, channel, current_path, keep_source, filename=filename, name=name,
                             version=version)

    @api_method
    def remove(self, pattern, query=None, packages=None, builds=None, src=False, force=False,
               remote=None, outdated=False):
        self._manager.remove(pattern, package_ids_filter=packages, build_ids=builds,
                             src=src, force=force, remote=remote, packages_query=query,
                             outdated=outdated)

    @api_method
    def copy(self, reference="", user_channel="", force=False, all=False, package=None):
        reference = ConanFileReference.loads(reference)
        new_ref = ConanFileReference.loads("%s/%s@%s" % (reference.name,
                                                         reference.version,
                                                         user_channel))
        if all:
            package = []
        self._manager.copy(reference, package, new_ref.user, new_ref.channel, force)

    @api_method
    def user(self, name=None, clean=False, remote=None, password=None):
        if clean:
            localdb = LocalDB(self._client_cache.localdb)
            localdb.init(clean=True)
            self._user_io.out.success("Deleted user data")
            return
        self._manager.user(remote, name, password)

    @api_method
    def search_recipes(self, pattern, remote=None, case_sensitive=False):
        refs = self._manager.search_recipes(pattern, remote, ignorecase=not case_sensitive)
        return refs

    @api_method
    def search_packages(self, reference, query=None, remote=None, outdated=False):
        ret = self._manager.search_packages(reference, remote, packages_query=query,
                                            outdated=outdated)
        return ret

    @api_method
    def upload(self, pattern, package=None, remote=None, all=False, force=False, confirm=False,
               retry=2, retry_wait=5, skip_upload=False, integrity_check=False):
        """ Uploads a package recipe and the generated binary packages to a specified remote
        """
        if package and not is_a_reference(pattern):
            raise ConanException("-p parameter only allowed with a valid recipe reference, "
                                 "not with a pattern")

        self._manager.upload(pattern, package, remote, all_packages=all, force=force,
                             confirm=confirm, retry=retry, retry_wait=retry_wait,
                             skip_upload=skip_upload, integrity_check=integrity_check)

    @api_method
    def remote_list(self):
        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
        return registry.remotes

    @api_method
    def remote_add(self, remote, url, verify_ssl=True, insert=None):
        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
        return registry.add(remote, url, verify_ssl, insert)

    @api_method
    def remote_remove(self, remote):
        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
        return registry.remove(remote)

    @api_method
    def remote_update(self, remote, url, verify_ssl=True, insert=None):
        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
        return registry.update(remote, url, verify_ssl, insert)

    @api_method
    def remote_list_ref(self):
        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
        return registry.refs

    @api_method
    def remote_add_ref(self, reference, remote):
        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
        return registry.add_ref(reference, remote)

    @api_method
    def remote_remove_ref(self, reference):
        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
        return registry.remove_ref(reference)

    @api_method
    def remote_update_ref(self, reference, remote):
        registry = RemoteRegistry(self._client_cache.registry, self._user_io.out)
        return registry.update_ref(reference, remote)

    @api_method
    def profile_list(self):
        folder = self._client_cache.profiles_path
        if os.path.exists(folder):
            return [name for name in os.listdir(folder) if not os.path.isdir(name)]
        else:
            self._user_io.out.info("No profiles defined")
            return []

    @api_method
    def create_profile(self, profile_name, detect=False):
        profile_path = get_profile_path(profile_name, self._client_cache.profiles_path, os.getcwd())
        if os.path.exists(profile_path):
            raise ConanException("Profile already exists")

        profile = Profile()
        if detect:
            settings = detect_defaults_settings(self._user_io.out)
            for name, value in settings:
                profile.settings[name] = value

        contents = profile.dumps()
        save(profile_path, contents)
        self._user_io.out.info("Empty profile created: %s" % profile_path)
        return profile_path

    @staticmethod
    def _get_profile_keys(key):
        # settings.compiler.version => settings, compiler.version
        tmp = key.split(".")
        first_key = tmp[0]
        rest_key = ".".join(tmp[1:]) if len(tmp) > 1 else None
        if first_key not in ("build_requires", "settings", "options", "scopes", "env"):
            raise ConanException("Invalid specified key: %s" % key)

        return first_key, rest_key

    @api_method
    def update_profile(self, profile_name, key, value):
        first_key, rest_key = self._get_profile_keys(key)

        profile, _ = read_profile(profile_name, os.getcwd(), self._client_cache.profiles_path)
        if first_key == "settings":
            profile.settings[rest_key] = value
        elif first_key == "options":
            tmp = OptionsValues([(rest_key, value)])
            profile.options.update(tmp)
        elif first_key == "env":
            profile.env_values.update(EnvValues.loads("%s=%s" % (rest_key, value)))
        elif first_key == "scopes":
            profile.update_scopes(Scopes.from_list(["%s=%s" % (rest_key, value)]))
        elif first_key == "build_requires":
            raise ConanException("Edit the profile manually to change the build_requires")

        contents = profile.dumps()
        profile_path = get_profile_path(profile_name, self._client_cache.profiles_path, os.getcwd())
        save(profile_path, contents)

    @api_method
    def delete_profile_key(self, profile_name, key):
        first_key, rest_key = self._get_profile_keys(key)
        profile, _ = read_profile(profile_name, os.getcwd(), self._client_cache.profiles_path)

        # For options, scopes, env vars
        try:
            package, name = rest_key.split(":")
        except ValueError:
            package = None
            name = rest_key

        try:
            if first_key == "settings":
                del profile.settings[rest_key]
            elif first_key == "options":
                profile.options.remove(name, package)
            elif first_key == "env":
                profile.env_values.remove(name, package)
            elif first_key == "scopes":
                profile.scopes.remove(name, package)
            elif first_key == "build_requires":
                raise ConanException("Edit the profile manually to delete a build_require")
        except KeyError:
            raise ConanException("Profile key '%s' doesn't exist" % key)

        contents = profile.dumps()
        profile_path = get_profile_path(profile_name, self._client_cache.profiles_path, os.getcwd())
        save(profile_path, contents)

    @api_method
    def read_profile(self, profile=None):
        p, _ = read_profile(profile, os.getcwd(), self._client_cache.profiles_path)
        return p

    @api_method
    def get_path(self, reference, package_id=None, path=None, remote=None):
        reference = ConanFileReference.loads(str(reference))
        return self._manager.get_path(reference, package_id, path, remote)

    @api_method
    def export_alias(self, reference, target_reference):
        reference = ConanFileReference.loads(str(reference))
        target_reference = ConanFileReference.loads(str(target_reference))
        return self._manager.export_alias(reference, target_reference)


Conan = ConanAPIV1


def _check_query_parameter_and_get_reference(query, pattern):
    reference = None
    if pattern:
        try:
            reference = ConanFileReference.loads(pattern)
        except ConanException:
            if query is not None:
                raise ConanException("-q parameter only allowed with a valid recipe "
                                     "reference as search pattern. e.j conan search "
                                     "MyPackage/1.2@user/channel -q \"os=Windows\"")
    return reference


def _parse_manifests_arguments(verify, manifests, manifests_interactive, cwd):
    if manifests and manifests_interactive:
        raise ConanException("Do not specify both manifests and "
                             "manifests-interactive arguments")
    if verify and (manifests or manifests_interactive):
        raise ConanException("Do not specify both 'verify' and "
                             "'manifests' or 'manifests-interactive' arguments")
    manifest_folder = verify or manifests or manifests_interactive
    if manifest_folder:
        if not os.path.isabs(manifest_folder):
            manifest_folder = os.path.join(cwd, manifest_folder)
        manifest_verify = verify is not None
        manifest_interactive = manifests_interactive is not None
    else:
        manifest_verify = manifest_interactive = False

    return manifest_folder, manifest_interactive, manifest_verify


def get_conan_runner():
    print_commands_to_output = get_env("CONAN_PRINT_RUN_COMMANDS", False)
    generate_run_log_file = get_env("CONAN_LOG_RUN_TO_FILE", False)
    log_run_to_output = get_env("CONAN_LOG_RUN_TO_OUTPUT", True)
    runner = ConanRunner(print_commands_to_output, generate_run_log_file, log_run_to_output)
    return runner


def _get_reference(ref, cwd=None):
    try:
        reference = ConanFileReference.loads(ref)
    except:
        if "@" in ref:
            raise
        if not os.path.isabs(ref):
            reference = os.path.normpath(os.path.join(cwd, ref))
        else:
            reference = ref
    return cwd, reference


def migrate_and_get_client_cache(base_folder, out, storage_folder=None):
    # Init paths
    client_cache = ClientCache(base_folder, storage_folder, out)

    # Migration system
    migrator = ClientMigrator(client_cache, Version(CLIENT_VERSION), out)
    migrator.migrate()

    return client_cache


# Profile helpers


def profile_from_args(profile, settings, options, env, scope, cwd, default_folder):
    """ Return a Profile object, as the result of merging a potentially existing Profile
    file and the args command-line arguments
    """
    file_profile, _ = read_profile(profile, cwd, default_folder)
    args_profile = _profile_parse_args(settings, options, env, scope)

    if file_profile:
        file_profile.update(args_profile)
        return file_profile
    else:
        return args_profile


def _profile_parse_args(settings, options, envs, scopes):
    """ return a Profile object result of parsing raw data
    """
    def _get_tuples_list_from_extender_arg(items):
        if not items:
            return []
        # Validate the pairs
        for item in items:
            chunks = item.split("=", 1)
            if len(chunks) != 2:
                raise ConanException("Invalid input '%s', use 'name=value'" % item)
        return [(item[0], item[1]) for item in [item.split("=", 1) for item in items]]

    def _get_simple_and_package_tuples(items):
        """Parse items like "thing:item=value or item2=value2 and returns a tuple list for
        the simple items (name, value) and a dict for the package items
        {package: [(item, value)...)], ...}
        """
        simple_items = []
        package_items = defaultdict(list)
        tuples = _get_tuples_list_from_extender_arg(items)
        for name, value in tuples:
            if ":" in name:  # Scoped items
                tmp = name.split(":", 1)
                ref_name = tmp[0]
                name = tmp[1]
                package_items[ref_name].append((name, value))
            else:
                simple_items.append((name, value))
        return simple_items, package_items

    def _get_env_values(env, package_env):
        env_values = EnvValues()
        for name, value in env:
            env_values.add(name, EnvValues.load_value(value))
        for package, data in package_env.items():
            for name, value in data:
                env_values.add(name, EnvValues.load_value(value), package)
        return env_values

    result = Profile()
    options = _get_tuples_list_from_extender_arg(options)
    result.options = OptionsValues(options)
    env, package_env = _get_simple_and_package_tuples(envs)
    env_values = _get_env_values(env, package_env)
    result.env_values = env_values
    settings, package_settings = _get_simple_and_package_tuples(settings)
    result.settings = OrderedDict(settings)
    for pkg, values in package_settings.items():
        result.package_settings[pkg] = OrderedDict(values)
    result.scopes = Scopes.from_list(scopes) if scopes else Scopes()
    return result
