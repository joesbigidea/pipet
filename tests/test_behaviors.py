from robot import behaviors
import unittest
 
class TestBehaviors(unittest.TestCase):
    
    def test_getPriorityForTime_GivenStartOfActiveWindow_ReturnsMaxPriority(self):
        result = behaviors.getPriorityForTime(1000, None, 60, 120, 1000)
        self.assertEqual(behaviors.BEHAVIOR_MAX_NORMAL_PRIORITY, result)


    def test_getPriorityForTime_GivenEndOfActiveWindow_ReturnsZero(self):
        result = behaviors.getPriorityForTime(1060, None, 60, 120, 1120)
        self.assertEqual(0, result)


    def test_getPriorityForTime_GivenPastActiveWindow_ReturnsZero(self):
        result = behaviors.getPriorityForTime(1060, None, 60, 120, 2000)
        self.assertEqual(0, result)


    def test_getPriorityForTime_GivenMiddleOfActiveWindow_ReturnsMiddlePriority(self):
        result = behaviors.getPriorityForTime(1060, None, 60, 120, 1090)
        self.assertEqual(behaviors.BEHAVIOR_MAX_NORMAL_PRIORITY / 2, result)


    def test_getPriorityForTime_GivenEndOfInactiveWindow_ReturnsMaxPriority(self):
        result = behaviors.getPriorityForTime(None, 100, 30, 120, 220)
        self.assertEqual(behaviors.BEHAVIOR_MAX_NORMAL_PRIORITY, result)


    def test_getPriorityForTime_GivenPastInactiveWindow_ReturnsMaxPriority(self):
        result = behaviors.getPriorityForTime(None, 100, 30, 120, 600)
        self.assertEqual(behaviors.BEHAVIOR_MAX_NORMAL_PRIORITY, result)


    def test_getPriorityForTime_GivenStartOfInactiveWindow_ReturnsZero(self):
        result = behaviors.getPriorityForTime(None, 100, 30, 120, 100)
        self.assertEqual(0, result)


    def test_getPriorityForTime_GivenMiddleOfInactiveWindow_ReturnsMidPriority(self):
        result = behaviors.getPriorityForTime(None, 100, 30, 120, 160)
        self.assertEqual(behaviors.BEHAVIOR_MAX_NORMAL_PRIORITY / 2, result)