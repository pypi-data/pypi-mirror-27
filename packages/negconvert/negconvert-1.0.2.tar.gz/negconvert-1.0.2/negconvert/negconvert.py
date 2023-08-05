# Andrew Salopek, Quan Nguyen
# Texas Tech University

import csv
import re
import enchant
import sys
import os
from pathlib import Path

from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost', port=9000)

_ROOT = os.path.abspath(os.path.dirname(__file__))

def getdatafilepath(path):
    return os.path.join(_ROOT, path)

def freqSort(text):
    frequency = {}
    if (text):
        for row in text:
            match_pattern = re.findall(r'\b[a-z]{3,15}\b', row['text'].lower())
            for word in match_pattern:
                count = frequency.get(word, 0)
                frequency[word] = count + 1
    filename = Path(sys.argv[1]).stem
    with open(filename + '_freq.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in frequency.items():
            writer.writerow([key, value])

def contraction(inData):
    with open(getdatafilepath('contractions.csv')) as f:
        f.readline()  # ignore first line (header)
        mydict = dict(csv.reader(f, delimiter=','))
        pattern = re.compile(r'\b(' + '|'.join(mydict.keys()) + r')\b')
        result = re.sub(pattern, lambda m: mydict.get(m.group(), m.group()), inData)
    # print(result, "contraction")
    return parser(result)


def affirm(inData):
    with open(getdatafilepath('opposites.csv')) as f:
        f.readline()  # ignore first line (header)
        mydict = dict(csv.reader(f, delimiter=','))
        pattern = re.compile(r'not\s(' + '|'.join(mydict.keys()) + r'\s)')
        result = re.sub(pattern, lambda m: mydict.get(m.group(1)), inData)
    # print(result, "affirm")
    return synonym(result)


def synonym(inData):
    wordList = inData.split()
    # print(wordList, "33")
    filename = Path(sys.argv[1]).stem
    with open(filename + '_freq.csv') as fd:
        freqDict = dict(csv.reader(fd, delimiter=','))
    with open(getdatafilepath('synonyms.csv')) as f:
        f.readline()  # ignore first line (header)
        syndict = dict(csv.reader(f, delimiter=','))
        for word in wordList:
            synArray = []
            if word in syndict.values():
                synArray.append(word)
                try:
                    word = syndict[word]
                except:
                    pass
        if (synArray):
            maxCnt = 0
            maxWord = synArray[0]
            for element in synArray:
                try:
                    if freqDict[element]:
                        if (freqDict[element] > maxCnt):
                            maxCnt = freqDict[element]
                            maxWord = element
                        else:
                            pass
                    else:
                        pass
                except:
                    pass
            wordList = [w.replace(word, maxWord) for w in wordList]
    return ' '.join(wordList)


def spellCheck(inData):
    newData = re.sub(r'!*\?*', '', inData)
    spellDict = enchant.Dict("en-US")
    outStr = []
    pattern = re.compile(r'^[(@|#]\w+')
    wordList = newData.split()
    for word in wordList:
        if not (pattern.match(word)):
            try:
                if not (spellDict.check(word)):
                    try:
                        newWord = spellDict.suggest(word)
                        outStr.append(newWord[0])
                    except:
                        outStr.append(word)
                else:
                    outStr.append(word)
            except ValueError:
                pass
        else:
            outStr.append(word)
    string = " ".join(outStr)
    return contraction(string)


def parser(inData):
    dep = nlp.dependency_parse(inData)
    result = [item for item in dep if item[0] == "neg"]
    if result:
        contr = affirm(inData)
        print(result, "parser-result")
        return contr
    else:
        print(result, "parser-noresult")
        return synonym(inData)

# Main
def main():
    if (not os.path.exists(sys.argv[1])):   # Check if file not found
        raise FileNotFoundError(sys.argv[1])

    with open(sys.argv[1], encoding="utf8") as textcsv:
        text = csv.DictReader(textcsv)
        freqSort(text)

    with open(sys.argv[1], encoding='utf-8') as textcsv:
        text = csv.DictReader(textcsv)
        filename = Path(sys.argv[1]).stem
        with open(filename + '_converted.csv', 'w', encoding="utf8", newline='') as convertcsv:
            headers = ["oldtext", "newtext"]
            csvwrite = csv.DictWriter(convertcsv, fieldnames=headers)
            csvwrite.writeheader()
            i = 0
            for row in text:
                line = spellCheck(row['text'].lower())
                print(i, line)
                i += 1
                csvwrite.writerow({"oldtext": row['text'], "newtext": line})
