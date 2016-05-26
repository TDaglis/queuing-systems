#!/usr/bin/env python
import sys

from simulation import simulate

if __name__ == '__main__':
    if len(sys.argv) == 1 or 'help' in sys.argv:
        print 'Usage:\n {} l(=1,1.5,2) k(=1,2,...,9)\n'.format(sys.argv[0])
        sys.exit(0)
    elif len(sys.argv) != 3:
        print 'Error. Exactly 2 arguments are required.\n' +\
        'Example: ./simulation.py 1.5 7'
        sys.exit(1)
    simulate(float(sys.argv[1]), int(sys.argv[2]))
