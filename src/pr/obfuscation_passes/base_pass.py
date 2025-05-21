class BaseObfuscationPass:
    """Abstract superclass for all AST-transforming obfuscation passes."""

    def apply(self, tree):
        """Transform *tree* in-place. Subclasses must override."""
        raise NotImplementedError("Obfuscation passes must implement the apply() method.")