from os.path import isfile, join
from os import listdir
import subprocess

def genome_assembly():
	# output2 = subprocess.getoutput('/home/dkesar3/Team1-WebServer/scripts/quast.sh -t 8 -q /home/projects/group-a/bin/quast/quast.py -p test_data -u /home/dkesar3/Team1-WebServer/unicycler_contigs -o /home/dkesar3/Team1-WebServer/assembled_contigs/ -v')
	output = subprocess.check_output('/home/dkesar3/Team1-WebServer/scripts/run_unicycler.sh -t 8 -p test_data -o /home/dkesar3/Team1-WebServer/unicycler_contigs -m /home/projects/group-a/bin/miniconda3/bin/unicycler -v')
	return output

def gene_prediction(f):
	assembled_files = [join('/home/dkesar3/Team1-WebServer/assembled_contigs/', f) for f in listdir('/home/dkesar3/Team1-WebServer/assembled_contigs/') if isfile(join('/home/dkesar3/Team1-WebServer/assembled_contigs/', f))]
	for l in assembled_files:
		input_dir = ["/home/dkesar3/Team1-WebServer/scripts/run_dfast.sh", "-i", l, "-o", "/home/dkesar3/Team1-WebServer/gene_predicted_files", "-v"]
		output = subprocess.check_output(input_dir)
		f.write(str(output))
	return output

subprocess.call(["python", "/home/dkesar3/Team1-WebServer/preinstall.py"])
f = open('genomeAssemblyLog.txt','w+')
g = genome_assembly()
f.write(g)
f.close()
f = open('genePredictionLog.txt','w+')
gene_prediction(f)
f.close()
