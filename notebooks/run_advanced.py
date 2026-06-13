
"""Execute Advanced_Analytics notebook code cells to generate deliverables."""
import json
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parent / "Advanced_Analytics.ipynb"
ns = {"__name__": "__main__"}
nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    source = "".join(cell["source"])
    if not source.strip():
        continue
    print(f"--- Cell {i} ---")
    exec(compile(source, f"<cell {i}>", "exec"), ns)

print("Done.")
