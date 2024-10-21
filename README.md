
# NGS Data QC Wrapper

## Overview

This program assists bioinformatics professionals by significantly reducing workload through local execution of FASTQC and comparison of sequencing results.

## Features

- Run FASTQC locally on FASTQ files.
- Generate a comprehensive HTML report comparing the results.
- Quick link to perform BLAST searches for similar sequences.

## Prerequisites

Before running the code, ensure you have the following:

1. **FASTQC**: Download and install [FASTQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/).
2. **Update the Code**: 
   - Copy the path to your local FASTQC installation and paste it in the code where indicated: `Copy path to your local FASTQC`.
   - Edit the file paths in the code to match your desired locations on your computer.

## How to Use

1. Run the program.
2. A directory selection window will appear. Choose the folder containing the FASTQ files you want to analyze.
3. The program will:
   - Create a folder named `fastqc_results` to store the FASTQC results.
   - Generate an HTML report named `my_report.html`, which compares the outputs of the uploaded files.
   - Provide a quick link to run BLAST for identifying similar sequences.

## Example and Sample Files

- An example of how to run the program is included in the repository.
- A ZIP folder containing sample files needed for upload is also provided.

## Conclusion

We hope you find this tool useful and effective in your bioinformatics work. Good luck!

