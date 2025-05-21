import argparse


def get_cli_args():
    """
    Parse and return command-line options for the Mini-C Obfuscator.
    """
    arg_parser = argparse.ArgumentParser(description="Mini-C Obfuscator CLI")

    # positional I/O paths
    arg_parser.add_argument("src_path", help="Path to the input C file")
    arg_parser.add_argument("dst_path", help="Path to save the obfuscated C file")

    # optional feature flags
    arg_parser.add_argument(
        "--rename-vars",
        dest="rename_vars",
        action="store_true",
        help="Enable variable renaming pass",
    )
    arg_parser.add_argument(
        "--remove-dead-code",
        dest="remove_dead_code",
        action="store_true",
        help="Enable dead-code elimination pass",
    )
    arg_parser.add_argument(
        "--insert-opaque",
        dest="insert_opaque",
        action="store_true",
        help="Insert opaque predicates pass",
    )

    # extend here for future obfuscation passes
    return arg_parser.parse_args()
