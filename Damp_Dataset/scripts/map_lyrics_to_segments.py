import sys, commands
import numpy as np
import os.path as path

"""
likelihood = commands.getstatusoutput('HVite -T 1 -a -m -o MN -H hmm_with_er/hmm7/hmmdefs -I segments.mlf lists/dict lists/phonelist mfc_train/dr1_fcjf0_sa1.mfc | tail -1 | rev | cut -d " " -f4 | rev')[1]
"""
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
    return commands.getstatusoutput('HVite -T 1 -a -m -o MN -H timit_4s_4m/hmmdefs -I Audio_test_segmentation/'+segment_name+'.mlf words_to_phone_dict lists/phonelist '+'Audio_test_segmentation/'+segment_name+'.mfc | tail -1 | rev | cut -d " " -f4 | rev')[1]

def make_mlf(wav_segment_name,lyric_lines):
    """
    Write word by word in a MLF file.
    """
    words = [str.split(i) for i in lyric_lines]
    words = [j for i in range(len(words)) for j in words[i]]
    words = [s.replace(',','') for s in words]
    words = [s.replace('.','') for s in words]
    F = open('Audio_test_segmentation/'+wav_segment_name+'.mlf','w')
    F.write('#!MLF!#\n')
    F.write('"*/'+wav_segment_name+'.lab"\n')
    F.write("pau\n")
    for i in range(len(words)):
        F.write(words[i]+'\n')
        F.write("pau\n")
    F.write(".\n")
    F.close()


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
            prev_likelihood = get_likelihood(segment_name)
            lyric_segment = lyrics[l1:l2]
            make_mlf(segment_name, lyric_segment)
            likelihood = get_likelihood(segment_name)
            print (prev_likelihood, likelihood)
            if (prev_likelihood>likelihood):
                continue
            while (likelihood>prev_likelihood):
                prev_likelihood = likelihood
                l2 += 1
                lyric_segment = lyrics[l1:l2]
                make_mlf(segment_name, lyric_segment)
                likelihood = get_likelihood(segment_name)
            lyric_segment = lyrics[l1:l2-1]
            make_mlf(segment_name, lyric_segment)
            l1 = l2-1


if __name__ == "__main__":
    main()
