import unittest
from packy_personality import Personality

class TestPersonality(unittest.TestCase):
    def test_clean_defaults(self):
        self.assertEqual(Personality().message("welcome"), "Come on in. Take a left where the old Ames used to be.")

    def test_desktop_uncensored_does_not_affect_public(self):
        personality = Personality(desktop_mode="uncensored", public_mode="uncensored")
        self.assertNotEqual(personality.message("welcome"), personality.message("welcome", public=True))

    def test_public_requires_explicit_opt_in(self):
        personality = Personality(public_mode="uncensored", allow_public_profanity=True)
        self.assertEqual(personality.message("welcome", public=True), "Come on in. Take a left where the old Ames used to be, and don't give me that New York crap.")

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            Personality(desktop_mode="invalid")
