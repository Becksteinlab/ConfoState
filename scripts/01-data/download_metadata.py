#!/usr/bin/env python3

import csv
from pathlib import Path

from confostate.data.io import download_metadata_from_RCSB

root = Path("../..").resolve()
struct_file = root / "data" / "protein_families" / "LeuT_transporters.txt"

header_written = False

with (
    struct_file.open(encoding="utf-8") as f,
    open(
        "protein_data.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file,
):
    writer = None

    for line in f:
        line = line.strip()

        # Ignore blank lines and comments
        if not line or line.startswith("#"):
            continue

        data = download_metadata_from_RCSB(line)

        if not header_written:
            writer = csv.DictWriter(csv_file, fieldnames=data.keys())
            writer.writeheader()
            header_written = True

        writer.writerow(data)
