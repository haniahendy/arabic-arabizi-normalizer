"""Lightweight script profiling for mixed Arabic/Latin/Arabizi text."""

from __future__ import annotations

import re

_ARABIC = re.compile(r"[؀-ۿ]")
_LATIN = re.compile(r"[a-zA-Z]")
_ARABIZI_DIGITS = re.compile(r"[235678]")


def script_profile(text: str) -> dict:
    """Return character-share profile: arabic / latin / digits / other.

    Shares are fractions of letters+digits only (whitespace excluded).
    """
    counts = {"arabic": 0, "latin": 0, "digit": 0, "other": 0}
    for ch in text:
        if ch.isspace():
            continue
        if _ARABIC.match(ch):
            counts["arabic"] += 1
        elif _LATIN.match(ch):
            counts["latin"] += 1
        elif ch.isdigit():
            counts["digit"] += 1
        else:
            counts["other"] += 1
    total = sum(counts.values()) or 1
    return {k: round(v / total, 4) for k, v in counts.items()}


def dominant_script(text: str) -> str:
    """One of: 'arabic', 'arabizi', 'latin', 'mixed', 'empty'."""
    prof = script_profile(text)
    if prof["arabic"] + prof["latin"] + prof["digit"] == 0:
        return "empty"
    if prof["arabic"] >= 0.8:
        return "arabic"
    if prof["latin"] + prof["digit"] >= 0.8:
        if prof["digit"] > 0 and _ARABIZI_DIGITS.search(text):
            return "arabizi"
        return "latin"
    return "mixed"
