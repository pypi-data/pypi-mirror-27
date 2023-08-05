""" manages the movement of conanfiles and associated files from the user space
to the local store, as an initial step before building or uploading to remotes
"""

import shutil
import os

from conans.util.log import logger
from conans.util.files import save, load, rmdir, is_dirty, set_dirty
from conans.paths import CONAN_MANIFEST, CONANFILE
from conans.errors import ConanException
from conans.model.manifest import FileTreeManifest
from conans.client.output import ScopedOutput
from conans.client.file_copier import FileCopier
from conans.model.conan_file import create_exports, create_exports_sources
from conans.client.loader_parse import load_conanfile_class
from conans.client.cmd.export_linter import conan_linter
from conans.model.ref import ConanFileReference


def cmd_export(user, channel, conan_file_path, output, search_manager, client_cache,
               keep_source=False, filename=None, name=None, version=None):
    """ Export the recipe
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
    conan_linter(conan_file_path, output)
    conanfile = _load_export_conanfile(conan_file_path, output, name, version)
    conan_ref = ConanFileReference(conanfile.name, conanfile.version, user, channel)
    conan_ref_str = str(conan_ref)
    # Maybe a platform check could be added, but depends on disk partition
    refs = search_manager.search(conan_ref_str, ignorecase=True)
    if refs and conan_ref not in refs:
        raise ConanException("Cannot export package with same name but different case\n"
                             "You exported '%s' but already existing '%s'"
                             % (conan_ref_str, " ".join(str(s) for s in refs)))
    output = ScopedOutput(str(conan_ref), output)
    with client_cache.conanfile_write_lock(conan_ref):
        _export_conanfile(output, client_cache, conanfile, src_folder, conan_ref, keep_source,
                          filename)


def _load_export_conanfile(conanfile_path, output, name, version):
    conanfile = load_conanfile_class(conanfile_path)

    for field in ["url", "license", "description"]:
        field_value = getattr(conanfile, field, None)
        if not field_value:
            output.warn("Conanfile doesn't have '%s'.\n"
                        "It is recommended to add it as attribute" % field)

    try:
        # Exports is the only object field, we need to do this, because conan export needs it
        conanfile.exports = create_exports(conanfile)
        conanfile.exports_sources = create_exports_sources(conanfile)
    except Exception as e:  # re-raise with file name
        raise ConanException("%s: %s" % (conanfile_path, str(e)))

    # check name and version were specified
    if not conanfile.name:
        if name:
            conanfile.name = name
        else:
            raise ConanException("conanfile didn't specify name")
    elif name and name != conanfile.name:
        raise ConanException("Package recipe exported with name %s!=%s" % (name, conanfile.name))

    if not conanfile.version:
        if version:
            conanfile.version = version
        else:
            raise ConanException("conanfile didn't specify version")
    elif version and version != conanfile.version:
        raise ConanException("Package recipe exported with version %s!=%s"
                             % (version, conanfile.version))

    return conanfile


def _export_conanfile(output, paths, conanfile, origin_folder, conan_ref, keep_source, filename):
    destination_folder = paths.export(conan_ref)
    exports_source_folder = paths.export_sources(conan_ref, conanfile.short_paths)
    previous_digest = _init_export_folder(destination_folder, exports_source_folder)
    _execute_export(conanfile, origin_folder, destination_folder, exports_source_folder,
                    output, filename)

    digest = FileTreeManifest.create(destination_folder, exports_source_folder)

    if previous_digest and previous_digest == digest:
        output.info("The stored package has not changed")
        modified_recipe = False
        digest = previous_digest  # Use the old one, keep old timestamp
    else:
        output.success('A new %s version was exported' % CONANFILE)
        output.info('Folder: %s' % destination_folder)
        modified_recipe = True
    save(os.path.join(destination_folder, CONAN_MANIFEST), str(digest))

    source = paths.source(conan_ref, conanfile.short_paths)
    remove = False
    if is_dirty(source):
        output.info("Source folder is dirty, forcing removal")
        remove = True
    elif modified_recipe and not keep_source and os.path.exists(source):
        output.info("Package recipe modified in export, forcing source folder removal")
        output.info("Use the --keep-source, -k option to skip it")
        remove = True
    if remove:
        output.info("Removing 'source' folder, this can take a while for big packages")
        try:
            # remove only the internal
            rmdir(source)
        except BaseException as e:
            output.error("Unable to delete source folder. "
                         "Will be marked as dirty for deletion")
            output.warn(str(e))
            set_dirty(source)


def _init_export_folder(destination_folder, destination_src_folder):
    previous_digest = None
    try:
        if os.path.exists(destination_folder):
            if os.path.exists(os.path.join(destination_folder, CONAN_MANIFEST)):
                manifest_content = load(os.path.join(destination_folder, CONAN_MANIFEST))
                previous_digest = FileTreeManifest.loads(manifest_content)
            # Maybe here we want to invalidate cache
            rmdir(destination_folder)
        os.makedirs(destination_folder)
    except Exception as e:
        raise ConanException("Unable to create folder %s\n%s" % (destination_folder, str(e)))
    try:
        if os.path.exists(destination_src_folder):
            rmdir(destination_src_folder)
        os.makedirs(destination_src_folder)
    except Exception as e:
        raise ConanException("Unable to create folder %s\n%s" % (destination_src_folder, str(e)))
    return previous_digest


def _execute_export(conanfile, origin_folder, destination_folder, destination_source_folder,
                    output, filename=None):

    def classify_patterns(patterns):
        patterns = patterns or []
        included, excluded = [], []
        for p in patterns:
            if p.startswith("!"):
                excluded.append(p[1:])
            else:
                included.append(p)
        return included, excluded

    included_exports, excluded_exports = classify_patterns(conanfile.exports)
    included_sources, excluded_sources = classify_patterns(conanfile.exports_sources)

    try:
        os.unlink(os.path.join(origin_folder, CONANFILE + 'c'))
    except OSError:
        pass

    copier = FileCopier(origin_folder, destination_folder)
    for pattern in included_exports:
        copier(pattern, links=True, excludes=excluded_exports)
    copier = FileCopier(origin_folder, destination_source_folder)
    for pattern in included_sources:
        copier(pattern, links=True, excludes=excluded_sources)
    package_output = ScopedOutput("%s export" % output.scope, output)
    copier.report(package_output)

    shutil.copy2(os.path.join(origin_folder, filename or CONANFILE),
                 os.path.join(destination_folder, CONANFILE))
