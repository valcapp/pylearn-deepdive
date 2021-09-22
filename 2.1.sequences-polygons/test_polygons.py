import unittest

import math
from polygon import Polygon
from polygons import Polygons

class TestPolygons(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(ValueError):
            Polygons(2,1)

    def test_repr(self):
        self.assertEqual(
            str(Polygons(3,2)),
            "Polygons(3,2)"
        )
    
    def test_max_edges(self):
        self.assertEqual(
            Polygons(5,4).max_edges,
            5
        )
        plygs5 = Polygons(5,4)
        self.assertEqual(
            max( plyg.edges for plyg in plygs5),
            5
        )

    def test_circumradius(self):
        self.assertEqual(
            Polygons(10,5).circumradius,
            5
        )

    def test_eq(self):
        self.assertEqual(
            Polygons(6,2),
            Polygons(6,2)
        )
    
    def test_gt(self):
        self.assertGreater(
            Polygons(6,3),
            Polygons(5,10)
        )

    def test_polygons(self):
        return self.assertEqual(
            Polygons(6,2),
            Polygons(6,2)
        )
    
    def test_getitem(self):
        self.assertEqual(
            Polygons(6,3)[2],
            Polygon(5,3)
        )
        self.assertEqual(
            Polygons(7,3)[3:],
            (Polygon(6,3), Polygon(7,3),)
        )
    
    def test_len(self):
        self.assertEqual(
            len(Polygons(8)),
            6
        )

    def test_max_effient(self):
        self.assertEqual(
            Polygons(10,1).max_efficient,
            Polygon(10,1)
        )


if __name__ == "__main__":
    unittest.main()