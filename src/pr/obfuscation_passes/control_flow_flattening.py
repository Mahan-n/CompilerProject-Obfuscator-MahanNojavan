import random
from lexer_parser.ast_nodes import *

def control_flow_flatten(ast):
    for func in ast.functions:
        flattened_stmts = []
        dispatcher_name = "__state"
        label_map = {}
        body = func.body.statements
        labels = list(range(len(body)))

        # Map each real statement to a label
        for i, label in enumerate(labels):
            label_map[label] = body[i]

        # Initial dispatcher variable
        flattened_stmts.append(Assignment(dispatcher_name, Num(0)))

        # Build loop with chained if statements
        loop_body = []

        for label in labels:
            condition = BinOp(Var(dispatcher_name), '==', Num(label))
            stmt = label_map[label]

            # After executing this stmt, move to next state or -1 to exit
            next_label = label + 1 if label + 1 < len(labels) else -1
            update_dispatch = Assignment(dispatcher_name, Num(next_label))
            block = Compound([stmt, update_dispatch])

            loop_body.append(If(condition, block))

        # while (__state != -1) { ... }
        loop = While(BinOp(Var(dispatcher_name), '!=', Num(-1)), Compound(loop_body))
        flattened_stmts.append(loop)

        # Replace the original body
        func.body.statements = flattened_stmts

    return ast
