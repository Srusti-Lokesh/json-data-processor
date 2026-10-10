
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from flask import Flask, render_template_string, request

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATASETS = {
    "employees": DATA_DIR / "employees.json",
    "products": DATA_DIR / "products.json",
    "students": DATA_DIR / "students.json",
}

app = Flask(__name__)

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JSON Data Processor</title>
<style>
:root { color-scheme: light; }
body { font-family: system-ui, Segoe UI, Arial, sans-serif; max-width: 1050px; margin: 32px auto; padding: 0 18px; color: #172554; background: #f4f7fb; }
header, section { background: white; border: 1px solid #dbe4f0; border-radius: 14px; padding: 22px; margin-bottom: 18px; box-shadow: 0 4px 16px #0f172a0b; }
h1 { margin: 0 0 6px; } .muted { color: #52627a; }
form { display: flex; gap: 10px; flex-wrap: wrap; align-items: end; }
label { display: grid; gap: 5px; font-size: .9rem; }
input, select, button { font: inherit; padding: 9px 11px; border: 1px solid #bac7d8; border-radius: 8px; }
button { background: #1d4ed8; color: white; border: 0; cursor: pointer; }
button:hover { background: #1e40af; }
.cards { display: flex; gap: 12px; flex-wrap: wrap; }
.card { background: #eff6ff; padding: 12px 16px; border-radius: 10px; min-width: 130px; }
table { width: 100%; border-collapse: collapse; margin-top: 12px; background: white; }
th, td { text-align: left; padding: 9px; border-bottom: 1px solid #e2e8f0; overflow-wrap: anywhere; }
th { background: #eff6ff; } .notice { color: #9a3412; }
@media (max-width: 600px) { body { margin: 14px auto; } header, section { padding: 15px; } }
</style>
</head>
<body>
<header>
<h1>JSON Data Processor</h1>
<p class="muted">Load structured JSON data, search records, filter by a field, and review a quick summary.</p>
<form method="get">
<label>Dataset
<select name="dataset">
{% for key in datasets %}
<option value="{{ key }}" {% if key == dataset %}selected{% endif %}>{{ key|capitalize }}</option>
{% endfor %}
</select></label>
<label>Search all fields
<input name="q" value="{{ q }}" placeholder="e.g. Alice or Bengaluru"></label>
<label>Filter field
<select name="field">
<option value="">-- no field filter --</option>
{% for f in fields %}
<option value="{{ f }}" {% if f == field %}selected{% endif %}>{{ f }}</option>
{% endfor %}
</select></label>
<label>Contains / equals
<input name="value" value="{{ value }}" placeholder="e.g. Engineering"></label>
<button type="submit">Process data</button>
</form>
</header>
{% if error %}<section class="notice"><strong>Data error:</strong> {{ error }}</section>{% endif %}
<section>
<h2>Summary</h2>
<div class="cards">
<div class="card"><strong>{{ total }}</strong><br>Records matched</div>
<div class="card"><strong>{{ all_total }}</strong><br>Total records</div>
<div class="card"><strong>{{ fields|length }}</strong><br>Available fields</div>
</div>
{% if numeric_summary %}
<h3>Numeric field summary</h3>
<ul>{% for key, val in numeric_summary.items() %}<li><strong>{{ key }}</strong>: min {{ val.min }}, max {{ val.max }}, average {{ "%.2f"|format(val.average) }}</li>{% endfor %}</ul>
{% endif %}
</section>
<section>
<h2>Results</h2>
{% if rows %}
<table><thead><tr>{% for f in fields %}<th>{{ f }}</th>{% endfor %}</tr></thead>
<tbody>{% for row in rows %}<tr>{% for f in fields %}<td>{{ row.get(f, "") }}</td>{% endfor %}</tr>{% endfor %}</tbody></table>
{% else %}<p>No records match the current search/filter.</p>{% endif %}
<p class="muted">Showing up to 200 matching records.</p>
</section>
</body></html>
"""

def load_records(dataset: str) -> list[dict[str, Any]]:
    """Read a JSON array of objects and validate its basic shape."""
    if dataset not in DATASETS:
        raise ValueError("Unknown dataset selected.")
    path = DATASETS[dataset]
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise ValueError(f"{path.name} must contain a JSON array of objects.")
    return payload

def matches(record: dict[str, Any], query: str, field: str, value: str) -> bool:
    if query:
        searchable = " ".join(str(v) for v in record.values()).casefold()
        if query.casefold() not in searchable:
            return False
    if field and value:
        if field not in record:
            return False
        actual = str(record[field]).casefold()
        expected = value.casefold()
        # Numeric values are compared by string representation; text uses case-insensitive contains.
        if expected not in actual:
            return False
    return True

def numeric_summary(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    keys = set.intersection(*(set(r.keys()) for r in records)) if records else set()
    result: dict[str, dict[str, float]] = {}
    for key in sorted(keys):
        values = [r[key] for r in records if isinstance(r.get(key), (int, float)) and not isinstance(r.get(key), bool)]
        if values:
            result[key] = {"min": min(values), "max": max(values), "average": sum(values) / len(values)}
    return result

@app.route("/", methods=["GET"])
def index():
    dataset = request.args.get("dataset", "employees")
    if dataset not in DATASETS:
        dataset = "employees"
    q = request.args.get("q", "").strip()[:150]
    field = request.args.get("field", "").strip()[:80]
    value = request.args.get("value", "").strip()[:150]
    error = ""
    try:
        records = load_records(dataset)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        records, error = [], str(exc)
    fields = sorted({key for row in records for key in row.keys()})
    filtered = [row for row in records if matches(row, q, field, value)]
    # Stable columns: all fields in the chosen dataset, including keys absent from an individual record.
    return render_template_string(
        PAGE, datasets=DATASETS.keys(), dataset=dataset, q=q, field=field, value=value,
        fields=fields, rows=filtered[:200], total=len(filtered), all_total=len(records),
        numeric_summary=numeric_summary(filtered), error=error
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
