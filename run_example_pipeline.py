#!/usr/bin/env python

import os
import glob
import subprocess
import tempfile
import sys
import argparse
import yagmail
import shutil

class Pipeline:
    """
    Runs pipeline either from beginning or intermediary stage
    """
    def __init__(self, tmp_folder, input_path, assemble=True, predict_genes=True, functional_annotation=True, comparative_genomics=True):
        """
        Initialize class and run demanded steps of pipeline
        tmp_folder: str, path to temporary folder
        assemble: boolean, Perform assembly of contigs
        predict_genes: boolean, perform gene prediction
        functional_annotation: boolean, perform functional annotation
        comparative_genomics: boolean, perform comparative genomics
        """
        self.tmp_folder = tmp_folder
        self.input_path = input_path
        self.assemble = assemble
        self.predict_genes = predict_genes
        self.annotate_function = functional_annotation
        self.compare_genomes = True
        # initialize results
        self.assembly = None
        self.gene_prediction = None
        self.functional_annotation = None
        self.comparative_genomics = None
        #import pdb; pdb.set_trace()
        # run assembling
        if self.assemble:
            self.assembly = self.run_genome_assembly()

        # run gene prediction
        if self.predict_genes:
            if not self.assemble:
                input_path = self.input_path
            else:
                input_path = self.output_path_assembly
            self.gene_prediction = self.run_gene_prediction(input_path)

        # run functional annotation
        #if self.annotate_function:
        #    self.functional_annotation = self.run_functional_annotation()

        # run comparative_genomics:
        #if self.compare_genomes:
        #    self.comparative_genomics = self.run_comparative_genomics()


    def run_genome_assembly(self):
       	# output2 = subprocess.getoutput('/home/dkesar3/Team1-WebServer/scripts/quast.sh -t 8 -q /home/projects/group-a/bin/quast/quast.py -p test_data -u /home/dkesar3/Team1-WebServer/unicycler_contigs -o /home/dkesar3/Team1-WebServer/assembled_contigs/ -v')
        # run unicycler
        self.output_path_assembly =f'{self.tmp_folder}/unicycler_contigs'
        log_file = open(f'{self.tmp_folder}/genomeAssemblyLog.txt','w+')
        #TODO: remove absolute path 
        #import pdb; pdb.set_trace()
        output = subprocess.check_output([f"{cwd}scripts/run_unicycler.sh", "-t", "8", "-p", self.input_path, "-o", self.tmp_folder, "-m", "/home/projects/group-a/bin/miniconda3/bin/unicycler", "-v"])
        log_file.write(output)
        log_file.close()
        return output

    def run_gene_prediction(self, input_path):
        log_file = open(f'{self.tmp_folder}/genePredictionLog.txt','w+')
        assembled_files = [os.path.join(f'{input_path}', f) for f in\
                           os.listdir(f'{input_path}') if\
                           os.path.isfile(os.path.join(f'{input_path}', f))]
        for l in assembled_files:
            input_dir = [f"{cwd}scripts/run_dfast.sh", "-i",\
                         l, "-o", self.tmp_folder +'/', "-v"]
            output = subprocess.check_output(input_dir)
            log_file.write(str(output))
        log_file.close()
        return output

    def run_functional_annotation(self, output_path):
        raise NotImplementedError


    def run_compartive_genomics(self, output_path):
        raise NotImplementedError

class Results:
    """
    Class that extracts results and prepares email send to user if provided
    """
    def __init__(self, tmp_folder, user_email):
        self.tmp_folder = tmp_folder
        self.job_id = tmp_folder.split('/')[-1]
        self.user_email = user_email
        self.files_to_send = []
        #import pdb; pdb.set_trace()
        if os.path.isfile(f'{self.tmp_folder}/assembly_statistics.txt'):
            self.files_to_send.append(f'{self.tmp_folder}/genomeAssemblyLog.txt')
        if len(glob.glob(f'{self.tmp_folder}/*.gff')) >= 1:
             predictions = glob.glob(f'{self.tmp_folder}/*.gff')
             self.extract_gene_prediction_statistics(predictions)
             self.files_to_send.append(f"{self.tmp_folder}/gene_prediction_statistics.txt")
        #self.zipped_files = zipfile.ZipFile(f"{self.tmp_folder}/log_files.zip", 'a')
        #for f in files_to_zip:
        #    self.zipped_files.write(f, compress_type = zipfile.ZIP_DEFLATED)
        self.send_email()
        #TODO:extensions of fa and cg files?
        #self.functional_annoation = os.listdir(f'{self.tmp_folder}/*.?')
        #self.comparative_genomics = os.listdir(f'{self.tmp_folder}/*.?')
    #TODO what do we want to sent? which files --> will need to compress them


    def extract_gene_prediction_statistics(self, list_of_gff):
        with open(self.tmp_folder + '/gene_prediction_statistics.txt' , 'w+') as out:
            out.write("Sample #CDS #tRNA #rRNA #CRISPR\n")
            for p in list_of_gff:
                statistics = subprocess.check_output([f'{cwd}extract_statistics_gene_prediction.sh', p])
                out.write(str(statistics.strip())[2:-1])
        out.close()


    def send_email(self):
        body = f"Results from ECHO for job {self.job_id}"
        # use oauth2 for authorization requires oauth2.json file to be in same folder as cwd
        yag = yagmail.SMTP("echowebserver@gmail.com", oauth2_file=f'{cwd}oauth2.json')
        yag.send(
        to=self.user_email,
        subject="ECHO results",
        contents=body, 
        attachments=self.files_to_send,
        )


def start_to_end(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--assemble', help='Assemble contigs, requires pair-end-reads in fastq format, default=0',
                        action='store_true', default=False, dest='assemble', required=False)
    parser.add_argument('-p', '--predict_genes', help='Predict genes in assembled contigs, requires either files in FASTA format or assembly must be run',
                        action='store_true', default=False, dest='predict_genes', required=False)
    #TODO: What is the required input?
    parser.add_argument('-f', '--functional_annoation', help='Perform functional annotation, ',
                        action='store_true', default=False, dest='functional_annotation', required=False)
    parser.add_argument('-c', '--comparative_genomics', help='Perform comparative genomics, ',
                        action='store_true', default=False, dest='comparative_genomics', required=False)
    parser.add_argument('-e', '--email', help="Email address of user to which results will be send",
                        default=None, required=False, dest='email')
    parser.add_argument('-i', '--input', help='Path to input files', required=True, dest='input')
    args = parser.parse_args()
    args = vars(args)
    input_path = args['input']
    assemble = args['assemble']
    predict_genes = args['predict_genes']
    functional_annotation = args['functional_annotation']
    comparative_genomics = args['comparative_genomics']
    user_email = args['email']
    global cwd
    cwd = os.getcwd() + '/'
    # create tmp dir in cwd
    current_tmp_dir = tempfile.mkdtemp(prefix=cwd)
    #subprocess.call(["python", "./preinstall.py"])
    pipeline = Pipeline(current_tmp_dir, input_path, assemble, predict_genes, functional_annotation, comparative_genomics)
    if user_email is not None:
        Results(current_tmp_dir, user_email)
    # done with everything --> clean up
    shutil.rmtree(current_tmp_dir)

if __name__ == "__main__":
    start_to_end(sys.argv[1:])
