import sys
import csv
from os import listdir
from os.path import isdir, join, isfile
from hitlist_reader import HitlistReader
from metrics import *

__author__ = 'ignacio'


HIT_SIMBOL = 1
NO_HIT_SIMBOL = 0
RESULTS_WINDOW_SIZE = 10

class Utils:

    def loadMatrix(self, path):
        with open(sys.argv[2], 'rb') as matrix_file:
            print matrix_file.readline()
                
if __name__ == "__main__":
    a = Utils()
    a.loadMatrix("commonNeighbours.out")