# Copyright: Micah Gajewski <micahbgaj@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import os
import codecs
import json
import re


def inReading(idx, character, expression, data):
    expression = expression[idx:]
    try:
        expression = expression[: expression.index("]")]
    except ValueError:
        pass
    for r in data[character]["reading"]:
        if r in expression:
            return True
    return False


def getChars(i):
    char_delim = "→"
    chars = i[i.index(char_delim) + 1 :]
    chars = list(re.sub("[, \n]", "", chars))
    return chars


def highlight(c, raw):
    delim_index = raw.index("→")
    chars = (raw)[delim_index:]
    highlight_index = (chars).index(c)
    total_index = delim_index + highlight_index
    highlighted = raw[:total_index] + "<b>" + c + "</b>" + raw[total_index + 1 :]
    return highlighted


def formatLines(phonetics):
    return "<br>".join(phonetics)


def getPhonetic(expression, data):
    phoenetics = []
    for idx, c in enumerate(expression):
        if c in data:
            if inReading(idx, c, expression, data):
                raw = data[c]["raw"]
                phoenetics.append(highlight(c, raw))

    return phoenetics


def getHighlightedPhonetics(expression):
    input_file = "data.json"
    data = PHONETIC_COMPONENTS_DATA(input_file)
    return formatLines(getPhonetic(expression, data))


#
# if __name__ == '__main__':
#     getHighlightedPhonetics(u'...について')
#     getHighlightedPhonetics('この 町[まち]には 消防署[しょうぼうしょ]が 1[ひと]つしかありません。')