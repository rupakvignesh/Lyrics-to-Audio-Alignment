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

lab_file_path = ''
msaf_segments_path = ''

def make_mlf(wav_segment_name,lyric_lines):
    """
    Write word by word in a MLF file.
    """
    words = [str.split(i) for i in lyric_lines]
    words = [j for i in range(len(words)) for j in words[i]]
    for i in range(len(words)):
        words[i] = ''.join(e for e in words[i] if e.isalpha())
    F = open('Audio_test_segmentation/'+wav_segment_name+'.mlf','w')
    F.write('#!MLF!#\n')
    F.write('"*/'+wav_segment_name+'.lab"\n')
    F.write("pau\n")
    for i in range(len(words)):
        F.write(words[i]+'\n')
        F.write("pau\n")
    F.write(".\n")
    F.close()

def get_boundaries_id(wav_id):
    """
    get all segments starting with wav_id and
    output a list of time stamps corresponding to msaf segments.
    """






def main():
    #Read labfile list

    #Get msaf boundaries for each file in list

    #Approximate to lab file time stamp

    #Get lyric segments within msaf boundaries

    #Make mlf 




if __name__ == "__main__":
    main()
