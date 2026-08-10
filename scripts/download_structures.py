"""Download PDB files from RCSB for a list of PDB codes.

Usage:
    python scripts/download_structures.py
    python scripts/download_structures.py \\
        --codes-file data/structures/pdb_codes.txt
    python scripts/download_structures.py \\
        --codes 3F3A 3F3C --output-dir data/structures
"""

import argparse
import os
import time
import urllib.error
import urllib.request

RCSB_URL = "https://files.rcsb.org/download/{code}.pdb"
DEFAULT_CODES_FILE = "data/structures/pdb_codes.txt"
DEFAULT_OUTPUT_DIR = "data/structures"


def load_codes(path: str) -> list[str]:
    with open(path) as f:
        return [
            line.strip().upper()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


def download_pdb(code: str, output_dir: str, overwrite: bool = False) -> bool:
    dest = os.path.join(output_dir, f"{code}.pdb")
    if os.path.exists(dest) and not overwrite:
        print(f"  {code}: already exists, skipping")
        return True

    url = RCSB_URL.format(code=code)
    try:
        urllib.request.urlretrieve(url, dest)
        size_kb = os.path.getsize(dest) / 1024
        print(f"  {code}: downloaded ({size_kb:.0f} KB)")
        return True
    except urllib.error.HTTPError as e:
        print(f"  {code}: HTTP error {e.code} — {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"  {code}: network error — {e.reason}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Download PDB files from RCSB.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--codes-file",
        default=DEFAULT_CODES_FILE,
        help=(
            "Path to text file with one PDB code per line "
            f"(default: {DEFAULT_CODES_FILE})"
        ),
    )
    group.add_argument(
        "--codes",
        nargs="+",
        metavar="CODE",
        help="One or more PDB codes to download (overrides --codes-file)",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save .pdb files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-download files that already exist",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        metavar="SECONDS",
        help="Seconds to wait between requests (default: 0.5)",
    )
    args = parser.parse_args()

    if args.codes:
        codes = [c.upper() for c in args.codes]
    else:
        codes = load_codes(args.codes_file)

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Downloading {len(codes)} structure(s) to {args.output_dir}/")
    ok, failed = 0, []
    for code in codes:
        success = download_pdb(code, args.output_dir, overwrite=args.overwrite)
        if success:
            ok += 1
        else:
            failed.append(code)
        if args.delay > 0:
            time.sleep(args.delay)

    print(f"\nDone: {ok}/{len(codes)} downloaded.")
    if failed:
        print(f"Failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
