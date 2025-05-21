from cli import parse_args  # <--- Import remains unchanged
from lexer_parser.parser import parser
from obfuscation_passes import RenameVariables, RemoveDeadCode, InsertOpaquePredicates
from codegen import CodeGenerator
import time
import os
from ast_visualizer import ASTVisualizer


def perform_obfuscation_passes(ast_tree, obf_passes):
    """Apply each obfuscation pass to the AST."""
    for obf_pass in obf_passes:
        obf_pass.apply(ast_tree)


def cli_entry():
    """Entry point for the CLI-based obfuscator."""
    opts = parse_args()

    # Read input C code
    with open(opts.input, 'r') as f:
        input_src = f.read()

    size_original = len(input_src.encode('utf-8'))

    # Parse the code into an AST
    ast_tree = parser.parse(input_src)

    # Collect the selected obfuscation passes
    selected_passes = []
    if opts.rename_vars:
        selected_passes.append(RenameVariables())
    if opts.remove_dead_code:
        selected_passes.append(RemoveDeadCode())
    if opts.insert_opaque:
        selected_passes.append(InsertOpaquePredicates())

    # Apply the obfuscation passes (with timing)
    t0 = time.time()
    perform_obfuscation_passes(ast_tree, selected_passes)
    t1 = time.time()

    # Generate obfuscated code
    code_generator = CodeGenerator()
    obf_code = code_generator.generate(ast_tree)

    # Write the obfuscated code to the output file
    with open(opts.output, 'w') as f:
        f.write(obf_code)

    size_obf = len(obf_code.encode('utf-8'))

    # Optional: visualize the AST after obfuscation
    visual = ASTVisualizer()
    visual.render(ast_tree, 'examples/ast_visualized.png')

    # Print results
    print("✅ Obfuscation completed. Output written to:", opts.output)
    print(f"⏱️  Obfuscation time: {t1 - t0:.4f} seconds")
    print(f"📦 Original size: {size_original} bytes")
    print(f"📦 Obfuscated size: {size_obf} bytes")
    print(f"📈 Size change: {size_obf - size_original:+} bytes")


if __name__ == "__main__":
    cli_entry()