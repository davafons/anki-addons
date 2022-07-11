import os
import codecs
import json
import re
from aqt import mw


def __loadSimilarKanjiData(input_file):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_file)
    file = codecs.open(file_path, "r", "utf-8")
    data = json.load(file)
    return data


KANJI_SIMILAR_DATA = __loadSimilarKanjiData("db/wk_niai_noto.json")


def getSimilarKanjis(expression):
    config = mw.addonManager.getConfig(__name__)

    minScore = float(config["minScore"])
    maxResults = int(config["maxResults"])
    return __formatLines(
        __getSimilarKanjis(expression, minScore, maxResults, KANJI_SIMILAR_DATA)
    )


def __formatLines(line):
    return "<br>".join(line)


def __getSimilarKanjis(expression, minScore, maxResults, similarKanjisData):
    similarKanjis = []
    for idx, character in enumerate(expression):
        if character not in similarKanjisData:
            continue

        kanjiData = similarKanjisData[character]

        similarKanjisExpression = __buildSimilarKanjiExpression(
            character, minScore, maxResults, kanjiData
        )
        if similarKanjisExpression:
            similarKanjis.append(similarKanjisExpression)

    return similarKanjis


def __buildSimilarKanjiExpression(character, minScore, maxResults, kanjiData):
    otherKanjis = []
    for data in kanjiData:
        if data["score"] <= minScore:
            continue

        otherKanjis.append(data["kan"])

    return (
        f"{character} → {', '.join(otherKanjis[:maxResults])}"
        if len(otherKanjis) > 0
        else None
    )
