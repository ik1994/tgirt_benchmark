#!/bin/bash

DATAPATH=${SCRATCH}/bench_marking/data
INDEX_PATH=${REF}/benchmarking/human_transcriptome
INDEX=${INDEX_PATH}/transcriptome_kallisto/transcriptome_kallisto
RESULTPATH=${SCRATCH}/bench_marking/alignment_free
COUNT_PATH=${RESULTPATH}/countFiles
BAM_PATH=${RESULTPATH}/bamFiles
THREADS=24
mkdir -p ${COUNT_PATH} ${BAM_PATH}

for R1 in ${DATAPATH}/*R1_001.fastq.gz
do
	R2=${R1/R1/R2}
	SAMPLENAME=$(basename ${R1%_R1_001.fastq.gz})
	echo time kallisto quant \
		-i ${INDEX} -o ${COUNT_PATH}/${SAMPLENAME} \
		--fr-stranded  --threads=${THREADS}\
		${R1} ${R2}  
done

