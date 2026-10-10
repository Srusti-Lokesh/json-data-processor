
import json
import tempfile
import unittest
from pathlib import Path

from processor import load_records, process, summarize

class ProcessorTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"name": "Alice", "team": "Engineering", "score": 90},
            {"name": "Bob", "team": "Sales", "score": 75},
            {"name": "Alicia", "team": "Engineering", "score": 85},
        ]

    def test_search_is_case_insensitive(self):
        self.assertEqual(len(process(self.rows, query="ALIC")), 2)

    def test_field_filter(self):
        self.assertEqual(len(process(self.rows, field="team", value="engine")), 2)

    def test_summary_numeric_fields(self):
        result = summarize(self.rows)
        self.assertEqual(result["record_count"], 3)
        self.assertEqual(result["numeric_fields"]["score"]["average"], 83.33)

    def test_rejects_non_array_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text(json.dumps({"name": "not a list"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_records(path)

if __name__ == "__main__":
    unittest.main()
