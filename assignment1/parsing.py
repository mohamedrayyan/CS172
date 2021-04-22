import re
import os
import zipfile
from collections import Counter

def readDocs():
    i = 0
    global documents
    # Regular expressions to extract data from the corpus
    doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
    docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
    text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

    with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
        zip_ref.extractall()

    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if
                    (filename != "readme" and filename != ".DS_Store")]

    for file in allfiles:
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
                if i == 0:
                    i = 1
                result = cleanstr(text.lower())
                dhash = mhash(docno)
                documents[dhash] = {'distinct': calcstats(result, dhash), 'total': len(result)}

                # step 2 - create tokens
                # step 3 - build index
    writeTermIndex()Index()

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
            tokens[ihash] = {'documents': {dhash: {'frequency': 1, 'position': [i + 1]}}, 'frequency': 0}
        elif dhash not in tokens[ihash]['documents']:
            tokens[ihash]['documents'][dhash] = {'frequency': 1, 'position': [i + 1]}
        else:
            tokens[ihash]['documents'][dhash]['frequency'] += 1
            tokens[ihash]['documents'][dhash]['position'].append(i + 1)

        tokens[ihash]['frequency'] += 1

    return len(Counter(list).keys())

def mhash(text):
    return ''.join(str(ord(c)) for c in text.upper())
    # return hashlib.md5(text.encode()).hexdigest()

def writeTermIndex():
    tindx =open('term_index.txt', 'w')
    tinfo =open('term_info.txt', 'w')

    line =''
    for k in tokens.keys():
        line =k
        for i in tokens[k]['documents'].keys():
            line +='   ' +str(i) +':'
            for p in tokens[k]['documents'][i]['position']:
                # line +='\t' +str(i) +':' +str(p)
                line +=str(p) +' '
        tinfo.write(k + ' ' +str(tindx.tell()) +' ' +str(tokens[k]['frequency']) +' '+str(len(tokens[k]['documents'].keys())) +'\n')
        tindx.write(line[:-1] +'\n')
    tindx.close()
    tinfo.close()

def readtermIndex(inline):
    my_file = open("test.txt", "r")
    content = my_file.readlines()
    content = re.sub(r':', " ", content[inline]) #any index will be the line number
    content_list = content.split('   ')
    my_file.close()

    freq = 0
    tokens[content_list[0]] = {'documents':{},'frequency':0}
    for i in range(1,len(content_list)):
        l = content_list[i].split(' ')
        tokens[content_list[0]]['documents'][l[0]] = {'frequency':0, 'position': []}
        for k in range(1, len(l)):
             tokens[content_list[0]]['documents'][l[0]]['position'].append(l[k])
        tokens[content_list[0]]['documents'][l[0]]['frequency'] = len(l)-1
        freq += len(l)-1

    tokens[content_list[0]]['frequency'] = freq

    # for p in tokens.keys():
    #     print(tokens[p],"\n")

def run():
    pass

documents = {}
tokens = {}
stopwords = readStopWords()

readDocs()

#94395
# words in quotes don't work
# add words following 't to stopwords.txt
# period in front of word doesn't work

# tmp =['123456789', '2525:25 15', '535:55 530']

# haha =['2525', '25', '15']