import re
import os
import zipfile
from collections import Counter

def readDocs():
    global documents

    with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
        zip_ref.extractall()

    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if
                    (filename != "readme" and filename != ".DS_Store")]

    for file in allfiles:
        readDoc(file)

    writeIndex()

def readDoc(file):
    # Regular expressions to extract data from the corpus
    doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
    docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
    text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document)) \
                .replace("<TEXT>", "").replace("</TEXT>", "") \
                .replace("\n", " ")

            # step 1 - lower-case words, remove punctuation, remove stop-words, etc.
            # step 2 - create tokens
            # step 3 - build index
            result = cleanstr(text.lower())
            dhash = mhash(docno)
            documents[dhash] = {'distinct': calcstats(result, dhash), 'total': len(result)}

def readStopWords():
    f = open("stopwords.txt", "r")
    return [x.strip() for x in f]

def cleanstr(text):
    pattern = r'\w+(\.?\w+)*'
    result = []

    # for i in text.split():
    for i in re.findall(r"[a-z0-9'.@#]+\S", text):
        loc = (re.match(pattern, i))

        if loc:
            result.append(loc.group())

    return [x for x in result if x not in stopwords]

def calcstats(list, dhash):
    global tokens

    for i in range(len(list)):
        ihash = mhash(list[i])

        if ihash not in tokens:
            tokens[ihash] = {'documents': {dhash: {'frequency': 1, 'position': [i + 1]}}, 'docnum': 0, 'frequency': 0}
        elif dhash not in tokens[ihash]['documents']:
            tokens[ihash]['documents'][dhash] = {'frequency': 1, 'position': [i + 1]}
        else:
            tokens[ihash]['documents'][dhash]['frequency'] += 1
            tokens[ihash]['documents'][dhash]['position'].append(i + 1)

        tokens[ihash]['frequency'] += 1
        tokens[ihash]['docnum'] =len(tokens[ihash]['documents'])

    return len(Counter(list).keys())

def mhash(text):
    return ''.join(str(ord(c)) for c in text.upper())
    # return hashlib.md5(text.encode()).hexdigest()

def writeIndex():
    tindx =open('term_index.txt', 'w')
    tinfo =open('term_info.txt', 'w')

    line =''
    for k in tokens.keys():
        line =k
        for i in tokens[k]['documents'].keys():
            line +='   ' +str(i) +':'
            for p in tokens[k]['documents'][i]['position']:
                line +=str(p) +' '
            line =line[:-1]
        tinfo.write(k + ' ' +str(tindx.tell()) +' ' +str(tokens[k]['frequency']) +' '+str(len(tokens[k]['documents'].keys())) +'\n')
        # tindx.write(line[:-1] +'\n')
        tindx.write(line +'\n')
    tindx.close()
    tinfo.close()

def readTermIndex(inline):
    my_file = open("term_index.txt", "r")

    my_file.seek(inline)
    content =my_file.readline()

    my_file.close()

    content =re.sub(r':', ' ', content)
    content =content.rstrip('\n')

    content_list =content.split('   ')

    for i in range(1,len(content_list)):
        l =content_list[i].split(' ')
        tokens[content_list[0]]['documents'][l[0]] ={'frequency': 0, 'position': []}
        for k in range(1, len(l)):
            tokens[content_list[0]]['documents'][l[0]]['position'].append(int(l[k]))
        tokens[content_list[0]]['documents'][l[0]]['frequency'] =len(l)-1

def readTermInfo():
    f =open('term_info.txt', 'r')

    for line in f.readlines():
        linesplit =line.split(' ')

        tokens[linesplit[0]] = {'documents': {}, 'offset': int(linesplit[1]), 'docnum': int(linesplit[2]), 'frequency': int(linesplit[3])}

    f.close()

def run():
    if os.path.exists('term_info.txt') and os.path.exists('term_index.txt'):
        readTermInfo()
    else:
        readDocs()

#94395
# words in quotes don't work
# add words following 't to stopwords.txt
# period in front of word doesn't work


def termlookup(term):
    thash =mhash(term)

    print('Listing for term: {}'.format(term))
    print('TERMID: {}'.format(thash))
    print('Number of documents containing term: {}'.format(tokens[thash]['docnum']))
    print('Term frequency in corpus: {}'.format(tokens[thash]['frequency']))

def doclookup(doc):
    dhash =mhash(doc)

    if dhash not in documents:
        readDoc('ap89_collection_small/'+doc.split('-')[0].lower())

    print('Listing for document: {}'.format(doc))
    print('DOCID: {}'.format(dhash))
    print('Distinct terms: {}'.format(documents[dhash]['distinct']))
    print('Total terms: {}'.format(documents[dhash]['total']))

def lookUp(term, doc):
    thash =mhash(term)
    dhash =mhash(doc)

    if tokens[thash]['documents'] =={}:
        readTermIndex(tokens[thash]['offset'])

    print('Inverted list for term: {}'.format(term))
    print('In document: {}'.format(doc))
    print('TERMID: {}'.format(thash))
    print('DOCID: {}'.format(dhash))
    print('Term frequency in document: {}'.format(tokens[thash]['documents'][dhash]['frequency']))
    print('Positions: {}'.format(tokens[thash]['documents'][dhash]['position']))


documents = {}
tokens = {}
stopwords = readStopWords()

run()