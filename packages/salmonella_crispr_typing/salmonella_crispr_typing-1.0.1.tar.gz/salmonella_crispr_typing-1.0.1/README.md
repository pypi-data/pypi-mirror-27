# Salmonella CRISPR Typing

[![Build Status](https://travis-ci.org/C3BI-pasteur-fr/Salmonella-CRISPR-Typing.svg?branch=master)](https://travis-ci.org/C3BI-pasteur-fr/Salmonella-CRISPR-Typing)
[![PyPI version](https://badge.fury.io/py/salmonella_crispr_typing.svg)](https://badge.fury.io/py/salmonella_crispr_typing)
[![bio.tools entry](https://img.shields.io/badge/bio.tools-Salmonella__CRISPR__typing-orange.svg)](https://bio.tools/Salmonella_CRISPR_typing)

CRISPR polymorphism is a powerful tool to subtype Salmonella strains and is now used in routine for epidemiological investigations.
This tool gets a CRISPR profile by identifying the presence of known spacers and direct repeats (DRs) in a given sequence based on a catalogue.

This tool is a reimplemntation of a former tool in Perl/CGI developed by G. Guigon

-------------------------

## Installation

#### Requirements

This tool is developed in Python3 and uses [Biopython](http://biopython.org/) library.

We recommand the use of a virtual environment to install and run the tool.

To install, run the following commands:

```bash
python3 -m venv crispr_typing
source crispr_typing/bin/activate
pip install salmonella_crispr_typing
```

To check if the installation was successful, try to display the help menu:

```bash
crispr_typing -h
```

## How does it work ?

Salmonella CRISPR Typing tool allows the discovery of spacers and DRs from either a PCR product of a full assembly.


```bash
crispr_typing your_file.fa
```

Please, read the help message for advanced features on the tool.

```bash
crispr_typing --help
```

## Example

In the example folder, you have example files from the following command:

```bash
crispr_typing query.fasta -o seq.output -c -l -e
```

#### Output files

Name | content |
---- | ------- |
seq.output | sequence with spacer sequences replaced by their names |
seq.bed | BED file of all the spacers found |
new_spacers.fa | sequence of new spacers found |


## References

Fabre L, Zhang J, Guigon G, Le Hello S, Guibert V, Accou-Demartin M, de Romans S, Lim C, Roux C, Passet V, Diancourt L, Guibourdenche M, Issenhuth-Jeanjean S, Achtman M, Brisse S, Sola C, Weill FX. CRISPR typing and subtyping for improved laboratory surveillance of Salmonella infections. PLoS One. 2012;7(5):e36995. DOI:[10.1371/journal.pone.0036995](http://doi.org/10.1371/journal.pone.0036995)
