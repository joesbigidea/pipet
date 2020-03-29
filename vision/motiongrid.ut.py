from motiongrid import MotionDetectionGrid
from boundingbox import BoundingBox
import unittest
 
class TestMotionDetectionGrid(unittest.TestCase):

    def test_rejects_empty_dimensions(self):
        with self.assertRaises(ValueError) : MotionDetectionGrid((0,0))


    def test_rejects_too_small_dimensions(self):
        too_small = 3 * 2 - 1
        with self.assertRaises(ValueError) : MotionDetectionGrid((too_small, too_small))


    def test_builds_grid_correctly(self):
        testee = MotionDetectionGrid((30, 60))
        self.assertEqual(3, len(testee.grid))

        [ self.assertEqual(3, len(row)) for row in testee.grid ]
        
        self.assertEqual(BoundingBox(0, 0, 10, 20), testee.grid[0][0].bounding_box)
        self.assertEqual(BoundingBox(10, 0, 20, 20), testee.grid[0][1].bounding_box)
        self.assertEqual(BoundingBox(20, 0, 30, 20), testee.grid[0][2].bounding_box)

        self.assertEqual(BoundingBox(0, 20, 10, 40), testee.grid[1][0].bounding_box)
        self.assertEqual(BoundingBox(10, 20, 20, 40), testee.grid[1][1].bounding_box)
        self.assertEqual(BoundingBox(20, 20, 30, 40), testee.grid[1][2].bounding_box)

        self.assertEqual(BoundingBox(0, 40, 10, 60), testee.grid[2][0].bounding_box)
        self.assertEqual(BoundingBox(10, 40, 20, 60), testee.grid[2][1].bounding_box)
        self.assertEqual(BoundingBox(20, 40, 30, 60), testee.grid[2][2].bounding_box)


    def test_check_motion_no_motion_for_no_boxes(self):
        testee = MotionDetectionGrid((30, 60))
        motion_result = testee.check_motion([])

        [[ self.assertFalse(c) for c in row] for row in motion_result.motion_results ]

        self.assertFalse(motion_result.has_motion())


    def test_check_motion_full_bounds_all_results_true(self):
        testee = MotionDetectionGrid((30, 60))
        motion_result = testee.check_motion([BoundingBox(0, 0, 30, 60)])

        [[ self.assertTrue(c) for c in row] for row in motion_result.motion_results ]

        self.assertTrue(motion_result.motion_on_right())
        self.assertTrue(motion_result.motion_in_middle())
        self.assertTrue(motion_result.motion_on_left())
        self.assertTrue(motion_result.has_motion())


    def test_check_motion_each_cell_true(self):
        testee = MotionDetectionGrid((30, 60))
        motion_result = testee.check_motion([
            BoundingBox(5, 5, 6, 6), BoundingBox(15, 5, 16, 6), BoundingBox(25, 5, 26, 6),
            BoundingBox(5, 25, 6, 26), BoundingBox(15, 25, 16, 26), BoundingBox(25, 25, 26, 26),
            BoundingBox(5, 45, 6, 46), BoundingBox(15, 45, 16, 46), BoundingBox(25, 45, 26, 46)
            ])

        [[ self.assertTrue(c) for c in row] for row in motion_result.motion_results ]

        self.assertTrue(motion_result.motion_on_right())
        self.assertTrue(motion_result.motion_in_middle())
        self.assertTrue(motion_result.motion_on_left())
        self.assertTrue(motion_result.has_motion())

    
    def test_check_motion_on_left(self):
        testee = MotionDetectionGrid((30, 60))
        motion_result = testee.check_motion([BoundingBox(5, 1, 9, 30), BoundingBox(1, 8, 4, 41)])

        [ self.assertTrue(row[0]) for row in motion_result.motion_results ]

        self.assertTrue(motion_result.motion_on_left())
        self.assertFalse(motion_result.motion_in_middle())
        self.assertFalse(motion_result.motion_on_right())
        self.assertTrue(motion_result.has_motion())
        

    def test_check_motion_in_middle(self):
        testee = MotionDetectionGrid((30, 60))
        motion_result = testee.check_motion([BoundingBox(10, 1, 11, 2), BoundingBox(15, 29, 19, 60)])

        [ self.assertTrue(row[1]) for row in motion_result.motion_results ]

        self.assertFalse(motion_result.motion_on_right())
        self.assertTrue(motion_result.motion_in_middle())
        self.assertFalse(motion_result.motion_on_left())
        self.assertTrue(motion_result.has_motion())


    def test_check_motion_on_right(self):
        testee = MotionDetectionGrid((30, 60))
        motion_result = testee.check_motion([BoundingBox(20, 0, 30, 60)])

        [ self.assertTrue(row[2]) for row in motion_result.motion_results ]

        self.assertFalse(motion_result.motion_on_left())
        self.assertFalse(motion_result.motion_in_middle())
        self.assertTrue(motion_result.motion_on_right())
        self.assertTrue(motion_result.has_motion())

if __name__ == '__main__':
    unittest.main()
