import os
import platform

from collections import OrderedDict
from contextlib import contextmanager

from conans.client import defs_to_string, join_arguments
from conans.errors import ConanException
from conans.model.conan_file import ConanFile
from conans.util.env_reader import get_env
from conans.util.files import mkdir
from conans.tools import cpu_count, args_to_string
from conans import tools
from conans.util.log import logger
from conans.util.config_parser import get_bool_from_text


def _get_env_cmake_system_name():
    env_system_name = get_env("CONAN_CMAKE_SYSTEM_NAME", "")
    return {"False": False, "True": True, "": None}.get(env_system_name, env_system_name)


class CMake(object):

    def __init__(self, conanfile, generator=None, cmake_system_name=True,
                 parallel=True, build_type=None, toolset=None):
        """
        :param settings_or_conanfile: Conanfile instance (or settings for retro compatibility)
        :param generator: Generator name to use or none to autodetect
        :param cmake_system_name: False to not use CMAKE_SYSTEM_NAME variable,
               True for auto-detect or directly a string with the system name
        :param parallel: Try to build with multiple cores if available
        :param build_type: Overrides default build type comming from settings
        :param toolset: Toolset name to use (such as llvm-vs2014) or none for default one,
                applies only to certain generators (e.g. Visual Studio)
        """
        if not isinstance(conanfile, ConanFile):
            raise ConanException("First argument of CMake() has to be ConanFile. Use CMake(self)")

        self._settings = conanfile.settings
        self._conanfile = conanfile

        self._os = self._settings.get_safe("os")
        self._compiler = self._settings.get_safe("compiler")
        self._compiler_version = self._settings.get_safe("compiler.version")
        self._arch = self._settings.get_safe("arch")
        self._op_system_version = self._settings.get_safe("os.version")
        self._libcxx = self._settings.get_safe("compiler.libcxx")
        self._runtime = self._settings.get_safe("compiler.runtime")
        self._build_type = self._settings.get_safe("build_type")

        self.generator = generator or self._generator()
        self.toolset = self._toolset(toolset)
        self.build_dir = None
        self._cmake_system_name = _get_env_cmake_system_name()
        if self._cmake_system_name is None:  # Not overwritten using environment
            self._cmake_system_name = cmake_system_name
        self.parallel = parallel
        self.definitions = self._get_cmake_definitions()
        if build_type and build_type != self._build_type:
            # Call the setter to warn and update the definitions if needed
            self.build_type = build_type

    @property
    def build_type(self):
        return self._build_type

    @build_type.setter
    def build_type(self, build_type):
        settings_build_type = self._settings.get_safe("build_type")
        if build_type != settings_build_type:
            self._conanfile.output.warn(
                'Set CMake build type "%s" is different than the settings build_type "%s"'
                % (build_type, settings_build_type))
        self._build_type = build_type
        self.definitions.update(self._build_type_definition())

    @property
    def flags(self):
        return defs_to_string(self.definitions)

    def _generator(self):

        if not self._compiler or not self._compiler_version or not self._arch:
            raise ConanException("You must specify compiler, compiler.version and arch in "
                                 "your settings to use a CMake generator")

        if "CONAN_CMAKE_GENERATOR" in os.environ:
            return os.environ["CONAN_CMAKE_GENERATOR"]

        if self._compiler == "Visual Studio":
            _visuals = {'8': '8 2005',
                        '9': '9 2008',
                        '10': '10 2010',
                        '11': '11 2012',
                        '12': '12 2013',
                        '14': '14 2015',
                        '15': '15 2017'}
            base = "Visual Studio %s" % _visuals.get(self._compiler_version,
                                                     "UnknownVersion %s" % self._compiler_version)
            if self._arch == "x86_64":
                return base + " Win64"
            elif "arm" in self._arch:
                return base + " ARM"
            else:
                return base

        if self._os == "Windows":
            return "MinGW Makefiles"  # it is valid only under Windows

        return "Unix Makefiles"

    def _toolset(self, toolset=None):
        if toolset:
            return toolset
        elif self._settings.get_safe("compiler") == "Visual Studio":
            subs_toolset = self._settings.get_safe("compiler.toolset")
            if subs_toolset:
                return subs_toolset
        return None

    def _cmake_compiler_options(self, the_os, arch):
        cmake_definitions = OrderedDict()

        if str(the_os).lower() == "macos":
            if arch == "x86":
                cmake_definitions["CMAKE_OSX_ARCHITECTURES"] = "i386"
        return cmake_definitions

    def _cmake_cross_build_defines(self, the_os, os_ver):
        ret = OrderedDict()
        os_ver = get_env("CONAN_CMAKE_SYSTEM_VERSION", os_ver)
        toolchain_file = get_env("CONAN_CMAKE_TOOLCHAIN_FILE", "")

        if toolchain_file != "":
            logger.info("Setting Cross build toolchain file: %s" % toolchain_file)
            ret["CMAKE_TOOLCHAIN_FILE"] = toolchain_file
            return ret

        if self._cmake_system_name is False:
            return ret

        if self._cmake_system_name is not True:  # String not empty
            ret["CMAKE_SYSTEM_NAME"] = self._cmake_system_name
            ret["CMAKE_SYSTEM_VERSION"] = os_ver
        else:  # detect if we are cross building and the system name and version
            platform_os = {"Darwin": "Macos"}.get(platform.system(), platform.system())
            if (platform_os != the_os) or os_ver:  # We are cross building
                if the_os:
                    ret["CMAKE_SYSTEM_NAME"] = "Darwin" if the_os in ["iOS", "tvOS", "watchOS"] else the_os
                    if os_ver:
                        ret["CMAKE_SYSTEM_VERSION"] = os_ver
                else:
                    ret["CMAKE_SYSTEM_NAME"] = "Generic"

        if ret:  # If enabled cross compile
            for env_var in ["CONAN_CMAKE_SYSTEM_PROCESSOR",
                            "CONAN_CMAKE_FIND_ROOT_PATH",
                            "CONAN_CMAKE_FIND_ROOT_PATH_MODE_PROGRAM",
                            "CONAN_CMAKE_FIND_ROOT_PATH_MODE_LIBRARY",
                            "CONAN_CMAKE_FIND_ROOT_PATH_MODE_INCLUDE"]:

                value = os.getenv(env_var, None)
                if value:
                    ret[env_var] = value

            if self._conanfile and self._conanfile.deps_cpp_info.sysroot:
                sysroot_path = self._conanfile.deps_cpp_info.sysroot
            else:
                sysroot_path = os.getenv("CONAN_CMAKE_FIND_ROOT_PATH", None)

            if sysroot_path:
                # Needs to be set here, can't be managed in the cmake generator, CMake needs
                # to know about the sysroot before any other thing
                ret["CMAKE_SYSROOT"] = sysroot_path.replace("\\", "/")

            # Adjust Android stuff
            if self._os == "Android":
                arch_abi_settings = {"armv8": "arm64-v8a",
                                     "armv7": "armeabi-v7a",
                                     "armv7hf": "armeabi-v7a",
                                     "armv6": "armeabi-v6",
                                     "armv5": "armeabi"
                                     }.get(self._arch,
                                           self._arch)
                if arch_abi_settings:
                    ret["CMAKE_ANDROID_ARCH_ABI"] = arch_abi_settings

        logger.info("Setting Cross build flags: %s"
                    % ", ".join(["%s=%s" % (k, v) for k, v in ret.items()]))
        return ret

    @property
    def is_multi_configuration(self):
        """ some IDEs are multi-configuration, as Visual. Makefiles or Ninja are single-conf
        """
        if "Visual" in self.generator or "Xcode" in self.generator:
            return True
        # TODO: complete logic
        return False

    @property
    def command_line(self):
        args = [
            '-G "%s"' % self.generator,
            self.flags,
            '-Wno-dev'
        ]
        if self.toolset:
            args.append('-T "%s"' % self.toolset)
        return join_arguments(args)

    def _build_type_definition(self):
        if self._build_type and not self.is_multi_configuration:
            return {'CMAKE_BUILD_TYPE': self._build_type}
        return {}

    @property
    def runtime(self):
        return defs_to_string(self._runtime_definition())

    def _runtime_definition(self):
        if self._runtime:
            return {"CONAN_LINK_RUNTIME": "/%s" % self._runtime}
        return {}

    @property
    def build_config(self):
        """ cmake --build tool have a --config option for Multi-configuration IDEs
        """
        if self._build_type and self.is_multi_configuration:
            return "--config %s" % self._build_type
        return ""

    def _get_cmake_definitions(self):
        ret = OrderedDict()
        ret.update(self._build_type_definition())
        ret.update(self._runtime_definition())
        ret.update(self._cmake_compiler_options(the_os=self._os,  arch=self._arch))
        ret.update(self._cmake_cross_build_defines(the_os=self._os, os_ver=self._op_system_version))

        ret["CONAN_EXPORTED"] = "1"
        if self._compiler:
            ret["CONAN_COMPILER"] = self._compiler
        if self._compiler_version:
            ret["CONAN_COMPILER_VERSION"] = str(self._compiler_version)

        # Force compiler flags -- TODO: give as environment/setting parameter?
        if self._os in ("Linux", "FreeBSD", "SunOS"):
            if self._arch == "x86" or self._arch == "sparc":
                ret["CONAN_CXX_FLAGS"] = "-m32"
                ret["CONAN_SHARED_LINKER_FLAGS"] = "-m32"
                ret["CONAN_C_FLAGS"] = "-m32"

            if self._arch == "x86_64" or self._arch == "sparcv9":
                ret["CONAN_CXX_FLAGS"] = "-m64"
                ret["CONAN_SHARED_LINKER_FLAGS"] = "-m64"
                ret["CONAN_C_FLAGS"] = "-m64"

        if self._libcxx:
            ret["CONAN_LIBCXX"] = self._libcxx

        # Shared library
        try:
            ret["BUILD_SHARED_LIBS"] = "ON" if self._conanfile.options.shared else "OFF"
        except ConanException:
            pass

        # Install to package folder
        try:
            if self._conanfile.package_folder:
                ret["CMAKE_INSTALL_PREFIX"] = self._conanfile.package_folder
        except AttributeError:
            pass

        if str(self._os) in ["Windows", "WindowsStore"] and self._compiler == "Visual Studio":
            if self.parallel:
                cpus = tools.cpu_count()
                ret["CONAN_CXX_FLAGS"] = "/MP%s" % cpus
                ret["CONAN_C_FLAGS"] = "/MP%s" % cpus
        return ret

    def configure(self, args=None, defs=None, source_dir=None, build_dir=None):
        args = args or []
        defs = defs or {}
        source_dir = source_dir or self._conanfile.source_folder
        self.build_dir = build_dir or self.build_dir or self._conanfile.build_folder

        mkdir(self.build_dir)
        arg_list = join_arguments([
            self.command_line,
            args_to_string(args),
            defs_to_string(defs),
            args_to_string([source_dir])
        ])
        command = "cd %s && cmake %s" % (args_to_string([self.build_dir]), arg_list)
        if platform.system() == "Windows" and self.generator == "MinGW Makefiles":
            with clean_sh_from_path():
                self._conanfile.run(command)
        else:
            self._conanfile.run(command)

    def build(self, args=None, build_dir=None, target=None):
        args = args or []
        build_dir = build_dir or self.build_dir or self._conanfile.build_folder
        if target is not None:
            args = ["--target", target] + args

        if self.parallel:
            if "Makefiles" in self.generator:
                if "--" not in args:
                    args.append("--")
                args.append("-j%i" % cpu_count())
            elif "Visual Studio" in self.generator:
                if "--" not in args:
                    args.append("--")
                args.append("/m:%i" % cpu_count())

        arg_list = join_arguments([
            args_to_string([build_dir]),
            self.build_config,
            args_to_string(args)
        ])
        command = "cmake --build %s" % arg_list
        self._conanfile.run(command)

    def install(self, args=None, build_dir=None):
        mkdir(self._conanfile.package_folder)
        if not self.definitions.get("CMAKE_INSTALL_PREFIX"):
            raise ConanException("CMAKE_INSTALL_PREFIX not defined for 'cmake.install()'\n"
                                 "Make sure 'package_folder' is defined")
        self.build(args=args, build_dir=build_dir, target="install")

    def test(self, args=None, build_dir=None, target=None):
        if not target:
            target = "RUN_TESTS" if self.is_multi_configuration else "test"
        self.build(args=args, build_dir=build_dir, target=target)

    @property
    def verbose(self):
        try:
            verbose = self.definitions["CMAKE_VERBOSE_MAKEFILE"]
            return get_bool_from_text(str(verbose))
        except KeyError:
            return False

    @verbose.setter
    def verbose(self, value):
        self.definitions["CMAKE_VERBOSE_MAKEFILE"] = "ON" if value else "OFF"


@contextmanager
def clean_sh_from_path():
    new_path = []
    for path_entry in os.environ.get("PATH", "").split(os.pathsep):
        if not os.path.exists(os.path.join(path_entry, "sh.exe")):
            new_path.append(path_entry)
    with tools.environment_append({"PATH": os.pathsep.join(new_path)}):
        yield
