# Test __init_subclass__ functionality (PEP 487)

# Check if __init_subclass__ support is enabled
try:
    class _TestBase:
        _called = False
        @classmethod
        def __init_subclass__(cls):
            _TestBase._called = True
    
    class _TestDerived(_TestBase):
        pass
    
    if not _TestBase._called:
        raise TypeError("__init_subclass__ not called")
except (TypeError, AttributeError):
    print("SKIP")
    raise SystemExit

# Test 1: Basic __init_subclass__ with @classmethod
print("Test 1: Basic __init_subclass__")
class Base:
    @classmethod
    def __init_subclass__(cls):
        print("__init_subclass__ called for", cls.__name__)
        cls.from_init_subclass = True

class Derived(Base):
    pass

print("Derived.from_init_subclass:", Derived.from_init_subclass)

# Test 2: __init_subclass__ without @classmethod decorator (implicit classmethod per PEP 487)
print("\nTest 2: __init_subclass__ without decorator")
class Base2:
    def __init_subclass__(cls):
        print("__init_subclass__ (no decorator) for", cls.__name__)
        cls.marker = "implicit_classmethod"

class Derived2(Base2):
    pass

print("Derived2.marker:", Derived2.marker)

# Test 3: __init_subclass__ with keyword arguments
print("\nTest 3: __init_subclass__ with kwargs")
class Base3:
    @classmethod
    def __init_subclass__(cls, **kwargs):
        print("__init_subclass__ for", cls.__name__, "with kwargs:", kwargs)
        cls.kwargs = kwargs

class Derived3(Base3, foo='bar', init=True):
    pass

print("Derived3.kwargs:", Derived3.kwargs)

# Test 4: __init_subclass__ with named kwargs (dataclass pattern)
print("\nTest 4: Dataclass-style __init_subclass__")
class ModelBase:
    @classmethod
    def __init_subclass__(cls, *, init=True, frozen=False, eq=True):
        print("ModelBase.__init_subclass__ for", cls.__name__)
        print("  init={}, frozen={}, eq={}".format(init, frozen, eq))
        cls.config = {'init': init, 'frozen': frozen, 'eq': eq}

class CustomerModel(ModelBase, init=False, frozen=True, eq=False):
    pass

print("CustomerModel.config:", CustomerModel.config)

# Test 5: Multiple levels of inheritance
print("\nTest 5: Multiple levels of inheritance")
class GrandParent:
    @classmethod
    def __init_subclass__(cls):
        print("GrandParent.__init_subclass__ for", cls.__name__)
        cls.from_grandparent = True

class Parent(GrandParent):
    @classmethod
    def __init_subclass__(cls):
        print("Parent.__init_subclass__ for", cls.__name__)
        cls.from_parent = True

class Child(Parent):
    pass

print("Child.from_grandparent:", Child.from_grandparent)
print("Child.from_parent:", Child.from_parent)

# Test 6: Multiple inheritance
print("\nTest 6: Multiple inheritance")
class BaseA:
    @classmethod
    def __init_subclass__(cls, **kwargs):
        print("BaseA.__init_subclass__ for", cls.__name__)
        cls.from_a = True

class BaseB:
    @classmethod
    def __init_subclass__(cls, **kwargs):
        print("BaseB.__init_subclass__ for", cls.__name__)
        cls.from_b = True

class Multi(BaseA, BaseB, x=1):
    pass

print("Multi.from_a:", Multi.from_a)
print("Multi.from_b:", Multi.from_b)

# Test 7: Base class without __init_subclass__ (should not error)
print("\nTest 7: Base without __init_subclass__")
class NoInit:
    pass

class DerivedNoInit(NoInit):
    pass

print("DerivedNoInit created successfully")

print("\nAll tests passed!")
