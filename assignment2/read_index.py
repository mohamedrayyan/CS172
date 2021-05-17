# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.

import sys
from parsing import *

if __name__ == '__main__':
    querylist =''
    outputfile =''

    if(len(sys.argv) <3 or len(sys.argv) >3):
        print('Invalid arguments')
        exit()
    else:
        querylist =sys.argv[1]
        outputfile =sys.argv[2]

        rank(querylist, outputfile)