class Foo:
    """Foo class for testing purposes."""

    def __init__(self, value=None):
        """Initialize Foo with an optional value."""
        self.value = value

    def get_value(self):
        """Return the stored value."""
        return self.value

    def set_value(self, value):
        """Set the stored value."""
        self.value = value

    def __repr__(self):
        """Return string representation of Foo."""
        return f"Foo(value={self.value})"
