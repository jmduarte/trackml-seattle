#!/bin/bash
# typically executed in your home directory /home/ec2-user/
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
export PATH="$CONDA_PREFIX/miniconda3/bin:$PATH"
