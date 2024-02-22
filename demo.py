import os
def find_md(path):
    total=0

    for filename in os.listdir(path):
        if filename.endswith('.md'):
            total+=1
        elif os.path.isdir(path+filename):
            total+=find_md(path+filename+'/')

    return total

print(find_md('../'))

