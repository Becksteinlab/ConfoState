#!/usr/bin/env python3

from confostate.data.io import download_metadata_from_RCSB

from pathlib import Path

root = Path('../..').resolve()
struct_file = (root / 'data' / 'protein_families' / 'LeuT_transporters.txt')

with struct_file.open() as f:
    for line in f:
        if line[0] != '#':
            download_metadata_from_RCSB(line.strip())