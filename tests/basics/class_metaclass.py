# Test metaclass functionality (PEP 3115)
# Note: This test is adapted for MicroPython's implementation which uses __init__ for metaclass customization

# Test 1: Basic metaclass with metaclass= keyword
print("Test 1: Basic metaclass")
class Meta(type):
    def __init__(cls, name, bases, dct):
        print("Meta.__init__ called for", name)
        cls.from_meta = True

class C(metaclass=Meta):
    pass

print("type(C):", type(C).__name__)
print("C.from_meta:", C.from_meta)

# Test 2: Metaclass with __prepare__
print("\nTest 2: __prepare__ method")
class OrderedMeta(type):
    @staticmethod
    def __prepare__(name, bases):
        print("__prepare__ called for", name)
        return {}
    
    def __init__(cls, name, bases, dct):
        print("OrderedMeta.__init__ called for", name)
        cls.prepared = True

class D(metaclass=OrderedMeta):
    x = 1
    y = 2

print("D.x:", D.x)
print("D.y:", D.y)
print("D.prepared:", D.prepared)

# Test 3: Metaclass with initialization
print("\nTest 3: Metaclass with __init__")
class InitMeta(type):
    def __init__(cls, name, bases, dct):
        print("InitMeta.__init__ called for", name)
        cls.initialized = True

class E(metaclass=InitMeta):
    pass

print("E.initialized:", E.initialized)

# Test 4: Metaclass inheritance - metaclass should be inherited
print("\nTest 4: Metaclass inheritance")
class F(E):
    pass

print("type(F):", type(F).__name__)
print("F.initialized:", F.initialized)

# Test 5: Metaclass with custom attribute access
print("\nTest 5: Custom metaclass behavior")
class AttrMeta(type):
    def __init__(cls, name, bases, dct):
        # Add a class attribute automatically
        cls.auto_added = 'automatic'

class G(metaclass=AttrMeta):
    manual = 'manual'

print("G.manual:", G.manual)
print("G.auto_added:", G.auto_added)

# Test 6: Metaclass from base class
print("\nTest 6: Metaclass from base")
class H(G):
    pass

print("type(H):", type(H).__name__)
print("H.auto_added:", H.auto_added)

# Test 7: __prepare__ returns custom dict
print("\nTest 7: __prepare__ with custom dict")
class CustomDictMeta(type):
    @staticmethod
    def __prepare__(name, bases):
        d = {}
        d['_prepared'] = 'yes'
        return d
    
    def __init__(cls, name, bases, dct):
        cls.had_prepared = '_prepared' in dct

class I(metaclass=CustomDictMeta):
    pass

print("I.had_prepared:", I.had_prepared)

print("\nAll tests passed!")

