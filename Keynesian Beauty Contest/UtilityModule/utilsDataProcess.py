import re
from typing import Dict, List
from UtilityModule.displaySystemInfo import display_error

def matchNumberInt(response:str, exception = 0):
    matches = re.findall(r'\d+', response)
    if matches:
        return int(matches[0])
    else:
        display_error(f"match number error from {response}", type = 'Standard text process')
        return exception
    
def matchNumberFloat(response:str, exception = 0.0):
    matches = float(re.search(r"[-+]?\d*\.\d+|\d+", response).group())
    if matches:
        return float(matches)
    else:
        display_error(f"match number error from {response}", type = 'Standard text process')
        return exception

def splitTextNumberResponses(response:str):
    lines = [line for line in response.splitlines() if line.strip()]
    
    if len(lines) < 2:
        display_error(f"Only one line from {response}", type = 'Standard text process')
        firstLine = lines[0].split(",")[0].strip()
        secondLine = lines[0].split(",")[-1].strip().replace('.','')
        if not isinstance(matchNumberInt(secondLine), int):
            firstLine = lines[0].split(" ")[0].strip()
            secondLine = lines[0].split(" ")[-1].strip().replace('.','')
            if not isinstance(matchNumberInt(secondLine), int):
                return firstLine, 0
            else: return firstLine, matchNumberInt(secondLine)
        else: return firstLine, matchNumberInt(secondLine)
    
    firstLine = lines[0].strip()
    secondLine = matchNumberInt(lines[-1].strip())
    
    return firstLine, secondLine

def generateShuffleList(N):
    import random
    numList = list(range(1, N + 1))
    random.shuffle(numList)
    return numList

def selectKeysfromDict(dictOrigin, keys):
    dictSub = {key: dictOrigin[key] for key in keys if key in dictOrigin}
    return dictSub

def findFirstIndex(list, value):
    try:
        index = list.index(value)
    except ValueError:
        index = -1
    return index

def DictisSubsetofDict(DictSub, DictAll):
    if all(item in DictAll.items() for item in DictSub.items()): return True
    else: return False

def formatListtoStr(dataList):
    return " ".join(str(dataList)[1:-1].split(', '))

def formatDicttoStr(dataDict, split = ' '):
    formatTemp = []
    for k, v in dataDict.items():
        if isinstance(v, str):
            formatTemp.append(f'[{k}: {v}]')
        if isinstance(v, List):
            formatTemp.append(f'[{k}: {" ".join(v)}]')
        if isinstance(v, Dict):
            formatTemp.append(f'[{k}: {{{formatDicttoStr(v)}}}]')
    return split.join(formatTemp)

def findActiveIndex(dictMessage):
    indexFirstActiveMessage = 1
    msgLen = len(dictMessage)
    for index in range(msgLen, 0, -1):
        if dictMessage[index].statusActive == False:
            indexFirstActiveMessage = index + 1
            break
    return indexFirstActiveMessage

def findActiveIndexList(dictMessage, conditionType:Dict = None):
    indexFirstActiveMessage = findActiveIndex(dictMessage)
    indexActiveList = []

    msgLen = len(dictMessage)
    for index in range(indexFirstActiveMessage, msgLen + 1):
        if dictMessage[index].statusActive == True:
            if conditionType == None:
                indexActiveList.append(index)
            else:
                if DictisSubsetofDict(conditionType, dictMessage[index].type):
                    indexActiveList.append(index)
    
    return indexActiveList

def caluRoundifFloat(value, digit = 2):
    return round(value, digit) if isinstance(value, float) else value
