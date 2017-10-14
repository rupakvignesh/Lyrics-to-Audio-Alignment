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
            boundaries, labels = msaf.process(f, boundaries_id="sf",
                                              labels_id="vmo",feature="mfcc")
            labels = [int(l) for l in labels]

            # conglomerate boundaries by label
            new_boundaries = [boundaries[0]]
            new_labels = [labels[0]]
            for i in xrange(1, len(labels)):
                if labels[i] == labels[i-1]:
                    continue
                new_boundaries.append(boundaries[i])
                new_labels.append(labels[i])
            boundaries = new_boundaries
            labels = new_labels

            # read wavfile, parse out segments
            rate, data = wavfile.read(f)
            segments = []
            for b_ind in xrange(1, len(boundaries)):
                seg_start = int(np.round(rate*(boundaries[b_ind - 1])))
                seg_end = int(np.round(rate*(boundaries[b_ind])))
                segments.append(data[seg_start:seg_end])

            assert len(segments) + 1 == len(boundaries) == len(labels)

            # merge short segments
            new_segments = [segments[0]]
            new_boundaries = [boundaries[0]]
            new_labels = [labels[0]]
            for i in xrange(1, len(segments)):
                seg = segments[i]
                if len(seg) < rate*MIN_SEG_LEN:
                    new_segments[i-1] = np.concatenate((new_segments[i-1], seg), axis=0)
                else:
                    new_segments.append(seg)
                    new_labels.append(labels[i])
                    new_boundaries.append(labels[i])

            if len(new_segments[0]) < rate*MIN_SEG_LEN:
                new_segments[1] = np.concatenate((new_segments[0], new_segments[1]), axis=0)
                new_boundaries[1] = new_boundaries[0]
                new_segments = new_segments[1:]
                new_boundaries = new_boundaries[1:]
                new_labels = new_labels[1:]

            segments = new_segments
            boundaries = new_boundaries
            labels = new_labels

            for i in xrange(len(segments)):
                outfilename = "{}-clip-{}-label-{}.wav".format(op.splitext(op.basename(f))[0],
                                                               i, labels[i])
                outpath = op.join(outdir, outfilename)
                wavfile.write(outpath, rate, segments[i])
                print("{} created.".format(outfilename))


if __name__ == '__main__':
    wavdir = sys.argv[1]
    outdir = sys.argv[2]
    files = [op.join(wavdir, f) for f in os.listdir(wavdir)]
    main(files, outdir)
