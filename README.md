# ConfoState (WARNING — NON-FUNCTIONAL Work-in-progress)

**NOTE: This is an experimental project. It is not working. You're more than welcome to fork it and work on it on your own.**


## Overview

ConfoState is a proof-of-principle software project for assigning membrane protein structures to known conformational states described in the literature. Starting from experimentally determined or predicted structures, ConfoState uses structural features and comparisons to reference structures to classify proteins into states such as inward-open, outward-open, occluded, active, or inactive. The initial focus is on building a curated set of state annotations and demonstrating that automated state assignment is feasible across representative membrane protein families. By providing a reproducible framework for conformational state classification, ConfoState aims to support the analysis of growing structural datasets and lay the groundwork for more general state annotation methods in structural biology.

## User requirements / user stories

1. As a user, I have coordinates of a membrane protein (eg a PDB or PDBx or mmCIF file) from an experiement (eg X-ray crystallography or cryo-EM). I want to know which functional state (conformation) the protein is in. I want this classification be tied to the literature. For example, for a secondary active transpoter, typical functional states I would expect to see are tied to the alternating access model (e.g. outward facing (OF), inward facing (IF), occluded, ...)

2. As a user, in addition to (1), I want to have a probabilistic interpretation of assigned functional states (e.g., 75% inward-facing open, 25% inward-facing occluded).

3. As a user I would like to get a human-understandable justification of the classification definition (e.g., solvent accessibility of binding sites, movement of known protein domains).

4. I want to use a command line tool that reads structure files as input (or takes database identifiers) and outputs text files.

5. I want to have a package with an API that I can use to accomplish my task.


## Background

### Statement of problem

Many membrane proteins function by cycling through different conformations. (see https://doi.org/10.1063/5.0047967 or https://pmc.ncbi.nlm.nih.gov/articles/PMC8984959/ for background). However, the 3D structure of a protein is not easily interpreted in terms of the functional states/conformations.

Given the vast amount of structures in databases (primarily ProteinDatabank https://www.rcsb.org/) that are directly linked to the scientific literature through the PDB metadata, we want to generate a training set (and a test set) to train a ML model to classify unknown structures and assign a functional state.

### Additional considerations

* Orientation of the membrane protein in the lipid bilayer: use OPM https://opm.phar.umich.edu/ (either using existing entries or submit jobs to calculate orientation)

* Access papers on Pubmed Central https://pmc.ncbi.nlm.nih.gov or preprint servers such as bioRxiv https://www.biorxiv.org/ or arXiv https://arxiv.org/ or Open Access papers at journals.

* We may also want to consider internal repeat symmetries to help with conformational assignment (see DOI 10.1146/annurev-biophys-051013-023008)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for coding style (Ruff, 79-character lines), pre-commit, and pull-request expectations.


