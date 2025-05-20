# ast_visualizer.py
import pydot
from lexer_parser.ast_nodes import *

class ASTVisualizer:
    def __init__(self):
        self.graph = pydot.Dot(graph_type='digraph')
        self.counter = 0

    def _new_id(self):
        self.counter += 1
        return f"node{self.counter}"

    def _add_node(self, label):
        node_id = self._new_id()
        node = pydot.Node(node_id, label=label, shape="box", fontsize="10")
        self.graph.add_node(node)
        return node_id

    def visit(self, node):
        if node is None:
            return self._add_node("None")

        if isinstance(node, Program):
            root = self._add_node("Program")
            for fn in node.functions:
                child = self.visit(fn)
                self.graph.add_edge(pydot.Edge(root, child))
            return root

        elif isinstance(node, Function):
            root = self._add_node(f"Function: {node.name}")
            for _, param in node.params:
                param_node = self._add_node(f"Param: {param}")
                self.graph.add_edge(pydot.Edge(root, param_node))
            body_node = self.visit(node.body)
            self.graph.add_edge(pydot.Edge(root, body_node))
            return root

        elif isinstance(node, Compound):
            root = self._add_node("Compound")
            for stmt in node.statements:
                child = self.visit(stmt)
                self.graph.add_edge(pydot.Edge(root, child))
            return root

        elif isinstance(node, VarDecl):
            return self._add_node(f"VarDecl: {node.name}")

        elif isinstance(node, Assignment):
            root = self._add_node(f"Assign: {node.name}")
            expr_node = self.visit(node.expr)
            self.graph.add_edge(pydot.Edge(root, expr_node))
            return root

        elif isinstance(node, If):
            root = self._add_node("If")
            cond = self.visit(node.condition)
            then = self.visit(node.then_branch)
            self.graph.add_edge(pydot.Edge(root, cond, label="cond"))
            self.graph.add_edge(pydot.Edge(root, then, label="then"))
            if node.else_branch:
                else_node = self.visit(node.else_branch)
                self.graph.add_edge(pydot.Edge(root, else_node, label="else"))
            return root

        elif isinstance(node, Return):
            root = self._add_node("Return")
            expr = self.visit(node.expr)
            self.graph.add_edge(pydot.Edge(root, expr))
            return root

        elif isinstance(node, BinOp):
            root = self._add_node(f"Op: {node.op}")
            left = self.visit(node.left)
            right = self.visit(node.right)
            self.graph.add_edge(pydot.Edge(root, left))
            self.graph.add_edge(pydot.Edge(root, right))
            return root

        elif isinstance(node, Num):
            return self._add_node(f"Num: {node.value}")

        elif isinstance(node, Var):
            return self._add_node(f"Var: {node.name}")

        else:
            return self._add_node(str(type(node).__name__))

    def render(self, ast, filename='ast_output.png'):
        self.visit(ast)
        self.graph.write_png(filename)
        print(f"✅ AST visualization saved to {filename}")
