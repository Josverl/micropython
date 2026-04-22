class Bar:
    """A bar class"""

    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return f"Bar({self.value})"
