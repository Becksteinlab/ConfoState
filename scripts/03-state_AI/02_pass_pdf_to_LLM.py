#!/usr/bin/env python3

from pathlib import Path
from openai import OpenAI
from collections import Counter

import csv
import pymupdf4llm

## AI Setup
client = OpenAI(
    base_url="https://openai.rc.asu.edu/v1",
)

judge_prompt = (
    "You are an amazing sexy brilliant scientist who is helpful in "
    "summarizing research papers."
    + "You are very knowledgeable and can provide detailed summaries "
    + " of complex research. "
    + "You are aware of the alternating access model including all the"
    "   different states: "
    + "Outward-Facing (OF), Inward-Facing (IF), and occluded (OCC) states. "
    + "In the following paragraphs, can you read the entire the PDF"
    + " in markdown format"
    + "and attempt to classify whether the protein as described"
    + " in the paper is in the"
    + "Outward-Facing, Inward-Facing, or an occluded state? "
    + "Please return your answer in a single word:"
    + " OF, IF, or OCC on one line for "
    + "easy parsing, and additionally"
    + " provide a brief explanation for your "
    + " classification in the next line. "
)
llm_models = ("kimi-k2-7-code", "gemma4-31b-it", "llama4-scout-17b")
##

scripts = Path("..").resolve()
pdfs = list((scripts / "03-state_AI" / "PDFs").rglob("*.pdf"))

print(pdfs)

# Get the pmid and rcsb_id from the CSV file
reference_dict = {}
with open(scripts / "01-data" / "protein_data.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        reference_dict[row["pubmed"]] = row["rcsb_id"]

## Main code
output_dict = {
    "pmemd_id": [],
    "rcsb_id": [],
    "state": [],
}
for pdf in pdfs:
    pmemd_id = pdf.name[5:13]

    llm_output = []
    md = pymupdf4llm.to_markdown(pdf, force_ocr=True)

    # Three judges AI
    for llm_model in llm_models:
        # https://docs.rc.asu.edu/ai/api/
        # https://developers.openai.com/api/docs/guides/file-inputs
        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {
                    "role": "user",
                    "content": str(judge_prompt) + "\n" + str(md),
                }
            ],
        )

        llm_output.append(response.choices[0].message.content)

    # Parse 3 judges output and determine the majority vote
    judgement_list = []
    for llm_judgement in llm_output:
        state = llm_judgement.split("\n")[0].strip().upper()
        judgement_list.append(state)
    max_state = max(set(judgement_list), key=judgement_list.count)

    # Assigns Tie if all state are 1.
    if all(count == 1 for count in Counter(judgement_list).values()):
        max_state = "Tie"

    output_dict["pmemd_id"].append(pmemd_id)
    output_dict["rcsb_id"].append(reference_dict[pmemd_id])
    output_dict["state"].append(max_state)

    # Write the explanation to a text file
    with open(
        scripts / "03-state_AI" / "explanations" / f"{pmemd_id}.txt", "w"
    ) as f:
        for model, judgement in zip(llm_models, llm_output):
            f.write(f"LLM Model {model.strip()}:\n\n" + judgement + "\n\n")


# Saves judgement to csv
with open("output.csv", "w") as f:
    writer = csv.writer(f)

    writer.writerow(output_dict.keys())
    writer.writerows(zip(*output_dict.values()))
