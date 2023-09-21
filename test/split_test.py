import unittest

from shared.types.lesson import Lesson
from shared.analyze.split import split_into_weeks

class SplitTest(unittest.TestCase):
  # Test with a list of lessons containing both '1н' and '2н' meta values
    def test_both_weeks_meta_values(self):
        lessons: list[Lesson] = [
            {
                'time': '9:00',
                'meta': '1н',
                'subject': 'Math',
                'type': 'Lecture',
                'room': '101',
                'weekday': 'Monday',
                'teacher': 'John Doe',
                'course': 'Calculus',
                'group': 'A'
            },
            {
                'time': '10:00',
                'meta': '2н',
                'subject': 'Physics',
                'type': 'Lecture',
                'room': '201',
                'weekday': 'Tuesday',
                'teacher': 'Jane Smith',
                'course': 'Mechanics',
                'group': 'B'
            },
            {
                'time': '11:00',
                'meta': '',
                'subject': 'Chemistry',
                'type': 'Lab',
                'room': '301',
                'weekday': 'Wednesday',
                'teacher': 'David Johnson',
                'course': 'Organic Chemistry',
                'group': 'C'
            }
        ]
        first_week, second_week, both_weeks = split_into_weeks(lessons)
        self.assertEqual(first_week, [lessons[0]])
        self.assertEqual(second_week, [lessons[1]])
        self.assertEqual(both_weeks, [lessons[2]])

    # Test with a list of lessons containing only '1н' meta values
    def test_only_first_week_meta_values(self):
        lessons: list[Lesson] = [
            {
                'time': '9:00',
                'meta': '1н',
                'subject': 'Math',
                'type': 'Lecture',
                'room': '101',
                'weekday': 'Monday',
                'teacher': 'John Doe',
                'course': 'Calculus',
                'group': 'A'
            },
            {
                'time': '10:00',
                'meta': '1н',
                'subject': 'Physics',
                'type': 'Lecture',
                'room': '201',
                'weekday': 'Tuesday',
                'teacher': 'Jane Smith',
                'course': 'Mechanics',
                'group': 'B'
            },
            {
                'time': '11:00',
                'meta': '',
                'subject': 'Chemistry',
                'type': 'Lab',
                'room': '301',
                'weekday': 'Wednesday',
                'teacher': 'David Johnson',
                'course': 'Organic Chemistry',
                'group': 'C'
            }
        ]
        first_week, second_week, both_weeks = split_into_weeks(lessons)
        self.assertEqual(first_week, lessons[:2])
        self.assertEqual(second_week, [])
        self.assertEqual(both_weeks, [lessons[2]])

    # Test with a list of lessons containing only '2н' meta values
    def test_only_second_week_meta_values(self):
        lessons: list[Lesson] = [
            {
                'time': '9:00',
                'meta': '2н',
                'subject': 'Math',
                'type': 'Lecture',
                'room': '101',
                'weekday': 'Monday',
                'teacher': 'John Doe',
                'course': 'Calculus',
                'group': 'A'
            },
            {
                'time': '10:00',
                'meta': '2н',
                'subject': 'Physics',
                'type': 'Lecture',
                'room': '201',
                'weekday': 'Tuesday',
                'teacher': 'Jane Smith',
                'course': 'Mechanics',
                'group': 'B'
            },
            {
                'time': '11:00',
                'meta': '',
                'subject': 'Chemistry',
                'type': 'Lab',
                'room': '301',
                'weekday': 'Wednesday',
                'teacher': 'David Johnson',
                'course': 'Organic Chemistry',
                'group': 'C'
            }
        ]
        first_week, second_week, both_weeks = split_into_weeks(lessons)
        self.assertEqual(first_week, [])
        self.assertEqual(second_week, lessons[:2])
        self.assertEqual(both_weeks, [lessons[2]])

    # Test with a list of lessons containing meta values other than '1н' and '2н'
    def test_other_meta_values(self):
        lessons: list[Lesson] = [
            {
                'time': '9:00',
                'meta': '',
                'subject': 'Math',
                'type': 'Lecture',
                'room': '101',
                'weekday': 'Monday',
                'teacher': 'John Doe',
                'course': 'Calculus',
                'group': 'A'
            },
            {
                'time': '10:00',
                'meta': '',
                'subject': 'Physics',
                'type': 'Lecture',
                'room': '201',
                'weekday': 'Tuesday',
                'teacher': 'Jane Smith',
                'course': 'Mechanics',
                'group': 'B'
            },
            {
                'time': '11:00',
                'meta': '',
                'subject': 'Chemistry',
                'type': 'Lab',
                'room': '301',
                'weekday': 'Wednesday',
                'teacher': 'David Johnson',
                'course': 'Organic Chemistry',
                'group': 'C'
            }
        ]
        first_week, second_week, both_weeks = split_into_weeks(lessons)
        self.assertEqual(first_week, [])
        self.assertEqual(second_week, [])
        self.assertEqual(both_weeks, lessons)

    # Test with a list of lessons containing meta values with leading/trailing spaces
    def test_meta_values_with_spaces(self):
        lessons: list[Lesson] = [
            {
                'time': '9:00',
                'meta': ' 1н ',
                'subject': 'Math',
                'type': 'Lecture',
                'room': '101',
                'weekday': 'Monday',
                'teacher': 'John Doe',
                'course': 'Calculus',
                'group': 'A'
            },
            {
                'time': '10:00',
                'meta': ' 2н ',
                'subject': 'Physics',
                'type': 'Lecture',
                'room': '201',
                'weekday': 'Tuesday',
                'teacher': 'Jane Smith',
                'course': 'Mechanics',
                'group': 'B'
            },
            {
                'time': '11:00',
                'meta': ' ',
                'subject': 'Chemistry',
                'type': 'Lab',
                'room': '301',
                'weekday': 'Wednesday',
                'teacher': 'David Johnson',
                'course': 'Organic Chemistry',
                'group': 'C'
            }
        ]
        first_week, second_week, both_weeks = split_into_weeks(lessons)
        self.assertEqual(first_week, [lessons[0]])
        self.assertEqual(second_week, [lessons[1]])
        self.assertEqual(both_weeks, [lessons[2]])

    # Test with a list of lessons containing meta values with mixed case
    def test_meta_values_with_mixed_case(self):
        lessons: list[Lesson] = [
            {
                'time': '9:00',
                'meta': '1Н',
                'subject': 'Math',
                'type': 'Lecture',
                'room': '101',
                'weekday': 'Monday',
                'teacher': 'John Doe',
                'course': 'Calculus',
                'group': 'A'
            },
            {
                'time': '10:00',
                'meta': '2н',
                'subject': 'Physics',
                'type': 'Lecture',
                'room': '201',
                'weekday': 'Tuesday',
                'teacher': 'Jane Smith',
                'course': 'Mechanics',
                'group': 'B'
            },
            {
                'time': '11:00',
                'meta': '',
                'subject': 'Chemistry',
                'type': 'Lab',
                'room': '301',
                'weekday': 'Wednesday',
                'teacher': 'David Johnson',
                'course': 'Organic Chemistry',
                'group': 'C'
            }
        ]
        first_week, second_week, both_weeks = split_into_weeks(lessons)
        self.assertEqual(first_week, [lessons[0]])
        self.assertEqual(second_week, [lessons[1]])
        self.assertEqual(both_weeks, [lessons[2]])