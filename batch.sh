#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH -t 5:00:00
module load cudnn/7.5-v5
module load cuda
module load cuda/7.5.18
module load python/2.7.9
cd $HOME/Stock
srun python Train.py