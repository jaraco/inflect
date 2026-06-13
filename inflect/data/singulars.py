"""
Derived singular data: si_sb_irregular maps and other singular-specific
word lists that are derived from plural data or defined independently.
"""

from __future__ import annotations

from .._shared import bysize


# DERIVED IRREGULAR SINGULARS (from plurals.py pl_sb_irregular*)

def _build_si_sb_irregular(pl_sb_irregular):
    result = {v: k for (k, v) in pl_sb_irregular.items()}
    for k in list(result):
        if "|" in k:
            k1, k2 = k.split("|")
            result[k1] = result[k2] = result[k]
            del result[k]
    return result


def _build_si_sb_irregular_compound(pl_sb_irregular_compound):
    result = {v: k for (k, v) in pl_sb_irregular_compound.items()}
    for k in list(result):
        if "|" in k:
            k1, k2 = k.split("|")
            result[k1] = result[k2] = result[k]
            del result[k]
    return result


# These are populated lazily to avoid circular imports at module load time.
# See _init() below.

si_sb_irregular = None
si_sb_irregular_caps = None
si_sb_irregular_compound = None


def _init():
    """
    Initialize the derived singular data from plural data.
    Called from data/__init__.py after all data modules are loaded.
    """
    global si_sb_irregular, si_sb_irregular_caps, si_sb_irregular_compound

    from .plurals import pl_sb_irregular, pl_sb_irregular_caps, pl_sb_irregular_compound

    si_sb_irregular = _build_si_sb_irregular(pl_sb_irregular)
    si_sb_irregular_caps = {v: k for (k, v) in pl_sb_irregular_caps.items()}
    si_sb_irregular_compound = _build_si_sb_irregular_compound(pl_sb_irregular_compound)
