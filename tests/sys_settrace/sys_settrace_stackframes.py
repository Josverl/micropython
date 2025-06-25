import sys

try:
    sys.settrace
except AttributeError:
    print("SKIP")
    raise SystemExit

# Global variable to collect stack frames
frames_seen = []


def simplified_repr(obj):
    """Create simplified string representations for consistent test output"""
    if isinstance(obj, (list, tuple)):
        return f"{type(obj).__name__}[{len(obj)} items]"
    elif isinstance(obj, dict):
        return f"dict[{len(obj)} items]"
    elif isinstance(obj, str) and len(obj) > 10:
        return f'"{obj[:10]}..."'
    else:
        return repr(obj)


def print_frame(frame, depth):
    """Print a single frame's information"""
    func_name = frame.f_code.co_name
    filename = frame.f_code.co_filename.split("/")[-1]  # Just the filename
    line = frame.f_lineno

    print(f"FRAME {depth}: {func_name} at {filename}:{line}")

    # Print local variables for this frame
    locals_dict = frame.f_locals
    if locals_dict:
        print("  Local variables:")
        for name, value in sorted(locals_dict.items()):
            if not name.startswith("__"):  # Skip special variables
                print(f"    {name} = {simplified_repr(value)}")


def stack_tracer(frame, event, arg):
    """Tracer function that examines stack frames"""
    # For test clarity, only print for specific events
    if event == "call" and frame.f_code.co_name in [
        "level1",
        "level2",
        "level3",
        "get_current_frame",
        "examine_frames",
    ]:
        print(f"\nEVENT: {event} in {frame.f_code.co_name}")

        # Collect frame IDs to avoid duplicates
        frame_id = id(frame)
        if frame_id not in frames_seen:
            frames_seen.append(frame_id)

    lineno = frame.f_lineno
    lineno = "fuzzy"

    print(f"( {lineno} , {frame.f_lasti} ) ", end="")
    f_locals = frame.f_locals.items()
    print(f"{f_locals=}")

    return stack_tracer


def level3(param):
    """Deepest level function"""
    local_var = "level3 local"

    # Just return some data
    return {"level": 3, "param": param, "local": local_var}


def level2(param):
    """Middle level function"""
    numbers = [10, 20, 30]

    # Call next level down
    result = level3(param + ".from_level2")

    return {"level": 2, "numbers": numbers, "inner_result": result}


def level1():
    """Top level function"""
    name = "top_level"

    # Call next level down
    result = level2(name)

    return {"level": 1, "name": name, "inner_result": result}


def get_current_frame():
    """Get the current frame using sys._getframe()"""
    frame = sys._getframe()

    print("\nDirect frame access:")
    print_frame(frame, 0)

    # Get and print parent frame too
    if frame.f_back:
        parent = frame.f_back
        print_frame(parent, 1)

    return "Frame inspection complete"


def examine_frames():
    """Walk through all frames in the call stack"""
    # Get current frame
    current = sys._getframe()
    depth = 0

    print("\nFull stack trace:")

    # Walk the stack from current frame to the bottom
    while current:
        print_frame(current, depth)
        current = current.f_back
        depth += 1
    return f"Stack depth: {depth}"


# Test functions for frame analysis
def test_nested_frames():
    """Test accessing variables in nested function frames"""
    print("Testing nested call stack frames with sys.settrace")

    # Clear frame tracking
    global stack_frames_seen
    stack_frames_seen = []

    # Enable tracing
    sys.settrace(stack_tracer)

    # Start the call chain
    result = level1()

    # Disable tracing
    sys.settrace(None)

    print(f"\nFinal result of nested calls: {result}")
    print(f"Total unique frames seen: {len(stack_frames_seen)}")

    return result


# Run the tests
test_nested_frames()

print("\nStack frame tests complete")
