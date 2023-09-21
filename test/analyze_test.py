import unittest
from shared.analyze import has_conflicts, has_conflict_inner_tuple, has_conflict_inner
from shared.types.lesson import Lesson

class HasConflictsTest(unittest.TestCase):
        # Two lessons with the same course, group, and meta
    def test_same_course_group_meta(self):
        l1: Lesson = {'course': 'Math', 'group': 'A', 'meta': 'Lesson 1', 'time': '9:00 AM', 'room': '101', 'weekday': 'Monday', 'teacher': 'Teacher 1', 'subject': 'Math', 'type': 'Lecture'}
        l2: Lesson = {'course': 'Math', 'group': 'A', 'meta': 'Lesson 1', 'time': '9:00 AM', 'room': '101', 'weekday': 'Monday', 'teacher': 'Teacher 1', 'subject': 'Math', 'type': 'Lecture'}
        self.assertFalse(has_conflict_inner_tuple(l1, l2))

if __name__ == '__main__':
    unittest.main()