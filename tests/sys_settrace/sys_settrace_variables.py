import sys

try:
    sys.settrace
except AttributeError:
    print("SKIP")
    raise SystemExit

# Global variables for testing
global_string = "global string value"
global_number = 9876
global_list = [10, 20, 30]
global_dict = {"global_key": "global_value"}

# Flag to track variable changes
var_changes = []


def simplified_repr(obj):
    """Create simplified string representations for consistent test output"""
    MAX_LEN = 40
    if isinstance(obj, (list, tuple)):
        return f"{type(obj).__name__}[{len(obj)} items]"
    elif isinstance(obj, dict):
        return f"dict[{len(obj)} items]"
    elif isinstance(obj, str) and len(obj) > MAX_LEN:
        return f'"{obj[:MAX_LEN]}..."'
    else:
        return repr(obj)


def tracer(frame, event, arg):
    """Trace function that tracks variables and their changes"""
    # TODO : frequent linenumber mismatch between unix and EPS32 ports
    lineno = frame.f_lineno
    # lineno = "fuzzy"

    print(f"( {lineno} , {frame.f_lasti} ) ", end="")

    f_locals = frame.f_locals.items()
    print(f"{f_locals=}")
    return tracer


def test_simple_vars():
    """Test accessing variables and types"""
    # Simple variable assignments
    local_string = "local string value"
    local_number = 42
    local_list = [1, 2, 3]
    local_dict = {"a": 1, "b": 2, "c": 3}

    # Access global values
    global_value = global_string

    # Return a data structure with all variables
    return {
        "local_string": local_string,
        "local_number": local_number,
        "local_list": local_list,
        "local_dict": local_dict,
        "global_value": global_value,
    }


def update_global():
    """Update a global variable and return its new value"""
    global global_number
    old_value = global_number
    global_number += 1
    return {"old_value": old_value, "new_value": global_number}


def test_var_changes():
    """Test tracking variable changes during execution"""
    counter = 0
    value = "initial"

    # Modify variables
    counter += 1
    value = "changed"

    # Use update_global to change a global variable
    global_update = update_global()

    return {"counter": counter, "value": value, "global_update": global_update}


# Run tests
print("Testing variable access with sys.settrace")
sys.settrace(tracer)

result1 = test_simple_vars()
print(f"Simple vars test result: {simplified_repr(result1)}")

result2 = test_var_changes()
print(f"Variable changes test result: {simplified_repr(result2)}")

# Disable tracing
sys.settrace(None)
print("Tests complete")
