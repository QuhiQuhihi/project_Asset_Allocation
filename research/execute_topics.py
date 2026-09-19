"""Execute the canonical educational notebooks; preserve last successful files."""

import argparse
import json
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="One topic directory, such as 01-mean-variance")
    args = parser.parse_args()
    for key, folder in [("MPLCONFIGDIR", "matplotlib"), ("IPYTHONDIR", "ipython")]:
        path = ROOT / ".cache" / folder
        path.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault(key, str(path))
    notebooks = sorted((ROOT / "topics").glob("*/study.ipynb"))
    if args.topic:
        notebooks = [p for p in notebooks if p.parent.name == args.topic]
    if not notebooks:
        raise ValueError("No matching topic notebooks")
    preview = ROOT / "research/preview/topics"
    preview.mkdir(parents=True, exist_ok=True)
    records = []
    for path in notebooks:
        notebook = nbformat.read(path, as_version=4)
        for cell in notebook.cells:
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
        NotebookClient(
            notebook,
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}},
        ).execute()
        nbformat.validate(notebook)
        temporary = path.with_suffix(".ipynb.partial")
        nbformat.write(notebook, temporary)
        temporary.replace(path)
        html, _ = HTMLExporter().from_notebook_node(notebook)
        (preview / f"{path.parent.name}.html").write_text(html)
        code = [cell for cell in notebook.cells if cell.cell_type == "code"]
        figures = sum(
            "image/png" in output.get("data", {}) for cell in code for output in cell.outputs
        )
        records.append({"topic": path.parent.name, "code_cells": len(code), "figures": figures})
        print(f"Executed {path.parent.name}: {len(code)} cells, {figures} figures", flush=True)
    (preview / "execution.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
