import client
import unittest


class TestPresenceFormat(unittest.TestCase):
    def test_presence_format(self):
        func = client.presence_format('presence', 'any_timestamp')
        self.assertEqual(func, {"action": "presence", "time": "any_timestamp"})


if __name__ == '__main__':
    unittest.main()
