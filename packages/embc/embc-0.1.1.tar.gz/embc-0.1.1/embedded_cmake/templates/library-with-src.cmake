# CMake configuration for {{ name }} from {{ url }}
SET_PROPERTY(TARGET ${PROJECT} APPEND PROPERTY INCLUDE_DIRECTORIES "${TOOLCHAIN_ROOT}/{{ name }}/src")
FILE(GLOB_RECURSE FOUND
     "${TOOLCHAIN_ROOT}/{{ name }}/src/*.[cCsShH]"
     "${TOOLCHAIN_ROOT}/{{ name }}/src/*.[cCsShH][pP][pP]")
SET_PROPERTY(TARGET ${PROJECT} APPEND PROPERTY SOURCES ${FOUND})
