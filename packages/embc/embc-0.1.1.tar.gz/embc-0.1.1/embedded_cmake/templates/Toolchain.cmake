# Preconfigured toolchain file for {{ TOOLCHAIN_NAME }}
SET(TOOLCHAIN_ROOT "{{ TOOLCHAIN_ROOT }}" CACHE INTERNAL "Root directory for all toolchain bits and pieces" FORCE)
SET(CMAKE_PREFIX_PATH "{{ PREFIX_PATH }}" CACHE INTERNAL "Root directory for all downloaded tools" FORCE)
SET(DOWNLOAD_DIR "{{ DOWNLOAD_DIR }}" CACHE INTERNAL "Directory to use for downloading stuff" FORCE)
INCLUDE("{{ TOOLCHAIN_FILE }}")
