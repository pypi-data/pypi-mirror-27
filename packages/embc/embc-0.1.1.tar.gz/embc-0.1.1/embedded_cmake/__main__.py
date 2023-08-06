"""
Usage:
  embc list
  embc init <toolchain> [--cpu=<cpu>] [-f=<frequency>] [--debug]
  embc install <url>
  embc build [--verbose]
  embc update
  embc -h | --help
  embc --version

Options:
  -h --help       Show this help
  --version       Show project version
  --cpu=<cpu>     Override the default CPU type
  -f=<frequency>  Override the default CPU frequency
  --verbose       Be verbose during build
"""

from __future__ import print_function
import docopt
import os

import subprocess
from jinja2 import Template

from . import environment as env
from .gitutils import update
import glob


from .download import download, download_git
from .libs import identify_template

def install_cmake():
    if not os.path.exists(env.CMAKE_ROOT):
        print("Downloading cmake...")
        download(env.CMAKE_PACKAGE, env.CMAKE_ROOT)

def find_cmake():
    candidates = glob.glob(os.path.join(env.CMAKE_ROOT, "cmake-*", "bin", "cmake"))
    return candidates[0]

def install_embedded_cmake():
    if not os.path.exists(env.CMAKE_SCRIPTS):
        print("Downloading embedded cmake scripts...")
        download_git(env.CMAKE_SCRIPTS_URL, env.CMAKE_SCRIPTS)

def update_embedded_cmake():
    install_embedded_cmake()
    update(env.CMAKE_SCRIPTS)

def toolchain_info(filename):
    with open(os.path.join(env.TOOLCHAINS_DIR, filename)) as f:
        header = f.readline()
    name = os.path.basename(filename).replace(".cmake", "")
    if not header.startswith("#"):
        header = ""
    return name + "\t\t" + header.lstrip("# \t")

def prepare_template(filename, toolchain_name, *args, **kwargs):
    if not os.path.exists(filename):
        template_file = os.path.join(env.TEMPLATE_DIR, toolchain_name, filename)
        if os.path.exists(template_file):
            print("Preparing default " + filename)
            with open(filename, "w") as dest, open(template_file) as tpl:
                template = Template(tpl.read())
                dest.write(template.render(*args, **kwargs))
        else:
            print(filename + " template for " + toolchain_name +
                  " not found. Please create it manually")
    else:
        print("Keeping the existing " + filename + " intact")

def run_cmake(*args):
    cmake_bin = find_cmake()
    cmake_bindir = os.path.dirname(cmake_bin)
    cmake_root = os.path.abspath(os.path.dirname(cmake_bindir))

    newenv = {}
    newenv.update(os.environ)
    newenv["CMAKE_ROOT"] = cmake_root
    newenv["PATH"] = cmake_bindir + ":" + newenv["PATH"]

    subprocess.Popen(("cmake",) + args,
                     executable = cmake_bin,
                     env = newenv).wait()

def find_initialized_root():
    cwd = os.getcwd()
    while cwd and not os.path.exists(os.path.join(cwd, "CMakeLists.txt")):
        cwd = os.path.dirname(cwd)
    return cwd

def switch_to_initialized_root():
    root = find_initialized_root()
    if not root:
        print("Could not find initialized project root.")
        exit(1)
    if root != os.getcwd():
        print("Using {root} as the project root.".format(root=root))
    os.chdir(root)

if __name__ == "__main__":
    options = docopt.docopt(__doc__, version = "0.1")
    print(options)

    if len(options) == 0:
        print(__doc__)
        exit(1)

    if options["update"]:
        install_cmake()
        update_embedded_cmake()
        exit(0)

    if options["list"]:
        install_embedded_cmake()
        toolchains = os.listdir(env.TOOLCHAINS_DIR)
        [ print(toolchain_info(toolchain))
          for toolchain in sorted(toolchains)
          if toolchain.endswith(".cmake") ]
        exit(0)

    if options["install"]:
        switch_to_initialized_root()
        url=options["<url>"]
        dirname, fmt = download(url, root=env.PACKAGES_DIR)
        try:
            os.makedirs(env.PROJECT_LIB)
        except OSError:
            pass

        name = os.path.basename(dirname)
        tplpath = identify_template(dirname)
        cmakepath = os.path.join(env.PROJECT_LIB, "use-" + name + ".cmake")

        with open(tplpath) as tplfd, open(cmakepath, "w") as cmakefd:
            template = Template(tplfd.read())
            cmakefd.write(template.render(
                name=name,
                format=fmt,
                url=url,
                dirname=dirname
            ))
        exit(0)

    if options["build"]:
        switch_to_initialized_root()
        install_cmake()
        makecmd = ["make"]
        if options["--verbose"]:
            makecmd.append("VERBOSE=1")

        for f in os.listdir("."):
            if os.path.isdir(f) and f.startswith("build-"):
                cwd = os.getcwd()
                os.chdir(f)
                print("--- Building {toolchain} ---".format(toolchain = f[6:]))
                rc = subprocess.Popen(makecmd).wait()
                os.chdir(cwd)
                if rc != 0:
                    exit(1)
        exit(0)

    if options["init"]:
        install_cmake()
        install_embedded_cmake()
        toolchain_name = options["<toolchain>"]
        toolchain = os.path.join(env.TOOLCHAINS_DIR, toolchain_name + ".cmake")

        if not os.path.exists(toolchain):
            print("The requested toolchain " + toolchain_name + " does not exist.")
            exit(1)

        # Prepare template CMakefile
	TEMPLATE_DIR=os.path.join(env.TEMPLATE_DIR, toolchain_name)
	if os.path.exists(TEMPLATE_DIR):
            for tpl in os.listdir(TEMPLATE_DIR):
                prepare_template(tpl,
                                 toolchain_name,
                                 CPU = options["--cpu"],
                                 F_CPU = options["-f"])

        # Create build directory
        try:
          os.makedirs("build-" + toolchain_name)
        except OSError:
            pass

        # Prepare toolchain file
        tpl_file = os.path.join(os.path.dirname(__file__), "templates", "Toolchain.cmake")
        toolchain_file = "Toolchain-{name}.cmake".format(name=toolchain_name)
        with open(tpl_file, "r") as tpl_fd,\
                open(toolchain_file, "w") as toolchain_fd:
            template = Template(tpl_fd.read())
            toolchain_fd.write(template.render(
                TOOLCHAIN_NAME = toolchain_name,
                TOOLCHAIN_FILE = toolchain,
                PREFIX_PATH = env.PACKAGES_DIR,
                DOWNLOAD_DIR = env.PACKAGES_DIR,
                TOOLCHAIN_ROOT = env.PACKAGES_DIR
            ))

        cwd = os.getcwd()
        os.chdir("build-" + toolchain_name)

        run_cmake("--no-warn-unused-cli",
                  "-Wno-dev",
                  "-DDOWNLOAD_DEPENDENCIES=1",
                  "-DCMAKE_TOOLCHAIN_FILE=" + os.path.join(cwd, toolchain_file),
                  "-DCMAKE_BUILD_TYPE=Release" if not options["--debug"] else "-DCMAKE_BUILD_TYPE=Debug",
                  "..")

        os.chdir(cwd)
        exit(0)

