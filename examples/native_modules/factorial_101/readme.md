## Defining a native module
ref: http://docs.micropython.org/en/latest/develop/natmod.html#natmod
A native .mpy module is defined by a set of files that are used to build the .mpy. The filesystem layout consists of two main parts, the source files and the Makefile:

In the simplest case only a single C source file is required, which contains all the code that will be compiled into the .mpy module. This C source code must include the py/dynruntime.h file to access the MicroPython dynamic API, and must at least define a function called mpy_init. This function will be the entry point of the module, called when the module is imported.

The module can be split into multiple C source files if desired. Parts of the module can also be implemented in Python. All source files should be listed in the Makefile, by adding them to the SRC variable (see below). This includes both C source files as well as any Python files which will be included in the resulting .mpy file.

The Makefile contains the build configuration for the module and list the source files used to build the .mpy module. It should define MPY_DIR as the location of the MicroPython repository (to find header files, the relevant Makefile fragment, and the mpy_ld.py tool), MOD as the name of the module, SRC as the list of source files, optionally specify the machine architecture via ARCH, and then include py/dynruntime.mk.

## Minimal example
This section provides a fully working example of a simple module named factorial. This module provides a single function factorial.factorial(x) which computes the factorial of the input and returns the result.