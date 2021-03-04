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


def try_split(value):
    for char in char_split:
        parts=comp.definition['name'].split(char)
        values=try_assign(parts)
        print (values)
        accept=input("accept?")
        if accept == "y":
            return values
    return {}

def try_assign(parts):
    values = {}
    for part in parts:
        for key in reading.keys():
            if part.endswith(key):
                values[reading[key]]=part
    return values

def check_values(values): # check for last character also in values read from 
    for key in reading.keys():
        if reading[key] not in values.keys():
            print("missing", reading[key])
            val=input("\tinsert value:")
            if not val.endswith(key):
                val+=key
            values[reading[key]]=val
    print(values)
    return values

def update_name (documentation,comp, new_name):
    print("new name:",new_name)
    old_name= comp.definition['name']
    comp.fields[1]['name'] = new_name
    comp.definition['name'] = new_name
    documentation.components[new_name]=lib.documentation.components[old_name]
    documentation.components.pop(old_name)



lib = SchLib('/home/marco/Documents/kicad_lib_manager/Resistors.lib')

for comp in lib.components:
    print("actual value:",comp.definition['name'])
    copy2clip(comp.getField('Manufacturer_Part_Number')['name'].replace('"',''))

    print("MPN:",comp.getField('Manufacturer_Part_Number')['name'])
    for line in comp.fields[1:]:
        print("\t", line['fieldname'], ":", line['name'])

    values_split=try_split(comp.definition['name'])
    values=check_values(values_split)
    new_name= '_'.join([values[k]for k in values.keys()])
    print("new name:",new_name)
    update_name(lib.documentation,comp, new_name)
    comp.comments =[]
    #add keywords
    lib.documentation.components[new_name].keywords = [values[k]for k in values.keys()]
    print(lib.documentation.components[new_name].keywords) #TODO FIX
    #create field for each key in value 
    for name in values.keys():
        field=comp.getField(name)
        if field is not None:
            if field['name'] is not values[name]:
                print("WARNING ",field['name'], " different from ",values[name], ": updating...")
                field['name'] = values[name]
        else:
            comp.addField(name, values[name])
    #check if fieldexists, then check for correct value

    description = comp.getField("Description")
    if description is None:
        print("WARNING description field not found")
    else:
        description['name'] = "Resistor " + ' '.join([values[k]for k in values.keys()]) +' ' + comp.getField("Manufacturer_Part_Number")['name'].replace('"','')
    # for line in comp.fields[1:]:
    #     print("\t", line)
        
    print('delete any field?')
lib.save('test.lib')
lib.documentation.save('test.dcm')
print('saved')
# proposta value: OHM_WATT_%
# campi resistenza, watt, precisione

#controllare posizionamento 

#_FN_KEYS = ['name','posx','posy','text_size','text_orient','visibility','htext_justify','vtext_justify','fieldname']