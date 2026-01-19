# Test to simulate Windows configuration
import sys
sys.path.insert(0, '../../tests')
sys.path.insert(0, '.')

# Test if decode exists
try:
    result = b''.decode()
    print("decode exists")
except AttributeError:
    print("decode does not exist")
    
# Test if 3-arg decode works
try:
    result = b'hello'.decode('utf-8', 'ignore')
    print("3-arg decode works:", repr(result))
except TypeError as e:
    print("3-arg decode fails with TypeError:", e)
except Exception as e:
    print("3-arg decode fails with:", type(e).__name__, e)
