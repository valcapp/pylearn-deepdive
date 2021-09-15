import unittest
from modulus import Mod

class TestMod(unittest.TestCase):
    def test_value(self):
        self.assertEqual(Mod(3,2).value, 1)
        self.assertEqual(Mod(5,3).value, 2)
        self.assertEqual(Mod(10,5).value, 0)
        
    def test_modulus(self):
        self.assertEqual(Mod(3,2).modulus, 2)
        self.assertEqual(Mod(5,3).modulus, 3)
        self.assertEqual(Mod(10,5).modulus, 5)
    
    def test_repr(self):
        for a,b in ((4,5), (9,4), (34,12)):
            self.assertEqual(repr(Mod(a,b)),
                f"Mod(value={a%b}, modulus={b})"
            )
    
    def test_check_implemented(self):
        for other in ('other', .5, [1,2,3], Mod(5,6)):
            with self.assertRaises(TypeError):
                Mod(3,4).check_implemented(other)
        for other in (6, Mod(8,4), 10, Mod(3,4)):
            self.assertIsNone(
                Mod(3,4).check_implemented(other)
            )
    
    def test_eq(self):
        self.assertTrue(Mod(2,5)==2)
        self.assertTrue(Mod(2,5)==Mod(7,5))
        self.assertTrue(Mod(6,3)==0)
        with self.assertRaises(TypeError):
            Mod(2,4) == Mod(2,5)
        with self.assertRaises(TypeError):
            Mod(2,4) == 2.0
    
    def test_hash(self):
        self.assertTrue(
            hash(Mod(8,3))==hash(Mod(8,3))
        )
        self.assertTrue(
            hash(Mod(8,3))==hash(Mod(2,3))
        )
        self.assertTrue(
            hash(Mod(8,3))!=hash(Mod(9,3))
        )
        self.assertTrue(
            hash(Mod(8,3))!=hash(Mod(8,6))
        )
    
    def test_int(self):
        self.assertEqual(Mod(9,4), 1)
        self.assertEqual(Mod(8,2), 0)
        self.assertEqual(Mod(2,3), 2)
    
    def test_add(self):
        self.assertEqual(
            Mod(1,5)+3,
            Mod(4,5)
        )
        self.assertEqual(
            Mod(6,7)+Mod(5,7),
            Mod(4,7)
        )
        with self.assertRaises(TypeError):
            Mod(6,7)+Mod(6,8)
        with self.assertRaises(TypeError):
            Mod(6,7)+8.9
            
    def test_radd(self):
        self.assertEqual(
            3+Mod(1,5),
            Mod(4,5)
        )
        with self.assertRaises(TypeError):
            8.9+Mod(6,7)
    
    def test_iadd(self):
        m1 = Mod(1,5)
        m1_id = id(m1)
        m1 += 4
        self.assertEqual(m1,0)
        self.assertEqual(m1_id, id(m1))
        m2 = m1 + 1
        self.assertEqual(m2,1)
        self.assertNotEqual(m1_id, id(m2))
    
    def test_neg(self):
        self.assertEqual(-Mod(3,4), Mod(-3,4))
    
    def test_sub(self):
        self.assertEqual(
            Mod(1,5)-3,
            Mod(-2,5)
        )
        self.assertEqual(
            Mod(6,7)-Mod(16,7),
            Mod(-3,7)
        )
        with self.assertRaises(TypeError):
            Mod(6,7)-Mod(6,8)
        with self.assertRaises(TypeError):
            Mod(6,7)-8.9
            
    def test_rsub(self):
        self.assertEqual(
            3+Mod(1,5),
            Mod(4,5)
        )
        with self.assertRaises(TypeError):
            8.9+Mod(6,7)
    
    def test_isub(self):
        m1 = Mod(1,5)
        m1_id = id(m1)
        m1 -= 4
        self.assertEqual(m1,-3)
        self.assertEqual(m1_id, id(m1))
        m2 = m1 - 1
        self.assertEqual(m2,-4)
        self.assertNotEqual(m1_id, id(m2))
    
    def test_mul(self):
        self.assertEqual(
            Mod(1,5)*3,
            Mod(3,5)
        )
        self.assertEqual(
            Mod(6,7)*Mod(3,7),
            Mod(4,7)
        )
        with self.assertRaises(TypeError):
            Mod(6,7)*Mod(6,8)
        with self.assertRaises(TypeError):
            Mod(6,7)*8.9
            
    def test_rmul(self):
        self.assertEqual(
            3*Mod(2,5),
            Mod(1,5)
        )
        with self.assertRaises(TypeError):
            8.9*Mod(6,7)
    
    def test_imul(self):
        m1 = Mod(1,5)
        m1_id = id(m1)
        m1 *= 4
        self.assertEqual(m1,4)
        self.assertEqual(m1_id, id(m1))
        m2 = m1 * 2
        self.assertEqual(m2,3)
        self.assertNotEqual(m1_id, id(m2))
        
    def test_pow(self):
        self.assertEqual(
            Mod(2,5)**3,
            Mod(3,5)
        )
        self.assertEqual(
            Mod(6,7)**Mod(2,7),
            Mod(1,7)
        )
        with self.assertRaises(TypeError):
            Mod(6,7)**Mod(6,8)
        with self.assertRaises(TypeError):
            Mod(6,7)**2.0

    def test_ipow(self):
        m1 = Mod(2,5)
        m1_id = id(m1)
        m1 **= 3
        self.assertEqual(m1,3)
        self.assertEqual(m1_id, id(m1))
        m2 = m1 ** 2
        self.assertEqual(m2,4)
        self.assertNotEqual(m1_id, id(m2))
    
    def test_ordering(self):
        self.assertTrue(
            Mod(1,5)<2<=Mod(2,4)<Mod(3,4)<5<=Mod(16,10)
        )
        self.assertFalse(
            4>Mod(17,6)
        )
        self.assertFalse(
            Mod(17,6)<5
        )

if __name__ == "__main__":
    unittest.main()