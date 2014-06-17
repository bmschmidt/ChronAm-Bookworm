#!/usr/bin/python

import sys
import json
import re

for line in sys.stdin:
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
    print json.dumps(output)
