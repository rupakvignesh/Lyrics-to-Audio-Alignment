"""
Converts lyrics (*.txt) files to 
HTK word level Master Label format (*.mlf)
and a word to phone dict.
Both Lyrics and MLF file do not have 
timing information. Adds a pause after every word.

Set lyrics path and t2p path
Args: lyrics_list
output: lists/lyrics.mlf

Author: Rupak Vignesh
"""

import os, sys, subprocess

lyrics_path = '/Users/RupakVignesh/Desktop/7100/Lyrics-to-Audio-Alignment/Damp_Dataset/Lyrics/'
T2P = '/Users/RupakVignesh/Documents/flite-1.4-release/bin/t2p' 
lyric_list_file = sys.argv[1]

with open(lyric_list_file) as L:
    lyric_list = [lines.rstrip() for lines in L]

lyrics_mlf = open("lists/lyrics.mlf",'a')
lyrics_mlf.write("#!MLF!#"+"\n")				# MLF header
word_phone_dict = open("lists/words_to_phone_dict",'a')

for i in range(len(lyric_list)):
    LF = open(os.path.join(lyrics_path,lyric_list[i]))
    lyrics_mlf.write("*/"+lyric_list[i] + '\n')

    lyric_content = []
    for word in LF.read().split():				# Reads and splits into words
        lyric_content.extend([word])

    phonemes_out = [] 
    for j in range(len(lyric_content)):
        lyric_content[j] = ''.join(e for e in lyric_content[j] if e.isalnum())				#Removes special charachters
        print lyric_content[j]
        shell_out = subprocess.Popen([T2P + " " + lyric_content[j]],stdout = subprocess.PIPE, shell = True)	#Output to the terminal is writter
        phonemes_out.extend([shell_out.communicate()[0]])
        phonemes_out[j] = phonemes_out[j].replace("pau ", "", 1)
        lyrics_mlf.write(lyric_content[j]+"\n")
        word_phone_dict.write(lyric_content[j] + " " + phonemes_out[j]+'\n')
#    os.system("sort lists/words_to_phone_dict -u -o lists/words_to_phone_dict")
    lyrics_mlf.write(".\n") 
    

