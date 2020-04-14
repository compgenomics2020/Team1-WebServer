#!/usr/bin/env python
import subprocess

g = subprocess.check_output(["conda", "info"])
if (len(g) < 5):
	subprocess.call(["curl", "-O", "https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh"])
	subprocess.call(["bash", "Anaconda3-2019.03-Linux-x86_64.sh"])

subprocess.call(["conda", "create", "--name", "Team1WebServer"])
subprocess.call(["conda", "activate", "Team1WebServer"])
subprocess.call(["conda", "install", "-c", "bioconda", "biopython"])
subprocess.call(["conda", "install", "-c", "bioconda/label/cf201901", "java-jdk"])
subprocess.call(["conda", "install", "-c", "bioconda", "unicycler"])
subprocess.call(["conda", "install", "-c", "bioconda", "prodigal"])
subprocess.call(["conda", "install", "-c", "conda-forge", "yagmail"])

