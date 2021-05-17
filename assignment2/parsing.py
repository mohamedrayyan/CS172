import re
import os
import zipfile
from collections import Counter
from numpy import log as ln
from math import sqrt as sqrt

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

    IDF(tokens)

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
            result = cleanstr(text)
            # dhash = mhash(docno)
            documents[docno] =TF(result, tokens)

def readQueries(file):
    f =open(file)
    queries =[]

    for i in f:
        queries.append(cleanstr(i))

    f.close()

    return queries

def readStopWords():
    f = open("stopwords.txt", "r")
    return [x.strip() for x in f]

def cleanstr(text):
    pattern = r'\w+(\.?\w+)*'
    result = []
    text =text.lower()

    # for i in text.split():
    for i in re.findall(r"[a-z0-9'.@#]+\S", text):
        loc = (re.match(pattern, i))

        if loc:
            result.append(loc.group())

    return [x for x in result if x not in stopwords]

def TF(list, tokens):
    doc ={}

    counted =Counter(list)
    for i in counted:
        ihash = mhash(i)

        doc[ihash] =counted[i] /len(list)

        if ihash not in tokens:
            tokens[ihash] ={'docfreq': 1}
        else:
            tokens[ihash]['docfreq'] +=1

    return doc

def IDF(tokens):
    for k in tokens.keys():
        tokens[k]['idf'] =(1+ln(len(documents.keys()) /tokens[k]['docfreq']))

def qTFIDF(list):
    doc ={}

    counted =Counter(list)
    for i in counted:
        ihash =mhash(i)

        doc[ihash] =counted[i] *tokens[ihash]['idf']
    return doc

def mhash(text):
    return ''.join(str(ord(c)) for c in text.upper())
    # return hashlib.md5(text.encode()).hexdigest()

def run():
    readDocs()

def rank(querylist, outputfile):
    queries =readQueries(querylist);
    f =open(outputfile, 'w')

    for q in queries:
        qtfidf =qTFIDF(q[1:])
        result ={}
        for k in documents:
            numer =0
            qdeno =0
            ddeno =0
            for i in qtfidf:
                if i in documents[k]:
                    numer +=(qtfidf[i] *(documents[k][i] *tokens[i]['idf']))
                    ddeno +=(documents[k][i] *tokens[i]['idf']) **2
                qdeno +=qtfidf[i] **2
            # result[k] =numer /(sqrt(qdeno) *sqrt(ddeno))
            if ddeno ==0:
                result[k] =0
            else:
                result[k] = numer / (sqrt(qdeno) * sqrt(ddeno))
        result =sorted(result.items(), key=lambda x: x[1], reverse=True)

        counter =1
        for i in result[:10]:
            line =str(q[0])  +' Q0 ' +str(i[0]) +' ' +str(counter) +' ' +str(i[1]) +' EXP' +'\n'
            f.write(line)

            counter +=1
    f.close()

documents = {}
tokens = {}
stopwords = readStopWords()

run()