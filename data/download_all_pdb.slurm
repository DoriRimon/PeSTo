#!/bin/sh
#SBATCH --job-name=download_pdb
#SBATCH --partition=cpu-killable
#SBATCH --output=./slurm-output/%j/logs.out
#SBATCH --time=1440 # max time (minutes)
#SBATCH --signal=USR1@120 # how to end job when time’s up
#SBATCH --nodes=1 # number of machines
#SBATCH --ntasks=1 # number of processes
#SBATCH --mem=32000 # CPU memory (MB)
#SBATCH --cpus-per-task=8 # CPU cores per process
bash rsyncPDB.sh
