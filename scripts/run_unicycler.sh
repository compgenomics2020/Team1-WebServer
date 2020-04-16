#!/bin/bash
get_input () {
        # Function for doing getopts

        # Setting default number of threads as 4
        threads=4

        while getopts "t:m:p:o:vh" option
        do
                case $option in
                        t) threads=$OPTARG;;
                        p) pathToInputFiles=$OPTARG;;
                        o) outputFolder=$OPTARG;;
                        m) unicyclerPath=$OPTARG;;
                        h) info_usage=1;;
                        v) verbose=1;;
                        *) echo "Incorrect arguments used. Use -h to know about the arguments available."
                esac
        done

        if ((info_usage)); then
                echo -e "The script contains a pipeline for running Unicycler.\nRun the script in the following format after giving the script executable permission:\n./run_unicycler.sh\nArguments available\n\t-m <Path to spades.py file>\n\t-p <Path to folder containing input fastq forward and backward reads annotated as <name>_1 and <name>_2 and are gzipped>\n\t-o <Path to output folder>\n\t-t <Number of threads>\n\t-v \tVerbose mode\n\t-h\tPrint usage information"
                exit
        fi
}


get_input "$@"
if ((verbose)); then
        echo "\nMaking output directory\n"
fi



if ((verbose)); then
        echo "\nStarted genome assembly\n"
fi
ls ${pathToInputFiles} | grep _1.fq.gz | xargs -I gw basename -s _1.fq.gz gw | xargs -I gwa mkdir ${outputFolder}/gwa_output
ls ${pathToInputFiles} | grep _1.fq.gz | xargs -I gw basename -s _1.fq.gz gw | xargs -I gwa ${unicyclerPath} -1 ${pathToInputFiles}/gwa_1.fq.gz -2 ${pathToInputFiles}/gwa_2.fq.gz -t ${threads} -o ${outputFolder}/gwa_output

for v in `ls ${pathToInputFiles} | grep _1.fq.gz | xargs -I gw basename -s _1.fq.gz gw`
do
        cp ${outputFolder}/${v}_output/assembly.fasta ${outputFolder}/${v}_assembled.fasta
	rm -r ${outputFolder}/${v}_output
done 
