# Test metaclass functionality (PEP 3115)
# Note: __prepare__ method requires MICROPY_METACLASS_PREPARE to be enabled

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

# Test 2: Metaclass with __init__
print("\nTest 2: Metaclass with __init__")
class InitMeta(type):
    def __init__(cls, name, bases, dct):
        print("InitMeta.__init__ called for", name)
        cls.initialized = True

class E(metaclass=InitMeta):
    pass

print("E.initialized:", E.initialized)

# Test 3: Metaclass inheritance - metaclass should be inherited
print("\nTest 3: Metaclass inheritance")
class F(E):
    pass

print("type(F):", type(F).__name__)
print("F.initialized:", F.initialized)

# Test 4: Custom metaclass behavior
print("\nTest 4: Custom metaclass behavior")
class AttrMeta(type):
    def __init__(cls, name, bases, dct):
        # Add a class attribute automatically
        cls.auto_added = 'automatic'

class G(metaclass=AttrMeta):
    manual = 'manual'

print("G.manual:", G.manual)
print("G.auto_added:", G.auto_added)

# Test 5: Metaclass from base class
print("\nTest 5: Metaclass from base")
class H(G):
    pass

print("type(H):", type(H).__name__)
print("H.auto_added:", H.auto_added)

# Test 6: Explicit metaclass with base
print("\nTest 6: Explicit metaclass with base")
class BaseClass:
    base_attr = 'base'

class ExplicitMeta(type):
    def __init__(cls, name, bases, dct):
        cls.explicit_meta = True

class DerivedExplicit(BaseClass, metaclass=ExplicitMeta):
    pass

print("type(DerivedExplicit):", type(DerivedExplicit).__name__)
print("DerivedExplicit.base_attr:", DerivedExplicit.base_attr)
print("DerivedExplicit.explicit_meta:", DerivedExplicit.explicit_meta)

print("\nAll tests passed!")
