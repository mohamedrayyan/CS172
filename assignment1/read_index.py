# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.

import sys
from parsing import *

if __name__ == '__main__':
    term =''
    docn =''

    if '--term' in sys.argv and '--doc' in sys.argv:
        term =sys.argv[2]
        docn =sys.argv[4]
    elif '--term' in sys.argv:
        term =sys.argv[2]
    elif '--doc' in sys.argv:
        docn =sys.argv[2]

    if term !='' and docn !='':
        lookUp(term, docn)
    elif term !='':
        termlookup(term)
    elif docn !='':
        doclookup(docn)
    else:
        print('Parameters not recognized')

