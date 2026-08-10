import requests
import pandas as pd

from datetime import datetime


def download_metadata_from_RCSB(pdb_id):
    """(GPT generated docstring! Code written by hand)

    Download and extract selected metadata for a protein
    structure from the RCSB PDB.

    Parameters
    ----------
    pdb_id : str
        The four-character Protein Data Bank identifier for the
        structure of interest,
        such as "3F3A".

    Returns
    -------
    dict
        A dictionary containing selected metadata fields
        for the requested PDB entry.

        Keys include:
        - rcsb_id : str
        - deposit_date : datetime.date
        - experimental_method : str
        - resolution : str
        - title : str
        - pubmed : str
        - doi : str

    Raises
    ------
    requests.HTTPError
        If the RCSB API request returns an unsuccessful HTTP status code.
    requests.RequestException
        If a network-related error occurs while contacting the RCSB API.
    KeyError
        If an expected metadata field is missing from the API response.
    ValueError
        If the deposit date cannot be parsed as an ISO-formatted date.

    Notes
    -----
    This function queries the RCSB REST API core entry endpoint,
    normalizes the JSON response into a pandas DataFrame, and
    extracts commonly used structure metadata.
    """

    metadata = {}

    r = requests.get(f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}")
    r.raise_for_status()
    df = pd.json_normalize(r.json())

    metadata["rcsb_id"] = df[
        "rcsb_entry_container_identifiers.rcsb_id"
    ].to_string(index=False)
    metadata["experimental_method"] = df[
        "rcsb_entry_info.experimental_method"
    ].to_string(index=False)
    metadata["resolution"] = df[
        "rcsb_entry_info.resolution_combined"
    ].to_string(index=False)

    metadata["deposit_date"] = datetime.fromisoformat(
        df["rcsb_accession_info.deposit_date"].to_string(index=False)
    ).date()
    metadata["title"] = str(df.at[0, "struct.title"])
    metadata["pubmed"] = df[
        "rcsb_primary_citation.pdbx_database_id_PubMed"
    ].to_string(index=False)
    metadata["doi"] = df[
        "rcsb_primary_citation.pdbx_database_id_DOI"
    ].to_string(index=False)

    return metadata
