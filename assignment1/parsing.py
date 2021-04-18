import re
import os
import zipfile
import hashlib
from collections import Counter

def readDocs():
    i =0
    global documents
    # Regular expressions to extract data from the corpus
    doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
    docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
    text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)


    with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
        zip_ref.extractall()

    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]

    for file in allfiles:
        with open(file, 'r', encoding='ISO-8859-1') as f:
            filedata = f.read()
            result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

            for document in result[0:]:
                # Retrieve contents of DOCNO tag
                docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
                # Retrieve contents of TEXT tag
                text = "".join(re.findall(text_regex, document))\
                          .replace("<TEXT>", "").replace("</TEXT>", "")\
                          .replace("\n", " ")

                # step 1 - lower-case words, remove punctuation, remove stop-words, etc.
                if i ==0:
                    i =1
                    result =cleanstr(text.lower())
                    dhash =md5Hash(docno)
                    print(len(Counter(result).keys()))
                    documents[dhash] ={'disticnt': calcstats(text, dhash), 'total': len(result)}

                # step 2 - create tokens
                # step 3 - build index


def readStopWords():
    f =open("stopwords.txt", "r")
    return [x.strip() for x in f]

def cleanstr(text):
    pattern = r'\w+(\.?\w+)*'
    result =[]

    # for i in text.split():
    for i in re.findall(r"[a-z0-9'.@#]+\S", text):
        loc =(re.match(pattern, i))

        if loc:
            result.append(loc.group())

    return [x for x in result if x not in stopwords]

def calcstats(list, dhash):
    global tokens
    distinct =0

    for i in range(len(list)):
        ihash =md5Hash(list[i])

        if ihash not in tokens:
            tokens[ihash] ={'documents': {dhash: {'frequency': 1, 'position': [i+1]}}, 'frequency': 1}
            distinct +=1
        else:
            tokens[ihash]['frequency'] +=1
            tokens[ihash]['documents'][dhash]['frequency'] +=1
            tokens[ihash]['documents'][dhash]['position'].append(i+1)

    return distinct

def md5Hash(text):
    return hashlib.md5(text.encode()).hexdigest()

documents ={}
tokens ={}
stopwords =readStopWords()

readDocs()

print(documents)
print()
print()
print(tokens)