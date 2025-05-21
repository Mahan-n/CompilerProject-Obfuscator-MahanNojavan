import pydot
from lexer_parser.ast_nodes import *


class SyntaxTreeVisualizer:
    """Generate a PNG diagram of the Mini‑C AST using pydot/Graphviz."""

    def __init__(self):
        self.dot_graph = pydot.Dot(graph_type="digraph")
        self.node_index = 0  # unique id counter

    # ------------------------------------------------------------------
    #  Low‑level helpers
    # ------------------------------------------------------------------
    def _next_id(self) -> str:
        """Return a new unique node identifier for Graphviz."""
        self.node_index += 1
        return f"n{self.node_index}"

    def _emit_node(self, label: str) -> str:
        """Create a labeled node in the dot graph and return its id."""
        node_id = self._next_id()
        gv_node = pydot.Node(node_id, label=label, shape="box", fontsize="10")
        self.dot_graph.add_node(gv_node)
        return node_id

    # ------------------------------------------------------------------
    #  Recursive descent over the AST
    # ------------------------------------------------------------------
    def _walk(self, ast_node):
        if ast_node is None:
            return self._emit_node("None")

        # Program root --------------------------------------------------
        if isinstance(ast_node, Program):
            root_id = self._emit_node("Program")
            for func in ast_node.functions:
                child_id = self._walk(func)
                self.dot_graph.add_edge(pydot.Edge(root_id, child_id))
            return root_id

        # Function definition ------------------------------------------
        if isinstance(ast_node, Function):
            root_id = self._emit_node(f"Function: {ast_node.name}")
            for _, param_name in ast_node.params:
                param_id = self._emit_node(f"Param: {param_name}")
                self.dot_graph.add_edge(pydot.Edge(root_id, param_id))
            body_id = self._walk(ast_node.body)
            self.dot_graph.add_edge(pydot.Edge(root_id, body_id))
            return root_id

        # Compound statement -------------------------------------------
        if isinstance(ast_node, Compound):
            root_id = self._emit_node("Compound")
            for stmt in ast_node.statements:
                stmt_id = self._walk(stmt)
                self.dot_graph.add_edge(pydot.Edge(root_id, stmt_id))
            return root_id

        # Variable declaration -----------------------------------------
        if isinstance(ast_node, VarDecl):
            return self._emit_node(f"VarDecl: {ast_node.name}")

        # Assignment ----------------------------------------------------
        if isinstance(ast_node, Assignment):
            root_id = self._emit_node(f"Assign: {ast_node.name}")
            expr_id = self._walk(ast_node.expr)
            self.dot_graph.add_edge(pydot.Edge(root_id, expr_id))
            return root_id

        # If‑statement --------------------------------------------------
        if isinstance(ast_node, If):
            root_id = self._emit_node("If")
            cond_id = self._walk(ast_node.condition)
            then_id = self._walk(ast_node.then_branch)
            self.dot_graph.add_edge(pydot.Edge(root_id, cond_id, label="cond"))
            self.dot_graph.add_edge(pydot.Edge(root_id, then_id, label="then"))
            if ast_node.else_branch:
                else_id = self._walk(ast_node.else_branch)
                self.dot_graph.add_edge(pydot.Edge(root_id, else_id, label="else"))
            return root_id

        # Return --------------------------------------------------------
        if isinstance(ast_node, Return):
            root_id = self._emit_node("Return")
            expr_id = self._walk(ast_node.expr)
            self.dot_graph.add_edge(pydot.Edge(root_id, expr_id))
            return root_id

        # Binary operation ---------------------------------------------
        if isinstance(ast_node, BinOp):
            root_id = self._emit_node(f"Op: {ast_node.op}")
            left_id = self._walk(ast_node.left)
            right_id = self._walk(ast_node.right)
            self.dot_graph.add_edge(pydot.Edge(root_id, left_id))
            self.dot_graph.add_edge(pydot.Edge(root_id, right_id))
            return root_id

        # Literals / identifiers ---------------------------------------
        if isinstance(ast_node, Num):
            return self._emit_node(f"Num: {ast_node.value}")
        if isinstance(ast_node, Var):
            return self._emit_node(f"Var: {ast_node.name}")

        # Fallback (unknown node type) ---------------------------------
        return self._emit_node(type(ast_node).__name__)

    # ------------------------------------------------------------------
    #  Public driver
    # ------------------------------------------------------------------
    def render_png(self, ast_root, outfile: str = "ast_visual.png") -> None:
        """Traverse the AST and write a Graphviz PNG to *outfile*."""
        self._walk(ast_root)
        self.dot_graph.write_png(outfile)
        print(f"✅ AST diagram saved to {outfile}")
