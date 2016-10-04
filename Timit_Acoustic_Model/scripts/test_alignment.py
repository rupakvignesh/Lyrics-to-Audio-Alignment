#!/usr/bin/python
"""
This script helps calculating how many segments fall
within the threshold (default 20ms) of the ground truth
Input Arguments: "ground truth folder" "output alignment folder" "list of files"
Output (to terminal): % of segments within the threshold.

Author: Rupak Vignesh
"""

import os, sys

hmm_path = '/Users/RupakVignesh/Desktop/7100/Lyrics-to-Audio-Alignment/Timit_Acoustic_Model' 

#Global variables
threshold = 200000				# 20ms default threshold
gt_folder = os.path.join(hmm_path,sys.argv[1])	# ground truth folder
op_folder = os.path.join(hmm_path,sys.argv[2])	# output alignment folder
lab = sys.argv[3]				# file containing lablist

"""
parse_file(file): Reads and parses lab file,
splits 'A B C' to ['A','B','C']
"""

def parse_file(infile):
    with open(infile,'r') as F:
        infile_contents = [lines.rstrip() for lines in F] 
    file_contents_parsed = []
    for i in range(len(infile_contents)):
        file_contents_parsed.extend([str.split(infile_contents[i])]) 
    return file_contents_parsed

"""
compute_deviation: calculated % of segments
lying outside the specified threshold
"""

def compute_deviation(file1,file2):		# file1 -> ground truth, file 2 -> output alignment
    file1_parsed = parse_file(file1)
    file2_parsed = parse_file(file2)
    dev_count = 0
    for i in range(len(file1_parsed)-1):
        if((float(file1_parsed[i][1])-float(file2_parsed[i][1]) > threshold)):		# 1st column gives end time stamp
            dev_count += 1.0
    avg_deviation = (dev_count/(len(file1_parsed)-1))
    return avg_deviation



"""
Compute the average deviation of each file in the database and 
find the overall average deviation
"""
with open(lab) as L:
    lab_list = [lines.rstrip() for lines in L]

avg_dev = 0
for i in range(len(lab_list)):
    print lab_list[i]
    avg_dev += compute_deviation(gt_folder+'/'+lab_list[i],op_folder+'/'+lab_list[i])

overall_deviation = 100*(avg_dev/len(lab_list))	# average deviation for all files
print str(overall_deviation)+"% segments lie outside threshold"


 
