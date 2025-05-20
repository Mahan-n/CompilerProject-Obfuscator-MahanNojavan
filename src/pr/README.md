# Mini-C Obfuscator

*A pedagogical compiler front-end + source-to-source obfuscator (pure Python)*

<div align="center">
<img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python"/>
<img src="https://img.shields.io/badge/License-MIT-brightgreen"/>
<img src="https://img.shields.io/badge/Project Phase-I (%F0%9F%93%8D)-orange"/>
</div>

> 📚 Semester project &nbsp;•&nbsp; **Compiler Design (1403-2)**  
> دانشگاه …

---

## Motivation & Goals
“Real” optimising compilers are huge; for learning (or CTF challenges) we
can get a lot of bang from a small *obfuscator*:

* Parse a subset of C → build an **AST**
* Apply **passes** that scramble identifiers, inject junk, flatten control flow …
* Re-emit valid C that compiles cleanly—but is painful to read

The code is split so every phase of a compiler pipeline is visible and hackable.

---

## Quick Demo

```console
$ python -m mini_c_obfuscator \
    examples/fibonacci.mc  build/fibonacci_obf.c \
    --rename-vars --insert-opaque --remove-dead-code --flatten

[✓]  Parsed                         0.05 s
[✓]  4 passes applied               0.02 s
[✓]  Emitted C   ▲ +63 % size       0.01 s   → build/fibonacci_obf.c





.
├─ lexer_parser/
│  ├─ lexer_refactored.py    # tokeniser
│  ├─ parser_refactored.py   # grammar rules
│  ├─ parsetab.py            # compressed LALR tables
│  └─ ast_nodes.py
├─ obfuscation_passes/
│  ├─ base_pass.py
│  ├─ rename_variables_refactored.py
│  ├─ dead_code_inserter_refactored.py
│  ├─ insert_opaque_predicates_refactored.py
│  └─ control_flow_flatten_refactored.py
├─ codegen_alt.py            # MiniCEmitter
├─ cli_options.py            # fast arg parser
├─ syntax_tree_visualizer.py # Graphviz helper
├─ tests/                    # PyTest suite
└─ README.md








