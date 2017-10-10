from __future__ import print_function
import msaf
import numpy as np
import scipy.io.wavfile as wavfile
import os, sys
import os.path as op

MIN_SEG_LEN = 1  # seconds

def main(wavlist, outdir):
    for f in wavlist:
        if f.endswith('.wav'):
            print("processing {}".format(f))
            boundaries, _ = msaf.process(f)
            rate, data = wavfile.read(f)
            buff = None
            segcnt = 1
            import pdb
            pdb.set_trace()
            for b_ind in xrange(1, len(boundaries)):
                segment = data[int(np.round(rate*(boundaries[b_ind - 1]))):int(round(rate*(boundaries[b_ind])))]
                if buff is None:
                    buff = segment
                else:
                    buff = np.concatenate((buff, segment), axis=0)
                if len(buff) > rate*MIN_SEG_LEN:
                    outfilename = op.join(outdir,
                                          "{}-{}.wav".format(
                                              op.splitext(op.basename(f))[0],
                                              segcnt))
                    wavfile.write(outfilename, rate, buff)
                    print("{} created.".format(outfilename))
                    segcnt += 1
                    buff = None

if __name__ == '__main__':
    wavdir = sys.argv[1]
    outdir = sys.argv[2]
    files = [op.join(wavdir, f) for f in os.listdir(wavdir)]
    main(files, outdir)
