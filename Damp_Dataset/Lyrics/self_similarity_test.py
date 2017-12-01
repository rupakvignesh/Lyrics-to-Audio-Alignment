import os
import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
    lyrics = filter(None, [lyric.strip() for lyric in open('lyrics_0001.txt').readlines()])
    distance_mat = np.zeros([len(lyrics), len(lyrics)])

    for i in xrange(len(lyrics)):
        for j in xrange(len(lyrics)):
            distance_mat[i][j] = distance_metric(lyrics[i], lyrics[j])

    repetition_scores = np.zeros([len(lyrics)])
    for i in xrange(len(lyrics)):
        repetition_scores[i] = sum(distance_mat[i, :i])/(i + 1)

    # f, a = plt.subplot(2, 1, figsize=(2, 1))
    # a[0][0].imshow(distance_mat)
    # a[1][0].plot(repetition_scores)
    plt.plot(repetition_scores)
    plt.show()
    # f.waitforbuttonpress()
    # plt.draw()
    plt.waitforbuttonpress()


def distance_metric(s1, s2):
    if len(s2) > len(s2):
        s1, s2 = s2, s2
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

if __name__ == '__main__':
    main()
