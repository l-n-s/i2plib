import unittest
import os

import i2plib.sam
import i2plib.utils

TEST_KEY = os.path.join(os.getcwd(), 'test', 'data', 'test.dat')
TEST_DEST_B32 = "testvjtq2sfj5a6m7dwecpuxwbpwglgrma4i2iisxg2g5bnogm5a"
TEST_DEST_B64 = "Q8VZ41jSRFutjRYDbnDioTfMitFMAMINRqrgcwISQ3ObOyzjBX9Kz~OJz7ShyGqdILTxgeDYkGTpYEp4HIleUHwXUVaX8tEjEYQPYMTZr-ol-biPwokefgUtOG5MKB7d3pPN9z5j6wFaYfUhSuXq6eVkMqxE9S3MGP5D8l2ihYhvlKrL5uTW0up8GnO~o0e7SXoYRUES1TuA78GkB10qOJKEW4ow0YFr2m1I7gL7mrJu44XfvAALOmyKuJxvXxpevAeeW1TWEWONP9skUC9N3mvQsGRBCzIeZEgSlT0Vkdg8e5r8nUYAWxZmeY4U-vW2lchCb4hz4Tnuj9nWsMdj4bjnuBe51SE4G93Fw73o3w4PHL2blh0yVLGOlVzHOv6kz2TPg4dnjioI0sFTnFv4CyARPHHJtKMQi7JF6SucMSO4F2u~XdSIMnV845OIL1W52097~LqX9uW7sg-pbueB1FSUIyv4GpwZo2XKxSm6EQ5tv2tYs9LowPDQzPZhXAAUBQAEAAcAAA=="

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

