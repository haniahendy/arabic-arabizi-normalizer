import unittest

from arabizi_norm import ArabicNormalizer, normalize


class TestArabicNormalizer(unittest.TestCase):
    def test_alef_folding(self):
        self.assertEqual(normalize("أحمد إيمان آيات"), "احمد ايمان ايات")

    def test_alef_folding_disabled(self):
        n = ArabicNormalizer(fold_alef=False)
        self.assertEqual(n.normalize("أحمد"), "أحمد")

    def test_ya_folding(self):
        self.assertEqual(normalize("على فكرى"), "علي فكري")

    def test_taa_marbuta_opt_in(self):
        self.assertEqual(ArabicNormalizer(fold_taa_marbuta=True).normalize("مدرسة جميلة"), "مدرسه جميله")
        self.assertEqual(normalize("مدرسة"), "مدرسة")  # default keeps taa marbuta

    def test_diacritics_removed(self):
        self.assertEqual(normalize("السَّلَامُ عَلَيْكُمْ"), "السلام عليكم")

    def test_tatweel_removed(self):
        self.assertEqual(normalize("مبرووووكـــ"), "مبرووووك")

    def test_eastern_digits(self):
        self.assertEqual(normalize("الساعة ٧ ونص"), "الساعة 7 ونص")

    def test_punctuation_mapped(self):
        self.assertEqual(normalize("إزيك، يا صاحبي؟"), "ازيك, يا صاحبي?")

    def test_whitespace_collapsed(self):
        self.assertEqual(normalize("  أهلا    بالعالم  "), "اهلا بالعالم")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            normalize(123)


if __name__ == "__main__":
    unittest.main()
