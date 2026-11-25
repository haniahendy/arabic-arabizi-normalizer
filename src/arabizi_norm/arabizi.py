"""Arabizi (Franco-Arabic) detection and heuristic decoding.

Arabizi writes Arabic with Latin letters and digits: 3 for ع, 7 for ح,
5 for خ, 2 for hamza. Decoding is genuinely ambiguous (e.g. "3" can be ع
inside a word but a literal 3 in "3 books"), so the decoder checks a small high-frequency
lexicon first and otherwise decodes greedily over multi-char patterns.
Treat output as a feature for downstream models, not ground truth.
"""

from __future__ import annotations

import re

# Longest-first so greedy matching wins for digraphs.
_PATTERNS = [
    ("sh", "ش"), ("kh", "خ"), ("gh", "غ"), ("th", "ث"), ("ch", "تش"),
    ("aa", "ا"), ("ee", "ي"), ("oo", "و"),
    ("a", "ا"), ("b", "ب"), ("t", "ت"), ("g", "ج"), ("j", "ج"),
    ("d", "د"), ("r", "ر"), ("z", "ز"), ("s", "س"), ("f", "ف"),
    ("q", "ق"), ("k", "ك"), ("l", "ل"), ("m", "م"), ("n", "ن"),
    ("h", "ه"), ("w", "و"), ("y", "ي"), ("e", "ي"), ("o", "و"),
    ("u", "و"), ("i", "ي"), ("c", "ك"), ("v", "ف"), ("p", "ب"),
    ("x", "كس"), ("'", "ء"),
]
_DIGIT_MAP = {"2": "ء", "3": "ع", "5": "خ", "6": "ط", "7": "ح", "8": "غ"}

_LEXICON = {
    "msh": "مش", "wala": "ولا", "w": "و", "ya": "يا", "ana": "أنا",
    "enta": "أنت", "enti": "أنتِ", "eh": "إيه", "fe": "في", "mn": "من",
    "3la": "على",
    "kda": "كده", "kwayes": "كويس", "tamam": "تمام", "shokran": "شكرا",
    "yarb": "يارب", "habibi": "حبيبي", "bukra": "بكرا", "delwa2ty": "دلوقتي",
}

_DIGIT_RE = re.compile(r"[a-zA-Z]+[235678][a-zA-Z0-9']*|[235678][a-zA-Z]+")
_LATIN_RE = re.compile(r"[a-zA-Z]")
_ARABIC_RE = re.compile(r"[؀-ۿ]")


def looks_like_arabizi(text: str) -> bool:
    """Heuristic: Latin text that uses Arabizi digits (2/3/5/6/7/8 inside
    or next to letters) and contains no Arabic script."""
    if _ARABIC_RE.search(text):
        return False
    return bool(_DIGIT_RE.search(text))


class ArabiziDecoder:
    def __init__(self, lexicon: dict | None = None) -> None:
        self.lexicon = dict(_LEXICON if lexicon is None else lexicon)
        pats = [(k.lower(), v) for k, v in _PATTERNS]
        pats.sort(key=lambda kv: -len(kv[0]))
        self._patterns = pats

    def decode_token(self, token: str) -> str:
        low = token.lower()
        if low in self.lexicon:
            return self.lexicon[low]
        out, i = [], 0
        while i < len(low):
            ch = low[i]
            if ch in _DIGIT_MAP:
                out.append(_DIGIT_MAP[ch])
                i += 1
                continue
            for pat, rep in self._patterns:
                if low.startswith(pat, i):
                    out.append(rep)
                    i += len(pat)
                    break
            else:
                out.append(ch)  # keep unknown char (numbers, punctuation)
                i += 1
        return "".join(out)

    def decode(self, text: str) -> str:
        """Decode each whitespace-separated token; non-Latin tokens pass through."""
        parts = []
        for tok in text.split(" "):
            if _LATIN_RE.search(tok) or any(d in tok for d in _DIGIT_MAP):
                parts.append(self.decode_token(tok))
            else:
                parts.append(tok)
        return " ".join(parts)
