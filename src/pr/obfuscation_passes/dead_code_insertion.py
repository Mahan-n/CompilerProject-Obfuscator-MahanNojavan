import random
from lexer_parser.ast_nodes import Assignment, Num
from obfuscation_passes.base_pass import BaseObfuscationPass  # external dependency

# ------------------------------------------------------------------
#  Internal helpers / constants
# ------------------------------------------------------------------

_FAKE_IDENTIFIERS = [
    "useless", "dummy", "junk", "tmp", "waste", "garbage", "trash"
]


def _make_dummy_assignment():
    """Create an assignment that has no effect on actual program semantics."""
    var_label = random.choice(_FAKE_IDENTIFIERS) + str(random.randint(100, 999))
    literal_val = random.randint(0, 1000)
    return Assignment(var_label, Num(literal_val))


def _inject_dead_code(ast_root):
    """Traverse all function bodies and splice in benign assignments."""
    for fn in ast_root.functions:
        stitched_body = []
        for stmt in fn.body.statements:
            # Occasionally prepend a dummy statement (40% chance)
            if random.random() < 0.4:
                stitched_body.append(_make_dummy_assignment())

            stitched_body.append(stmt)

            # Occasionally append a dummy statement (30% chance)
            if random.random() < 0.3:
                stitched_body.append(_make_dummy_assignment())

        fn.body.statements = stitched_body
    return ast_root


# ------------------------------------------------------------------
#  Public pass wrapper (retains original class name for compatibility)
# ------------------------------------------------------------------
class RemoveDeadCode(BaseObfuscationPass):
    """Ironically *adds* inert assignments to obscure program intent."""

    def apply(self, ast):
        _inject_dead_code(ast)
