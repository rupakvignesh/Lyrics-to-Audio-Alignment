from __future__ import print_function
import msaf
import numpy as np
import scipy.io.wavfile as wavfile
import os, sys
import os.path as op

def main(wavlist, outdir):
    for f in wavlist:
        if f.endswith('.wav'):
            print("processing {}".format(f))
            boundaries, _ = msaf.process(f)
            rate, data = wavfile.read(f)
            for b_ind in xrange(1, len(boundaries)):
                segment = data[int(np.round(rate*(boundaries[b_ind - 1]))):int(round(rate*(boundaries[b_ind])))]
                outfilename = op.join(outdir,
                                      "{}-{}.wav".format(op.splitext(op.basename(f))[0], b_ind))
                wavfile.write(outfilename, rate, segment)
                print("{} created.".format(outfilename))

if __name__ == '__main__':
    wavdir = sys.argv[1]
    outdir = sys.argv[2]
    files = [op.join(wavdir, f) for f in os.listdir(wavdir)]
    main(files, outdir)
