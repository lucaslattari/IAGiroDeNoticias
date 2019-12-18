# coding: utf-8
import string
import re

def is_ok(c):
    return c.isalnum() or c in string.punctuation or c in " "

def cleanSentence(s):
    s = ''.join(filter(is_ok, s))
    s = s.replace("&#39;", "\'")
    s = s.replace("&quot;", "\"")
    s = re.sub("<.*?>", "", s)
    s = re.sub("[0-9]+\)", "", s)
    s = re.sub("[0-9]+\.", "", s)

    return s
