import os

HOME=os.path.expanduser('~')
EMBC=os.path.join(HOME, ".embc")

PACKAGES_DIR = os.path.join(EMBC, "packages")
CMAKE_ROOT = os.path.join(EMBC, "cmake")

CMAKE_SCRIPTS=os.path.join(EMBC, "scripts")
CMAKE_SCRIPTS_URL="https://MarSik@bitbucket.org/MarSik/embedded-cmake.git"

TOOLCHAINS_DIR = os.path.join(CMAKE_SCRIPTS, "Toolchains")
TEMPLATE_DIR = os.path.join(CMAKE_SCRIPTS, "Templates")
TEMPLATE_SUFFIX = ".j2"

CMAKE_PACKAGE = "https://cmake.org/files/v3.8/cmake-3.8.1-Linux-x86_64.tar.gz"

PROJECT_LIB = "lib"
