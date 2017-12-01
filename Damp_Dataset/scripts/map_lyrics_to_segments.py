import sys, commands
import numpy as np
import os.path as path
import scipy.io.wavfile as wave
import pdb
"""
likelihood = commands.getstatusoutput('HVite -T 1 -a -m -o MN -H hmm_with_er/hmm7/hmmdefs -I segments.mlf lists/dict lists/phonelist mfc_train/dr1_fcjf0_sa1.mfc | tail -1 | rev | cut -d " " -f4 | rev')[1]
"""

VOC_THRES = -2.5
def get_lyrics(wav_id, wav2lyric):
    """
    get lyric_id from wav2lyric dict and
    read the corresponding file.
    return lines in the lyric files as list.
    """

    lyric_id = wav2lyric[wav_id]
    with open('Lyrics/'+lyric_id+'.txt','r') as F:
        lyric_lines = [lines.rstrip() for lines in F]
    F.close()
    lyric_lines = filter(None, lyric_lines)
    return lyric_lines

def get_likelihood(segment_name):
    likelihood = commands.getstatusoutput('HVite -t 250.0 150.0 10000.0 -T 1 -a -m -o MN -H hmm_with_er/hmm5/hmmdefs -I Audio_test_segmentation/'+segment_name+'.mlf words_to_phone_dict lists/phonelist '+'Audio_test_segmentation/'+segment_name+'.mfc | tail -1 | rev | cut -d " " -f4 | rev')[1]
    commands.getstatusoutput("rm Audio_test_segmentation/"+segment_name+".rec")
    return likelihood
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

def classify_silence(segment_name):
    [fs,x] = wave.read('Audio_test_segmentation/'+segment_name+'.wav')
    x = x/(2.0**16)
    ms = sum([a**2 for a in x])/len(x)
    rms_db = np.log10(pow(ms, 0.5))
    if (rms_db > VOC_THRES): #Not Silence
        return 0
    else:
        return 1


def main():
    # Create a wav2lyric dictionary
    with open('lists/lyricid_songid_map.txt','r') as F:
        lyricid_to_song = [lines.rstrip() for lines in F]
    F.close()
    lyricid_to_song_parsed = []
    for i in range(len(lyricid_to_song)):
        lyricid_to_song_parsed.extend([str.split(lyricid_to_song[i])])
    lyricid_to_song_parsed = np.array(lyricid_to_song_parsed)
    keys_wav = lyricid_to_song_parsed[:,1]
    values_lyrics = lyricid_to_song_parsed[:,0]
    wav2lyric = dict(zip(keys_wav, values_lyrics))

    # Open wavlist and readlines
    with open(sys.argv[1],'r') as F:
        wavlist = [lines.rstrip() for lines in F]           # 360_xxxx.wav
    F.close()

    # Open wav segments list and readlines
    with open(sys.argv[2],'r') as F:
        wav_segment_list = [lines.rstrip() for lines in F]  # 360_xxxx-1.wav, 360_xxxx-2.wav, etc
    F.close()

    # For each wavfile, open each of its segments
    for i in range(len(wavlist)):
        wav_id = path.splitext(path.basename(wavlist[i]))[0]
        lyrics = get_lyrics(wav_id, wav2lyric)
        #get wav segments
        wav_segments = [wav_seg for wav_seg in wav_segment_list if wav_seg.startswith(wav_id)]
        #For each segment find set of lyric lines from HVite
        l1 = 0          # lyric starting line number
        l2 = 1          # lyric ending line number
        for j in range(len(wav_segments)):
            #Make mlf for each line
            segment_name = path.splitext(wav_segments[j])[0]
            make_mlf(segment_name, [])      # initial pau
            prev_likelihood = float(get_likelihood(segment_name))
            if classify_silence(segment_name):
            #    print(segment_name)
                continue
            lyric_segment = lyrics[l1:l2]
            make_mlf(segment_name, lyric_segment)
            likelihood = get_likelihood(segment_name)
            if (likelihood == 'final'): #No tokens survived error
                print('Did not perform segm alignment on ',wav_id, ': No tokens survived')
                break
            likelihood = float(likelihood)
            if (prev_likelihood>likelihood):
                make_mlf(segment_name, [])
                continue
            while (likelihood>prev_likelihood):
                prev_likelihood = likelihood
                l2 += 1
                lyric_segment = lyrics[l1:l2]
                make_mlf(segment_name, lyric_segment)
                likelihood = float(get_likelihood(segment_name))
            lyric_segment = lyrics[l1:l2-1]
            make_mlf(segment_name, lyric_segment)
            l1 = l2-1
        print("name: ", wav_id," Length of lyrics ",len(lyrics)," End of lyric line in last segment ", l2)          


if __name__ == "__main__":
    main()
