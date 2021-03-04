from schlib import *
import json
import urllib
from urllib import request, parse
import urllib.parse
import urllib.request

import subprocess

def copy2clip(txt):
    cmd='echo "'+txt.strip()+'" |xclip -sel clip'
    return subprocess.check_call(cmd, shell=True)
# search_dict ={
#   "SearchByPartRequest": {
#     "mouserPartNumber": "RC0603FR-071K",
#     "partSearchOptions": "string"
#   }
# }

# data = parse.urlencode(search_dict).encode()
# req =  request.Request('https://api.mouser.com/api/v1/search/partnumber', data=data) # this will make the method "POST"
# resp = request.urlopen(req)

# print(resp)
# exit(0)

char_split= ['_','-']

reading= OrderedDict()
reading['R']='resistance'
reading['W']='watt'
reading['%']='precision'

#impose format for resistance and watt


lib1 = SchLib('/home/marco/Documents/kicad_lib_manager/Resistors.lib')
lib2 = SchLib('/home/marco/Documents/kicad_lib_manager/test.lib')

print("len1=",len(lib1.components), " len2=",len(lib2.components))

for i in range(len(lib1.components)):
    print(lib1.components[i].definition['name']+ ">>>" +lib2.components[i].definition['name'])