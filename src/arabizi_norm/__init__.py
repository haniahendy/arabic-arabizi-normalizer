"""Egyptian Arabic + Arabizi text normalization utilities."""

from .normalizer import ArabicNormalizer, normalize
from .arabizi import ArabiziDecoder, looks_like_arabizi
from .language import script_profile, dominant_script

__all__ = [
    "ArabicNormalizer",
    "normalize",
    "ArabiziDecoder",
    "looks_like_arabizi",
    "script_profile",
    "dominant_script",
]

__version__ = "0.1.0"
