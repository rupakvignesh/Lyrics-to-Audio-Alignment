"""
Takes in label files
and removes the pauses
that are less than certain threshold (set pau_threshold)
"""

import numpy as np
import sys


pau_threshold = 0.08    # 8 milli second

def remove_pause(lablines_parsed):
    pau_removed = [lablines_parsed[0]]
    skip_flag = 0       # to skip the i+1 iteration following pau
    for i in range(1, len(lablines_parsed)-1):
        print('loop number {}'.format(i))
        if skip_flag==i:
            continue
        start_time = float(lablines_parsed[i][0])
        end_time = float(lablines_parsed[i][1])
        print(start_time-end_time)
        if (lablines_parsed[i][2] == 'pau') and ((end_time-start_time) <= (10**7)*pau_threshold):
            #print(lablines_parsed[i])
            end_time = float(lablines_parsed[i+1][1])
            label = lablines_parsed[i+1][2]
            #print(str(start_time), str(end_time), label)
            pau_removed.extend([[str(start_time), str(end_time), label]])
            skip_flag = i+1         #skip the next iteration
        else:
            pau_removed.extend([lablines_parsed[i]])

    return pau_removed


def main():
    lab_list = sys.argv[1].readlines()
    for i in range(len(lab_list)):
        with open(lab_list[i],'r') as F:
            lablines = [lines.rstrip() for lines in F]
        F.close()
        lablines_parsed = []
        for j in range(len(lablines)):
            lablines_parsed.extend(str.split(lablines[j]))
        pau_removed = remove_pause(lablines_parsed)
        with open(lab_list[i],'w') as F:
            for j in range(len(pau_removed)):
                F.write(pau_removed[j][0]+' '+pau_removed[1]+' '+pau_removed[2]+'\n')
        F.close()

if __name__ == "__main__":
    main()
