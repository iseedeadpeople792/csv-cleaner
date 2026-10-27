import unittest

from csv_cleaner import clean, norm_phone


class CleanerTest(unittest.TestCase):
    def test_phone_normalization(self):
        self.assertEqual(norm_phone("8 (999) 000-11-22"), "+79990001122")
        self.assertEqual(norm_phone("+7 999 000 11 22"), "+79990001122")
        self.assertEqual(norm_phone("9990001122"), "+79990001122")
        self.assertIsNone(norm_phone("123"))

    def test_clean_rejects_and_dedupes(self):
        rows = [
            {"name": " Анна ", "phone": "8 999 000 11 22", "email": "Anna@Mail.ru "},
            {"name": "Анна 2", "phone": "+7 999 000 11 22", "email": "other@mail.ru"},  # тот же телефон
            {"name": "Олег", "phone": "89990002233", "email": "bad-email"},  # плохой email
            {"name": "", "phone": "89990003344", "email": "x@y.ru"},  # нет имени
            {"name": "Ира", "phone": "89990004455", "email": "ira@mail.ru"},
        ]
        good, bad = clean(rows)
        self.assertEqual([g["name"] for g in good], ["Анна", "Ира"])
        self.assertEqual(good[0]["email"], "anna@mail.ru")
        self.assertEqual(len(bad), 3)


if __name__ == "__main__":
    unittest.main()
