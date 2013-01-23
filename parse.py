#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse, os
parser = argparse.ArgumentParser(description='Process EC Data Files.')
parser.add_argument('filenames', nargs='+',  help="The file(s) to parse.")
parser.add_argument('--format', help="The format of the file, e.g. 'allcurves'", default = 'allcurves')
args = parser.parse_args()

files = {}
try:
    for fn in args.filenames:
        f = os.path.split(fn)[-1]
        files[f] = open(fn, 'r')
except:
    print "file not found"
    exit(1)

def read_allcurves(files):
    r"""
    N = conductor
    C = isogeny class (letter(s))
    # = number of curve in class = 1 (except for 990h3)
    curve = curve coefficients in format [a1,a2,a3,a4,a6]
    r = rank
    t = order of torsion
    """
    for fn, f in files.iteritems():
        print 'parsing "%s" …' % fn
        for line in f:
            N, C, nb, coeff, r, t = line.rstrip().split(' ')
            coeff = map(int, coeff[1:-1].split(','))
            N, nb, r, t = map(int, (N, nb, r, t))
            #print N, C, nb, coeff, r, t

if __name__ == '__main__':
    print args.format
    assert args.format == 'allcurves'
    read_allcurves(files)

