import sys
import os
from pathlib import Path

# Ensure the project root is in sys.path for direct module imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from lexer_parser.parser import parser
from obfuscation_passes.rename_variables import RenameVariables
from codegen_refactored import CCodeGenerator  # updated import path and class name


def test_variable_renaming_pass():
    """Verify that the RenameVariables pass replaces original identifiers."""

    sample_source = """
    int main() {
        int x;
        int y;
        x = 5;
        y = x + 3;
        return y;
    }
    """

    # Parse → transform → generate C
    ast_tree = parser.parse(sample_source)
    RenameVariables().apply(ast_tree)
    generated_code = CCodeGenerator().generate_c_code(ast_tree)

    # Ensure the original identifiers no longer appear in the output C code
    assert "x" not in generated_code
    assert "y" not in generated_code
