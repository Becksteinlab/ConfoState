#!/usr/bin/env python3
import requests
import pandas as pd
from datetime import datetime

metadata = {}

r = requests.get(f'https://data.rcsb.org/rest/v1/core/entry/3F3C')
r.raise_for_status()
df = pd.json_normalize(r.json())


metadata['rcsb_id'] = df['rcsb_entry_container_identifiers.rcsb_id'].to_string(index=False)
metadata['experimental_method'] = df['rcsb_entry_info.experimental_method'].to_string(index=False)
metadata['resolution'] = df['rcsb_entry_info.resolution_combined'].to_string(index=False)

metadata['deposit_date'] = datetime.fromisoformat(df['rcsb_accession_info.deposit_date'].to_string(index=False)).date()
metadata['title'] = str(df.at[0, 'struct.title'])
metadata['pubmed'] = df['rcsb_primary_citation.pdbx_database_id_PubMed'].to_string(index=False)
metadata['doi'] = df['rcsb_primary_citation.pdbx_database_id_DOI'].to_string(index=False)

# Paperscraper
print(metadata['doi'])

#https://www.ncbi.nlm.nih.gov/books/NBK25497/
#https://www.ncbi.nlm.nih.gov/books/NBK25497/