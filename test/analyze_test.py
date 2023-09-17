import unittest
from shared.analyze import has_conflicts

class AnalyzeTest(unittest.TestCase):
    def test_analyze(self):
        self.assertFalse(has_conflicts([{
            'subject': "Subject 2",
            'course': '1',
            'group': '1',
            'meta': '1н',
            'room': '404',
            'teacher': 'Teacher 1',
            'time': '11:15-12:35',
            'type': 'Практика',
            'weekday': 'среда',
        }, {
            'subject': "Subject 2",
            'course': '1',
            'group': '3',
            'meta': '2н',
            'room': '404',
            'teacher': 'Teacher 1',
            'time': '11:15-12:35',
            'type': 'Практика',
            'weekday': 'среда',
        }]))

if __name__ == '__main__':
    unittest.main()