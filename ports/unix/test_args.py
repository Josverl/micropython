# Test function argument handling
def func1(a, b):
    return f"a={a}, b={b}"

# Try calling with 3 args
try:
    result = func1(1, 2, 3)
    print("3 args works:", result)
except TypeError as e:
    print("TypeError:", e)
