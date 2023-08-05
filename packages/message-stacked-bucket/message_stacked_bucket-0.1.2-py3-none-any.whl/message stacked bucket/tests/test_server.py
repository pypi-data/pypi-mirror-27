import server
import unittest


# Ничего не работает, тест не выполняется, голову сломал
class TestResponseFormat(unittest.TestCase):
    def test_response_format(self):
        func = server.response_format("200", "any_timestamp", "any_text")
        self.assertEqual(func, {"response": "200", "time": "any_timestamp", "alert": "any_text"})


if __name__ == '__main__':
    unittest.main()