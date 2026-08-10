#!/usr/bin/env bash
#SBATCH -J AI_processing
#SBATCH -w yamsolo
#SBATCH -c 12
#SBATCH -N 1

eval "$(mamba shell hook --shell bash)" && mamba activate confostate

python 02_pass_pdf_to_LLM.py
