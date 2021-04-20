# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.

import sys
from parsing import *

def termlookup(term):
    thash =md5Hash(term.lower())

    print('Listing for term: {}'.format(term))
    print('TERMID: {}'.format(thash))
    print('Number of documents containing term: {}'.format(len(tokens[thash]['documents'])))
    print('Term frequency in corpus: {}'.format(tokens[thash]['frequency']))

def doclookup(doc):
    dhash =md5Hash(doc)

    print('Listing for document: {}'.format(doc))
    print('DOCID: {}'.format(md5Hash(dhash)))
    print('Distinct terms: {}'.format(documents[dhash]['distinct']))
    print('Total terms: {}'.format(documents[dhash]['total']))

def lookUp(term, doc):
    thash =md5Hash(term.lower())
    dhash =md5Hash(doc.lower())

    print('Inverted list for term: {}'.format(term))
    print('In document: {}'.format(doc))
    print('TERMID: {}'.format(thash))
    print('DOCID: {}'.format(dhash))
    print('Term frequency in document: {}'.format(tokens[thash]['documents'][dhash]['frequency']))
    print('Positions: {}'.format(tokens[thash]['documents'][dhash]['position']))

if __name__ == '__main__':
    term =''
    docn =''

    if '--term' in sys.argv:
        term =sys.argv[2]
    if '--doc' in sys.argv:
        docn =sys.argv[4]

    if term !='' and docn !='':
        lookUp(term, docn)
    elif term !='':
        termlookup(term)
    elif docn !='':
        doclookup(docn)
    else:
        print('Parameters not recognized')

