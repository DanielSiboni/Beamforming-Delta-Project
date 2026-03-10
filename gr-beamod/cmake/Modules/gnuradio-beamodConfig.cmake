find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_BEAMOD gnuradio-beamod)

FIND_PATH(
    GR_BEAMOD_INCLUDE_DIRS
    NAMES gnuradio/beamod/api.h
    HINTS $ENV{BEAMOD_DIR}/include
        ${PC_BEAMOD_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_BEAMOD_LIBRARIES
    NAMES gnuradio-beamod
    HINTS $ENV{BEAMOD_DIR}/lib
        ${PC_BEAMOD_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-beamodTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_BEAMOD DEFAULT_MSG GR_BEAMOD_LIBRARIES GR_BEAMOD_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_BEAMOD_LIBRARIES GR_BEAMOD_INCLUDE_DIRS)
