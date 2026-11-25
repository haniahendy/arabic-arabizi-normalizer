# arabic-arabizi-normalizer

Preprocessing utilities for Egyptian Arabic social text and Arabizi
("Franco-Arabic": Arabic written in Latin letters and digits, e.g.
`ana 3ayez akol`). Built for the messy reality of Egyptian chat data:
mixed scripts, Arabizi digits, decorative tatweel, and optional tashkeel.

Pure Python 3.10+, zero dependencies.

## What it does

| Function | Input | Output |
|----------|-------|--------|
| `normalize("أحمد إيمان آيات")` | MSA/Egyptian Arabic | `احمد ايمان ايات` |
| `looks_like_arabizi("7abibi ta3ala")` | any text | `True` |
| `ArabiziDecoder().decode("ana msh 3aref")` | Arabizi | `أنا مش عاريف` (heuristic, see limits) |
| `dominant_script(...)` | any text | `arabic` / `arabizi` / `latin` / `mixed` / `empty` |
| `script_profile(...)` | any text | per-script character shares |

## Examples

```python
from arabizi_norm import normalize, ArabiziDecoder, dominant_script

normalize("السَّلَامُ عَلَيْكُمْ يا صاحبى، الساعة ٧")
# 'السلام عليكم يا صاحبي, الساعة 7'  (ya folded, diacritics stripped, Eastern digit mapped; taa marbuta kept by default)

ArabiziDecoder().decode("shokran ya 7abibi, kolo tamam")
# 'شكرا يا حابيبي, كولو تمام'  (heuristic: the decoder adds a vowel letter here; not a transcription)

dominant_script("ana 3ayez amshy")   # 'arabizi'
dominant_script("أنا بحب python")     # 'arabic' or 'mixed' depending on share
```

`ArabicNormalizer` options: `fold_alef`, `fold_ya`, `fold_taa_marbuta`
(default False, it changes morphology), `strip_diacritics`, `strip_tatweel`,
`eastern_digits` (٠١٢٣→0123).

## Honest limits

- Arabizi decoding is **heuristic**, not transcription. Digits are
  ambiguous (`3` = ع inside words, but a literal 3 in "3 books"), and one
  Arabizi spelling can map to several Arabic words. A small high-frequency
  Egyptian lexicon takes precedence over the greedy pattern pass, but
  out-of-lexicon words are decoded mechanically. Use the output as a model
  feature, never as display text.
- No vowel restoration: Arabizi carries no short-vowel information.
- `looks_like_arabizi` errs conservative: plain English with digits
  adjacent to letters ("b2b sales") can score positive.
- Normalization is lossy by design (search/index orientation); keep the
  original text alongside.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

24 tests covering folding options, diacritics/tatweel stripping, digit
mapping, digraph greediness, lexicon precedence, detection false-positive
guards, and script profiling.
