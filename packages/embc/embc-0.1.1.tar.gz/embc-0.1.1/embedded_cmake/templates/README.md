# Internal template directory

This directory will contain mostly template CMakeLists.txt files
used for importing Arduino, Energia, mbed or platformio libraries.

Install phase of those will unpack them somewhere (most likely
under project/lib/) and generate a relevant CMakeLists.txt file
using templates from here. Including the template to the main
CMakelists.txt will add the lib to the project.
