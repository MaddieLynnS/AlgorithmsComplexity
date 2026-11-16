import unittest
from random import Random
from week09_skiplist import SkipListSet
class ScriptedRng:
    def __init__(self, values):
        self.values = iter(values)

    def random(self):
        return next(self.values)

class SkipListTests(unittest.TestCase):
    def test_empty_structure_and_boundaries(self):
        s = SkipListSet(rng=Random(1))
        self.assertEqual(len(s), 0)
        self.assertEqual(s.to_list(), [])
        self.assertFalse(s.contains(5))
        self.assertFalse(s.delete(5))
        self.assertIsNone(s.predecessor(5))
        self.assertIsNone(s.successor(5))

    def test_insert_order_and_duplicate(self):
        s = SkipListSet(rng=Random(2))
        self.assertEqual([s.insert(x) for x in [20, 10, 30, 25]],
        [True, True, True, True])
        self.assertFalse(s.insert(20))
        self.assertEqual(s.to_list(), [10, 20, 25, 30])
        self.assertEqual(len(s), 4)

    def test_predecessor_and_successor(self):
        s = SkipListSet(rng=Random(3))
        for x in [10, 20, 30]:
            s.insert(x)
        self.assertEqual(s.predecessor(20), 10)
        self.assertEqual(s.successor(20), 30)
        self.assertIsNone(s.predecessor(10))
        self.assertIsNone(s.successor(30))
        self.assertEqual(s.predecessor(25), 20)
        self.assertEqual(s.successor(25), 30)

    def test_delete_leaf_middle_and_missing(self):
        s = SkipListSet(rng=Random(4))
        for x in [10, 20, 30, 40]:
            s.insert(x)
        self.assertTrue(s.delete(10))
        self.assertTrue(s.delete(30))
        self.assertFalse(s.delete(99))
        self.assertEqual(s.to_list(), [20, 40])

    def test_promotion_is_capped(self):
        s = SkipListSet(max_level=3, rng=ScriptedRng([0.0] * 10))
        self.assertTrue(s.insert(7))
        self.assertLessEqual(s.height, 3)

    def test_invalid_configuration(self):
        with self.assertRaises(ValueError):
            SkipListSet(max_level=0)
        with self.assertRaises(ValueError):
            SkipListSet(promotion_probability=0.0)
        with self.assertRaises(ValueError):
            SkipListSet(promotion_probability=1.0)

    def test_valid_single_key_structure(self):
        s = SkipListSet(max_level=3, rng=ScriptedRng([0.9]))

        self.assertTrue(s.insert(7))
        self.assertEqual(s.height, 1)
        self.assertEqual(len(s), 1)
        self.assertEqual(s.head.forward[0].value, 7)
        self.assertIsNone(s.head.forward[0].forward[0])

    def test_deletion_of_only_key(self):
        s = SkipListSet(max_level=3, rng=ScriptedRng([0.1, 0.1, 0.9]))

        self.assertTrue(s.insert(7))
        self.assertEqual(s.height, 3)
        self.assertTrue(s.delete(7))
        self.assertEqual(len(s), 0)
        self.assertEqual(s.to_list(), [])
        self.assertEqual(s.height, 1)
        self.assertTrue(all(node is None for node in s.head.forward))

    def test_query_below_min(self):
        s = SkipListSet(rng=Random(5))
        for key in [10, 20, 30]:
            s.insert(key)

        self.assertIsNone(s.predecessor(5))
        self.assertEqual(s.successor(5), 10)

    def test_query_above_max(self):
        s = SkipListSet(rng=Random(6))
        for key in [10, 20, 30]:
            s.insert(key)

        self.assertEqual(s.predecessor(35), 30)
        self.assertIsNone(s.successor(35))

    def test_multiple_duplicate_insertions(self):
        s = SkipListSet(rng=Random(7))

        self.assertTrue(s.insert(12))
        self.assertFalse(s.insert(12))
        self.assertFalse(s.insert(12))
        self.assertEqual(len(s), 1)
        self.assertEqual(s.to_list(), [12])

    def test_promotion_pattern_with_generator(self):
        s = SkipListSet(
            max_level=4,
            promotion_probability=0.5,
            rng=ScriptedRng([0.1, 0.2, 0.9, 0.9]),
        )

        self.assertTrue(s.insert(20))
        self.assertTrue(s.insert(10))

        level_two_node = s.head.forward[2]
        level_one_node = s.head.forward[1]
        self.assertIs(level_two_node, level_one_node)
        self.assertEqual(level_two_node.value, 20)
        self.assertEqual(s.head.forward[0].value, 10)
        self.assertIs(s.head.forward[0].forward[0], level_two_node)
        self.assertEqual(s.height, 3)

    def test_deletion_removes_from_all_levels(self):
        s = SkipListSet(
            max_level=4,
            promotion_probability=0.5,
            rng=ScriptedRng([0.9, 0.1, 0.1, 0.9, 0.1, 0.9]),
        )
        for key in [10, 20, 30]:
            self.assertTrue(s.insert(key))

        self.assertEqual(s.height, 3)
        self.assertTrue(s.delete(20))
        self.assertEqual(s.to_list(), [10, 30])
        self.assertEqual(len(s), 2)
        self.assertEqual(s.height, 2)
        self.assertIsNone(s.head.forward[2])
        self.assertEqual(s.head.forward[1].value, 30)
        self.assertEqual(s.head.forward[0].value, 10)
        self.assertEqual(s.head.forward[0].forward[0].value, 30)

if __name__ == "__main__":
    unittest.main()