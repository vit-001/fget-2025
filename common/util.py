# -*- coding: utf-8 -*-
__author__ = 'Vit'

from bs4 import BeautifulSoup

def _iter(source):
    if source is None:
        return []
    else:
        return source

def get_menu_handler(function,*args,**options):
    return lambda:function(*args,**options)

def quotes(text:str, from_lex:str, to_lex:str)->str:
    return text.partition(from_lex)[2].partition(to_lex)[0]

def collect_string(soup:BeautifulSoup, divider='')->str:
    result=''
    for s in soup.stripped_strings:
        result += s + divider

    return result.strip(divider)

def collect_string_to_array(soup:BeautifulSoup)->list[str]:
    result=list()
    for s in soup.stripped_strings:
        result.append(s)

    return result


def time_format(ms)->str:
    dur = ms // 1000
    hours = dur // 3600
    minutes = dur // 60 - hours * 60
    secundes = dur - minutes * 60 - hours * 3600
    if hours == 0:
        return '%2d:%02d' % (minutes, secundes)
    else:
        return '%d:%02d:%02d' % (hours, minutes, secundes)

def sp():
    print('=========================================')

def psp(*arguments, **keywords):
    print(*arguments, **keywords)
    sp()

def pretty(soup:BeautifulSoup):
    psp(soup.prettify())

if __name__ == "__main__":
    pass