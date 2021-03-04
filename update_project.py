#somehow ask user for projec
from os import walk
from os import listdir
from os.path import isfile, join


trads=[]


project_folder = "/home/marco/Y/tmpCS010/CS011_REV1_pulito2"
old_lib = "Resistors.lib"
new_lib = "test.lib"

correspodence_file = "trads.txt"

with open(correspodence_file, "r") as file:
    correspodences = file.readlines()
    for corr in correspodences:
        trads.append(corr.split('>>>'))
#for each .sch files in project folder
print (trads)
onlyfiles = [f for f in listdir(project_folder) if isfile(join(project_folder, f))]
for f in onlyfiles:
    if f.endswith(".sch"):
        print(f)
        with open(join(project_folder, f), "r") as file:
            filedata = file.read()
        for trad in trads:
            old_str= "L "+old_lib.split('.')[0]+":"+trad[0]
            new_str= "L "+new_lib.split('.')[0]+":"+trad[1].strip()
            print(old_str,">>>",new_str)
            filedata = filedata.replace(old_str, new_str)
# Write the file out again
        with open(join(project_folder, f), "w") as file:
            file.write(filedata)
