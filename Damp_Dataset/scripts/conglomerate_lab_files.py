"""
grab all files with similar names, and then rewrite all the files with
extensions such that they include offsets from the previous files. Prior
to the writing of this script, I think the case is that each file starts
at around 0
"""
import os
import os.path as op
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--in_dir', help="directory from which to concatenate .lab files")
parser.add_argument('-o', '--out_dir', help="directory in which to place conglomerated .lab files")
args = parser.parse_args()

name_dict = {}
for filename in os.listdir(args.in_dir):
    print('sorting {}'.format(filename))
    parts = filename.split('.')[0].split('-')
    assert len(parts) == 3
    if parts[0] not in name_dict:
        name_dict[parts[0]] = []
    name_dict[parts[0]].append({'filename': filename,
                                'basename': parts[0],
                                'segment_num': parts[1],
                                'label': parts[2]})

for name in name_dict.keys():
    print('writing %s'%(op.join(args.out_dir, name + '.lab')))
    outfile = open(op.join(args.out_dir, name + '.lab'), 'w')
    name_dict[name].sort(key=lambda x: x['segment_num'])
    curr_offset = 0
    for segment in name_dict[name]:
        print('processing segment %d'%int(segment['segment_num']))
        seglines = [line.strip() for line in open(
            op.join(args.in_dir, segment['filename']), 'r').readlines()]
        for line in seglines:
            start, end, lyric = line.split()
            outfile.write('{} {} {}\n'.format(int(start) + curr_offset,
                                              int(end) + curr_offset, lyric))
        curr_offset = int(end) + curr_offset
    outfile.close()
