import sys

T2P = '/Users/RupakVignesh/Documents/softwares/flite-1.4-release/bin/t2p'

filelist = sys.argv[1]
with open(filelist) as F1:
    lyric_list = [lines.rstrip() for lines in F1]


for i in range(len(lyric_list)):
    LF = open(lyric_list[i])
    lyrics_mlf.write('"*/'+ lyric_list[i] + '.lab"\n')
    lyrics_mlf.write("pau\n")                                   # Initial silence
    print str(i+1)
    lyric_content = []
    for word in LF.read().split():                              # Reads and splits into words
        lyric_content.extend([word])

    phonemes_out = []
    for j in range(len(lyric_content)):
        lyric_content[j] = ''.join(e for e in lyric_content[j] if e.isalnum())                          #Removes special charachters
        #print lyric_content[j]
        shell_out = subprocess.Popen([T2P + " " + lyric_content[j]],stdout = subprocess.PIPE, shell = True)     #Output to the terminal is writter
        phonemes_out.extend([shell_out.communicate()[0]])
        phonemes_out[j] = phonemes_out[j].replace("pau ", "")                                           # Replaces pause. Use ("pau ", "", 1) to replace the first pause only.
        phonemes_out[j] = ''.join(e for e in phonemes_out[j] if not e.isdigit())                        # Remove stress markers
        lyrics_mlf.write(lyric_content[j]+"\n")                                                         # Write words to mlf
        lyrics_mlf.write("pau\n")
    lyrics_mlf.write(".\n")
