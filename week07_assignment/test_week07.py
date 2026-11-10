import unittest
from week07_scheduling import interval_schedule
class IntervalSchedulingTests(unittest.TestCase):

    def check_schedule(self, intervals, expected):
        before = intervals[:]
        result = interval_schedule(intervals)

        self.assertEqual(result, expected)
        self.assertEqual(intervals, before)
        self.assertIsNot(result, intervals)
    
    def test_empty_input(self):
        self.check_schedule([], [])
    
    def test_earliest_finish_time_schedule(self):
        self.check_schedule(
            [(0, 3), (1, 4), (3, 5), (5, 7), (4, 8), (8, 10)],
            [0, 2, 3, 5],
        )

    def test_touching_intervals_are_compatible(self):
        self.check_schedule(
            [(1, 2), (2, 3), (3, 4)],
            [0, 1, 2],
        )

    def test_contained_long_interval_is_rejected(self):
        self.check_schedule(
            [(0, 10), (1, 2), (2, 3), (3, 4)],
            [1, 2, 3],
        )

    def test_equal_finish_time_prefers_earlier_start(self):
        self.check_schedule(
            [(1, 2), (0, 2), (2, 3)],
            [1, 2],
        )

    def test_all_intervals_overlap(self):
        self.check_schedule(
            [(0, 5), (1, 4), (2, 3)],
            [2],
        )

    def test_unsorted_input(self):
        self.check_schedule(
            [(5, 7), (0, 3), (3, 5), (1, 4), (8, 10), (4, 8)],
            [1, 2, 0, 4],
        )

    def test_input_with_duplicate_intervals(self):
        self.check_schedule(
            [(1, 2), (1, 2), (2, 3)],
            [0, 2],
        )

    def test_input_with_several_touching_endpoint_intervals(self):
        self.check_schedule(
            [(4, 5), (1, 2), (2, 3), (3, 4), (5, 6)],
            [1, 2, 3, 0, 4],
        )

    def test_multiple_intervals_with_same_start_time(self):
        self.check_schedule(
            [(0, 2), (2, 5), (2, 3), (3, 4)],
            [0, 2, 3],
        )

    def test_input_list_is_not_mutated(self):
        intervals = [(3, 5), (0, 2), (2, 3)]
        before = intervals[:]

        interval_schedule(intervals)

        self.assertEqual(intervals, before)

    def test_compatible_result_with_max_cardinality(self):
        self.check_schedule(
            [(0, 4), (1, 2), (2, 3), (3, 5), (5, 6)],
            [1, 2, 3, 4],
        )

if __name__ == "__main__":
    unittest.main()