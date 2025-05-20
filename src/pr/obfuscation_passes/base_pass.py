class BaseObfuscationPass:
    def apply(self, ast):
        raise NotImplementedError("Obfuscation passes must implement the apply() method.")
