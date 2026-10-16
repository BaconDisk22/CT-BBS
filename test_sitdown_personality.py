import unittest
from sitdown_personality import Personality

class TestPersonality(unittest.TestCase):
    def test_clean_defaults(self):
        self.assertEqual(Personality().message("welcome"), "Ayyy, pull up a chair. We gotta talk.")

    def test_desktop_uncensored_does_not_affect_public(self):
        personality = Personality(desktop_mode="uncensored", public_mode="uncensored")
        self.assertNotEqual(personality.message("welcome"), personality.message("welcome", public=True))

    def test_public_requires_explicit_opt_in(self):
        personality = Personality(public_mode="uncensored", allow_public_profanity=True)
        self.assertEqual(personality.message("welcome", public=True), personality.message("welcome", public=False) if False else "Ayyy, pull up a chair. Don't bust my balls, we gotta talk.")

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            Personality(desktop_mode="invalid")
