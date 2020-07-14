from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from conans import __version__ as client_version
import os

# A little hack to get around Conan's forcing User-Agent which unfortunately
# makes the tools.get fail against Angelscript server (it seems to be blocking
# Python's requests User-Agent)
class immutable_dict(dict):
    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        pass

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable
    
class AngelscriptConan(ConanFile):
    name = "angelscript"    
    license = "Zlib"        
    description = "Angelscript is an extremely flexible cross-platform scripting library designed to allow applications to extend their functionality through external scripts"    
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    
    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="sdk/angelscript/projects/cmake")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)
  
    def source(self):        
        try:
            sources = self.conan_data["sources"][self.version]
            url = sources["url"]
            sha256 = sources["sha256"]            
        except KeyError:
            raise ConanInvalidConfiguration("No matching download URL for specified version: {}. Check conandata.yml.".format(self.version))
        tools.get(url, sha256=sha256, headers=immutable_dict({"User-Agent": "Conan/{}".format(client_version)}))
        
    def package(self):
        self.copy("*.h", dst="include", src="sdk/angelscript/include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["angelscriptd"]
        else:
            self.cpp_info.libs = ["angelscript"]
