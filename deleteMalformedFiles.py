import hashlib
import json
import urllib2
import os

origin = urllib2.urlopen('http://chroniclingamerica.loc.gov/ocr.json')

file = json.loads(origin.read())

docs = file['ocr']


def checksum(filename):
"""
code from http://www.pythoncentral.io/hashing-files-with-python/
"""
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

for doc in docs:
    try:
        name = doc['name']
        original = doc['sha1']
        downloaded = checksum("downloads/"+name)
        if original != downloaded:
            print "removing " + name
            os.remove("downloads/" + name)
        else:
            print name + " checks out OK"
    except:
        print "problem with "
        print doc

