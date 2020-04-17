#!/bin/env python3
import argparse
import subprocess

#def MUMmer(prefix, reference_file, query_file, delta_file):
#    '''Requires a reference sequence (ref.seq) in FASTA format and a query sequences in FastA format (qry.seq) 
#   
#    <reference>  specifies the multi-FastA sequence file that contains
#                 the reference sequences, to be aligned with the queries.
#    <query>      specifies the multi-FastA sequence file that contains
#                 the query sequences, to be aligned with the references.
#    OUTPUT:
#    <prefix>.delta    the delta encoded alignments between the reference and
#                      query sequences.  
#     '''   
	 
   # nucmer_command = ["nucmer", "-p", "prefix", reference_file, query_file, delta_file]
   # dnaff_command = ["dnaff", "-p", "-d", delta_file]
   # subprocess.call(nucmer_command)
   # subprocess.call(dnaff_command   

def chewBBACA(input_genomes,output_dir, cpu):
    '''Creates a wgMLST and cgMLST schema as well as a Newick tree of the cgMLST
       Input: 
            input_genomes = directory where complete or draft genomes are located
            output_dir = directory for output
            cpu = Number of cpus
    '''
    # Get training file
    subprocess.run("wget -P " + output_dir + "  https://github.com/B-UMMI/chewBBACA/blob/master/CHEWBBACA/prodigal_training_files/Escherichia_coli.trn", shell = True)
    # wgMLST Schema Creation
    subprocess.run("../tools/chewBBACA.py CreateSchema -i " + input_genomes + " --cpu" + cpu + " -o "+ output_dir +"Schema --ptf prodigal_training_files/Escherichia_coli.trn", shell = True)
    # Allele Calling
    subprocess.run("../tools/chewBBACA.py AlleleCall -i " + input_genomes + " -g schema/ -o "+ output_dir +"results_allele --cpu "+cpu+" --ptf prodigal_training_files/Escherichia_coli.trn", shell = True)
    # Define cgMLST schema
    date = subprocess.run("ls -t results_allele/ | head -n1", shell = True)
    subprocess.run("../tools/chewBBACA.py ExtractCgMLST -i results_allele/"+ date +"/results_alleles.tsv -o " + output_dir +"cgMLST/ -r " + output_dir + "results_allele/" + date + "/RepeatedLoci.txt -p 0.95", shell = True)
    # Create Newick Tree
    subprocess.run("grapetree " + output_dir + "cgMLST/cgMLST.tsv > cgMLST.tree", shell = True)
#    return None

def kSNP():

    ### kSNP should be on your path
    ### Input: assembled Reads

    ### options

    ## if parsimony

    ## if maximum likelihood

    ## if neighbour-joining

    ## getting the required input files

    pathToInputFiles = "/home/projects/group-a/Team1-GenomeAssembly/assembled_output/"
    input_files_command = 'ls '+ path_to_gpresults + '*.fasta'
    input_files = subprocess.check_output(input_files_command,shell=True)
    input_files = input_files.split('\n')

    #### creating an input fasta file for kSNP:

    ## running Kchooser

    #### running kSNP

    return None

def main():

    #get options using os or argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="directory for input genomes", required = True)
    parser.add_argument("-o", "--output", help="name of output directory", required = True)
    parser.add_argument("-c", "--cpu", help="Number of cpus to use", default = 6)
    parser.add_argument("-t", "--tool", help="Tool of choice: MUMmer (m), chewBBACA (c), kSNP (k), or all (a)", choices = ['m', 'c', 'k', 'a'], required = True)
    args = parser.parse_args()

    output = args.output
    if output[-1] != "/":
        output += "/"
   
     #call MUMmer
    #if args.delta:
     #   MUMmer(args.prefix, args.reference_file, args.query_file, args.delta_file)
    #else:
    #    MUMmer(args.prefix, args.reference_file, args.query_file))

    #call chewBBACA
    if args.tool == 'c' or args.tool == 'a':
        chewBBACA(args.input, output, args.cpu)

    #call kSNP

    #analysis or visualization -- if we're including it here

if __name__ == "__main__":
    main()
