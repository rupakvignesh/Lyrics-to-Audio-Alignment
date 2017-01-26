"""
This script converts lab (words-level) to
lrc. lrc file is off the form:
"[ phrase ] start_time 1 end_time"

This is an intermediate conversion
for computing the overlap between 
groundtruth and automatic alignment

Author: Rupak Vignesh
"""

import sys,os

output_lab_words = "/Users/RupakVignesh/Desktop/7100/Lyrics-to-Audio-Alignment/Damp_Dataset/test_lab_word_male_damp"
lrc_dir = "/Users/RupakVignesh/Desktop/7100/Lyrics-to-Audio-Alignment/Damp_Dataset/lrc_groundtruth"

lrc_list = sys.argv[1]

with open(lrc_list) as LRC:
    lrc_files = [lines.rstrip() for lines in LRC]

"""
Function returns the start and end time stamps of 
a phrase from word-level lab file
"""
def getTimeStamps(lab_lines_parsed, lrc_lines_parsed):
    
    k = 0								# k = word count (including pau models)
    time_stamp_list = []
    for i in range(len(lrc_lines_parsed)):				# i = iterates phrases
        for j in range(1, len(lrc_lines_parsed[i])-4):			# j = iterates words in Phrases of the form "[ phrase ] start_time 1 end_time" 
            word = ''.join(e for e in lrc_lines_parsed[i][j] if e.isalnum())	# Removes special characters from the words
            #print word
            if (lab_lines_parsed[k][2] == "pau") :			# skip pau if they are present in output_lab_word
                k += 1
            if (j==1) and (lab_lines_parsed[k][2] == word):             # s2 = start_time in phrase of lab file
                s2 = lab_lines_parsed[k][0]
            if (lab_lines_parsed[k][2] == word):			# e2 = end_time in phrase of lab file
                e2 = lab_lines_parsed[k][1]
                k += 1
        #print s2,e2
        s1 = float(lrc_lines_parsed[i][-3])				# s1 = start_time in phrase of lrc file
        e1 = s1 + float(lrc_lines_parsed[i][-1])			# e1 = end_time in phrase of lrc file
        s2 = float(s2)/pow(10,7)
        e2 = float(e2)/pow(10,7)
        time_stamp_list.extend([[s1,e1,s2,e2]])
    return time_stamp_list

def getOverlapPercentage(time_stamp_list):
    overlapPercent = 0
    for i in range(len(time_stamp_list)):
        [s1,e1,s2,e2] = time_stamp_list[i]
        overlap = max(0,min(e1,e2)-max(s1,s2))
        overlapPercent += overlap/(e1-s1)

    return overlapPercent/len(time_stamp_list)

for i in range(len(lrc_files)):
    
    with open(os.path.join(lrc_dir,lrc_files[i])) as LF:		# open lrc files "[ phrase ] start_time 1 end_time"
        lrc_file_lines = [lines.rstrip() for lines in LF]
    lab_file = lrc_files[i][:-3] + "lab"
    with open(os.path.join(output_lab_words,lab_file)) as LAB:		# open lab files " start_time(ns) end_time(ns) word"
        lab_file_lines = [lines.rstrip() for lines in LAB]
    
    lrc_lines_parsed = []
    for j in range(len(lrc_file_lines)):
        lrc_lines_parsed.extend([str.split(lrc_file_lines[j])])
    
    lab_lines_parsed = []
    for j in range(len(lab_file_lines)):
        lab_lines_parsed.extend([str.split(lab_file_lines[j])])
    
    time_stamp_list = getTimeStamps(lab_lines_parsed, lrc_lines_parsed)
    
    overlapPercent = getOverlapPercentage(time_stamp_list)
    print overlapPercent
    


