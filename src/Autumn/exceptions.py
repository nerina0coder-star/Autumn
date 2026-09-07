

class DeprecationException(Exception):
    """
    Raised when a feature is deprecated.
    """

class OptimizedError(Exception):
    def __init__(self, name: str):
        self.args = (f"Cannot multiply a child of {name} using {name}'s" +
                  " performance-optimized multiplication, use AbstractTag's multiplication instead.",)
        Exception.__init__(self, self.args)

class ContextError(Exception):
    def __init__(self, message: str =
    """
    Working outside of the base context.
    To work with the base context, write:
    
    with Base:
       ... # Your code here
    """):
        Exception.__init__(self, message)