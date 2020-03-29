from boundingbox import BoundingBox
import unittest
 
class TestBoundingBox(unittest.TestCase):

    def test_intersection_adjacent_returnsempty(self):
        testee = BoundingBox(0, 0, 1, 1)
        other = BoundingBox(1, 1, 2, 2)
        intersection = testee.intersection(other)
        self.assertTrue(intersection.empty())

    
    def test_intersection_intersectsonlyx_returnsempty(self):
        testee = BoundingBox(10, 10, 21, 21)
        other = BoundingBox(15, 21, 25, 25)
        intersection = testee.intersection(other)
        self.assertTrue(intersection.empty())


    def test_intersection_intesectsonlyy_retunrsempty(self):
        testee = BoundingBox(10, 10, 21, 21)
        other = BoundingBox(0, 0, 10, 11)
        intersection = testee.intersection(other)
        self.assertTrue(intersection.empty())


    def test_intersection_containsother_equalsother(self):
        testee = BoundingBox(10, 10, 21, 21)
        other = BoundingBox(15, 15, 16, 16)
        intersection = testee.intersection(other)
        self.assertEqual(other, intersection)


    def test_intersection_othercontainstestee_equalstestee(self):
        testee = BoundingBox(11, 11, 20, 20)
        other = BoundingBox(10, 10, 21, 21)
        intersection = testee.intersection(other)
        self.assertEqual(testee, intersection)


    def test_intersection_samebox_equalsboundingbox(self):
        testee = BoundingBox(20, 30, 25, 40)
        intersection = testee.intersection(BoundingBox(20, 30, 25, 40))
        self.assertEqual(testee, intersection)


    def test_invalidxbound_raisesvalueerror(self):
        with self.assertRaises(ValueError) : BoundingBox(10, 10, 9, 20)

 
if __name__ == '__main__':
    unittest.main()
