import sys

try:
    sys.settrace
except AttributeError:
    print("SKIP")
    raise SystemExit

_MAX_LEN = 40
# Global variables for testing
global_var1 = "global_string"
global_var2 = 42
global_list = [1, 2, 3]
global_dict = {"key1": "value1", "key2": "value2"}

# Flag to track if breakpoint was hit
breakpoint_hit = False


# Simplify the output for consistent testing
def simplified_repr(obj):
    """Create simplified string representations for consistent test output"""
    if isinstance(obj, (list, tuple)):
        return f"{type(obj).__name__}[{len(obj)} items]"
    elif isinstance(obj, dict):
        return f"dict[{len(obj)} items]"
    elif isinstance(obj, str):
        if len(obj) > _MAX_LEN:
            return f'"{obj[:_MAX_LEN]}..."'
        return repr(obj)
    else:
        r = repr(obj)
        if " at 0x" in r:
            return "<object>"
        return r


def print_frame_info(frame, event, arg):
    """Print frame information including locals and globals"""
    print(f"Event: {event}")
    print(f"Function: {frame.f_code.co_name}")
    print(f"Line: {frame.f_lineno}")
    print(f"Last instruction: {frame.f_lasti}")


def tracer(frame, event, arg):
    global breakpoint_hit

    # Set breakpoint at specific line in test_function
    if (
        event == "line" and frame.f_code.co_name == "test_function" and frame.f_lineno == 80
    ):  # Line with the comment "# BREAKPOINT HERE"
        breakpoint_hit = True

        print("\n*** BREAKPOINT HIT ***")
        print_frame_info(frame, event, arg)

    # Print basic info for all frames to track execution
    if event == "call":
        # Only print for significant functions to reduce output noise
        if frame.f_code.co_name not in ["<module>", "<lambda>"]:
            print(f"TRACE {event}: Entering {frame.f_code.co_name}")
    elif event == "return":
        # Only print for significant functions to reduce output noise
        if frame.f_code.co_name not in ["<module>", "<lambda>"]:
            print(
                f"TRACE {event}: Leaving {frame.f_code.co_name} with value: {simplified_repr(arg)}"
            )

    return tracer


def test_function():
    local_var1 = "hello debugger"
    _under = "this is an under variable"
    __dunder = "this is a double under variable"
    a = 100
    b = 2200
    c = 33333
    l = [1, 2, 3]
    d = {"a": 1, "b": 2, "c": 3}
    tuple1 = (1, 2, 3)
    tuple2 = (a, b, c, a)
    long_name = a + b + c  # BREAKPOINT HERE

    return long_name


def nested_function(depth=2):
    """Create a chain of nested function calls to test stack frame access"""
    if depth <= 0:
        # At maximum depth, examine current and parent frame only
        current_frame = sys._getframe()
        parent_frame = current_frame.f_back

        print("\n*** STACK FRAMES ***")

        # Print current frame info
        print("\nCurrent frame:")
        print(f"  Name: {current_frame.f_code.co_name}")
        print(f"  Line: {current_frame.f_lineno}")
        print("  Local variables:")
        for key, value in sorted(current_frame.f_locals.items()):
            if not key.startswith("__"):
                print(f"    {key} = {simplified_repr(value)}")

        # Print parent frame info
        if parent_frame:
            print("\nParent frame:")
            print(f"  Name: {parent_frame.f_code.co_name}")
            print(f"  Line: {parent_frame.f_lineno}")
            print("  Local variables:")
            for key, value in sorted(parent_frame.f_locals.items()):
                if not key.startswith("__"):
                    print(f"    {key} = {simplified_repr(value)}")

        return "Bottom of recursion"
    else:
        # Add some local variables at each level to make the frames more interesting
        level_data = f"data at level {depth}"
        level_number = depth * 10
        return nested_function(depth - 1)


def do_breakpoint_test():
    # Run tests
    sys.settrace(tracer)

    # Part 1: Test function with breakpoints
    result = test_function()
    print(f"Test function result: {result}")
    print(f"Breakpoint was hit: {breakpoint_hit}")

    # Part 2: Test stack frames with a depth of 2
    print("Testing stack frames with nested calls:")
    nested_result = nested_function(2)
    print(f"Nested result: {nested_result}")

    # Disable tracing
    sys.settrace(None)


print("Starting sys.settrace tests for breakpoints and frame access")
do_breakpoint_test()
print("Tests complete")
