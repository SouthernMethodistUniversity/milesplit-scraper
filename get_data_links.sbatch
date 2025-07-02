#!/bin/bash
#SBATCH -A egodat_oit_research_tech_0001
#SBATCH -D /users/mlangstonsmith/milesplit-scraper/
#SBATCH -J get_data_links
#SBATCH -o /users/mlangstonsmith/milesplit-scraper/debug/output-%j.txt
#SBATCH -e /users/mlangstonsmith/milesplit-scraper/debug/error-%j.txt
#SBATCH -p standard-s
#SBATCH -t 60
#SBATCH --mem=5G
#SBATCH --array=0-252

mkdir -p debug

CHUNK_SIZE=30
START=$((SLURM_ARRAY_TASK_ID * CHUNK_SIZE))
END=$((START + CHUNK_SIZE))

module load conda
conda activate milesplit

python get_data_links.py --start $START --end $END