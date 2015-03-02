import rdflib
import json
import re

g=rdflib.Graph()
g.load("newspapers.rdf")


seen = dict()

for s,p,o in g:
    #I should keep the context, but whatever.
    p = re.sub(".*/","",p)
    try:
        seen[s][p] = o
    except:
        seen[s] = dict()
        seen[s][p] = o

def convertID(string):
    try:
        return re.findall(r"file:///lccn/(.*)#title",string)[0]
    except IndexError:
        return False


jsoncatalog = []

for name in seen.keys():
    id = convertID(name)
    
    if id:
        attributes = dict()
        attributes['paper'] = id
        for attribute in seen[name].keys():
            attributes[attribute] = seen[name][attribute]
        jsoncatalog.append(attributes)

keys = ["paper","publisher","title","coverage","subject","placeOfPublication"]
print "\t".join(keys)

for line in jsoncatalog:
    newline = []
    for key in keys:
        try:
            newline.append(line[key])
        except KeyError:
            newline.append("")
    print "\t".join(newline)

