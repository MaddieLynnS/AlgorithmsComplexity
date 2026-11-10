import unittest
from random import Random
from week08_randomized import freivalds_check

class ScriptedRng: 
    def __init__(self, bits): 
        self.bits = iter(bits) 
        
    def randint(self, low, high): 
        self.assert_range(low, high) 
        return next(self.bits)

    @staticmethod
    def assert_range(low, high):
        if (low, high) != (0, 1):
            raise AssertionError("expected randint(0, 1)")

class FreivaldsTests(unittest.TestCase): 
    def test_correct_product_returns_true(self): 
        A = [[1, 0], [0, 1]] 
        B = [[0, 1], [1, 0]] 
        C = [[0, 1], [1, 0]] 
        self.assertTrue(freivalds_check(A, B, C, 4, Random(3))) 
        
    def test_incorrect_product_is_detected(self): 
        A = [[1, 0], [0, 1]] 
        B = [[1, 0], [0, 1]] 
        C = [[0, 0], [0, 0]] 
        self.assertFalse( freivalds_check(A, B, C, 1, ScriptedRng([1, 0])) ) 

    def test_one_by_one_product(self): 
        self.assertTrue(freivalds_check([[1]], [[1]], [[1]], 2, Random(4)))

    def test_input_is_not_mutated(self): 
        A = [[1, 1], [0, 1]] 
        B = [[1, 0], [1, 1]] 
        C = [[0, 1], [1, 1]] 
        before = ([row[:] for row in A], [row[:] for row in B], [row[:] for row in C]) 
        freivalds_check(A, B, C, 2, Random(5)) 
        self.assertEqual(A, before[0]) 
        self.assertEqual(B, before[1]) 
        self.assertEqual(C, before[2]) 

    def test_invalid_shapes_and_repetitions(self): 
        with self.assertRaises(ValueError): 
            freivalds_check([], [], [], 1, Random(1)) 
        with self.assertRaises(ValueError): 
            freivalds_check([[1]], [[1, 0]], [[1]], 1, Random(1)) 
        with self.assertRaises(ValueError): 
            freivalds_check([[1]], [[1]], [[1]], 0, Random(1))

    def test_correct_product_of_dimension_3(self):
        A = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        B = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        C = [[0, 0, 0], [1, 0, 1], [0, 0, 0]]
        self.assertTrue(freivalds_check(A, B, C, 4, Random(6)))

    def test_incorrect_product_with_more_than_one_repetition(self):
        A = [[1, 0], [0, 1]] 
        B = [[1, 0], [0, 1]] 
        C = [[0, 0], [0, 0]] 
        self.assertFalse( freivalds_check(A, B, C, 3, ScriptedRng([1, 0])) )

if __name__ == "__main__": 
    unittest.main()