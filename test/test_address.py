import unittest
import os

import i2plib.sam

TEST_KEY = os.path.join(os.getcwd(), 'test', 'data', 'test.dat')
TEST_DEST_B32 = "testvjtq2sfj5a6m7dwecpuxwbpwglgrma4i2iisxg2g5bnogm5a"
TEST_DEST_B64 = "Q8VZ41jSRFutjRYDbnDioTfMitFMAMINRqrgcwISQ3ObOyzjBX9Kz~OJz7ShyGqdILTxgeDYkGTpYEp4HIleUHwXUVaX8tEjEYQPYMTZr-ol-biPwokefgUtOG5MKB7d3pPN9z5j6wFaYfUhSuXq6eVkMqxE9S3MGP5D8l2ihYhvlKrL5uTW0up8GnO~o0e7SXoYRUES1TuA78GkB10qOJKEW4ow0YFr2m1I7gL7mrJu44XfvAALOmyKuJxvXxpevAeeW1TWEWONP9skUC9N3mvQsGRBCzIeZEgSlT0Vkdg8e5r8nUYAWxZmeY4U-vW2lchCb4hz4Tnuj9nWsMdj4bjnuBe51SE4G93Fw73o3w4PHL2blh0yVLGOlVzHOv6kz2TPg4dnjioI0sFTnFv4CyARPHHJtKMQi7JF6SucMSO4F2u~XdSIMnV845OIL1W52097~LqX9uW7sg-pbueB1FSUIyv4GpwZo2XKxSm6EQ5tv2tYs9LowPDQzPZhXAAUBQAEAAcAAA=="

class TestDestination(unittest.TestCase):

    def test_private_key(self):
        pk = i2plib.sam.Destination(path=TEST_KEY, has_private_key=True)
        self.assertEqual(pk.base32, TEST_DEST_B32)
        self.assertEqual(pk.base64, TEST_DEST_B64)

    def test_destination(self):
        dest = i2plib.sam.Destination(TEST_DEST_B64)
        self.assertEqual(dest.base32, TEST_DEST_B32)
