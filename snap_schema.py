#somehow ask user for projec
from os import walk
from os import listdir
from os.path import isfile, join

snap_options=["bot","top","closer"]
snap="bot"
grid_size_mils = 50
project_folder = "/home/marco/Y/tmpCS010/CS010_BLDC_FAN_JC"


def snap(n):
    s=str(int(n)-(int(n)%grid_size_mils))
    if n.endswith('\n'):
        s+='\n'
    return str(s)


def remove_from_list(list,element):
    try:
        while True:
            list.remove(element)
    except ValueError:
        pass
    return list


onlyfiles = [f for f in listdir(project_folder) if isfile(join(project_folder, f))]
for f in onlyfiles:
    if f.endswith(".sch"):
        new_text=[]
        print(f)
        with open(join(project_folder, f), "r") as file:
            lines = file.readlines()
            for index,line in enumerate(lines):
                if line.strip() == "Wire Wire Line":
                    #print(lines[index+1])
                    numbers=lines[index+1].split(' ')
                    for jndex, n in enumerate(numbers):
                        numbers[jndex]=snap(n)
                    lines[index+1]='\t' +' '.join(numbers)
                    #print( lines[index+1])
                if line.strip() == "$EndComp":
                    #print(lines[index-2])
                    numbers=lines[index-2].split(' ')
                    numbers=remove_from_list(numbers,'')
                    numbers=remove_from_list(numbers,'\t1')
                    for jndex, n in enumerate(numbers):
                        numbers[jndex]=snap(n)
                    lines[index-2]='\t1    ' +' '.join(numbers)
                    #print(lines[index-2])

                if line.strip().startswith('P'):
                    #print(lines[index])
                    numbers=lines[index].split(' ')
                    numbers=remove_from_list(numbers,'P')
                    for jndex, n in enumerate(numbers):
                        numbers[jndex]=snap(n)
                    lines[index]='P ' +' '.join(numbers)
                    #print(lines[index])
                if line.strip().startswith('Connection ~'):
                    #print(lines[index])
                    numbers=lines[index].split(' ')
                    numbers=remove_from_list(numbers,'Connection')
                    numbers=remove_from_list(numbers,'~')
                    for jndex, n in enumerate(numbers):
                        numbers[jndex]=snap(n)
                    lines[index]='Connection ~ ' +' '.join(numbers)
                    #print(lines[index])
                if line.strip().startswith('Text Label '):
                    print(lines[index])
                    numbers=lines[index].split(' ')
                    numbers=remove_from_list(numbers,'Text')
                    numbers=remove_from_list(numbers,'Label')
                    numbers_to_snap=numbers[0:2]
                    for jndex, n in enumerate(numbers_to_snap):
                        numbers_to_snap[jndex]=snap(n)
                    lines[index]='Text Label ' +' '.join(numbers_to_snap)+ ' '+ ' '.join(numbers[2:])
                    print(lines[index])
                if line.strip().startswith('Text GLabel '):
                    print(lines[index])
                    numbers=lines[index].split(' ')
                    numbers=remove_from_list(numbers,'Text')
                    numbers=remove_from_list(numbers,'GLabel')
                    numbers_to_snap=numbers[0:2]
                    for jndex, n in enumerate(numbers_to_snap):
                        numbers_to_snap[jndex]=snap(n)
                    lines[index]='Text GLabel ' +' '.join(numbers_to_snap)+ ' '+ ' '.join(numbers[2:])
                    print(lines[index])
                if line.strip().startswith('NoConn ~ '):
                    print(lines[index])
                    numbers=lines[index].split(' ')
                    numbers=remove_from_list(numbers,'NoConn')
                    numbers=remove_from_list(numbers,'~')
                    for jndex, n in enumerate(numbers):
                        numbers[jndex]=snap(n)
                    lines[index]='NoConn ~  ' +' '.join(numbers)
                    print(lines[index])
            for line in lines:
                new_text.append(line)
        with open(join(project_folder, f), "w") as file:
            for line in new_text:
                file.write(line)