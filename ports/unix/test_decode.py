# Test what happens when feature is disabled
try:
    result = b'\xff\xfe'.decode('utf-8', 'ignore')
    print("Result:", repr(result))
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
