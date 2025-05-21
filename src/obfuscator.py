"""
obfuscator.py — نسخهٔ پایدار (self‑contained)
================================================
این اسکریپت را داخل همان پوشه‌ای بگذارید که `lexer.py`, `parser.py`, و
`mc_ast.py` قرار دارند (پوشۀ `src/`).

اجرا:
    python obfuscator.py input.mc output.mc
اگر آرگومان ندهید به‌طور پیش‌فرض «input.mc» و «output.mc» در همان پوشه را
استفاده می‌کند.
"""
from __future__ import annotations
import sys, os, importlib.util

# --------------------------------------------------
# ۱) اطمینان از وجود پوشهٔ اسکریپت در sys.path
# --------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# --------------------------------------------------
# ۲) وارد کردن ماژول‌های محلی
# --------------------------------------------------
try:
    from parser import parser  # فایل گرامر تاپل
except ModuleNotFoundError as e:
    print("❌ parser.py در همین پوشه پیدا نشد!", file=sys.stderr)
    raise

try:
    from mc_ast import (from_tuple, RenameIdentifiers, NodeVisitor,
                        Program, Declaration, Identifier, Literal,
                        Assign, BinOp, Call, Block, If, While, Return)
except ModuleNotFoundError as e:
    print("❌ mc_ast.py در همین پوشه پیدا نشد!", file=sys.stderr)
    raise

# --------------------------------------------------
# ۳) Code‑Generator — AST ➜ متن Mini‑C
# --------------------------------------------------
class CodeGenerator(NodeVisitor):
    def __init__(self):
        self.lines: list[str] = []
        self.ind = 0

    def emit(self, txt: str):
        self.lines.append("    " * self.ind + txt)

    def result(self) -> str:
        return "\n".join(self.lines)

    # ---------- Visitor methods ----------
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
        arg_str = ", ".join(a.accept(self) for a in n.args)
        self.emit(f"{n.func}({arg_str});")

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
    tuple_ast = parser.parse(code)
    root      = from_tuple(tuple_ast)
    RenameIdentifiers().visit_Program(root)
    gen = CodeGenerator(); root.accept(gen)
    return gen.result()

# --------------------------------------------------
# ۵) CLI
# --------------------------------------------------
if __name__ == "__main__":
    # آرگومان‌های پیش‌فرض اگر چیزی داده نشود
    in_path  = sys.argv[1] if len(sys.argv) >= 2 else "input.mc"
    out_path = sys.argv[2] if len(sys.argv) >= 3 else "output.mc"

    in_path  = os.path.join(SCRIPT_DIR, in_path)  if not os.path.isabs(in_path)  else in_path
    out_path = os.path.join(SCRIPT_DIR, out_path) if not os.path.isabs(out_path) else out_path

    if not os.path.exists(in_path):
        print(f"❌ ورودی '{in_path}' پیدا نشد.")
        sys.exit(1)

    code = open(in_path, "r", encoding="utf-8").read()
    obf  = obfuscate(code)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(obf)

    print(f"✅ خروجی مبهم‌شده در '{out_path}' ذخیره شد.")
