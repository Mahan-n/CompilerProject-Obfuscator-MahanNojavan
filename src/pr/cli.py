import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Mini C Obfuscator CLI")
    parser.add_argument("input", help="Path to the input C file")
    parser.add_argument("output", help="Path to the output obfuscated C file")
    parser.add_argument("--rename-vars", action="store_true", help="Enable variable renaming")
    parser.add_argument("--remove-dead-code", action="store_true", help="Enable dead code removal")
    parser.add_argument("--insert-opaque", action="store_true", help="Insert opaque predicates")
    # Add more flags here if you introduce new obfuscation passes
    return parser.parse_args()
