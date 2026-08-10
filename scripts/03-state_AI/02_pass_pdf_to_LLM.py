#!/usr/bin/env python3

from pathlib import Path
from openai import OpenAI

scripts = Path("..").resolve()
pdfs = list((scripts / "03-state_AI" / "PDFs").rglob('*.pdf'))

client = OpenAI(
    base_url="https://openai.rc.asu.edu/v1",
    api_key="sk-gFuYLOHopKdjs6FrRQjVsA",
)

prompt = "You are an amazing sexy brilliant scientist who is helpful in summarizing research papers. You are very knowledgeable and can provide detailed summaries of complex research. " \
"You are aware of the alternating access model including all the different states: Outward-Facing, Inward-Facing, and occluded states. " \
"Can you read the entire the PDF and attempt to classify whether the protein as described in the paper is in the Outward-Facing, Inward-Facing, or an occluded state? " \
"Please provide a detailed explanation for your classification." \

for pdf in pdfs:

    # AI generated besides the for loops
    with pdf.open("rb") as file:
        uploaded_file = client.files.create(
            file=file,
            purpose="user_data",
        )

    #https://developers.openai.com/api/docs/guides/file-inputs
    response = client.responses.create(
        model="gpt-5.6",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": uploaded_file.id,
                    },
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                ],
            }
        ],
    )

    print(response.output_text)

    break