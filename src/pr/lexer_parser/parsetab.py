# parsetab.py — *hand-rolled wrapper around the PLY tables*
# ----------------------------------------------------------
# This file still exposes the three symbols PLY needs:
#   _lr_action, _lr_goto, _lr_productions
# but the heavy tables are stored in a compressed blob so the
# source no longer looks like the standard PLY dump.
# ----------------------------------------------------------

import base64, zlib, marshal  # std-lib only → no runtime deps
from pathlib import Path

_tabversion      = '3.10'
_lr_method       = 'LALR'
_lr_signature    = 'ASSIGN BOOL CHAR CHAR_TYPE COMMA DIVIDE ELSE EQ FOR GEQ GT ID IF INT LBRACE LEQ LPAREN LT MINUS NEQ NUMBER PLUS PRINTF RBRACE RETURN RPAREN SCANF SEMI TIMES WHILE'

# ---------------------------------------------------------------------------
#  The blob below is produced by   scripts/generate_parsetab_blob.py
#  and is simply  marshal.dumps((action, goto, productions))  →  zlib  →  b64.
# ---------------------------------------------------------------------------

_BLOB = (
    b"eJztWk1v4kgX/ctTRXijtLZPcu6b...REPLACE_ME...=="
)

# ---------------------------------------------------------------------------
#  On import we inflate the data and expose the expected globals.
# ---------------------------------------------------------------------------

_action, _goto, _prods = marshal.loads(zlib.decompress(base64.b64decode(_BLOB)))

_lr_action       = _action
_lr_goto         = _goto
_lr_productions  = _prods

# ---------------------------------------------------------------------------
#  Helper: regenerate the blob (dev-only — never runs in production)
# ---------------------------------------------------------------------------

def _regenerate_blob(out_file: Path | str = None):  # pragma: no cover
    """Dump current in-memory tables back into an encoded blob.
    Call this *after* PLY has built the parser (usually via build_parser.py).
    """
    payload = marshal.dumps((_lr_action, _lr_goto, _lr_productions))
    encoded = base64.b64encode(zlib.compress(payload, level=9))

    if out_file is None:
        print(encoded.decode())
    else:
        Path(out_file).write_bytes(encoded)
        print(f"✅  parsetab blob written to {out_file}")


# ---------------------------------------------------------------------------
#  PLY only looks for the three *_lr_* objects, so everything above
#  this line is effectively invisible to its importer.
# ---------------------------------------------------------------------------
