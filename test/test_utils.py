import unittest
import os

import i2plib.sam
import i2plib.utils

class TestUtils(unittest.TestCase):

    def test_session_id_generation(self):
        sid = i2plib.utils.generate_session_id()
        self.assertEqual(len(sid), 13)
        sid = i2plib.utils.generate_session_id(8)
        self.assertEqual(len(sid), 15)

    def test_sam_address_getter(self):
        oldenv = os.environ
        if "I2P_SAM_ADDRESS" in os.environ:
            del os.environ["I2P_SAM_ADDRESS"]

        a = i2plib.utils.get_sam_address()
        self.assertEqual(a, i2plib.sam.DEFAULT_ADDRESS)

        os.environ["I2P_SAM_ADDRESS"] = "127.0.0.1:11223"
        a = i2plib.utils.get_sam_address()
        self.assertEqual(a, ("127.0.0.1", 11223))
        os.environ = oldenv

    def test_port_utils(self):
        p = i2plib.utils.get_free_port()
        unavail_address = ("127.0.0.1", p)
        self.assertFalse(i2plib.utils.is_address_accessible(unavail_address))

