"""
mc_ast.py
----------
۱) تعریف کلاس‌های درخت نحوی (AST) برای Mini-C
۲) Visitor پایه + Pass «RenameIdentifiers»
۳) تابع from_tuple برای تبدیل خروجی تاپلِ parser به این کلاس‌ها
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Union, Optional, Any
import itertools

# --------------------------------------------------
#   پایه‌ی درخت و بازدیدکننده
# --------------------------------------------------
class Node:
    def accept(self, visitor: "NodeVisitor"):
        method = getattr(visitor, "visit_" + self.__class__.__name__,
                         visitor.generic_visit)
        return method(self)

class NodeVisitor:
    def generic_visit(self, node: Node):
        for value in vars(node).values():
            if isinstance(value, Node):
                value.accept(self)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Node):
                        item.accept(self)

# --------------------------------------------------
#   کلاس‌های AST
# --------------------------------------------------
@dataclass
class Program(Node):
    body: List[Node]

@dataclass
class Declaration(Node):
    vartype: str   # 'int' یا 'char'
    name: str

@dataclass
class Identifier(Node):
    name: str

@dataclass
class Literal(Node):
    value: Union[int, str]   # عدد یا رشتهٔ "%d"

@dataclass
class Assign(Node):
    target: Identifier
    value: Node              # Literal یا Identifier یا BinOp

@dataclass
class BinOp(Node):
    op: str
    left: Node
    right: Node

@dataclass
class Call(Node):
    func: str
    args: List[Node]

@dataclass
class Block(Node):
    statements: List[Node]

@dataclass
class If(Node):
    test: Node
    consequent: Block
    alternate: Optional[Block] = None

@dataclass
class While(Node):
    test: Node
    body: Block

@dataclass
class Return(Node):
    value: Node

# --------------------------------------------------
#   Pass: تغییر نام متغیرها / توابع
# --------------------------------------------------
class RenameIdentifiers(NodeVisitor):
    """
    همهٔ شناسه‌های کاربر را به var1, var2, … تغییر می‌دهد.
    """
    def __init__(self):
        self.counter = itertools.count(1)
        self.map: Dict[str, str] = {}
        self.reserved = {
            'int', 'char', 'if', 'else', 'while', 'for', 'return',
            'printf', 'scanf'
        }

    # تولید نام تازه
    def _fresh(self):
        return f"var{next(self.counter)}"

    # Visitor متناسب با هر کلاس
    def visit_Program(self, n: Program):
        for s in n.body:
            s.accept(self)

    def visit_Declaration(self, n: Declaration):
        if n.name not in self.reserved:
            n.name = self.map.setdefault(n.name, self._fresh())

    def visit_Assign(self, n: Assign):
        n.target.accept(self)
        n.value.accept(self)

    def visit_Identifier(self, n: Identifier):
        if n.name not in self.reserved:
            n.name = self.map.setdefault(n.name, self._fresh())

    def visit_BinOp(self, n: BinOp):
        n.left.accept(self)
        n.right.accept(self)

    def visit_Call(self, n: Call):
        if n.func not in self.reserved:
            n.func = self.map.setdefault(n.func, self._fresh())
        for a in n.args:
            a.accept(self)

    def visit_Block(self, n: Block):
        for s in n.statements:
            s.accept(self)

    def visit_If(self, n: If):
        n.test.accept(self)
        n.consequent.accept(self)
        if n.alternate:
            n.alternate.accept(self)

    def visit_While(self, n: While):
        n.test.accept(self)
        n.body.accept(self)

    def visit_Return(self, n: Return):
        n.value.accept(self)

# --------------------------------------------------
#   تبدیل خروجی تاپلِ parser به این کلاس‌ها
# --------------------------------------------------
def from_tuple(t: Any) -> Node:
    """
    تبدیل تاپلِ parser به گره‌های شیئی.
    ابتدا عدد و رشته را چک می‌کنیم تا خطای
    'int' object is not subscriptable رفع شود.
    """
    # ----- حالت‌های ساده (برگ) -----
    if isinstance(t, int):
        return Literal(t)

    if isinstance(t, str):
        if t.startswith('"'):          # رشته‌ی "%d"
            return Literal(t)
        return Identifier(t)           # نام متغیر یا تابع

    # ------------------------------
    tag = t[0]

    if tag == 'program':
        return Program([from_tuple(x) for x in t[1]])

    if tag == 'declaration':
        _, typ, name = t
        return Declaration(typ, name)

    if tag == 'assign':
        _, tgt, val = t
        return Assign(Identifier(tgt), from_tuple(val))

    if tag == 'binop':
        _, op, left, right = t
        return BinOp(op, from_tuple(left), from_tuple(right))

    if tag == 'block':
        _, lst = t
        return Block([from_tuple(s) for s in lst])

    if tag == 'call':
        _, func, args = t
        return Call(func, [from_tuple(a) for a in args])

    if tag == 'if':
        _, cond, blk = t
        return If(from_tuple(cond), from_tuple(blk))

    # (می‌توان while و return را در صورت اضافه‌شدن گرامر، اینجا هندل کرد)

    raise ValueError(f"Unhandled tuple form: {t}")

# --------------------------------------------------
#   تست سریع: اجرا با `python mc_ast.py`
# --------------------------------------------------
if __name__ == "__main__":
    # نمونه تاپل ساده
    sample = (
        'program', [
            ('declaration', 'int', 'x'),
            ('assign', 'x', 5),
            ('call', 'printf', ['"%d"', 'x'])
        ]
    )

    root = from_tuple(sample)
    print("قبل از Obfuscation:", root)

    RenameIdentifiers().visit_Program(root)
    print("بعد از Obfuscation :", root)
