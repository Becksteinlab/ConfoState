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

### Download all LeuT transporters to input directory

```bash
python scripts/download_structures.py \
    --codes-file data/protein_families/LeuT_transporters.txt \
    --output-dir input
```

### Download specific structures

```bash
python scripts/download_structures.py \
    --codes 3F3A 3F3C 3F3D 3F3E \
    --output-dir input
```

### Re-download with overwrite

```bash
python scripts/download_structures.py \
    --codes-file data/protein_families/LeuT_transporters.txt \
    --output-dir input \
    --overwrite
```

### Faster downloads (no delay between requests)

```bash
python scripts/download_structures.py \
    --codes-file data/protein_families/LeuT_transporters.txt \
    --output-dir input \
    --delay 0
```

## Output

- `.pdb` files saved to `--output-dir` with names matching their PDB codes (uppercase)
- Example: downloading PDB code `3F3A` creates `input/3F3A.pdb`
- Console output reports: success count, failed codes (if any), and HTTP/network errors
- Existing files are reported as "skipped" (unless `--overwrite` is used)

## Notes

- PDB codes are normalized to uppercase internally
- Default delay of 0.5 seconds between requests respects RCSB rate limits
- Failed downloads are reported at the end but do not stop execution
- Files are downloaded from `https://files.rcsb.org/download/{CODE}.pdb`
