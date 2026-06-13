import os
import pandas as pd

pdb_dir = "."

rows = []

for filename in sorted(os.listdir(pdb_dir)):
    if not filename.endswith(".pdb"):
        continue

    pdb_id = filename.replace(".pdb", "")

    title = ""
    doi = ""
    resolution = ""
    keywords = ""

    with open(os.path.join(pdb_dir, filename), "r", encoding="utf-8", errors="ignore") as f:
        for line in f:

            if line.startswith("TITLE"):
                title += line[10:].strip() + " "

            elif line.startswith("KEYWDS"):
                keywords += line[10:].strip() + " "

            elif line.startswith("REMARK   2 RESOLUTION."):
                resolution = line.split("RESOLUTION.")[-1].strip()

            elif line.startswith("JRNL        DOI"):
                doi = line.split("DOI")[-1].strip()

    rows.append(
        {
            "pdb_id": pdb_id,
            "title": title.strip(),
            "resolution": resolution,
            "doi": doi,
            "keywords": keywords.strip(),
            "state": "",
            "notes": "",
        }
    )

df = pd.DataFrame(rows)

os.makedirs("data/annotations", exist_ok=True)

outfile = "leut_metadata.csv"

df.to_csv(outfile, index=False)

print(f"Saved {len(df)} entries to {outfile}")