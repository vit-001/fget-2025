# -*- coding: utf-8 -*-
__author__ = 'Vit'

from pathlib import Path

def line_count(fd):
    n=0
    for line in fd:
        n+=1

    return n

def directory_count():
    pass

if __name__ == "__main__":
    n=0
    p=Path('C:\\PyWork\\fget-2025\\')  #C:\PyWork\fget-2025
    list_files=list(p.glob('**/*.py'))
    for item in list_files:
        if '\\venv' in str(item) or '\\.venv\\' in str(item):
            continue
        with open(str(item),encoding='utf8') as fd:
            print(item)
            i=line_count(fd)
            print(item, i)
            n+=i
    print(n)



