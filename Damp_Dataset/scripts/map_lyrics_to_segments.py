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
    return commands.getstatusoutput('HVite -T 1 -a -m -o MN -H hmm_with_er/hmm7/hmmdefs -I Audio_segments/'+segment_name+'.mlf lists/dict lists/phonelist mfc_train/dr1_fcjf0_sa1.mfc | tail -1 | rev | cut -d " " -f4 | rev')[1]

def make_mlf(wav_segment_name,lyric_lines):
    """
    Write word by word in a MLF file.
    """
    words = str.split(lyric_line)
    F = open('Audio_segments/'+wav_segment_name+'.mlf','w')
    F.write('#!MLF!#')
    F.write('"*/'+wav_segment_name+'.mlf"\n')
    F.write("pau\n")
    for i in range(len(words)):
        F.write(words[i]+'\n')
        F.write("pau\n")
    F.write(".")
    F.close()


def main():
    # Create a wav2lyric dictionary
    with open('lists/train_lyricid_songid_map.txt','r') as F:
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
        wavlist = [lines.rstrip() for lines in F]
    F.close()

    # Open wav segments list and readlines
    with open(sys.argv[2],'r') as F:
        wav_segment_list = [lines.rstrip() for lines in F]
    F.close()

    # For each wavfile, open each of its segments
    for i in range(len(wavlist)):
        wav_id = path.splitext(path.basename(wavlist[i]))[0]
        lyrics = get_lyrics(wav_id, wav2lyric)
        #get wav segments
        wav_segments = [wav_seg for wav_seg in wav_segment_list if wav_seg.startswith(wav_id)]
        #For each segment find set of lyric lines from HVite
        l1 = 0
        l2 = 1
        for j in range(len(wav_segments)):
            #Make mlf for each line
            segment_name = path.splitext(wav_segments[i])[0]

            prev_likelihood = -10000
            lyric_segment = []
            lyric_segment.append(lyrics[l1:l2])
            make_mlf(segment_name, lyric_segment)
            likelihood = get_likelihood(segment_name)
            while (likelihood>prev_likelihood):
                l2 += 1
                lyric_segment.append(lyric_segment[l1:l2])
                make_mlf(segment_name, lyric_segment)
                likelihood = get_likelihood(segment_name)
            make_mlf(segment_name, lyric_segment)
            l1 = l2
            l2 += 1





if __name__ == "__main__":
    main()
