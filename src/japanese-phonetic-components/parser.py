# Copyright: Micah Gajewski <micahbgaj@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import os
import codecs
import json
import re


def __loadPhoneticComponentsData(input_file):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_file)
    file = codecs.open(file_path, "r", "utf-8")
    data = json.load(file)
    return data


PHONETIC_COMPONENTS_DATA = __loadPhoneticComponentsData("phonetic-components.json")


def getHighlightedPhonetics(expression):
    return __formatLines(__getPhonetics(expression, PHONETIC_COMPONENTS_DATA))


def __formatLines(phonetics):
    return "<br>".join(phonetics)


def __getPhonetics(expression, phoneticComponentsData):
    phoenetics = []
    for idx, character in enumerate(expression):
        if character not in phoneticComponentsData:
            continue

        kanjiData = phoneticComponentsData[character]

        if __matchReading(idx, character, expression, kanjiData):
            phoneticsExpression = __buildPhoneticsExpression(character, kanjiData)
            phoenetics.append(phoneticsExpression)

    return phoenetics


def __matchReading(idx, character, expression, kanjiData):
    expression = expression[idx:]
    try:
        expression = expression[: expression.index("]")]
    except ValueError:
        pass

    for reading in kanjiData["reading"]:
        if reading in expression:
            return True
    return False


def __buildPhoneticsExpression(kanji, kanjiData):
    radical = kanjiData["radical"]
    readings = ", ".join(kanjiData["reading"])
    relatives = ", ".join(
        map(lambda relative: __highlightKanji(kanji, relative), kanjiData["relative"])
    )
    phonetics = f"{radical} ({readings}) → {relatives}"
    return phonetics
    print(phonetics)


def __highlightKanji(kanji, relative):
    if kanji == relative:
        return f"<b>{relative}</b>"
    else:
        return relative


# if __name__ == '__main__':
#     getHighlightedPhonetics(u'...について')
#     getHighlightedPhonetics('この 町[まち]には 消防署[しょうぼうしょ]が 1[ひと]つしかありません。')
