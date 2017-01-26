

import sys

filelist = sys.argv[1]

with open(filelist,'r') as F1:
    list_lab = [lines.rstrip() for lines in F1] 


for i in range(len(list_lab)):
    with open("test_lab_word_male_damp/"+list_lab[i]) as F2:
        lab_contents = [lines.rstrip() for lines in F2]
    #print lab_contents
    lab_contents_parsed = []
    for j in range(len(lab_contents)):
        lab_contents_parsed.extend([str.split(lab_contents[j])])
   
    newlab = open("audacity_labels/"+list_lab[i][:-4]+".txt",'w')
    for j in range(len(lab_contents_parsed)):
        ts_1 = float(lab_contents_parsed[j][0])/pow(10,7)
        ts_2 = float(lab_contents_parsed[j][1])/pow(10,7)
        newlab.write(str(ts_1) +"\t"+ str(ts_2) +"\t"+ lab_contents_parsed[j][2] +"\n")
    newlab.close() 
    
