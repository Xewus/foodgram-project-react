import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class TestFoodgramSheme(unittest.TestCase):
    def test_path(self):
        self.assertEqual(
            '.././', BASE_DIR
        )


if __name__ == '__main__':
    unittest.main()
