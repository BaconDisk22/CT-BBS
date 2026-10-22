import unittest

from packy_commands import resolve_shortcut


class PackyCommandsTest(unittest.TestCase):
    def test_aliases_ignore_case_and_spaces(self):
        self.assertEqual(resolve_shortcut(" /PaCkY "), "x")
        self.assertEqual(resolve_shortcut("/MAIL"), "cm")
        self.assertEqual(resolve_shortcut("/towngreen"), "b")
        self.assertEqual(resolve_shortcut("/Grinder"), "q")
        self.assertEqual(resolve_shortcut("/nutmeg"), "f")

    def test_normal_message_is_unchanged(self):
        self.assertIsNone(resolve_shortcut("Apizza at Pepe's or Sally's?"))
        self.assertIsNone(resolve_shortcut("sm,,recipient,subject,hello"))
        self.assertIsNone(resolve_shortcut("/unknown"))

    def test_do_not_override_text_entry(self):
        state = {"command": "BULLETIN_POST_CONTENT"}
        self.assertIsNone(resolve_shortcut("/fortune", state))
        self.assertEqual(resolve_shortcut("/cancel", state), "x")


if __name__ == "__main__":
    unittest.main()
