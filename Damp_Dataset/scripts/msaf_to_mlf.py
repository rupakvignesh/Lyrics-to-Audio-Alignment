"""
Takes in MSAF boundary information,
determine the nearest boundary from the initial segmentation.
Make mlf using the lyrics contained within the MSAF segment.
arg1 -- lab file list (song level) in htk format
"""

import numpy as np
import scipy.io.wavfile as wavfile
import os, sys
import os.path as op
import pdb

lab_file_path = '/Users/RupakVignesh/Desktop/fall16/7100/Lyrics-to-Audio-Alignment/Damp_Dataset/train_lab_word_damp_model/'
msaf_segments_path = '/Users/RupakVignesh/Desktop/fall16/7100/Lyrics-to-Audio-Alignment/Damp_Dataset/Audio_train_segmentation/'

def make_mlf(wav_segment_name, words):
    """
    Write word by word in a MLF file.
    """
    F = open(msaf_segments_path+wav_segment_name[:-4]+'.mlf','w')
    F.write('#!MLF!#\n')
    F.write('"*/'+wav_segment_name[:-4]+'.lab"\n')
    for i in range(len(words)):
        F.write(words[i]+'\n')
    F.write(".\n")
    F.close()

def find_nearest_word(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def get_boundaries_id(wav_id):
    """
    get all segments starting with wav_id and
    output a list of time stamps corresponding to msaf segments.
    """
    segment_list = [wav_seg for wav_seg in os.listdir(msaf_segments_path) if (wav_seg.startswith(wav_id) and wav_seg.endswith('wav'))]
    #Sort segment list according to the segment number (the number after clip-)
    seg_num = [ int(str.split(list_str,'-')[2]) for list_str in segment_list ]
    arg_sorted = sorted(range(len(seg_num)), key=lambda k: seg_num[k])
    segment_list = [segment_list[i] for i in arg_sorted]
    boundaries_id = []
    for i in segment_list:
        [fs,x] = wavfile.read(msaf_segments_path+i)
        dur = float(len(x))/fs
        boundaries_id.append(dur)

    boundaries_id = np.cumsum(boundaries_id)
    return (segment_list, boundaries_id)

def main():
    #Read labfile list
    with open(sys.argv[1],'r') as F:
        labfile_list = [lines.strip() for lines in F]
    F.close()

    for i in range(len(labfile_list)):
        print (i, labfile_list[i])
        with open(lab_file_path + labfile_list[i], 'r') as F:
            lablines = [ str.split(lines.strip()) for lines in F]
        F.close()
        lab_word_boundaries = []
        lab_words = []
        for j in range(len(lablines)):
            #Convert from 100ns to seconds
            lab_word_boundaries.append(float(lablines[j][1])/(10**7))
            lab_words.append(lablines[j][2])

        #Get msaf boundaries for each file in list
        wav_id = op.splitext(labfile_list[i])
        [segment_list, boundaries_id] = get_boundaries_id(wav_id)

        prev_word_idx = 0
        for bound_idx in range(len(boundaries_id)):
            #Approximate to lab file time stamp
            word_idx = find_nearest_word(lab_word_boundaries, boundaries_id[bound_idx]) #Computes nearest word boundary to msaf boundary
            #Get lyric segments within msaf boundaries
            lyric_seg = lab_words[prev_word_idx:word_idx+1]
            prev_word_idx = word_idx
            #Make mlf
            make_mlf(segment_list[bound_idx], lyric_seg)




if __name__ == "__main__":
    main()
