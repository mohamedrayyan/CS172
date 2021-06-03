# input urlseeds.dat, numpages, numlevels
import requests
from requests.api import get
import bs4
import sys
from elasticsearch import Elasticsearch
from datetime import datetime
import os

def getBodyLinks(body):
    atag =bs4.BeautifulSoup(body, features="lxml", parse_only=bs4.SoupStrainer('a'))
    links =[]
    for a in atag:
        if(a.has_attr('href')) and a['href'][:5] =='https':
            links.append(a['href'])

    return links

def bulkUpload(filename):
    command ='curl -X POST -u elastic:ysnwxOkXJrhrSDFINyQPoBnF "https://cs172-69dc7d.es.us-west1.gcp.cloud.es.io:9243/cs172-index/_bulk" -H "Content-Type: application/x-ndjson" --data-binary @data.json'
    # command ="curl -XGET -u elastic:ysnwxOkXJrhrSDFINyQPoBnF 'https://cs172-69dc7d.es.us-west1.gcp.cloud.es.io:9243/_cluster/health?pretty'"

    os.system(command)
    print()
    print()

if __name__ =='__main__':
    es = Elasticsearch()
    numpages =int(sys.argv[2])
    f =open(sys.argv[1], 'r')

    links =[x.strip() for x in f]

    f.close()

    visited ={}
    datafile ='data.json'
    f =open(datafile, 'w')

    count =0
    for link in links:
        if link not in visited.keys():
            req =requests.get(link)
            content =req.content
            body =bs4.BeautifulSoup(content, features="lxml").find('body')

            links.extend(getBodyLinks(str(body)))

            tmpbody =str(body.get_text())
            tmpbody =tmpbody.replace('"', '\\"')
            tmpbody =tmpbody.replace('\'', '')
            tmpbody =tmpbody.replace('\n', '')

            # f =open(datafile, 'w')
            f.write('{"index":{}}\n')
            f.write('{"html":"' +tmpbody[:500] +'"}\n')
            # f.close()

            # bulkUpload(datafile)

            visited[link] =True

            count +=1
        else:
            pass

        if count ==numpages:
            print(len(links))
            break

    f.close()

    bulkUpload(datafile)