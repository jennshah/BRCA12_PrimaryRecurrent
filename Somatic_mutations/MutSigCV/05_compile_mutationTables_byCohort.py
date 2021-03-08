#Make a master file of all mutation tables for a cohort specified in a list, for use as MutSigCV input
#Required inputs:
	#Argument -i : txt file of tumors to include; one tumor per line
	#Argument -o : name of master cohort mutation table outfile (should be *.maf)
	#Each tumor in the list should have a maf file generated by maf2mutationTable.py; will report to you if not
#Required organization
	#To be run out of a directory in which each tumor has a subdirectory
	#mutation table maf for a given tumor should be in that tumor's subdirectory
	#mutation table maf should be named <tumor subdirectory name>.all.somatic.variants.filtered.MutSigCV.table.maf

import csv
import argparse
import os

#Parse and check the arguments
parser=argparse.ArgumentParser()
parser.add_argument('-i',action='store',dest='infile',help='Enter the filepath of your txt file of tumors')
parser.add_argument('-o',action='store',dest='outfile',help='Enter the name of your master mutation table output file for MutSigCV')
args=parser.parse_args()

if args.infile==None:
	print("Error: specify tumor list filepath with -i")
	exit()
if args.outfile==None:
	print("Error: specify filepath for output file with -o")
	exit()
else:
	()

#start a list of tumors that are listed in input file but are missing a variants file
missing_variants_files=[]

#Open an empty file for writing output, then add a header 
outfields=['Tumor_Sample_Barcode','Hugo_Symbol','Chromosome','Start_Position','Reference_Allele','Tumor_Seq_Allele1','Tumor_Seq_Allele2','effect']
with open(args.outfile,'w') as master_file:
	writer=csv.DictWriter(master_file,delimiter='\t',fieldnames=outfields)
	writer.writeheader()

#For each line (tumor) in the input file:
	#find the appropriate mutation table file
	#pare down to only columns we need for MutsigCV
	#Write to the master outfile 
with open(args.infile,'r') as input:
	for line in input:
		tumor=line.strip()
		if os.path.exists(tumor+'/'+tumor+'.all.somatic.variants.filtered.MutSigCV.table.maf'):
			with open(tumor+'/'+tumor+'.all.somatic.variants.filtered.MutSigCV.table.maf','r') as tumor_file, open(args.outfile,'a') as master_file:
				reader=csv.DictReader(tumor_file,delimiter='\t')
				writer=csv.DictWriter(master_file,delimiter='\t',fieldnames=outfields)
				#add every following line of tumor variants to the master file 
				for row in reader:
					outRow={'Tumor_Sample_Barcode':row['Tumor_Sample_Barcode'],'Hugo_Symbol':row['Hugo_Symbol'],'Chromosome':row['Chromosome'],
					'Start_Position':row['Start_Position'] ,'Reference_Allele':row['Reference_Allele'],'Tumor_Seq_Allele1':row['Tumor_Seq_Allele1'],
					'Tumor_Seq_Allele2':row['Tumor_Seq_Allele2'],'effect':row['effect']}
					writer.writerow(outRow)
		else:
			print(tumor+" mutation table file does not exist")
			missing_variants_files.append(tumor)

#Write the tumors missing variants to a log file 
if not missing_variants_files:
	print("Compilation complete, all files found")
else:
	with open((os.path.splitext(args.outfile)[0])+'_log.txt','w') as missing_variants_log:
		writer=csv.writer(missing_variants_log, delimiter=",")
		missing_variants_log.write("These tumors were missing mutation table files: \n")
		writer.writerow(missing_variants_files)