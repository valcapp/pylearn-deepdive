import unittest

import math
from polygon import Polygon

class TestPolygon(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(ValueError):
            Polygon(1,1)

    def test_repr(self):
        self.assertEqual(
            str(Polygon(3,2)),
            "Polygon(3,2)"
        )
    
    def test_edges(self):
        self.assertEqual(
            Polygon(5,4).edges,
            5
        )

    def test_vertices(self):
        self.assertEqual(
            Polygon(7,2).vertices,
            7
        )

    def test_circumradius(self):
        self.assertEqual(
            Polygon(10,5).circumradius,
            5
        )

    def test_eq(self):
        self.assertEqual(
            Polygon(6,2),
            Polygon(6,2)
        )
    
    def test_gt(self):
        self.assertGreater(
            Polygon(6,3),
            Polygon(5,10)
        )
    
    def test_interior_angle(self):
        n,r = 9,4
        self.assertAlmostEqual(
            Polygon(n,r).interior_angle,
            (n-2)*180/n
        )
    
    def test_edge_length(self):
        n,r = 4,5
        self.assertAlmostEqual(
            Polygon(n,r).edge_length,
            2*r*math.sin(math.pi/n)
        )

    def test_apothem(self):
        n,r = 6,4
        self.assertAlmostEqual(
            Polygon(n,r).apothem,
            r*math.cos(math.pi/n)
        )
    
    def test_perimeter(self):
        n,r = 5,10
        plyg = Polygon(n,r)
        self.assertEqual(
            plyg.perimeter,
            plyg.edges * plyg.edge_length
        )

    def test_area(self):
        n,r = 12, 13
        plyg = Polygon(n,r)
        self.assertAlmostEqual(
            plyg.area,
            plyg.perimeter * plyg.apothem / 2
        )


if __name__ == "__main__":
    unittest.main()