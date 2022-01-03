import unittest
from pathlib import Path
from api import urls

BASE_DIR = Path(__file__).resolve()

class TestFoodgramSheme(unittest.TestCase):
    def test_path(self):
        self.assertEqual(
            '.././', BASE_DIR
        )


if __name__ == '__main__':
    unittest.main()
