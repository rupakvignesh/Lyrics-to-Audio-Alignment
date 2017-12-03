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

lab_file_path = '/Users/RupakVignesh/Desktop/fall16/7100/Lyrics-to-Audio-Alignment/Damp_Dataset/test_lab_word_damp_model/'
msaf_segments_path = '/Users/RupakVignesh/Desktop/fall16/7100/Lyrics-to-Audio-Alignment/Damp_Dataset/Audio_test_segmentation/'

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
    segment_list = [wav_seg for wav_seg in os.listdir(msaf_segments_path) if (wav_seg.startswith(wav_id) and wav_seg.endswith('wav'))]
    boundaries_id = []
    for i in segment_list:
        [fs,x] = wavfile.read(msaf_segments_path+i)
        dur = float(len(x))/fs
        boundaries_id.append(dur)

    boundaries_id = np.cumsum(boundaries_id)
    return boundaries_id



def main():
    #Read labfile list
    with open(sys.argv[1],'r') as F:
        labfile_list = [lines.strip() for lines in F]
    F.close()

    for i in range(len(labfile_list)):
        with open(lab_file_path + labfile_list[i], 'r') as F:
            lablines = [ str.split(lines.strip()) for lines in F]
        F.close()
        for j in range(len(lablines)):
            #Convert from 100ns to seconds
            lablines[j][0] = float(lablines[j][0])/(10**7)
            lablines[j][1] = float(lablines[j][1])/(10**7)

        #Get msaf boundaries for each file in list
        wav_id = op.splitext(labfile_list[i])
        boundaries_id = get_boundaries_id(wav_id)
        pdb.set_trace()
    #Approximate to lab file time stamp


    #Get lyric segments within msaf boundaries

    #Make mlf




if __name__ == "__main__":
    main()
