import unittest

from compacthdwallets.derive import *


class TestsDerive(unittest.TestCase):

    def test_derive(self):
        p = 32
        P = point_mul(G, p)
        i = 1
        p_i = CKDprv(p, i)
        P_i = CKDpub(P, i)
        self.assertEqual(point_mul(G, p_i), P_i)
