import tarfile
import os
import re
import sys
import json
import gzip

def parseLOCline(line):
    line = line.split("\t")[0]
    output = dict()
    splat = line.split("/")
    output['paper'] = splat[0]
    output['publish'] = "-".join(splat[1:4])
    output['edition'] = int(splat[4][3:])
    output['filename'] = line
    output['page'] = int(splat[5][4:])
    website = "http://chroniclingamerica.loc.gov/lccn/"+re.sub("/ocr","",line)
    thumbnail = website+"/thumbnail.jpg"
    output['searchstring'] = '<img src="'+ thumbnail + '"</img><a href="' + website +'">Read online</a>'
    return json.dumps(output)

class tarballExtractor(object):
    def __init__(self,filename,printFullFileText=True):
        self.filename = filename
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
        if name.endswith(".txt"):
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
    for fileToExtract in files:
        if fileToExtract.endswith(".tar.bz2") or fileToExtract.endswith(".tar.gz"):
            #(If it's a bz2 or gz tarball)
            try:
                extractor = tarballExtractor(dirname + "/" + fileToExtract,printFullFileText=printFullFileText)
                for file in extractor:
                    try:
                        print file
                    except:
                        raise
                        sys.stderr.write("error extracting " + extractor.filename + "\n")
            except:
                raise
                sys.stderr.write("error extracting " + fileToExtract + "\n")

def printFile(filename,fulltext=True):
    if not filename.endswith("tar.bz2"):
        return
    shortname = re.sub(r".*/(.*)\.tar\..*",r"\1",filename)
    jsonfile = gzip.open("jsoncatalogs/" + shortname + ".txt.gz","wb")
    txtFile = gzip.open("inputfiles/" + shortname + ".txt.gz","wb")
    extractor = tarballExtractor(filename)
    for text in extractor:
        try:
            txtFile.write(text + "\n")
            jsonfile.write(parseLOCline(text) + "\n")
        except:
            raise
            sys.stderr.write("error extracting " + extractor.filename + "\n")
    jsonfile.close()
    txtFile.close()

if __name__=="__main__":
    for filename in sys.argv[1:]:
        printFile(filename)
"""
if __name__=="__main__":
    import sys
    printDirectory(sys.argv[1])
"""
