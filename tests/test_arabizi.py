import unittest

from arabizi_norm import ArabiziDecoder, looks_like_arabizi
from arabizi_norm.language import dominant_script, script_profile


class TestDetection(unittest.TestCase):
    def test_arabizi_detected(self):
        self.assertTrue(looks_like_arabizi("ana 3ayez akol"))
        self.assertTrue(looks_like_arabizi("7abibi ta3ala"))

    def test_plain_english_not_arabizi(self):
        self.assertFalse(looks_like_arabizi("see you tomorrow at 7"))
        # digits not adjacent to letters -> not arabizi pattern
        self.assertFalse(looks_like_arabizi("call me on 12345"))

    def test_arabic_script_not_arabizi(self):
        self.assertFalse(looks_like_arabizi("أنا عايز 3"))


class TestDecoder(unittest.TestCase):
    def setUp(self):
        self.d = ArabiziDecoder()

    def test_digits(self):
        self.assertEqual(self.d.decode_token("3amr"), "عامر")
        self.assertEqual(self.d.decode_token("7aga"), "حاجا")

    def test_digraphs(self):
        self.assertEqual(self.d.decode_token("shams"), "شامس")
        self.assertEqual(self.d.decode_token("khobz"), "خوبز")
        # lexicon wins over pattern decode for known words
        self.assertEqual(self.d.decode_token("shokran"), "شكرا")

    def test_lexicon_hit(self):
        self.assertEqual(self.d.decode_token("kwayes"), "كويس")
        self.assertEqual(self.d.decode_token("tamam"), "تمام")

    def test_sentence_passthrough(self):
        out = self.d.decode("ana msh 3aref, بجد")
        self.assertIn("مش", out)
        self.assertIn("بجد", out)

    def test_unknown_chars_kept(self):
        self.assertIn("9", self.d.decode_token("a9"))


class TestScriptProfile(unittest.TestCase):
    def test_arabic_dominant(self):
        self.assertEqual(dominant_script("أنا بحب القراية جدا"), "arabic")

    def test_arabizi_dominant(self):
        self.assertEqual(dominant_script("ana 3ayez amshy delwa2ty"), "arabizi")

    def test_latin(self):
        self.assertEqual(dominant_script("hello world"), "latin")

    def test_mixed(self):
        self.assertEqual(dominant_script("أنا بحب python وبستخدمه كل يوم"), "mixed")

    def test_empty(self):
        self.assertEqual(dominant_script("   "), "empty")

    def test_profile_sums_to_one(self):
        prof = script_profile("abc ديف 123 !")
        self.assertAlmostEqual(sum(prof.values()), 1.0, places=3)


if __name__ == "__main__":
    unittest.main()
