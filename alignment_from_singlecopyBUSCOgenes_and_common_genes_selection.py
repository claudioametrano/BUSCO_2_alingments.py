#!/usr/bin/python3
print("*****************************************")
print("*Claudio G. Ametrano @ FIELD MUSEUM 2020*")
print("*****************************************")
# USE: from signlecopy busco folder for each species take every gene with the same name and cat them into an alingment,
# then counting how many time a gene is present select and copy in a new folder the alignments which are in common among all samples
import os
import re 
path = os.getcwd()
os.system("mkdir BUSCOs_alignments")
os.system("mkdir BUSCO_common_to_all_samples_alignments")
#print(path)

file_list = []
file_list1 = []
## create a list with all the file names
for root, dirs, files in os.walk(path, topdown=True):
	for i in files:
		if i.endswith(".fna"):
			if i not in file_list:
				file_list.append(i)
for j in file_list:
	file_list1.append(j.replace(".fna",""))				
print("The file fasta (genes) present in the folder are:")
print(file_list1)				

## modify all header inserting sample name in each header and deleting the annoying "<unknown description>"
for root, dirs, files in os.walk(path, topdown=True):
	for fld in dirs:
		path1 = path + "/" + fld
		print("Putting assembly name in the sequence headers from: ",path1)
		for root, dirs, files in os.walk(path1, topdown=True):
			#print(root)
			for fl in files:
				if fl.endswith(".fna"):
					filez = open(root + "/" + fl)
					filez_content = filez.readlines()
					out_file = open(path1 + "/" + fl.replace(".fna","") + "_renamed.fas", "w")
					for line in filez_content:
						if line.startswith(">"):
							line1 = ">" + fld + "_" + line.replace(">","")
							line2 = line1.replace("<unknown description","")
							#print(line2)
							out_file.write(line2)
						else:
							out_file.write(line)
					out_file.close()									
										
				
## create the alignment picking the file with that gene names and appending in the output alignment file 
##(each se have already tha sample name in the header)
for k in file_list1:
	#output_file = open(path +"/" + "BUSCOs_alignments" + "/" + k +"_alignment.fas", "w")
	for root, dirs, files in os.walk(path, topdown=True):
		for fldr in dirs:
			path2 = path + "/" + fldr
			for root, dirs, files in os.walk(path2, topdown=True):
				for z in files:
					if z == k + "_renamed.fas":
						#print(z)
						my_file = open(path2 + "/" + z)
						my_file_content = my_file.read()
						#print(my_file_content)
						output_file = open(path +"/" + "BUSCOs_alignments" + "/" + k +"_alignment.fasta", "a")
						print("Writing to alignment",k,"_alignment.fasta ...")
						output_file.write(my_file_content)
						output_file.close()

## among the alignment select those which has the number of seqs = to the number of samples (genes which are always present)
# counts the samples directories 
count_dir = 0 
for root, dirs, files in os.walk(path, topdown=True):
	for directory in dirs:
		match_regex = re.search(r'GC[F|A]_', directory)
		if match_regex:
			count_dir = count_dir + 1
print("Samples folder are: ", count_dir)

# counts the seq in the alignments, copies only the alignments which has the entire number of samples (genes common to all samples)
path3 = path + "/" + "BUSCOs_alignments" + "/"
for root, dirs, files in os.walk(path3, topdown=True):
	for q in files:	
		#print(q)		
		if q.endswith("_alignment.fasta"):
			count = 0
			alignment = open(path3 + "/" + q)
			alignment_content = alignment.readlines()
			for g in alignment_content:
				if g.startswith(">"):
					#print(g)
					count = count + 1
					#print(count)
				# if the number of seqs in the alignment is + to number of folders (genes) copy to 	
				if count ==	count_dir:
					command = "cp " + path3 + "/" + q +" "+ path + "/" +"BUSCO_common_to_all_samples_alignments"
					os.system(command)	
