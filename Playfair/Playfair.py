import tkinter as tk
from math import gcd
import string
import unicodedata
import random as rand


def fixtext(strng):
    CHARS_TO_REMOVE = '''!ˇ´()-[]{};:'",<>./?@#$%^&*_~'''

    for char in CHARS_TO_REMOVE:
        strng = strng.replace(char, "")

    strng = str.lower(strng)
    return strng

list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']