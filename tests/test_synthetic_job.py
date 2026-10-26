import unittest
from examples.synthetic_job import count_records


class SyntheticJobTests(unittest.TestCase):
    def test_default(self):
        self.assertEqual(count_records(), {"status": "success", "records_processed": 3})

    def test_boundaries(self):
        for value in (0, 10000):
            self.assertEqual(count_records(value)["records_processed"], value)

    def test_invalid_inputs(self):
        for value in (-1, 10001, True, 3.5, "3", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                count_records(value)


if __name__ == "__main__":
    unittest.main()
