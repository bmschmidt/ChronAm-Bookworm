import tarfile
import os
import re

class tarballExtractor(object):
    def __init__(self,filename,printFullFileText=True):
        self.input = tarfile.open(filename)
        self.printFullFileText=printFullFileText
    def __iter__(self):
        return self
    def next(self):
        info = self.input.next()
        try:
            name = info.name
        except AttributeError:
            raise StopIteration
        if name[-1:-5:-1]=="txt.":
            #ie, the last four characters are '.txt'; skips directories and XML files.
            name=name[:-4]
            content = self.input.extractfile(info).read()
            return name + "\t" + re.sub("\n"," ",content)
        else:
            #if it's not text, recurse through the next line.
            #May break by recursion limit if the file contains a
            #string of almost no (way less than 1%) .txt files.
            return next(self)

def printDirectory(dirname,printFullFileText=True):
    files = os.listdir(dirname)
    for file in files:
        if file [-1:-7:-1] in ['2zb.ra','gz.rat.']:
            #(If it's a bz2 or gz tarball)
            extractor = tarballExtractor(dirname + "/" + file,printFullFileText=printFullFileText)
            for file in extractor:
                print file

if __name__=="__main__":
    import sys
    printDirectory(sys.argv[1])

