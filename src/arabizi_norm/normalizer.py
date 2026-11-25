"""Normalization for Modern Standard and Egyptian Arabic text.

Design notes:
- NFC compose first so combining marks are predictable.
- Alef variants (hamza above/below, madda) fold to bare alef by default;
  this is standard for search/indexing, not for display.
- Diacritics (tashkeel) and tatweel are removed by default: both are rare
  in social text and inflate token sparsity.
"""

from __future__ import annotations

import re
import unicodedata

_DIACRITICS = re.compile(r"[ً-ْٰ]")
_TATWEEL = "ـ"
_EASTERN_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
_ALEF_FORMS = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا"}
_PUNCT_MAP = str.maketrans({"،": ",", "؛": ";", "؟": "?", "«": '"', "»": '"',
                            "‐": "-", "‑": "-", "–": "-", "—": "-"})


class ArabicNormalizer:
    """Configurable Arabic normalizer.

    fold_alef / fold_ya / fold_taa_marbuta mirror common IR practice.
    Set any of them False to keep the original orthography.
    """

    def __init__(
        self,
        fold_alef: bool = True,
        fold_ya: bool = True,
        fold_taa_marbuta: bool = False,
        strip_diacritics: bool = True,
        strip_tatweel: bool = True,
        eastern_digits: bool = True,
    ) -> None:
        self.fold_alef = fold_alef
        self.fold_ya = fold_ya
        self.fold_taa_marbuta = fold_taa_marbuta
        self.strip_diacritics = strip_diacritics
        self.strip_tatweel = strip_tatweel
        self.eastern_digits = eastern_digits

    def normalize(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("normalize() expects str")
        out = unicodedata.normalize("NFC", text)
        if self.strip_diacritics:
            out = _DIACRITICS.sub("", out)
        if self.strip_tatweel:
            out = out.replace(_TATWEEL, "")
        if self.fold_alef:
            for src, dst in _ALEF_FORMS.items():
                out = out.replace(src, dst)
        if self.fold_ya:
            out = out.replace("ى", "ي")
        if self.fold_taa_marbuta:
            out = out.replace("ة", "ه")
        if self.eastern_digits:
            out = out.translate(_EASTERN_DIGITS)
        out = out.translate(_PUNCT_MAP)
        out = re.sub(r"\s+", " ", out).strip()
        return out


def normalize(text: str, **kwargs) -> str:
    """One-shot normalization with default settings."""
    return ArabicNormalizer(**kwargs).normalize(text)
