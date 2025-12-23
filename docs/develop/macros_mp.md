

### MP_BC

This configuration set defines the structure and behavior of bytecode operations in a MicroPython environment, including the encoding of various instructions, the handling of data types, and the management of control flow. It encompasses the creation and manipulation of fundamental data structures, function calls, and variable management, ensuring efficient execution of Python code at the bytecode level.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_BC_BASE_BYTE_E`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BASE_BYTE_E&type=code) | Base value for bytecode instructions with specific encoding. | (0x60) // --BREEEYYI------ |
| [`MP_BC_BASE_BYTE_O`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BASE_BYTE_O&type=code) | Base value for bytecode operations with specific bit patterns. | (0x50) // LLLLSSDTTTTTEEFF |
| [`MP_BC_BASE_JUMP_E`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BASE_JUMP_E&type=code) | Base value for jump-related bytecode operations. | (0x40) // J-JJJJJEEEEF---- |
| [`MP_BC_BASE_QSTR_O`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BASE_QSTR_O&type=code) | Base value for bytecode operations involving qstr (string) constants. | (0x10) // LLLLLLSSSDDII--- |
| [`MP_BC_BASE_RESERVED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BASE_RESERVED&type=code) | Indicates reserved opcode value for bytecode. | (0x00) // ---------------- |
| [`MP_BC_BASE_VINT_E`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BASE_VINT_E&type=code) | Base value for variable-length integer bytecode operations. | (0x20) // MMLLLLSSDDBBBBBB |
| [`MP_BC_BASE_VINT_O`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BASE_VINT_O&type=code) | Base value for variable integer bytecode operations. | (0x30) // UUMMCCCC-------- |
| [`MP_BC_BINARY_OP_MULTI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BINARY_OP_MULTI&type=code) | Represents a multi-byte binary operation opcode. | (0xd7) //        OOOOOOOOO |
| [`MP_BC_BINARY_OP_MULTI_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BINARY_OP_MULTI_NUM&type=code) | Defines the number of binary operation bytecode instructions. | (MP_BINARY_OP_NUM_BYTECODE) |
| [`MP_BC_BUILD_LIST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BUILD_LIST&type=code) | Represents the bytecode operation for building a list. | (MP_BC_BASE_VINT_E + 0x0b) // uint |
| [`MP_BC_BUILD_MAP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BUILD_MAP&type=code) | Represents the bytecode instruction for building a map (dictionary) object. | (MP_BC_BASE_VINT_E + 0x0c) // uint |
| [`MP_BC_BUILD_SET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BUILD_SET&type=code) | Represents the bytecode operation for building a set. | (MP_BC_BASE_VINT_E + 0x0d) // uint |
| [`MP_BC_BUILD_SLICE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BUILD_SLICE&type=code) | Represents the bytecode for building a slice object. | (MP_BC_BASE_VINT_E + 0x0e) // uint |
| [`MP_BC_BUILD_TUPLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_BUILD_TUPLE&type=code) | Represents the bytecode operation for building a tuple. | (MP_BC_BASE_VINT_E + 0x0a) // uint |
| [`MP_BC_CALL_FUNCTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_CALL_FUNCTION&type=code) | Represents the bytecode instruction for calling a function with positional and keyword arguments. | (MP_BC_BASE_VINT_O + 0x04) // uint |
| [`MP_BC_CALL_FUNCTION_VAR_KW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_CALL_FUNCTION_VAR_KW&type=code) | Represents a bytecode instruction for calling a function with variable positional and keyword arguments. | (MP_BC_BASE_VINT_O + 0x05) // uint |
| [`MP_BC_CALL_METHOD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_CALL_METHOD&type=code) | Represents the bytecode operation for calling a method with positional and keyword arguments. | (MP_BC_BASE_VINT_O + 0x06) // uint |
| [`MP_BC_CALL_METHOD_VAR_KW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_CALL_METHOD_VAR_KW&type=code) | Represents a bytecode instruction for calling a method with variable positional and keyword arguments. | (MP_BC_BASE_VINT_O + 0x07) // uint |
| [`MP_BC_DELETE_DEREF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_DELETE_DEREF&type=code) | Represents a bytecode operation for deleting a dereferenced variable. | (MP_BC_BASE_VINT_E + 0x09) // uint |
| [`MP_BC_DELETE_FAST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_DELETE_FAST&type=code) | Represents a bytecode operation for fast deletion of local variables. | (MP_BC_BASE_VINT_E + 0x08) // uint |
| [`MP_BC_DELETE_GLOBAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_DELETE_GLOBAL&type=code) | Bytecode for deleting a global variable identified by a qstr. | (MP_BC_BASE_QSTR_O + 0x0a) // qstr |
| [`MP_BC_DELETE_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_DELETE_NAME&type=code) | Bytecode for deleting a variable by name, represented as a qstr. | (MP_BC_BASE_QSTR_O + 0x09) // qstr |
| [`MP_BC_DUP_TOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_DUP_TOP&type=code) | Replicates the top item on the stack. | (MP_BC_BASE_BYTE_O + 0x07) |
| [`MP_BC_DUP_TOP_TWO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_DUP_TOP_TWO&type=code) | Duplicates the top two items on the stack. | (MP_BC_BASE_BYTE_O + 0x08) |
| [`MP_BC_END_FINALLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_END_FINALLY&type=code) | Handles the end of a finally block, managing the top of stack based on its value. | (MP_BC_BASE_BYTE_O + 0x0d) |
| [`MP_BC_FORMAT_BYTE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_FORMAT_BYTE&type=code) | Represents the byte format in bytecode. | (0) |
| [`MP_BC_FORMAT_OFFSET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_FORMAT_OFFSET&type=code) | Indicates an opcode format that uses an offset for addressing. | (3) |
| [`MP_BC_FORMAT_QSTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_FORMAT_QSTR&type=code) | Indicates that the bytecode format is a QSTR (string constant). Examples include loading string constants in bytecode operations. | (1) |
| [`MP_BC_FORMAT_VAR_UINT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_FORMAT_VAR_UINT&type=code) | Indicates a variable-length unsigned integer format for bytecode. | (2) |
| [`MP_BC_FOR_ITER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_FOR_ITER&type=code) | Unsigned relative bytecode offset for the 'for' iteration operation. | (MP_BC_BASE_JUMP_E + 0x0b) // unsigned relative bytecode offset |
| [`MP_BC_GET_ITER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_GET_ITER&type=code) | Bytecode for retrieving an iterator from the top of the stack. | (MP_BC_BASE_BYTE_O + 0x0e) |
| [`MP_BC_GET_ITER_STACK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_GET_ITER_STACK&type=code) | Bytecode for obtaining an iterator using stack slots. | (MP_BC_BASE_BYTE_O + 0x0f) |
| [`MP_BC_IMPORT_FROM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_IMPORT_FROM&type=code) | Opcode for importing a specific attribute from a module. | (MP_BC_BASE_QSTR_O + 0x0c) // qstr |
| [`MP_BC_IMPORT_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_IMPORT_NAME&type=code) | Represents the bytecode operation for importing a module by name. | (MP_BC_BASE_QSTR_O + 0x0b) // qstr |
| [`MP_BC_IMPORT_STAR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_IMPORT_STAR&type=code) | Opcode for importing all names from a module. | (MP_BC_BASE_BYTE_E + 0x09) |
| [`MP_BC_JUMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_JUMP&type=code) | Represents a signed relative bytecode offset for a jump instruction. | (MP_BC_BASE_JUMP_E + 0x02) // signed relative bytecode offset |
| [`MP_BC_JUMP_IF_FALSE_OR_POP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_JUMP_IF_FALSE_OR_POP&type=code) | Handles jumping to a label if the top stack value is false, otherwise pops the value. | (MP_BC_BASE_JUMP_E + 0x06) // unsigned relative bytecode offset |
| [`MP_BC_JUMP_IF_TRUE_OR_POP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_JUMP_IF_TRUE_OR_POP&type=code) | Executes a jump if the top stack value is true, otherwise pops the value. | (MP_BC_BASE_JUMP_E + 0x05) // unsigned relative bytecode offset |
| [`MP_BC_LOAD_ATTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_ATTR&type=code) | Loads an attribute from an object using its qualified string identifier. | (MP_BC_BASE_QSTR_O + 0x03) // qstr |
| [`MP_BC_LOAD_BUILD_CLASS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_BUILD_CLASS&type=code) | Bytecode for loading the build class function. | (MP_BC_BASE_BYTE_O + 0x04) |
| [`MP_BC_LOAD_CONST_FALSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_FALSE&type=code) | Represents the bytecode instruction to load the constant value False. | (MP_BC_BASE_BYTE_O + 0x00) |
| [`MP_BC_LOAD_CONST_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_NONE&type=code) | Represents the bytecode operation to load the constant None onto the stack. | (MP_BC_BASE_BYTE_O + 0x01) |
| [`MP_BC_LOAD_CONST_OBJ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_OBJ&type=code) | Loads a constant object pointer onto the stack. | (MP_BC_BASE_VINT_E + 0x03) // ptr |
| [`MP_BC_LOAD_CONST_SMALL_INT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_SMALL_INT&type=code) | Loads a signed small integer constant using a variable-length encoding. | (MP_BC_BASE_VINT_E + 0x02) // signed var-int |
| [`MP_BC_LOAD_CONST_SMALL_INT_MULTI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_SMALL_INT_MULTI&type=code) | Represents a bytecode operation for loading multiple small integer constants. | (0x70) // LLLLLLLLLLLLLLLL |
| [`MP_BC_LOAD_CONST_SMALL_INT_MULTI_EXCESS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_SMALL_INT_MULTI_EXCESS&type=code) | Defines the excess offset for loading multiple small integer constants. | (16) |
| [`MP_BC_LOAD_CONST_SMALL_INT_MULTI_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_SMALL_INT_MULTI_NUM&type=code) | Defines the maximum number of small integer constants that can be loaded in a single bytecode operation. | (64) |
| [`MP_BC_LOAD_CONST_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_STRING&type=code) | Loads a constant string (qstr) onto the stack. | (MP_BC_BASE_QSTR_O + 0x00) // qstr |
| [`MP_BC_LOAD_CONST_TRUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_CONST_TRUE&type=code) | Represents the bytecode for loading the constant boolean value True. | (MP_BC_BASE_BYTE_O + 0x02) |
| [`MP_BC_LOAD_DEREF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_DEREF&type=code) | Represents a bytecode operation to load a variable from a closure or local scope. | (MP_BC_BASE_VINT_E + 0x05) // uint |
| [`MP_BC_LOAD_FAST_MULTI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_FAST_MULTI&type=code) | Bytecode for loading multiple fast local variables. | (0xb0) // LLLLLLLLLLLLLLLL |
| [`MP_BC_LOAD_FAST_MULTI_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_FAST_MULTI_NUM&type=code) | Indicates the number of fast variable loading bytecodes. | (16) |
| [`MP_BC_LOAD_FAST_N`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_FAST_N&type=code) | Represents a bytecode operation for loading a local variable by index. | (MP_BC_BASE_VINT_E + 0x04) // uint |
| [`MP_BC_LOAD_GLOBAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_GLOBAL&type=code) | Loads a global variable using its qstr identifier. | (MP_BC_BASE_QSTR_O + 0x02) // qstr |
| [`MP_BC_LOAD_METHOD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_METHOD&type=code) | Loads a method from an object using its qualified string identifier. | (MP_BC_BASE_QSTR_O + 0x04) // qstr |
| [`MP_BC_LOAD_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_NAME&type=code) | Represents a bytecode operation for loading a variable by name using a qstr. | (MP_BC_BASE_QSTR_O + 0x01) // qstr |
| [`MP_BC_LOAD_NULL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_NULL&type=code) | Represents the bytecode operation to load a null value (MP_OBJ_NULL). Examples include loading null in variable assignments or function returns. | (MP_BC_BASE_BYTE_O + 0x03) |
| [`MP_BC_LOAD_SUBSCR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_SUBSCR&type=code) | Bytecode for loading a subscription (indexing) operation. | (MP_BC_BASE_BYTE_O + 0x05) |
| [`MP_BC_LOAD_SUPER_METHOD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_LOAD_SUPER_METHOD&type=code) | Loads a method from a superclass using a qualified string. | (MP_BC_BASE_QSTR_O + 0x05) // qstr |
| [`MP_BC_MAKE_CLOSURE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_MAKE_CLOSURE&type=code) | Represents the bytecode operation for creating a closure with an extra byte. | (MP_BC_BASE_VINT_E + 0x00) // uint; extra byte |
| [`MP_BC_MAKE_CLOSURE_DEFARGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_MAKE_CLOSURE_DEFARGS&type=code) | Represents a bytecode instruction for creating a closure with additional arguments. | (MP_BC_BASE_VINT_E + 0x01) // uint; extra byte |
| [`MP_BC_MAKE_FUNCTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_MAKE_FUNCTION&type=code) | Represents the bytecode instruction for creating a function. | (MP_BC_BASE_VINT_O + 0x02) // uint |
| [`MP_BC_MAKE_FUNCTION_DEFARGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_MAKE_FUNCTION_DEFARGS&type=code) | Represents a bytecode instruction for creating a function with default arguments. | (MP_BC_BASE_VINT_O + 0x03) // uint |
| [`MP_BC_MASK_EXTRA_BYTE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_MASK_EXTRA_BYTE&type=code) | Mask for determining the presence of an extra byte in bytecode. | (0x9e) |
| [`MP_BC_MASK_FORMAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_MASK_FORMAT&type=code) | Mask for identifying bytecode format in instruction parsing. | (0xf0) |
| [`MP_BC_POP_EXCEPT_JUMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_POP_EXCEPT_JUMP&type=code) | Unsigned relative bytecode offset for jumping after popping an exception block. | (MP_BC_BASE_JUMP_E + 0x0a) // unsigned relative bytecode offset |
| [`MP_BC_POP_JUMP_IF_FALSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_POP_JUMP_IF_FALSE&type=code) | Represents a bytecode instruction that conditionally jumps if the top stack value is false. | (MP_BC_BASE_JUMP_E + 0x04) // signed relative bytecode offset |
| [`MP_BC_POP_JUMP_IF_TRUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_POP_JUMP_IF_TRUE&type=code) | Represents a bytecode instruction that pops a value and jumps if it is true, using a signed relative offset. | (MP_BC_BASE_JUMP_E + 0x03) // signed relative bytecode offset |
| [`MP_BC_POP_TOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_POP_TOP&type=code) | Removes the top item from the stack. | (MP_BC_BASE_BYTE_O + 0x09) |
| [`MP_BC_RAISE_FROM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_RAISE_FROM&type=code) | Represents a bytecode operation for raising exceptions with a specified cause. | (MP_BC_BASE_BYTE_E + 0x06) |
| [`MP_BC_RAISE_LAST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_RAISE_LAST&type=code) | Represents the bytecode operation for raising the last exception. | (MP_BC_BASE_BYTE_E + 0x04) |
| [`MP_BC_RAISE_OBJ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_RAISE_OBJ&type=code) | Represents bytecode for raising an exception object. | (MP_BC_BASE_BYTE_E + 0x05) |
| [`MP_BC_RETURN_VALUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_RETURN_VALUE&type=code) | Represents the bytecode operation for returning a value from a function. | (MP_BC_BASE_BYTE_E + 0x03) |
| [`MP_BC_ROT_THREE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_ROT_THREE&type=code) | Bytecode operation for rotating the top three stack elements. | (MP_BC_BASE_BYTE_O + 0x0b) |
| [`MP_BC_ROT_TWO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_ROT_TWO&type=code) | Rotates the top two values on the stack. | (MP_BC_BASE_BYTE_O + 0x0a) |
| [`MP_BC_SETUP_EXCEPT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_SETUP_EXCEPT&type=code) | Unsigned relative bytecode offset for setting up exception handling. | (MP_BC_BASE_JUMP_E + 0x08) // unsigned relative bytecode offset |
| [`MP_BC_SETUP_FINALLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_SETUP_FINALLY&type=code) | Defines an unsigned relative bytecode offset for the SETUP_FINALLY operation. | (MP_BC_BASE_JUMP_E + 0x09) // unsigned relative bytecode offset |
| [`MP_BC_SETUP_WITH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_SETUP_WITH&type=code) | Unsigned relative bytecode offset for the SETUP_WITH opcode. | (MP_BC_BASE_JUMP_E + 0x07) // unsigned relative bytecode offset |
| [`MP_BC_STORE_ATTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_ATTR&type=code) | Bytecode for storing an attribute value using a qualified string. | (MP_BC_BASE_QSTR_O + 0x08) // qstr |
| [`MP_BC_STORE_COMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_COMP&type=code) | Represents the bytecode operation for storing a comprehension result. | (MP_BC_BASE_VINT_E + 0x0f) // uint |
| [`MP_BC_STORE_DEREF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_DEREF&type=code) | Represents a bytecode operation for storing a value in a dereferenced variable. | (MP_BC_BASE_VINT_E + 0x07) // uint |
| [`MP_BC_STORE_FAST_MULTI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_FAST_MULTI&type=code) | Represents a bytecode operation for storing multiple fast local variables. | (0xc0) // SSSSSSSSSSSSSSSS |
| [`MP_BC_STORE_FAST_MULTI_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_FAST_MULTI_NUM&type=code) | Limits the number of fast store operations to 16. | (16) |
| [`MP_BC_STORE_FAST_N`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_FAST_N&type=code) | Represents a bytecode operation for storing a value in a fast local variable. | (MP_BC_BASE_VINT_E + 0x06) // uint |
| [`MP_BC_STORE_GLOBAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_GLOBAL&type=code) | Encodes the bytecode operation for storing a global variable using a qstr. | (MP_BC_BASE_QSTR_O + 0x07) // qstr |
| [`MP_BC_STORE_MAP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_MAP&type=code) | Bytecode for storing a value in a map (dictionary) object. | (MP_BC_BASE_BYTE_E + 0x02) |
| [`MP_BC_STORE_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_NAME&type=code) | Bytecode operation for storing a value in a variable identified by a qstr. | (MP_BC_BASE_QSTR_O + 0x06) // qstr |
| [`MP_BC_STORE_SUBSCR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_STORE_SUBSCR&type=code) | Bytecode for storing a value in a subscripted location. | (MP_BC_BASE_BYTE_O + 0x06) |
| [`MP_BC_UNARY_OP_MULTI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_UNARY_OP_MULTI&type=code) | Represents a bytecode for multiple unary operations. | (0xd0) // OOOOOOO |
| [`MP_BC_UNARY_OP_MULTI_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_UNARY_OP_MULTI_NUM&type=code) | Indicates the number of unary operation bytecodes available. | (MP_UNARY_OP_NUM_BYTECODE) |
| [`MP_BC_UNPACK_EX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_UNPACK_EX&type=code) | Handles unpacking of multiple values from a sequence with specified counts. | (MP_BC_BASE_VINT_O + 0x01) // uint |
| [`MP_BC_UNPACK_SEQUENCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_UNPACK_SEQUENCE&type=code) | Opcode for unpacking a sequence of values. | (MP_BC_BASE_VINT_O + 0x00) // uint |
| [`MP_BC_UNWIND_JUMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_UNWIND_JUMP&type=code) | Represents a signed relative bytecode offset for unwinding jumps in exception handling. | (MP_BC_BASE_JUMP_E + 0x00) // signed relative bytecode offset; then a byte |
| [`MP_BC_WITH_CLEANUP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_WITH_CLEANUP&type=code) | Represents bytecode for the 'with' statement that includes cleanup handling. | (MP_BC_BASE_BYTE_O + 0x0c) |
| [`MP_BC_YIELD_FROM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_YIELD_FROM&type=code) | Represents the bytecode operation for yielding from a generator. | (MP_BC_BASE_BYTE_E + 0x08) |
| [`MP_BC_YIELD_VALUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BC_YIELD_VALUE&type=code) | Represents the bytecode for yielding a value from a generator. | (MP_BC_BASE_BYTE_E + 0x07) |


### MP_BLOCKDEV

This configuration set manages the behavior and capabilities of block devices, including their initialization, synchronization, and interaction with filesystems. It provides flags and ioctl commands that facilitate operations such as reading, writing, and erasing blocks, as well as managing the lifecycle of block device objects.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_BLOCKDEV_FLAG_FREE_OBJ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_FLAG_FREE_OBJ&type=code) | Indicates that the fs_user_mount_t object should be freed upon unmounting. | (0x0002) // fs_user_mount_t obj should be freed on umount |
| [`MP_BLOCKDEV_FLAG_HAVE_IOCTL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_FLAG_HAVE_IOCTL&type=code) | Indicates support for the new block protocol with ioctl functionality. | (0x0004) // new protocol with ioctl |
| [`MP_BLOCKDEV_FLAG_NATIVE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_FLAG_NATIVE&type=code) | Indicates that readblocks[2]/writeblocks[2] contain native functions. | (0x0001) // readblocks[2]/writeblocks[2] contain native func |
| [`MP_BLOCKDEV_FLAG_NO_FILESYSTEM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_FLAG_NO_FILESYSTEM&type=code) | Indicates that the block device lacks a filesystem. | (0x0008) // the block device has no filesystem on it |
| [`MP_BLOCKDEV_IOCTL_BLOCK_COUNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_IOCTL_BLOCK_COUNT&type=code) | Retrieves the total number of blocks in a block device. | (4) |
| [`MP_BLOCKDEV_IOCTL_BLOCK_ERASE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_IOCTL_BLOCK_ERASE&type=code) | Erases a specified block in a block device. | (6) |
| [`MP_BLOCKDEV_IOCTL_BLOCK_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_IOCTL_BLOCK_SIZE&type=code) | Retrieves the size of a block in bytes for block devices. | (5) |
| [`MP_BLOCKDEV_IOCTL_DEINIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_IOCTL_DEINIT&type=code) | Command for deinitializing a block device. | (2) |
| [`MP_BLOCKDEV_IOCTL_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_IOCTL_INIT&type=code) | Indicates initialization of a block device in the block protocol. | (1) |
| [`MP_BLOCKDEV_IOCTL_SYNC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLOCKDEV_IOCTL_SYNC&type=code) | Indicates a request to synchronize the block device. | (3) |


### MP_BLUETOOTH

This configuration set manages various aspects of Bluetooth functionality, including address modes, characteristic properties, and GATT operations. It defines parameters for authentication, encryption, and permissions, ensuring secure and efficient communication between Bluetooth devices.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_BLUETOOTH_ADDRESS_MODE_NRPA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_ADDRESS_MODE_NRPA&type=code) | Represents the Non-Resolvable Private Address mode for Bluetooth. | (3) |
| [`MP_BLUETOOTH_ADDRESS_MODE_PUBLIC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_ADDRESS_MODE_PUBLIC&type=code) | Indicates the use of a public Bluetooth address. | (0) |
| [`MP_BLUETOOTH_ADDRESS_MODE_RANDOM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_ADDRESS_MODE_RANDOM&type=code) | Indicates the use of a random Bluetooth address mode. | (1) |
| [`MP_BLUETOOTH_ADDRESS_MODE_RPA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_ADDRESS_MODE_RPA&type=code) | Represents the Resolvable Private Address mode for Bluetooth. | (2) |
| [`MP_BLUETOOTH_CCCD_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CCCD_LEN&type=code) | Defines the length of the Client Characteristic Configuration Descriptor (CCCD) as 2 bytes. | (2) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_AUTHENTICATED_SIGNED_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_AUTHENTICATED_SIGNED_WRITE&type=code) | Indicates that a characteristic supports authenticated signed writes. | (0x0040) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_AUX_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_AUX_WRITE&type=code) | Extended flag for Bluetooth characteristic indicating auxiliary write capability. | (0x0100) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_BROADCAST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_BROADCAST&type=code) | Indicates that the characteristic can be broadcasted. | (0x0001) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_INDICATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_INDICATE&type=code) | Indicates that a Bluetooth characteristic supports indications for data transfer. | (0x0020) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_NOTIFY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_NOTIFY&type=code) | Indicates that a Bluetooth characteristic supports notifications. | (0x0010) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_READ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_READ&type=code) | Indicates that a Bluetooth characteristic can be read. | (0x0002) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_READ_AUTHENTICATED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_READ_AUTHENTICATED&type=code) | Indicates that a Bluetooth characteristic requires authenticated access for reading. | (0x0400) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_READ_AUTHORIZED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_READ_AUTHORIZED&type=code) | Indicates that a Bluetooth characteristic read requires authorization. | (0x0800) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_READ_ENCRYPTED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_READ_ENCRYPTED&type=code) | Indicates that a Bluetooth characteristic requires encrypted access for reading. | (0x0200) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE&type=code) | Indicates that a Bluetooth characteristic supports write operations. | (0x0008) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE_AUTHENTICATED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE_AUTHENTICATED&type=code) | Indicates that a Bluetooth characteristic requires authenticated write access. | (0x2000) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE_AUTHORIZED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE_AUTHORIZED&type=code) | Indicates that a Bluetooth characteristic write operation is authorized. | (0x4000) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE_ENCRYPTED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE_ENCRYPTED&type=code) | Indicates that a Bluetooth characteristic requires encrypted write access. | (0x1000) |
| [`MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE_NO_RESPONSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CHARACTERISTIC_FLAG_WRITE_NO_RESPONSE&type=code) | Indicates a Bluetooth characteristic that allows writing without requiring a response. | (0x0004) |
| [`MP_BLUETOOTH_CONNECT_DEFAULT_SCAN_DURATION_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_CONNECT_DEFAULT_SCAN_DURATION_MS&type=code) | Default duration for Bluetooth scanning in milliseconds. | 2000 |
| [`MP_BLUETOOTH_DEFAULT_ATTR_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_DEFAULT_ATTR_LEN&type=code) | Defines the default attribute length for Bluetooth GATT services, set to 20 bytes. | (20) |
> REVIEW: docs/library/bluetooth.rst does not currently describe this default attribute length; consider adding a short note or aligning if ports use a different limit.
| [`MP_BLUETOOTH_GAP_ADV_MAX_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GAP_ADV_MAX_LEN&type=code) | Maximum length of Bluetooth advertisement packets. | (32) |
| [`MP_BLUETOOTH_GATTS_ERROR_INSUFFICIENT_AUTHENTICATION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GATTS_ERROR_INSUFFICIENT_AUTHENTICATION&type=code) | Indicates insufficient authentication for a GATT server operation. | (0x05) |
| [`MP_BLUETOOTH_GATTS_ERROR_INSUFFICIENT_AUTHORIZATION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GATTS_ERROR_INSUFFICIENT_AUTHORIZATION&type=code) | Indicates insufficient authorization for a GATT operation, represented by the value 0x08. | (0x08) |
| [`MP_BLUETOOTH_GATTS_ERROR_INSUFFICIENT_ENCRYPTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GATTS_ERROR_INSUFFICIENT_ENCRYPTION&type=code) | Indicates insufficient encryption for a GATT server operation. | (0x0f) |
| [`MP_BLUETOOTH_GATTS_ERROR_READ_NOT_PERMITTED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GATTS_ERROR_READ_NOT_PERMITTED&type=code) | Indicates that a read request is not permitted. | (0x02) |
| [`MP_BLUETOOTH_GATTS_ERROR_WRITE_NOT_PERMITTED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GATTS_ERROR_WRITE_NOT_PERMITTED&type=code) | Indicates that a write operation is not permitted. | (0x03) |
| [`MP_BLUETOOTH_GATTS_NO_ERROR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GATTS_NO_ERROR&type=code) | Indicates a successful read request with no errors. | (0x00) |
| [`MP_BLUETOOTH_GATTS_OP_INDICATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GATTS_OP_INDICATE&type=code) | Represents the operation for sending an indication in Bluetooth GATT. | (2) |
| [`MP_BLUETOOTH_GATTS_OP_NOTIFY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_GATTS_OP_NOTIFY&type=code) | Represents the notify operation for Bluetooth GATT server notifications. | (1) |
| [`MP_BLUETOOTH_IO_CAPABILITY_DISPLAY_ONLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IO_CAPABILITY_DISPLAY_ONLY&type=code) | Represents the Bluetooth I/O capability for devices that can only display information. | (0) |
| [`MP_BLUETOOTH_IO_CAPABILITY_DISPLAY_YESNO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IO_CAPABILITY_DISPLAY_YESNO&type=code) | Indicates the device can display a prompt and receive a yes/no response during Bluetooth pairing. | (1) |
| [`MP_BLUETOOTH_IO_CAPABILITY_KEYBOARD_DISPLAY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IO_CAPABILITY_KEYBOARD_DISPLAY&type=code) | Indicates a device can display a passkey and accept input from a keyboard. | (4) |
| [`MP_BLUETOOTH_IO_CAPABILITY_KEYBOARD_ONLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IO_CAPABILITY_KEYBOARD_ONLY&type=code) | Indicates that the device has keyboard-only input capability. | (2) |
| [`MP_BLUETOOTH_IO_CAPABILITY_NO_INPUT_OUTPUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IO_CAPABILITY_NO_INPUT_OUTPUT&type=code) | Indicates no input or output capabilities for Bluetooth pairing. | (3) |
| [`MP_BLUETOOTH_IRQ_CENTRAL_CONNECT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_CENTRAL_CONNECT&type=code) | Indicates a central device connection event for the IRQ handler. | (1) |
| [`MP_BLUETOOTH_IRQ_CENTRAL_DISCONNECT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_CENTRAL_DISCONNECT&type=code) | Indicates a disconnection event from a central Bluetooth device. | (2) |
| [`MP_BLUETOOTH_IRQ_CONNECTION_UPDATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_CONNECTION_UPDATE&type=code) | Indicates a connection update event in Bluetooth communication. | (27) |
| [`MP_BLUETOOTH_IRQ_ENCRYPTION_UPDATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_ENCRYPTION_UPDATE&type=code) | Triggers an interrupt for Bluetooth encryption updates. | (28) |
| [`MP_BLUETOOTH_IRQ_GATTC_CHARACTERISTIC_DONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_CHARACTERISTIC_DONE&type=code) | Indicates the completion of a GATT characteristic discovery process. | (12) |
| [`MP_BLUETOOTH_IRQ_GATTC_CHARACTERISTIC_RESULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_CHARACTERISTIC_RESULT&type=code) | Indicates a result for a GATT client characteristic operation. | (11) |
| [`MP_BLUETOOTH_IRQ_GATTC_DESCRIPTOR_DONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_DESCRIPTOR_DONE&type=code) | Indicates the completion of a GATT descriptor discovery operation. | (14) |
| [`MP_BLUETOOTH_IRQ_GATTC_DESCRIPTOR_RESULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_DESCRIPTOR_RESULT&type=code) | Indicates a result from a GATT Client operation related to a descriptor. | (13) |
| [`MP_BLUETOOTH_IRQ_GATTC_INDICATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_INDICATE&type=code) | Indicates a GATT indication event for Bluetooth communication. | (19) |
| [`MP_BLUETOOTH_IRQ_GATTC_NOTIFY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_NOTIFY&type=code) | Indicates a GATT client notification event. | (18) |
| [`MP_BLUETOOTH_IRQ_GATTC_READ_DONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_READ_DONE&type=code) | Indicates the completion of a GATT client read operation. | (16) |
| [`MP_BLUETOOTH_IRQ_GATTC_READ_RESULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_READ_RESULT&type=code) | Indicates a result from a GATT client read operation. | (15) |
| [`MP_BLUETOOTH_IRQ_GATTC_SERVICE_DONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_SERVICE_DONE&type=code) | Indicates the completion of a GATT service discovery operation. | (10) |
| [`MP_BLUETOOTH_IRQ_GATTC_SERVICE_RESULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_SERVICE_RESULT&type=code) | Indicates a result from a GATT client service discovery event. | (9) |
| [`MP_BLUETOOTH_IRQ_GATTC_WRITE_DONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTC_WRITE_DONE&type=code) | Indicates the completion status of a GATT client write operation. | (17) |
| [`MP_BLUETOOTH_IRQ_GATTS_INDICATE_DONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTS_INDICATE_DONE&type=code) | Indicates the completion of a GATT server indication event. | (20) |
| [`MP_BLUETOOTH_IRQ_GATTS_READ_REQUEST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTS_READ_REQUEST&type=code) | Indicates a read request event for a GATT server. | (4) |
| [`MP_BLUETOOTH_IRQ_GATTS_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GATTS_WRITE&type=code) | Indicates a write event on a GATT server, providing connection and value handles. | (3) |
| [`MP_BLUETOOTH_IRQ_GET_SECRET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_GET_SECRET&type=code) | Triggers an interrupt to retrieve a secret key in Bluetooth operations. | (29) |
| [`MP_BLUETOOTH_IRQ_L2CAP_ACCEPT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_L2CAP_ACCEPT&type=code) | IRQ for handling L2CAP connection accept events. | (22) |
| [`MP_BLUETOOTH_IRQ_L2CAP_CONNECT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_L2CAP_CONNECT&type=code) | IRQ for handling L2CAP connection events. | (23) |
| [`MP_BLUETOOTH_IRQ_L2CAP_DISCONNECT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_L2CAP_DISCONNECT&type=code) | Indicates a disconnection event in the L2CAP layer of Bluetooth. | (24) |
| [`MP_BLUETOOTH_IRQ_L2CAP_RECV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_L2CAP_RECV&type=code) | Triggers an interrupt for receiving L2CAP data. | (25) |
| [`MP_BLUETOOTH_IRQ_L2CAP_SEND_READY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_L2CAP_SEND_READY&type=code) | Indicates that the L2CAP layer is ready to send data. | (26) |
| [`MP_BLUETOOTH_IRQ_MTU_EXCHANGED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_MTU_EXCHANGED&type=code) | Indicates that the MTU (Maximum Transmission Unit) has been exchanged during a Bluetooth connection. | (21) |
| [`MP_BLUETOOTH_IRQ_PASSKEY_ACTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_PASSKEY_ACTION&type=code) | IRQ for handling Bluetooth passkey actions during pairing. | (31) |
| [`MP_BLUETOOTH_IRQ_PERIPHERAL_CONNECT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_PERIPHERAL_CONNECT&type=code) | Indicates a successful connection from a peripheral device. | (7) |
| [`MP_BLUETOOTH_IRQ_PERIPHERAL_DISCONNECT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_PERIPHERAL_DISCONNECT&type=code) | Indicates a peripheral device has disconnected from the Bluetooth connection. | (8) |
| [`MP_BLUETOOTH_IRQ_SCAN_DONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_SCAN_DONE&type=code) | Indicates the completion of a Bluetooth scan without parameters. | (6) |
| [`MP_BLUETOOTH_IRQ_SCAN_RESULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_SCAN_RESULT&type=code) | Indicates a Bluetooth scan result event with associated parameters. | (5) |
| [`MP_BLUETOOTH_IRQ_SET_SECRET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_IRQ_SET_SECRET&type=code) | IRQ identifier for setting a Bluetooth secret. | (30) |
| [`MP_BLUETOOTH_NIMBLE_MAX_SERVICES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_NIMBLE_MAX_SERVICES&type=code) | Limits the maximum number of Bluetooth services to 8. | (8) |
| [`MP_BLUETOOTH_PASSKEY_ACTION_DISPLAY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_PASSKEY_ACTION_DISPLAY&type=code) | Indicates that the passkey should be displayed to the user. | (3) |
| [`MP_BLUETOOTH_PASSKEY_ACTION_INPUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_PASSKEY_ACTION_INPUT&type=code) | Indicates that a passkey input action is required during Bluetooth pairing. | (2) |
| [`MP_BLUETOOTH_PASSKEY_ACTION_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_PASSKEY_ACTION_NONE&type=code) | Represents no action for Bluetooth passkey input. | (0) |
| [`MP_BLUETOOTH_PASSKEY_ACTION_NUMERIC_COMPARISON`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_PASSKEY_ACTION_NUMERIC_COMPARISON&type=code) | Represents the action for numeric comparison during Bluetooth passkey entry. | (4) |
| [`MP_BLUETOOTH_UUID_TYPE_128`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_UUID_TYPE_128&type=code) | Represents a 128-bit Bluetooth UUID type. | (16) |
| [`MP_BLUETOOTH_UUID_TYPE_16`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_UUID_TYPE_16&type=code) | Indicates a 16-bit Bluetooth UUID type, with the value also representing its length. | (2) |
| [`MP_BLUETOOTH_UUID_TYPE_32`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_UUID_TYPE_32&type=code) | Represents a 32-bit Bluetooth UUID type. | (4) |
| [`MP_BLUETOOTH_WRITE_MODE_NO_RESPONSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_WRITE_MODE_NO_RESPONSE&type=code) | Indicates a write operation without expecting a response in Bluetooth GATT client operations. | (0) |
| [`MP_BLUETOOTH_WRITE_MODE_WITH_RESPONSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_WRITE_MODE_WITH_RESPONSE&type=code) | Indicates that a Bluetooth write operation expects a response. | (1) |
| [`MP_BLUETOOTH_ZEPHYR_MAX_SERVICES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BLUETOOTH_ZEPHYR_MAX_SERVICES&type=code) | Limits the maximum number of Bluetooth services in the Zephyr port to 8. | (8) |


### MP_EMIT

This collection of macros configures the bytecode emission process for various operations in a programming language environment. It encompasses actions related to attribute manipulation, data structure construction, variable handling, import statements, and control flow, enabling efficient execution of high-level constructs in the generated bytecode.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_EMIT_ATTR_DELETE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_ATTR_DELETE&type=code) | Indicates the operation to delete an attribute in bytecode emission. | (2) |
| [`MP_EMIT_ATTR_LOAD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_ATTR_LOAD&type=code) | Indicates loading an attribute during bytecode emission. | (0) |
| [`MP_EMIT_ATTR_STORE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_ATTR_STORE&type=code) | Indicates the operation for storing an attribute. | (1) |
| [`MP_EMIT_BREAK_FROM_FOR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_BREAK_FROM_FOR&type=code) | Indicates a break from a for loop during bytecode emission. | (0x8000) |
| [`MP_EMIT_BUILD_LIST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_BUILD_LIST&type=code) | Indicates the construction of a list during bytecode emission. | (1) |
| [`MP_EMIT_BUILD_MAP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_BUILD_MAP&type=code) | Indicates the construction of a map (dictionary) during bytecode emission. | (2) |
| [`MP_EMIT_BUILD_SET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_BUILD_SET&type=code) | Indicates the construction of a set in the bytecode emitter. | (3) |
| [`MP_EMIT_BUILD_SLICE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_BUILD_SLICE&type=code) | Indicates the building of a slice in the bytecode emitter. | (4) |
| [`MP_EMIT_BUILD_TUPLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_BUILD_TUPLE&type=code) | Indicates the kind for building a tuple during bytecode emission. | (0) |
| [`MP_EMIT_IDOP_GLOBAL_GLOBAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_IDOP_GLOBAL_GLOBAL&type=code) | Indicates the kind for global variable operations in the emitter. | (1) |
| [`MP_EMIT_IDOP_GLOBAL_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_IDOP_GLOBAL_NAME&type=code) | Identifies the operation for emitting global names. | (0) |
| [`MP_EMIT_IDOP_LOCAL_DEREF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_IDOP_LOCAL_DEREF&type=code) | Indicates a local variable dereference operation in bytecode emission. | (1) |
| [`MP_EMIT_IDOP_LOCAL_FAST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_IDOP_LOCAL_FAST&type=code) | Indicates a fast local variable operation in the emitter. | (0) |
| [`MP_EMIT_IMPORT_FROM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_IMPORT_FROM&type=code) | Indicates the kind of import operation for importing specific attributes from a module. | (1) |
| [`MP_EMIT_IMPORT_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_IMPORT_NAME&type=code) | Indicates the kind for emitting an import statement for a module name. | (0) |
| [`MP_EMIT_IMPORT_STAR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_IMPORT_STAR&type=code) | Indicates the import of all names from a module. | (2) |
| [`MP_EMIT_SETUP_BLOCK_EXCEPT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_SETUP_BLOCK_EXCEPT&type=code) | Indicates the setup for an exception handling block during bytecode emission. | (1) |
| [`MP_EMIT_SETUP_BLOCK_FINALLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_SETUP_BLOCK_FINALLY&type=code) | Indicates the setup for a finally block in exception handling. | (2) |
| [`MP_EMIT_SETUP_BLOCK_WITH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_SETUP_BLOCK_WITH&type=code) | Indicates the kind for setting up a 'with' block during bytecode emission. | (0) |
| [`MP_EMIT_STAR_FLAG_DOUBLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_STAR_FLAG_DOUBLE&type=code) | Indicates the presence of double-star arguments in function calls. | (0x02) |
| [`MP_EMIT_STAR_FLAG_SINGLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_STAR_FLAG_SINGLE&type=code) | Indicates the presence of a single star argument in function calls. | (0x01) |
| [`MP_EMIT_SUBSCR_DELETE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_SUBSCR_DELETE&type=code) | Indicates the operation for deleting a subscription in bytecode emission. | (2) |
| [`MP_EMIT_SUBSCR_LOAD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_SUBSCR_LOAD&type=code) | Indicates loading a subscription from a data structure. | (0) |
| [`MP_EMIT_SUBSCR_STORE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_SUBSCR_STORE&type=code) | Indicates the operation for storing a value in a subscription. | (1) |
| [`MP_EMIT_YIELD_FROM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_YIELD_FROM&type=code) | Indicates the kind of yield operation for generator functions. | (1) |
| [`MP_EMIT_YIELD_VALUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMIT_YIELD_VALUE&type=code) | Indicates the kind for emitting a yield operation. | (0) |


### MP_HAL

This configuration set manages the behavior and characteristics of GPIO pins, including their drive strength, modes, pull-up/down settings, and interrupt triggers. It allows for precise control over pin functionalities such as analog input, digital output, and signal timing, enabling efficient hardware interaction in embedded applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_HAL_BITSTREAM_NS_OVERHEAD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_BITSTREAM_NS_OVERHEAD&type=code) | Defines the overhead in nanoseconds for bitstream timing calculations. | (5) |
| [`MP_HAL_PIN_DRIVE_0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_DRIVE_0&type=code) | Represents low power drive strength for GPIO pins. | (GPIO_LOW_POWER) |
| [`MP_HAL_PIN_DRIVE_1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_DRIVE_1&type=code) | Represents a mid-level power drive configuration for GPIO pins. | (GPIO_MID_POWER) |
| [`MP_HAL_PIN_DRIVE_12MA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_DRIVE_12MA&type=code) | Defines the drive strength of a pin to 12mA. | (PADCTRL_OUTPUT_DRIVE_STRENGTH_12MA) |
| [`MP_HAL_PIN_DRIVE_2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_DRIVE_2&type=code) | Represents a pin drive strength level of mid-fast power. | (GPIO_MID_FAST_POWER) |
| [`MP_HAL_PIN_DRIVE_2MA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_DRIVE_2MA&type=code) | Defines the output drive strength of a pin to 2mA. | (PADCTRL_OUTPUT_DRIVE_STRENGTH_2MA) |
| [`MP_HAL_PIN_DRIVE_3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_DRIVE_3&type=code) | Represents a high power drive mode for GPIO pins. | (GPIO_HIGH_POWER) |
| [`MP_HAL_PIN_DRIVE_4MA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_DRIVE_4MA&type=code) | Sets the pin drive strength to 4mA. | (PADCTRL_OUTPUT_DRIVE_STRENGTH_4MA) |
| [`MP_HAL_PIN_DRIVE_8MA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_DRIVE_8MA&type=code) | Defines the drive strength of a pin to 8mA. | (PADCTRL_OUTPUT_DRIVE_STRENGTH_8MA) |
| [`MP_HAL_PIN_FMT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_FMT&type=code) | Format specifier for pin names, typically used in print functions. | "%q" |
| [`MP_HAL_PIN_MODE_ADC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_MODE_ADC&type=code) | Configures a pin for analog-to-digital conversion mode. | (GPIO_MODE_ANALOG) |
| [`MP_HAL_PIN_MODE_ALT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_MODE_ALT&type=code) | Configures a pin for alternate function mode. | (GPIO_MODE_AF_PP) |
| [`MP_HAL_PIN_MODE_ALT_OPEN_DRAIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_MODE_ALT_OPEN_DRAIN&type=code) | Configures a pin for alternate function in open-drain mode. | (GPIO_MODE_AF_OD) |
| [`MP_HAL_PIN_MODE_ANALOG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_MODE_ANALOG&type=code) | Defines the analog pin mode for GPIO configuration. | (GPIO_MODE_ANALOG) |
| [`MP_HAL_PIN_MODE_INPUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_MODE_INPUT&type=code) | Represents the input mode for GPIO pins. | (GPIO_MODE_INPUT) |
| [`MP_HAL_PIN_MODE_OPEN_DRAIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_MODE_OPEN_DRAIN&type=code) | Configures a pin for open-drain output mode. | (GPIO_MODE_OUTPUT_OD) |
| [`MP_HAL_PIN_MODE_OUTPUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_MODE_OUTPUT&type=code) | Defines the output mode for GPIO pins. | (GPIO_MODE_OUTPUT_PP) |
| [`MP_HAL_PIN_PULL_DOWN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_PULL_DOWN&type=code) | Indicates a pull-down resistor configuration for a pin. | PIN_PULL_DOWN_100K |
| [`MP_HAL_PIN_PULL_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_PULL_NONE&type=code) | Indicates that no pull-up or pull-down resistor is enabled for a pin. | PIN_PULL_DISABLED |
| [`MP_HAL_PIN_PULL_UP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_PULL_UP&type=code) | Enables a pull-up resistor on a pin. | PIN_PULL_UP_100K |
| [`MP_HAL_PIN_SPEED_HIGH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_SPEED_HIGH&type=code) | Sets the pin speed to high, enabling fast signal transitions. | (PADCTRL_SLEW_RATE_FAST) |
| [`MP_HAL_PIN_SPEED_LOW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_SPEED_LOW&type=code) | Sets the GPIO pin speed to low frequency. | (GPIO_SPEED_FREQ_LOW) |
| [`MP_HAL_PIN_SPEED_MEDIUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_SPEED_MEDIUM&type=code) | Defines the medium speed setting for GPIO pins. | (GPIO_SPEED_FREQ_MEDIUM) |
| [`MP_HAL_PIN_SPEED_VERY_HIGH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_SPEED_VERY_HIGH&type=code) | Defines a very high speed setting for GPIO pins. | (GPIO_SPEED_FREQ_VERY_HIGH) |
| [`MP_HAL_PIN_TRIGGER_FALL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_TRIGGER_FALL&type=code) | Indicates a falling edge interrupt trigger for GPIO pins. | kGPIO_IntFallingEdge |
| [`MP_HAL_PIN_TRIGGER_FALLING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_TRIGGER_FALLING&type=code) | Defines the falling edge trigger for GPIO interrupts. | (GPIO_IRQ_FALLING) |
| [`MP_HAL_PIN_TRIGGER_HIGHLEVEL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_TRIGGER_HIGHLEVEL&type=code) | Indicates a high-level trigger for GPIO interrupts. | (GPIO_IRQ_HIGHLEVEL) |
| [`MP_HAL_PIN_TRIGGER_LOWLEVEL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_TRIGGER_LOWLEVEL&type=code) | Indicates a low-level trigger for GPIO interrupts. | (GPIO_IRQ_LOWLEVEL) |
| [`MP_HAL_PIN_TRIGGER_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_TRIGGER_NONE&type=code) | Indicates no interrupt mode for GPIO pins. | kGPIO_NoIntmode |
| [`MP_HAL_PIN_TRIGGER_RISE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_TRIGGER_RISE&type=code) | Indicates a rising edge trigger for GPIO interrupts. | kGPIO_IntRisingEdge |
| [`MP_HAL_PIN_TRIGGER_RISE_FALL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_TRIGGER_RISE_FALL&type=code) | Triggers an interrupt on both rising and falling edges of a GPIO pin. | kGPIO_IntRisingOrFallingEdge |
| [`MP_HAL_PIN_TRIGGER_RISING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_PIN_TRIGGER_RISING&type=code) | Indicates a rising edge trigger for GPIO interrupts. | (GPIO_IRQ_RISING) |
| [`MP_HAL_UNIQUE_ID_ADDRESS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HAL_UNIQUE_ID_ADDRESS&type=code) | Memory address for accessing the unique identifier of the hardware. | (0x1ffff7ac)   /* To be fixed */ |


### MP_MPU

This configuration set manages memory protection unit (MPU) settings, defining various memory attributes and regions to control access permissions and caching behaviors. It ensures that different types of memory, such as SRAM, flash, and peripheral regions, are appropriately configured for optimal performance and security.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_MPU_ATTR_NORMAL_NON_CACHEABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_ATTR_NORMAL_NON_CACHEABLE&type=code) | Defines a memory region attribute for normal memory that is non-cacheable. | (4) |
| [`MP_MPU_ATTR_NORMAL_WB_RA_WA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_ATTR_NORMAL_WB_RA_WA&type=code) | Defines memory attributes for normal memory with write-back caching and read-allocate/write-allocate policies. | (2) |
| [`MP_MPU_ATTR_NORMAL_WT_RA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_ATTR_NORMAL_WT_RA&type=code) | Memory attribute for normal memory with write-through and read-allocate caching. | (3) |
| [`MP_MPU_ATTR_NORMAL_WT_RA_TRANSIENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_ATTR_NORMAL_WT_RA_TRANSIENT&type=code) | Defines a memory attribute for normal memory with write-through caching and read-allocate, transient behavior. | (0) |
| [`MP_MPU_REGION_HOST_PERIPHERALS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_REGION_HOST_PERIPHERALS&type=code) | Identifies the memory region for host peripherals with specific access permissions. | (2) |
| [`MP_MPU_REGION_MRAM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_REGION_MRAM&type=code) | Identifies the Memory Region Attribute for MRAM in the MPU configuration. | (3) |
| [`MP_MPU_REGION_OPENAMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_REGION_OPENAMP&type=code) | Identifies the OpenAMP memory region for MPU configuration. | (7) |
| [`MP_MPU_REGION_OSPI0_XIP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_REGION_OSPI0_XIP&type=code) | Identifies the OSPI0 XIP flash memory region with specific access permissions. | (5) |
| [`MP_MPU_REGION_OSPI1_XIP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_REGION_OSPI1_XIP&type=code) | Identifies the OSPI1 XIP flash memory region with specific access permissions. | (6) |
| [`MP_MPU_REGION_OSPI_REGISTERS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_REGION_OSPI_REGISTERS&type=code) | Identifies the memory region for OSPI registers with specific access permissions. | (4) |
| [`MP_MPU_REGION_SRAM0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_REGION_SRAM0&type=code) | Identifies the first SRAM region in the MPU configuration. | (0) |
| [`MP_MPU_REGION_SRAM1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MPU_REGION_SRAM1&type=code) | Identifies the second SRAM region in the memory protection unit configuration. | (1) |


### MP_OBJ

This collection of macros is focused on defining and managing object types and their properties within the MicroPython environment. They facilitate type checking, memory management, and function argument handling, ensuring efficient and accurate manipulation of various object types.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_OBJ_ARRAY_FREE_SIZE_BITS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_ARRAY_FREE_SIZE_BITS&type=code) | Bit size allocated for the 'free' member in the mp_obj_array_t structure. | (8 * sizeof(size_t) - 8) |
| [`MP_OBJ_ARRAY_TYPECODE_FLAG_RW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_ARRAY_TYPECODE_FLAG_RW&type=code) | Indicates a writable memoryview when set in the typecode. | (0x80) |
| [`MP_OBJ_FUN_ARGS_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_FUN_ARGS_MAX&type=code) | Sets the maximum number of arguments for function calls. | (0xffff) // to set maximum value in n_args_max below |
| [`MP_OBJ_IS_FUN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_IS_FUN&type=code) | Checks if an object is a function. | mp_obj_is_fun |
| [`MP_OBJ_IS_INT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_IS_INT&type=code) | Checks if an object is an integer. | mp_obj_is_int |
| [`MP_OBJ_IS_OBJ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_IS_OBJ&type=code) | Checks if an object is of type 'object'. | mp_obj_is_obj |
| [`MP_OBJ_IS_QSTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_IS_QSTR&type=code) | Checks if an object is a QSTR (interned string) type. | mp_obj_is_qstr |
| [`MP_OBJ_IS_SMALL_INT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_IS_SMALL_INT&type=code) | Maps the legacy API for checking small integer objects. | mp_obj_is_small_int |
| [`MP_OBJ_IS_STR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_IS_STR&type=code) | Checks if an object is a string. | mp_obj_is_str |
| [`MP_OBJ_IS_STR_OR_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_IS_STR_OR_BYTES&type=code) | Checks if an object is either a string or bytes. | mp_obj_is_str_or_bytes |
| [`MP_OBJ_IS_TYPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_IS_TYPE&type=code) | Checks if an object is of a specific type. | mp_obj_is_type |
| [`MP_OBJ_ITER_BUF_NSLOTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_ITER_BUF_NSLOTS&type=code) | Calculates the number of slots required for mp_obj_iter_buf_t on the Python value stack. | ((sizeof(mp_obj_iter_buf_t) + sizeof(mp_obj_t) - 1) / sizeof(mp_obj_t)) |
| [`MP_OBJ_JSPROXY_REF_GLOBAL_THIS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_JSPROXY_REF_GLOBAL_THIS&type=code) | Reference identifier for the JavaScript globalThis object. | (0) |
| [`MP_OBJ_JSPROXY_REF_UNDEFINED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_JSPROXY_REF_UNDEFINED&type=code) | Represents an undefined JavaScript proxy reference. | (1) |
| [`MP_OBJ_NULL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_NULL&type=code) | Represents a null object pointer in the MicroPython object system. | (MP_OBJ_FROM_PTR((void *)0)) |
| [`MP_OBJ_SENTINEL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_SENTINEL&type=code) | Represents a sentinel value used to indicate special conditions or states in object handling. | (MP_OBJ_FROM_PTR((void *)8)) |
| [`MP_OBJ_STOP_ITERATION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_STOP_ITERATION&type=code) | Indicates the end of an iteration in various iterable contexts. | (MP_OBJ_FROM_PTR((void *)4)) |
| [`MP_OBJ_WORD_MSBIT_HIGH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_OBJ_WORD_MSBIT_HIGH&type=code) | mp_int_t value with the most significant bit set. | (((mp_uint_t)1) << (MP_BYTES_PER_OBJ_WORD * MP_BITS_PER_BYTE - 1)) |


### MP_SCOPE

This configuration group manages various flags related to function scopes in MicroPython, enabling specific behaviors for functions, including support for default arguments, variable arguments, and generator functions. It also handles aspects related to the native emitter and viper code, such as the presence of constants, global references, and read-only data, ensuring efficient execution and memory management.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_SCOPE_FLAG_ALL_SIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_ALL_SIG&type=code) | Mask for all significant scope flags (4 bits) in function signatures. | (0x0f) |
| [`MP_SCOPE_FLAG_DEFKWARGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_DEFKWARGS&type=code) | Indicates the presence of default keyword arguments in a function's scope. | (0x08) |
| [`MP_SCOPE_FLAG_GENERATOR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_GENERATOR&type=code) | Indicates that the current scope is a generator, enabling specific behaviors for async functions and yield expressions. | (0x01) |
| [`MP_SCOPE_FLAG_HASCONSTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_HASCONSTS&type=code) | Indicates the presence of constant values in the current scope when native emitter is enabled. | (0x20) // used only if native emitter enabled |
| [`MP_SCOPE_FLAG_REFGLOBALS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_REFGLOBALS&type=code) | Indicates that a function/closure takes a reference to the current global variables when the native emitter is enabled. | (0x10) // used only if native emitter enabled |
| [`MP_SCOPE_FLAG_VARARGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_VARARGS&type=code) | Indicates that a function accepts variable positional arguments. | (0x04) |
| [`MP_SCOPE_FLAG_VARKEYWORDS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_VARKEYWORDS&type=code) | Indicates the presence of variable keyword arguments in a function's scope. | (0x02) |
| [`MP_SCOPE_FLAG_VIPERBSS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_VIPERBSS&type=code) | Indicates the presence of BSS (Block Started by Symbol) section when loading viper from .mpy files. | (0x40) // used only when loading viper from .mpy |
| [`MP_SCOPE_FLAG_VIPERRELOC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_VIPERRELOC&type=code) | Indicates relocation of viper code when loading from .mpy files. | (0x10) // used only when loading viper from .mpy |
| [`MP_SCOPE_FLAG_VIPERRET_POS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_VIPERRET_POS&type=code) | Indicates the position of viper return type bits for compiler to native emitter communication. | (6) // 3 bits used for viper return type, to pass from compiler to native emitter |
| [`MP_SCOPE_FLAG_VIPERRODATA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCOPE_FLAG_VIPERRODATA&type=code) | Indicates the presence of read-only data when loading viper code from .mpy files. | (0x20) // used only when loading viper from .mpy |


### MP_STREAM

This collection of macros is designed to manage and configure stream operations, including reading, writing, and error handling. They provide essential functionalities for stream control, such as flushing buffers, polling for status, and setting options, ensuring efficient data handling in various stream contexts.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_STREAM_CLOSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_CLOSE&type=code) | Indicates a request to close a stream. | (4) |
| [`MP_STREAM_ERROR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_ERROR&type=code) | Indicates an error in stream operations, represented by the value ((mp_uint_t)-1). Examples include read/write failures in I2S and deflate operations. | ((mp_uint_t)-1) |
| [`MP_STREAM_FLUSH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_FLUSH&type=code) | Request code for flushing a stream's output buffer. | (1) |
| [`MP_STREAM_GET_BUFFER_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_GET_BUFFER_SIZE&type=code) | Retrieves the preferred buffer size for file streams. | (11) // Get preferred buffer size for file |
| [`MP_STREAM_GET_DATA_OPTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_GET_DATA_OPTS&type=code) | Retrieves options related to data or message handling. | (8)  // Get data/message options |
| [`MP_STREAM_GET_FILENO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_GET_FILENO&type=code) | Retrieves the file descriptor of the underlying file. | (10) // Get fileno of underlying file |
| [`MP_STREAM_GET_OPTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_GET_OPTS&type=code) | Retrieves options for a stream. | (6)  // Get stream options |
| [`MP_STREAM_OP_IOCTL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_OP_IOCTL&type=code) | Indicates the ioctl operation for stream objects. | (4) |
| [`MP_STREAM_OP_READ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_OP_READ&type=code) | Flag for read operations in stream protocols, can be combined with other operation flags. | (1) |
| [`MP_STREAM_OP_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_OP_WRITE&type=code) | Indicates the stream operation for writing data. | (2) |
| [`MP_STREAM_POLL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_POLL&type=code) | Used for polling stream objects to check their read/write status. | (3) |
| [`MP_STREAM_POLL_ERR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_POLL_ERR&type=code) | Indicates an error state in stream polling. | (0x0008) |
| [`MP_STREAM_POLL_HUP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_POLL_HUP&type=code) | Indicates that a stream has been hung up or closed by the peer. | (0x0010) |
| [`MP_STREAM_POLL_NVAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_POLL_NVAL&type=code) | Indicates an invalid socket or file descriptor during polling operations. | (0x0020) |
| [`MP_STREAM_POLL_RD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_POLL_RD&type=code) | Indicates readiness for reading in stream polling, compatible with Linux poll values. | (0x0001) |
| [`MP_STREAM_POLL_RDWR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_POLL_RDWR&type=code) | Combines read and write polling flags for stream operations. | (MP_STREAM_POLL_RD \| MP_STREAM_POLL_WR) |
| [`MP_STREAM_POLL_WR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_POLL_WR&type=code) | Indicates that a stream is writable. | (0x0004) |
| [`MP_STREAM_RW_ONCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_RW_ONCE&type=code) | Indicates that a stream operation should be performed only once. | 1 |
| [`MP_STREAM_RW_READ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_RW_READ&type=code) | Flag indicating read operation for stream functions. | 0 |
| [`MP_STREAM_RW_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_RW_WRITE&type=code) | Flag indicating a write operation in stream functions. | 2 |
| [`MP_STREAM_SEEK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_SEEK&type=code) | Request code for seeking within a stream. | (2) |
| [`MP_STREAM_SET_DATA_OPTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_SET_DATA_OPTS&type=code) | Sets data/message options for a stream. | (9)  // Set data/message options |
| [`MP_STREAM_SET_OPTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_SET_OPTS&type=code) | Sets options for a stream. | (7)  // Set stream options |
| [`MP_STREAM_TIMEOUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STREAM_TIMEOUT&type=code) | Get or set the timeout for a single stream operation. | (5)  // Get/set timeout (single op) |
> REVIEW: The user docs for io streams ([docs/library/io.rst](docs/library/io.rst)) omit this ioctl constant; please add or confirm it remains internal-only.


### MP_TYPE

This collection of macros configures various behaviors and characteristics of types in MicroPython, such as method binding, equality checks, iteration mechanisms, and special accessors. They enable fine-tuning of type functionalities, allowing for custom implementations and optimizations in type handling.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_TYPE_FLAG_BINDS_SELF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_BINDS_SELF&type=code) | Indicates that a method binds 'self' as the first argument. | (0x0020) |
| [`MP_TYPE_FLAG_BUILTIN_FUN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_BUILTIN_FUN&type=code) | Indicates that the type is a built-in function type. | (0x0040) |
| [`MP_TYPE_FLAG_EQ_CHECKS_OTHER_TYPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_EQ_CHECKS_OTHER_TYPE&type=code) | Enables equality checks between different types. | (0x0008) |
| [`MP_TYPE_FLAG_EQ_HAS_NEQ_TEST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_EQ_HAS_NEQ_TEST&type=code) | Indicates that a type implements the __ne__ operator for inequality checks. | (0x0010) |
| [`MP_TYPE_FLAG_EQ_NOT_REFLEXIVE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_EQ_NOT_REFLEXIVE&type=code) | Indicates that equality comparison (__eq__) is not reflexive, meaning A==A may return False. | (0x0004) |
| [`MP_TYPE_FLAG_HAS_SPECIAL_ACCESSORS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_HAS_SPECIAL_ACCESSORS&type=code) | Indicates that attribute lookups for a class should check for special accessor methods. | (0x0002) |
| [`MP_TYPE_FLAG_INSTANCE_TYPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_INSTANCE_TYPE&type=code) | Indicates that a type is an instance type defined in Python. | (0x0200) |
| [`MP_TYPE_FLAG_IS_SUBCLASSED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_IS_SUBCLASSED&type=code) | Indicates that subclasses of the class have been created, preventing certain mutations. | (0x0001) |
| [`MP_TYPE_FLAG_ITER_IS_CUSTOM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_ITER_IS_CUSTOM&type=code) | Indicates that the 'iter' slot points to a custom iterator structure with both 'getiter' and 'iternext' functions. | (0x0100) |
| [`MP_TYPE_FLAG_ITER_IS_GETITER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_ITER_IS_GETITER&type=code) | Indicates that the type uses the default behavior for the iterator slot, utilizing the getiter function. | (0x0000) |
| [`MP_TYPE_FLAG_ITER_IS_ITERNEXT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_ITER_IS_ITERNEXT&type=code) | Indicates that the 'iter' slot corresponds to the __next__ special method. | (0x0080) |
| [`MP_TYPE_FLAG_ITER_IS_STREAM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_ITER_IS_STREAM&type=code) | Indicates that a type supports streaming iteration with a default getiter implementation. | (MP_TYPE_FLAG_ITER_IS_ITERNEXT \| MP_TYPE_FLAG_ITER_IS_CUSTOM) |
| [`MP_TYPE_FLAG_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_NONE&type=code) | Indicates no special type behavior flags are set. | (0x0000) |
| [`MP_TYPE_FLAG_SUBSCR_ALLOWS_STACK_SLICE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TYPE_FLAG_SUBSCR_ALLOWS_STACK_SLICE&type=code) | Enables the 'subscr' slot to accept stack-allocated slices without retaining references. | (0x0400) |


### MP_MISC

This collection of macros provides essential configurations and constants for various aspects of the MicroPython environment, including error handling, buffer management, and runtime initialization. It facilitates low-level operations, optimizations, and compatibility across different platforms and compilers, ensuring efficient execution and resource management.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MP_3_PI_4`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_3_PI_4&type=code) | Represents the constant value of 3π/4 as a floating-point number. | MICROPY_FLOAT_CONST(2.35619449019234492885) |
| [`MP_ALWAYSINLINE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ALWAYSINLINE&type=code) | Forces functions to be always inlined by the compiler. | __attribute__((always_inline)) |
| [`MP_ASAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ASAN&type=code) | Enables AddressSanitizer feature if supported by the compiler. | __has_feature(address_sanitizer) |
| [`MP_ASM_PASS_COMPUTE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ASM_PASS_COMPUTE&type=code) | Indicates the assembly pass for computation in the assembly framework. | (1) |
| [`MP_ASM_PASS_EMIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ASM_PASS_EMIT&type=code) | Indicates the assembly pass for emitting code. | (2) |
| [`MP_BINARY_OP_NUM_BYTECODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BINARY_OP_NUM_BYTECODE&type=code) | Defines the count of bytecode operations for binary operations. | (MP_BINARY_OP_POWER + 1) |
| [`MP_BINARY_OP_NUM_RUNTIME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BINARY_OP_NUM_RUNTIME&type=code) | Determines the number of runtime binary operations based on the presence of reverse special methods. | (MP_BINARY_OP_REVERSE_POWER + 1) |
| [`MP_BITS_PER_BYTE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BITS_PER_BYTE&type=code) | Represents the number of bits in a byte, set to 8. | (8) |
| [`MP_BUFFER_RAISE_IF_UNSUPPORTED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BUFFER_RAISE_IF_UNSUPPORTED&type=code) | Triggers a TypeError if the buffer protocol is unsupported. | (4) |
| [`MP_BUFFER_READ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BUFFER_READ&type=code) | Indicates that a buffer is to be read from, allowing access to its contents. | (1) |
| [`MP_BUFFER_RW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BUFFER_RW&type=code) | Combines read and write buffer access flags for buffer operations. | (MP_BUFFER_READ \| MP_BUFFER_WRITE) |
| [`MP_BUFFER_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BUFFER_WRITE&type=code) | Indicates that a buffer is intended for writing data. | (2) |
| [`MP_BYTES_PER_OBJ_WORD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_BYTES_PER_OBJ_WORD&type=code) | Defines the number of bytes in an object word based on the size of mp_uint_t. | (sizeof(mp_uint_t)) |
| [`MP_CLOCKS_PER_SEC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_CLOCKS_PER_SEC&type=code) | Represents the number of clock ticks per second, adjusted for compatibility with different compilers. | MP_REMOVE_BRACKETSC(CLOCKS_PER_SEC) |
| [`MP_CODE_STATE_EXC_SP_IDX_SENTINEL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_CODE_STATE_EXC_SP_IDX_SENTINEL&type=code) | Sentinel value indicating an invalid exception stack pointer index. | ((uint16_t)-1) |
| [`MP_DYNRUNTIME_INIT_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_DYNRUNTIME_INIT_ENTRY&type=code) | Initializes the dynamic runtime environment for a module, setting up global variables and context. | \ |
| [`MP_DYNRUNTIME_INIT_EXIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_DYNRUNTIME_INIT_EXIT&type=code) | Restores the global dictionary and returns None at the end of dynamic runtime initialization. | \ |
| [`MP_E2BIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_E2BIG&type=code) | Indicates that the argument list is too long. | (7) // Argument list too long |
| [`MP_EACCES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EACCES&type=code) | Represents a permission denied error with a value of 13. | (13) // Permission denied |
| [`MP_EADDRINUSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EADDRINUSE&type=code) | Error code indicating that an address is already in use. | (98) // Address already in use |
| [`MP_EAFNOSUPPORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EAFNOSUPPORT&type=code) | Error code indicating the address family is not supported by the protocol. | (97) // Address family not supported by protocol |
| [`MP_EAGAIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EAGAIN&type=code) | Indicates that an operation should be retried. | (11) // Try again |
| [`MP_EALREADY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EALREADY&type=code) | Indicates that an operation is already in progress. | (114) // Operation already in progress |
| [`MP_EBADF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EBADF&type=code) | Indicates a bad file number error. | (9) // Bad file number |
| [`MP_EBUSY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EBUSY&type=code) | Indicates that a device or resource is busy. | (16) // Device or resource busy |
| [`MP_ECANCELED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ECANCELED&type=code) | Error code indicating that an operation was canceled. | (125) // Operation canceled |
| [`MP_ECHILD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ECHILD&type=code) | Indicates that there are no child processes. | (10) // No child processes |
| [`MP_ECONNABORTED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ECONNABORTED&type=code) | Indicates a software-caused connection abort with a value of 103. | (103) // Software caused connection abort |
| [`MP_ECONNREFUSED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ECONNREFUSED&type=code) | Error code indicating that a connection attempt was refused. | (111) // Connection refused |
| [`MP_ECONNRESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ECONNRESET&type=code) | Indicates a connection reset by the peer. | (104) // Connection reset by peer |
| [`MP_EDOM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EDOM&type=code) | Math argument out of domain of function. | (33) // Math argument out of domain of func |
| [`MP_EEXIST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EEXIST&type=code) | Indicates that a file or directory already exists. | (17) // File exists |
| [`MP_EFAULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EFAULT&type=code) | Indicates a bad address error with a value of 14. | (14) // Bad address |
| [`MP_EFBIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EFBIG&type=code) | Indicates that a file is too large. | (27) // File too large |
| [`MP_EHOSTUNREACH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EHOSTUNREACH&type=code) | Indicates that there is no route to the host. | (113) // No route to host |
| [`MP_EINPROGRESS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EINPROGRESS&type=code) | Indicates that an operation is currently in progress. | (115) // Operation now in progress |
| [`MP_EINTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EINTR&type=code) | Represents an interrupted system call error with a value of 4. | (4) // Interrupted system call |
| [`MP_EINVAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EINVAL&type=code) | Error code indicating an invalid argument. | (22) // Invalid argument |
| [`MP_EIO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EIO&type=code) | Represents an I/O error with a value of 5. | (5) // I/O error |
| [`MP_EISCONN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EISCONN&type=code) | Error code indicating that a transport endpoint is already connected. | (106) // Transport endpoint is already connected |
| [`MP_EISDIR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EISDIR&type=code) | Error code indicating that the operation is attempted on a directory. | (21) // Is a directory |
| [`MP_EMFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMFILE&type=code) | Error code indicating too many open files. | (24) // Too many open files |
| [`MP_EMLINK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EMLINK&type=code) | Error code indicating too many links to a file. | (31) // Too many links |
| [`MP_ENCODE_UINT_MAX_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENCODE_UINT_MAX_BYTES&type=code) | Calculates the maximum number of bytes needed to encode an unsigned integer using a variable-length encoding scheme. | ((MP_BYTES_PER_OBJ_WORD * 8 + 6) / 7) |
| [`MP_ENDIANNESS_BIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENDIANNESS_BIG&type=code) | Indicates big-endian byte order, defined as the negation of MP_ENDIANNESS_LITTLE. | (!MP_ENDIANNESS_LITTLE) |
| [`MP_ENDIANNESS_LITTLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENDIANNESS_LITTLE&type=code) | Indicates little-endian byte order, primarily for compatibility with Windows. | (1) |
| [`MP_ENDPOINT_IS_SERVER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENDPOINT_IS_SERVER&type=code) | Indicates that the endpoint is a server in the TLS/DTLS protocol. | (1 << 0) |
| [`MP_ENFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENFILE&type=code) | Indicates a file table overflow error. | (23) // File table overflow |
| [`MP_ENOBUFS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOBUFS&type=code) | Indicates that no buffer space is available. | (105) // No buffer space available |
| [`MP_ENODEV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENODEV&type=code) | Indicates that no such device exists. | (19) // No such device |
| [`MP_ENOENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOENT&type=code) | Error code indicating no such file or directory exists. | (2) // No such file or directory |
| [`MP_ENOEXEC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOEXEC&type=code) | Error code indicating an exec format error. | (8) // Exec format error |
| [`MP_ENOMEM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOMEM&type=code) | Indicates an out of memory error. | (12) // Out of memory |
| [`MP_ENOSPC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOSPC&type=code) | Error code indicating no space left on device. | (28) // No space left on device |
| [`MP_ENOTBLK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOTBLK&type=code) | Error code indicating a block device is required. | (15) // Block device required |
| [`MP_ENOTCONN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOTCONN&type=code) | Indicates that a transport endpoint is not connected. | (107) // Transport endpoint is not connected |
| [`MP_ENOTDIR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOTDIR&type=code) | Error code indicating that a specified path is not a directory. | (20) // Not a directory |
| [`MP_ENOTTY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENOTTY&type=code) | Error code indicating that the operation is not supported on the specified device. | (25) // Not a typewriter |
| [`MP_ENXIO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ENXIO&type=code) | Error code indicating no such device or address. | (6) // No such device or address |
| [`MP_EOPNOTSUPP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EOPNOTSUPP&type=code) | Indicates that an operation is not supported on the transport endpoint. | (95) // Operation not supported on transport endpoint |
| [`MP_EPERM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EPERM&type=code) | Indicates that an operation is not permitted. | (1) // Operation not permitted |
| [`MP_EPIPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EPIPE&type=code) | Error code for a broken pipe. | (32) // Broken pipe |
| [`MP_ERANGE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ERANGE&type=code) | Math result not representable. | (34) // Math result not representable |
| [`MP_EROFS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EROFS&type=code) | Indicates a read-only file system error. | (30) // Read-only file system |
| [`MP_ESPIPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ESPIPE&type=code) | Error code for illegal seek operation. | (29) // Illegal seek |
| [`MP_ESRCH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ESRCH&type=code) | Error code indicating no such process. | (3) // No such process |
| [`MP_ETIMEDOUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ETIMEDOUT&type=code) | Indicates a connection timeout error (110). Examples include I2C operations and socket timeouts. | (110) // Connection timed out |
| [`MP_ETXTBSY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ETXTBSY&type=code) | Error code indicating that a text file is busy. | (26) // Text file busy |
| [`MP_EWOULDBLOCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EWOULDBLOCK&type=code) | Indicates that an operation would block, equivalent to MP_EAGAIN. | MP_EAGAIN // Operation would block |
| [`MP_EXDEV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_EXDEV&type=code) | Error code for cross-device link. | (18) // Cross-device link |
| [`MP_FALLTHROUGH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FALLTHROUGH&type=code) | Annotates intentional fall-through behavior in switch-case statements. | __attribute__((fallthrough)); |
| [`MP_FFUINT_FMT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FFUINT_FMT&type=code) | Format specifier for unsigned long integers in floating-point formatting. | "%lu" |
| [`MP_FLOAT_EXP_BIAS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FLOAT_EXP_BIAS&type=code) | Calculates the bias for floating-point exponent representation. | ((1 << (MP_FLOAT_EXP_BITS - 1)) - 1) |
| [`MP_FLOAT_EXP_BITS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FLOAT_EXP_BITS&type=code) | Defines the number of exponent bits for floating-point representation, set to 11 for double precision. | (11) |
| [`MP_FLOAT_EXP_OFFSET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FLOAT_EXP_OFFSET&type=code) | Represents the exponent offset for floating-point numbers in double precision format. | (1023) |
| [`MP_FLOAT_EXP_SHIFT_I32`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FLOAT_EXP_SHIFT_I32&type=code) | Calculates the shift amount for the exponent in a floating-point representation based on fractional bits. | (MP_FLOAT_FRAC_BITS % 32) |
| [`MP_FLOAT_FRAC_BITS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FLOAT_FRAC_BITS&type=code) | Determines the number of bits used for the fractional part of floating-point numbers, set to 52 for double precision. | (52) |
| [`MP_FLOAT_REPR_PREC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FLOAT_REPR_PREC&type=code) | Sets the precision value for optimal float representation behavior. | (99) // magic `prec` value for optimal `repr` behaviour |
| [`MP_FLOAT_SIGN_SHIFT_I32`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FLOAT_SIGN_SHIFT_I32&type=code) | Calculates the bit position for the sign bit in a 32-bit integer representation of a floating-point number. | ((MP_FLOAT_FRAC_BITS + MP_FLOAT_EXP_BITS) % 32) |
| [`MP_FROZEN_PATH_PREFIX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FROZEN_PATH_PREFIX&type=code) | Indicates the virtual sys.path entry for frozen modules, prefixed with '.frozen/'. | ".frozen/" |
| [`MP_FROZEN_STR_NAMES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_FROZEN_STR_NAMES&type=code) | Contains a list of frozen module names for inclusion in the build. | \ |
| [`MP_GCC_HAS_BUILTIN_OVERFLOW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_GCC_HAS_BUILTIN_OVERFLOW&type=code) | Indicates support for GCC's integer overflow builtins starting from version 5. | (__GNUC__ >= 5) |
| [`MP_HW_SPI_MAX_XFER_BITS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HW_SPI_MAX_XFER_BITS&type=code) | Calculates the maximum transfer size in bits for hardware SPI based on the maximum transfer size in bytes. | (MP_HW_SPI_MAX_XFER_BYTES * 8) // Has to be an even multiple of 8 |
| [`MP_HW_SPI_MAX_XFER_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_HW_SPI_MAX_XFER_BYTES&type=code) | Maximum number of bytes that can be transferred in a single SPI transaction, set to 4092. | (4092) |
| [`MP_IGMP_IP_ADDR_TYPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_IGMP_IP_ADDR_TYPE&type=code) | Defines the type for IGMP IP addresses, using ip4_addr_t for LWIP version 2 and ip_addr_t for earlier versions. | ip4_addr_t |
| [`MP_INT_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_INT_MAX&type=code) | Represents the maximum value for integer types based on pointer size. | INTPTR_MAX |
| [`MP_INT_MIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_INT_MIN&type=code) | Represents the minimum value for signed integer types. | INTPTR_MIN |
| [`MP_INT_TYPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_INT_TYPE&type=code) | Determines the integer type used for mp_int_t based on the object representation. | (MP_INT_TYPE_INTPTR) |
| [`MP_INT_TYPE_INT64`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_INT_TYPE_INT64&type=code) | Indicates the use of 64-bit integers for the mp_int_t type. | (1) |
| [`MP_INT_TYPE_INTPTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_INT_TYPE_INTPTR&type=code) | Defines the integer type as a pointer-sized integer for mp_int_t and mp_uint_t. | (0) |
| [`MP_INT_TYPE_OTHER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_INT_TYPE_OTHER&type=code) | Indicates a custom integer type for exceptions requiring specific typedefs and defines. | (2) |
| [`MP_LEXER_EOF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_LEXER_EOF&type=code) | Represents the end-of-file character in the lexer. | ((unichar)MP_READER_EOF) |
| [`MP_MACHINE_I2C_FLAG_READ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MACHINE_I2C_FLAG_READ&type=code) | Indicates a read operation in I2C communication; if not set, a write operation occurs. | (0x01) // if not set then it's a write |
| [`MP_MACHINE_I2C_FLAG_STOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MACHINE_I2C_FLAG_STOP&type=code) | Indicates that a STOP condition should be sent after an I2C transaction. | (0x02) |
| [`MP_MACHINE_I2C_FLAG_WRITE1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MACHINE_I2C_FLAG_WRITE1&type=code) | Indicates that the first buffer in an I2C transfer is a write operation. | (0x04) |
| [`MP_MAP_SLOT_IS_FILLED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MAP_SLOT_IS_FILLED&type=code) | Checks if a specific slot in a map is filled with an element. | mp_map_slot_is_filled |
| [`MP_MAX_UNCOMPRESSED_TEXT_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_MAX_UNCOMPRESSED_TEXT_LEN&type=code) | Determines the maximum length for uncompressed error text strings. | (73) |
| [`MP_NATIVE_TYPE_BOOL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_BOOL&type=code) | Represents the native boolean type in function signatures. | (0x01) |
| [`MP_NATIVE_TYPE_INT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_INT&type=code) | Represents the native integer type in function signatures. | (0x02) |
| [`MP_NATIVE_TYPE_OBJ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_OBJ&type=code) | Represents the object type in native (viper) function signatures. | (0x00) |
| [`MP_NATIVE_TYPE_PTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_PTR&type=code) | Represents a pointer type in native function signatures. | (0x04) |
| [`MP_NATIVE_TYPE_PTR16`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_PTR16&type=code) | Represents a 16-bit pointer type. | (0x06) |
| [`MP_NATIVE_TYPE_PTR32`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_PTR32&type=code) | Represents a 32-bit pointer type in native code. | (0x07) |
| [`MP_NATIVE_TYPE_PTR8`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_PTR8&type=code) | Represents a pointer type with 8-bit addressing. | (0x05) |
| [`MP_NATIVE_TYPE_QSTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_QSTR&type=code) | Indicates the QSTR type for dynamic native modules. | (0x08) |
| [`MP_NATIVE_TYPE_UINT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NATIVE_TYPE_UINT&type=code) | Represents the unsigned integer type in native function signatures. | (0x03) |
| [`MP_NEED_LOG2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NEED_LOG2&type=code) | Requires a non-macro implementation of the log2 function. | (1) |
| [`MP_NOINLINE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NOINLINE&type=code) | Prevents function inlining to manage stack usage and maintain function call integrity. | __attribute__((noinline)) |
| [`MP_NORETURN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_NORETURN&type=code) | Indicates that a function does not return to the caller. | __attribute__((noreturn)) |
| [`MP_PARSE_NODE_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PARSE_NODE_ID&type=code) | Represents a parse node type for identifiers. | (0x02) |
| [`MP_PARSE_NODE_NULL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PARSE_NODE_NULL&type=code) | Represents a null parse node value. | (0) |
| [`MP_PARSE_NODE_SMALL_INT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PARSE_NODE_SMALL_INT&type=code) | Represents a small integer node in the parse tree. | (0x1) |
| [`MP_PARSE_NODE_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PARSE_NODE_STRING&type=code) | Represents a string node in the parse tree. | (0x06) |
| [`MP_PARSE_NODE_TOKEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PARSE_NODE_TOKEN&type=code) | Represents a token node in the parse tree with a value of 0x0a. | (0x0a) |
| [`MP_PI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PI&type=code) | Represents the mathematical constant π with high precision. | MICROPY_FLOAT_CONST(3.14159265358979323846) |
| [`MP_PIN_INPUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PIN_INPUT&type=code) | Represents the input mode for a pin. | (3) |
| [`MP_PIN_OUTPUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PIN_OUTPUT&type=code) | Represents a pin configured for output mode. | (4) |
| [`MP_PIN_READ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PIN_READ&type=code) | Indicates a request to read the value of a pin. | (1) |
| [`MP_PIN_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PIN_WRITE&type=code) | Indicates a request to write a value to a pin. | (2) |
| [`MP_PI_4`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PI_4&type=code) | Represents the value of π/4 as a constant float. | MICROPY_FLOAT_CONST(0.78539816339744830962) |
| [`MP_PROTOCOL_DTLS_CLIENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PROTOCOL_DTLS_CLIENT&type=code) | Indicates the use of DTLS protocol for client connections. | MP_TRANSPORT_IS_DTLS |
| [`MP_PROTOCOL_DTLS_SERVER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PROTOCOL_DTLS_SERVER&type=code) | Indicates a DTLS server endpoint with transport layer security. | (MP_ENDPOINT_IS_SERVER \| MP_TRANSPORT_IS_DTLS) |
| [`MP_PROTOCOL_TLS_CLIENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PROTOCOL_TLS_CLIENT&type=code) | Indicates the TLS client protocol. | 0 |
| [`MP_PROTOCOL_TLS_SERVER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PROTOCOL_TLS_SERVER&type=code) | Indicates the use of TLS protocol for server endpoints. | MP_ENDPOINT_IS_SERVER |
| [`MP_PROTO_FUN_INDICATOR_RAW_CODE_0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PROTO_FUN_INDICATOR_RAW_CODE_0&type=code) | Indicates a raw code structure for distinguishing between mp_raw_code_t and bytecode pointers. | (0) |
| [`MP_PROTO_FUN_INDICATOR_RAW_CODE_1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PROTO_FUN_INDICATOR_RAW_CODE_1&type=code) | Indicates a raw code function pointer in the proto_fun_indicator array. | (0) |
| [`MP_PYSTACK_DEBUG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PYSTACK_DEBUG&type=code) | Enables memory allocation debugging to verify consistency between allocated and freed memory. | (0) |
| [`MP_PYTHON_PRINTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_PYTHON_PRINTER&type=code) | Points to the function used for printing output, typically the standard output. | &mp_sys_stdout_print |
| [`MP_READER_EOF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_READER_EOF&type=code) | Indicates the end of the input stream for read operations. | ((mp_uint_t)(-1)) |
| [`MP_READER_IS_ROM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_READER_IS_ROM&type=code) | Indicates that the data is in ROM and remains valid until a soft reset. | ((size_t)-1) |
| [`MP_ROM_FALSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ROM_FALSE&type=code) | Represents the constant false value as a read-only pointer. | MP_ROM_PTR(&mp_const_false_obj) |
| [`MP_ROM_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ROM_NONE&type=code) | Represents a constant value equivalent to None in Python. | MP_ROM_PTR(&mp_const_none_obj) |
| [`MP_ROM_TRUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_ROM_TRUE&type=code) | Represents a constant pointer to the true object. | MP_ROM_PTR(&mp_const_true_obj) |
| [`MP_SANITIZER_BUILD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SANITIZER_BUILD&type=code) | Indicates if either Undefined Behavior Sanitizer (UBSAN) or Address Sanitizer (ASAN) is enabled. | (MP_UBSAN \|\| MP_ASAN) |
| [`MP_SCHED_IDLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCHED_IDLE&type=code) | Indicates that the scheduler is in an idle state. | (1) |
| [`MP_SCHED_LOCKED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCHED_LOCKED&type=code) | Indicates that the scheduler is in a locked state, preventing task switching. | (-1) |
| [`MP_SCHED_PENDING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SCHED_PENDING&type=code) | Indicates that the scheduler has pending tasks to execute. | (0) // 0 so it's a quick check in the VM |
| [`MP_SEEK_CUR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SEEK_CUR&type=code) | Indicates seeking from the current position in a stream. | (1) |
| [`MP_SEEK_END`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SEEK_END&type=code) | Indicates seeking to the end of a stream. | (2) |
| [`MP_SEEK_SET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SEEK_SET&type=code) | Indicates the start of a stream for seeking operations. | (0) |
| [`MP_SET_SLOT_IS_FILLED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SET_SLOT_IS_FILLED&type=code) | Determines if a slot in a map is filled. | mp_set_slot_is_filled |
| [`MP_SMALL_INT_BITS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SMALL_INT_BITS&type=code) | Number of bits in a small integer type, including the sign bit. | (MP_IMAX_BITS(MP_SMALL_INT_MAX) + 1) |
| [`MP_SMALL_INT_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SMALL_INT_MAX&type=code) | Maximum value for small integers, calculated as the bitwise negation of the minimum small integer. | ((mp_int_t)(~(MP_SMALL_INT_MIN))) |
| [`MP_SMALL_INT_MIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SMALL_INT_MIN&type=code) | Defines the minimum value for small integers based on the highest bit representation. | ((mp_int_t)(((mp_int_t)MP_OBJ_WORD_MSBIT_HIGH) >> 1)) |
| [`MP_SMALL_INT_POSITIVE_MASK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SMALL_INT_POSITIVE_MASK&type=code) | Mask for truncating mp_int_t to positive values. | ~(MP_OBJ_WORD_MSBIT_HIGH \| (MP_OBJ_WORD_MSBIT_HIGH >> 1) \| (MP_OBJ_WORD_MSBIT_HIGH >> 2)) |
| [`MP_SPIFLASH_ERASE_BLOCK_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SPIFLASH_ERASE_BLOCK_SIZE&type=code) | Defines the erase block size for SPI flash, set to 4096 bytes. | (4096) // must be a power of 2 |
| [`MP_SSIZE_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_SSIZE_MAX&type=code) | Defines the maximum size for signed integers, typically set to the largest value of ssize_t. | (0x7fffffffffffffff) |
| [`MP_STATE_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STATE_PORT&type=code) | Accesses port-specific state variables, typically used for managing resources like network interfaces or device states. | MP_STATE_VM |
| [`MP_STATIC_ASSERT_STR_ARRAY_COMPATIBLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_STATIC_ASSERT_STR_ARRAY_COMPATIBLE&type=code) | Ensures compatibility between mp_obj_str_t and mp_obj_array_t by checking offset alignment of their struct members. | \ |
| [`MP_S_IFDIR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_S_IFDIR&type=code) | Represents a directory type in file system operations, with a value of 0x4000. | (0x4000) |
| [`MP_S_IFREG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_S_IFREG&type=code) | Indicates a regular file type with a value of 0x8000. | (0x8000) |
| [`MP_TASK_COREID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TASK_COREID&type=code) | Determines the core ID for task creation, either core 0 or core 1 based on FreeRTOS configuration. | (0) |
| [`MP_TASK_PRIORITY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TASK_PRIORITY&type=code) | Determines the priority level of the MicroPython task in FreeRTOS. | (ESP_TASK_PRIO_MIN + 1) |
| [`MP_THREAD_DEFAULT_STACK_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_THREAD_DEFAULT_STACK_SIZE&type=code) | Calculates the default stack size for threads by adding minimum stack size and stack check margin. | (MP_THREAD_MIN_STACK_SIZE + MICROPY_STACK_CHECK_MARGIN) |
| [`MP_THREAD_GC_SIGNAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_THREAD_GC_SIGNAL&type=code) | Signal used for triggering garbage collection in multi-threaded environments. | (SIGRTMIN + 5) |
| [`MP_THREAD_MAXIMUM_USER_THREADS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_THREAD_MAXIMUM_USER_THREADS&type=code) | Limits the maximum number of user threads that can be created. | (4) |
| [`MP_THREAD_MIN_STACK_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_THREAD_MIN_STACK_SIZE&type=code) | Defines the minimum stack size for threads, set to 4 KB. | (4 * 1024) |
| [`MP_THREAD_PRIORITY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_THREAD_PRIORITY&type=code) | Sets the thread priority to match the main thread's priority. | (k_thread_priority_get(k_current_get()))    // same priority as the main thread |
| [`MP_THREAD_TERMINATE_SIGNAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_THREAD_TERMINATE_SIGNAL&type=code) | Signal used for terminating threads on Android platforms. | (SIGRTMIN + 6) |
| [`MP_TRANSPORT_IS_DTLS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_TRANSPORT_IS_DTLS&type=code) | Indicates the use of Datagram Transport Layer Security (DTLS) protocol. | (1 << 1) |
| [`MP_UART_ALLOWED_FLAGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UART_ALLOWED_FLAGS&type=code) | Allowed IRQ flags for UART user configuration. | (UART_UARTMIS_RTMIS_BITS \| UART_UARTMIS_TXMIS_BITS \| UART_UARTMIS_BEMIS_BITS) |
| [`MP_UART_IRQ_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UART_IRQ_RX&type=code) | Indicates a receive interrupt for UART. | (1) |
| [`MP_UART_IRQ_RXIDLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UART_IRQ_RXIDLE&type=code) | Indicates the UART RX idle interrupt event. | (2) |
| [`MP_UART_IRQ_TXIDLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UART_IRQ_TXIDLE&type=code) | Indicates the UART transmit idle interrupt. | (4) |
| [`MP_UART_RESERVED_FLAGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UART_RESERVED_FLAGS&type=code) | IRQ flags that are not to be modified by the user. | ((uint16_t)0x0020) |
| [`MP_UBSAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UBSAN&type=code) | Enables Undefined Behavior Sanitizer if supported by the compiler. | __has_feature(undefined_behavior_sanitizer) |
| [`MP_UINT_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UINT_MAX&type=code) | Represents the maximum value for unsigned integers based on the pointer type. | INTPTR_UMAX |
| [`MP_UNARY_OP_NUM_BYTECODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UNARY_OP_NUM_BYTECODE&type=code) | Defines the bytecode boundary for unary operations. | (MP_UNARY_OP_NOT + 1) |
| [`MP_UNARY_OP_NUM_RUNTIME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UNARY_OP_NUM_RUNTIME&type=code) | Count of unary operations available at runtime. | (MP_UNARY_OP_SIZEOF + 1) |
| [`MP_UNREACHABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_UNREACHABLE&type=code) | Indicates unreachable code, allowing the compiler to optimize accordingly. | __builtin_unreachable(); |
| [`MP_USBD_BUILTIN_DESC_CFG_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_USBD_BUILTIN_DESC_CFG_LEN&type=code) | Length calculation for the built-in USB configuration descriptor including optional CDC and MSC descriptors. | (TUD_CONFIG_DESC_LEN +                     \ |
| [`MP_USBD_MAX_PEND_EXCS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_USBD_MAX_PEND_EXCS&type=code) | Limits the number of pending exceptions during a TinyUSB task execution. | 2 |
| [`MP_VFS_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_VFS_NONE&type=code) | Indicates that a path was not found in the virtual file system. | ((mp_vfs_mount_t *)1) |
| [`MP_VFS_ROM_IOCTL_GET_NUMBER_OF_SEGMENTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_VFS_ROM_IOCTL_GET_NUMBER_OF_SEGMENTS&type=code) | Returns the number of segments in the ROM filesystem. | (1) // rom_ioctl(1) |
| [`MP_VFS_ROM_IOCTL_GET_SEGMENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_VFS_ROM_IOCTL_GET_SEGMENT&type=code) | Retrieves a segment of the ROM filesystem. | (2) // rom_ioctl(2, <id>) |
| [`MP_VFS_ROM_IOCTL_WRITE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_VFS_ROM_IOCTL_WRITE&type=code) | Command for writing data to ROM with specified offset and buffer. | (4) // rom_ioctl(4, <id>, <offset>, <buf>) |
| [`MP_VFS_ROM_IOCTL_WRITE_COMPLETE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_VFS_ROM_IOCTL_WRITE_COMPLETE&type=code) | Indicates completion of a write operation in the VFS ROM IOCTL interface. | (5) // rom_ioctl(5, <id>) |
| [`MP_VFS_ROM_IOCTL_WRITE_PREPARE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_VFS_ROM_IOCTL_WRITE_PREPARE&type=code) | Prepares for writing data to a specified range in ROM. | (3) // rom_ioctl(3, <id>, <len>) |
| [`MP_VFS_ROOT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_VFS_ROOT&type=code) | Represents the root directory in the virtual file system. | ((mp_vfs_mount_t *)0) |
| [`MP_WEAK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MP_WEAK&type=code) | Marks a function as weak, allowing it to be overridden by a stronger definition. | __attribute__((weak)) |