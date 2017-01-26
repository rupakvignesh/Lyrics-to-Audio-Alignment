"""
Converts lyrics (*.txt) files to 
HTK word level Master Label format (*.mlf)
and a word to phone dict.
Both Lyrics and MLF file do not have 
timing information. Adds a pause after every word.

Set lyrics path and t2p path
Args: lyrics_list
output: words_to_phone_dict, lyrics.mlf

Author: Rupak Vignesh
"""

import os, sys, subprocess

damp_path = '/Users/RupakVignesh/Desktop/7100/Lyrics-to-Audio-Alignment/Damp_Dataset/'
lyrics_path = damp_path+'Lyrics/'
T2P = '/Users/RupakVignesh/Documents/softwares/flite-1.4-release/bin/t2p' 
lyric_list_file = sys.argv[1]					# list (360_21740786, 360_4127898, ...)

with open(lyric_list_file) as L:
    lyric_list = [lines.rstrip() for lines in L]

with open(damp_path+"lists/test_lyricid_songid_map.txt",'r') as LS:
    lyricid_songid = [lines.rstrip() for lines in LS]		# list containint lyricidi(lyric_01001) and songid(360_21740786)

lyricid_songid_parsed = []
for i in range(len(lyricid_songid)):
    lyricid_songid_parsed.extend([str.split(lyricid_songid[i])])

def get_lyric_id(songid):
    for i,j in enumerate(lyricid_songid_parsed):
        if j[1] == songid:
            return j[0]						# j[0] is lyric id

#print get_lyric_id(lyric_list[0])

lyrics_mlf = open(damp_path+'test_lyrics.mlf','a')
lyrics_mlf.write("#!MLF!#"+"\n")				# MLF header
word_phone_dict = open(damp_path+"words_to_phone_dict",'a')

for i in range(len(lyric_list)):
    songid = lyric_list[i]
    lyric_id = get_lyric_id(songid) + ".txt"
    LF = open(os.path.join(lyrics_path,lyric_id))
    lyrics_mlf.write('"*/'+ songid + '.lab"\n')
    lyrics_mlf.write("pau\n")					# Initial silence
    print str(i+1)
    lyric_content = []
    for word in LF.read().split():				# Reads and splits into words
        lyric_content.extend([word])

    phonemes_out = [] 
    for j in range(len(lyric_content)):
        lyric_content[j] = ''.join(e for e in lyric_content[j] if e.isalnum())				#Removes special charachters
        #print lyric_content[j]
        shell_out = subprocess.Popen([T2P + " " + lyric_content[j]],stdout = subprocess.PIPE, shell = True)	#Output to the terminal is writter
        phonemes_out.extend([shell_out.communicate()[0]])
        phonemes_out[j] = phonemes_out[j].replace("pau ", "") 						# Replaces pause. Use ("pau ", "", 1) to replace the first pause only.
        phonemes_out[j] = ''.join(e for e in phonemes_out[j] if not e.isdigit())			# Remove stress markers
        lyrics_mlf.write(lyric_content[j]+"\n")								# Write words to mlf
        lyrics_mlf.write("pau\n")
        word_phone_dict.write(lyric_content[j] + " " + phonemes_out[j]+'\n')				# write words to phones 
    lyrics_mlf.write(".\n") 
    

