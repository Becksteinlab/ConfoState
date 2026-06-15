# download_structures

Download PDB files from RCSB for a list of PDB codes.

## Synopsis

    python scripts/download_structures.py [OPTIONS]

## Description

Reads a list of four-character PDB codes and fetches the corresponding `.pdb`
files from `https://files.rcsb.org/download/`. Files that already exist in the
output directory are skipped unless `--overwrite` is set. A configurable delay
between requests avoids overloading the RCSB servers.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--codes-file PATH` | `data/structures/pdb_codes.txt` | Text file with one PDB code per line. Lines beginning with `#` are ignored. Mutually exclusive with `--codes`. |
| `--codes CODE [CODE ...]` | — | One or more PDB codes supplied directly on the command line. Mutually exclusive with `--codes-file`. |
| `--output-dir DIR` | `data/structures` | Directory in which to save `.pdb` files. Created automatically if it does not exist. |
| `--overwrite` | off | Re-download files that already exist. |
| `--delay SECONDS` | `0.5` | Pause between HTTP requests (seconds). |

## Examples

Download all codes in the default codes file:

    python scripts/download_structures.py

Re-download everything to a custom directory:

    python scripts/download_structures.py --output-dir /tmp/pdb --overwrite

Download a specific subset of structures:

    python scripts/download_structures.py --codes 3F3A 3F3C 6XWM

## Input

`data/structures/pdb_codes.txt` (default) — plain text, one PDB code per line.

## Output

One `<CODE>.pdb` file per code written to `--output-dir`. A summary line is
printed to stdout after all downloads complete, listing any failures.
