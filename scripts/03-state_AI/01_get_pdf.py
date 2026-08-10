#!/usr/bin/env python3

import csv
from pathlib import Path

from pypaperretriever import PaperRetriever

scripts = Path("..").resolve()


with open(scripts / "01-data" / "protein_data.csv") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:

        retriever = PaperRetriever(
            email="your.email@gmail.com",
            pmid=row['pubmed'],
            download_directory='PDFs',
            allow_scihub=False
        )

        retriever.download()