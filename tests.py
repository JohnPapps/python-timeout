import unittest
from time import sleep

from timeout import timeout, TimeoutError


class TestTimeout(unittest.TestCase):

    def test_does_not_timeout(self):
        @timeout(seconds=1)
        def quick_function(first, second, multiple):
            return (first + second) * multiple
        result = quick_function(3, 4, multiple=5)
        self.assertEqual(result, 35)

    def test_does_timeout(self):
        @timeout(seconds=1)
        def slow_function():
            sleep(2)
        with self.assertRaises(TimeoutError):
            slow_function()

    def test_raises_exception(self):
        @timeout(seconds=1)
        def bad_operation():
            return 5 / 0
        with self.assertRaises(ZeroDivisionError):
            bad_operation()


if __name__ == '__main__':
    unittest.main()
