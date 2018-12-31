import unittest
import os

import i2plib.sam
import i2plib.utils

class TestSAM(unittest.TestCase):

    def test_sam_message(self):
        text = "COMMAND SUBCOMMAND NAME=VALUE NAME2=VALUE\n"
        m = i2plib.sam.Message(text)
        self.assertEqual(m.cmd, "COMMAND")
        self.assertEqual(str(m), text)

        m = i2plib.sam.Message(text.encode())
        self.assertEqual(m["NAME"], "VALUE")

