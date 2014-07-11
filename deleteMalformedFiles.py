import hashlib
import json
import sys
import urllib2
import os
import subprocess
origin = urllib2.urlopen('http://chroniclingamerica.loc.gov/ocr.json')

file = json.loads(origin.read())

docs = file['ocr']


print "Comparing expected and actual checksums for every download: each dot represents a successful file."

def checksum(filename):
    output = subprocess.check_output(["sha1sum",filename])
    return output.split(" ")[0]
    
for doc in docs:
    try:
        name = doc['name']
        original = doc['sha1']
        downloaded = checksum("downloads/"+name)
        if original != downloaded:
            print "\nREMOVING " + name
            os.remove("downloads/" + name)
        else:
            sys.stdout.write(".")
    except:
        print "problem with "
        print doc

