"""
obfuscator.py  –  خط لولهٔ سادهٔ مبهم‌سازی Mini-C
==================================================
ورودی  : input.mc
خروجی  : output.mc (نام متغیرها به var1, var2, … تغییر کرده)

اجرا:
    # از داخل پوشهٔ src
    python obfuscator.py input.mc output.mc

اگر نام فایل‌ها را ندهید، به طور پیش‌فرض «input.mc» و «output.mc»
کنار همین اسکریپت استفاده می‌شود.
"""

from __future__ import annotations
import sys, os

# --------------------------------------------------
# ۱) اطمینان path
# --------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# --------------------------------------------------
# ۲) وارد کردن ماژول‌ها
# --------------------------------------------------
from parser import parser  # ← فایل گرامرِ تاپل
from mc_ast import (from_tuple, RenameIdentifiers, NodeVisitor,
                    Program, Declaration, Identifier, Literal,
                    Assign, BinOp, Call, Block, If, While, Return)

# --------------------------------------------------
# ۳) CodeGenerator  (AST → متن Mini-C)
# --------------------------------------------------
class CodeGenerator(NodeVisitor):
    def __init__(self):
        self.lines: list[str] = []
        self.ind = 0

    def emit(self, txt: str):
        self.lines.append("    " * self.ind + txt)

    def result(self) -> str:
        return "\n".join(self.lines)

    # ---------- visitor methods ----------
    def visit_Program(self, n: Program):
        for s in n.body:
            s.accept(self)

    def visit_Declaration(self, n: Declaration):
        self.emit(f"{n.vartype} {n.name};")

    def visit_Identifier(self, n: Identifier):
        return n.name

    def visit_Literal(self, n: Literal):
        return str(n.value)

    def visit_Assign(self, n: Assign):
        self.emit(f"{n.target.accept(self)} = {n.value.accept(self)};")

    def visit_BinOp(self, n: BinOp):
        return f"{n.left.accept(self)} {n.op} {n.right.accept(self)}"

    def visit_Call(self, n: Call):
        args = ", ".join(a.accept(self) for a in n.args)
        self.emit(f"{n.func}({args});")

    def visit_Block(self, n: Block):
        self.emit("{")
        self.ind += 1
        for s in n.statements:
            s.accept(self)
        self.ind -= 1
        self.emit("}")

    def visit_If(self, n: If):
        self.emit(f"if ({n.test.accept(self)})")
        n.consequent.accept(self)
        if n.alternate:
            self.emit("else")
            n.alternate.accept(self)

    def visit_While(self, n: While):
        self.emit(f"while ({n.test.accept(self)})")
        n.body.accept(self)

    def visit_Return(self, n: Return):
        self.emit(f"return {n.value.accept(self)};")

# --------------------------------------------------
# ۴) خط لولهٔ مبهم‌سازی
# --------------------------------------------------
def obfuscate(code: str) -> str:
    tuple_ast = parser.parse(code)          # 1) تاپل AST
    root      = from_tuple(tuple_ast)       # 2) تبدیل به شیء-AST
    RenameIdentifiers().visit_Program(root) # 3) تغییر نام‌ها
    gen = CodeGenerator(); root.accept(gen) # 4) تولید متن
    return gen.result()

# --------------------------------------------------
# ۵) CLI
# --------------------------------------------------
if __name__ == "__main__":
    # آرگومان‌های پیش‌فرض
    in_file  = sys.argv[1] if len(sys.argv) >= 2 else "input.mc"
    out_file = sys.argv[2] if len(sys.argv) >= 3 else "output.mc"

    in_file  = os.path.join(SCRIPT_DIR, in_file)  if not os.path.isabs(in_file)  else in_file
    out_file = os.path.join(SCRIPT_DIR, out_file) if not os.path.isabs(out_file) else out_file

    if not os.path.exists(in_file):
        print(f"❌ فایل ورودی '{in_file}' پیدا نشد.")
        sys.exit(1)

    src = open(in_file, "r", encoding="utf-8").read()
    obf = obfuscate(src)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(obf)

    print(f"✅ خروجی مبهم‌شده در '{out_file}' ذخیره شد.")
