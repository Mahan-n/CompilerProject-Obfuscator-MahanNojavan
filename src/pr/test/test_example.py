# test/test_example.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lexer_parser.parser import parser
from obfuscation_passes.rename_variables import RenameVariables
from codegen import CodeGenerator

def test_rename_variables():
    code = """
    int main() {
        int x;
        int y;
        x = 5;
        y = x + 3;
        return y;
    }
    """
    ast = parser.parse(code)
    RenameVariables().apply(ast)
    output = CodeGenerator().generate(ast)

    # Test that original variable names are not in output
    assert "x" not in output
    assert "y" not in output
