#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse, os
parser = argparse.ArgumentParser(description='Process EC Data Files.')
parser.add_argument('filenames', nargs='*',  help="The file(s) to parse.")
parser.add_argument('--format', help="The format of the file, e.g. 'allcurves'", default = 'allcurves', choices= ['allcurves'])
parser.add_argument('--hdf', help="the HDF5 file")
#parser.add_argument('--init', help="initializes the HDF5 data store for the given format", action='store_true')
parser.add_argument('--read', help="reads the contents", action = 'store_true')
args = parser.parse_args()

def read_allcurves(files):
    r"""
    N = conductor
    C = isogeny class (letter(s))
    # = number of curve in class = 1 (except for 990h3)
    curve = curve coefficients in format [a1,a2,a3,a4,a6]
    r = rank
    t = order of torsion
    """

    import tables
    hdf_store = tables.openFile(args.hdf, 'w')
    allcurves = hdf_store.createGroup(hdf_store.root, 'allcurves')
    from scheme import EC_Curve_1
    table = hdf_store.createTable(allcurves, "table", EC_Curve_1)
    print table
    print hdf_store

    entry = table.row

    for fn, f in files.iteritems():
        print 'parsing "%s" …' % fn
        for line in f:
            N, C, nb, coeff, r, t = line.rstrip().split(' ')
            coeff = map(int, coeff[1:-1].split(','))
            N, nb, r, t = map(int, (N, nb, r, t))
            #print N, C, nb, coeff, r, t
            assert r >= 0 and t >= 0 and N >= 0 and C >= 0 and len(C) <= 3 and  nb >= 0, line

            # adding the data
            entry['conductor'] = N
            entry['isogeny']   = C
            entry['nb']        = nb
            entry['rank']      = r
            entry['torsion']   = t
            entry['coefficient/a1'] = coeff[0]
            entry['coefficient/a2'] = coeff[1]
            entry['coefficient/a3'] = coeff[2]
            entry['coefficient/a4'] = coeff[3]
            print N, C, nb, r, t
            print coeff[4]
            entry['coefficient/a6'] = coeff[4]
            entry.append()
    table.flush()


def read_allcurves_hdf():
    import tables
    hdf_store = tables.openFile(args.hdf, 'r')
    print hdf_store.root.allcurves
    table = hdf_store.root.allcurves.table
    for row in table.where('''(conductor > 3092) & (conductor < 3100)'''):
        print row['conductor'], row['isogeny'], row['nb'], row['rank'], row['torsion'], \
              '[', row['coefficient/a1'], row['coefficient/a2'], row['coefficient/a3'], row['coefficient/a4'], row['coefficient/a6'], ']'

if __name__ == '__main__':
    print args.format
    assert args.format == 'allcurves'

    files = {}
    try:
        for fn in args.filenames:
            f = os.path.split(fn)[-1]
            files[f] = open(fn, 'r')
    except:
        print "file not found"
        exit(1)

    if len(args.filenames) > 0:
        read_allcurves(files)
    if args.read:
        read_allcurves_hdf()

