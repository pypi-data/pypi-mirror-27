from os.path import join, exists, isdir
import os.path


def is_platform(dirname):
    return exists(join(dirname, "platform.txt")) and \
           exists(join(dirname, "boards.txt")) and \
           exists(join(dirname, "programmers.txt"))


def is_library_with_src(dirname):
    return exists(join(dirname, "library.properties")) and \
           exists(join(dirname, "src")) and \
           isdir(join(dirname, "src"))


def is_library_without_src(dirname):
    return exists(join(dirname, "library.properties")) and \
           not exists(join(dirname, "src")) and \
           not isdir(join(dirname, "src"))


def is_library_platformio_with_src(dirname):
    return exists(join(dirname, "library.properties")) and \
           exists(join(dirname, "src")) and \
           isdir(join(dirname, "src"))


def is_library_platformio_without_src(dirname):
    return exists(join(dirname, "library.properties")) and \
           not exists(join(dirname, "src")) and \
           not isdir(join(dirname, "src"))


def identify_template(dirname):
    order = [
        (is_platform, "platform.cmake"),
        (is_library_platformio_with_src, "library-with-src.cmake"),
        (is_library_platformio_without_src, "library-without-src.cmake"),
        (is_library_with_src, "library-with-src.cmake"),
        (is_library_without_src, "library-without-src.cmake")
    ]
    for test, cmake in order:
        if test(dirname):
            return join(os.path.dirname(__file__), "templates", cmake)
