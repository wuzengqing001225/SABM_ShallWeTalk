import json
import os
import csv
from UtilityModule.displayFormat import displayFirstValueofDictPrefix

def generateFileTimestamp(mode = "second"):
    import datetime
    import time
    if mode == "second":
        return f"{datetime.date.today().strftime('%y%m%d')}_{time.strftime('%H%M%S')}"
    elif mode == "minute":
        return f"{datetime.date.today().strftime('%y%m%d')}_{time.strftime('%H%M')}"

def formatConfigAPIKeyExtract(configAPIKeySource, configFilename = './configAPIKey.json', model = 'GPT'):
    configAPIKeyFile = readJson(configFilename)
    
    if configAPIKeySource != None:
        configAPIKey = configAPIKeyFile[configAPIKeySource]
    else:
        configAPIKeySource, configAPIKey = displayFirstValueofDictPrefix(configAPIKeyFile, model)
    
    return configAPIKey

def formatSuffixCheck(filename, suffix = 'json'):
    if not filename.endswith(f'.{suffix}'):
        filename += f'.{suffix}'
    return filename

def readJson(filename):
    filename = formatSuffixCheck(filename)
    with open(filename, 'r', encoding='utf-8') as file:
        dataJSON = json.load(file)

    def displayJSON(obj, prefix='', displayTemp = {}):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                if isinstance(value, (dict, list)):
                    displayJSON(value, new_prefix)
                else:
                    displayTemp[new_prefix] = value
                    # print(f"{new_prefix}: {value}")
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                new_prefix = f"{prefix}"
                if isinstance(item, (dict, list)):
                    displayJSON(item, new_prefix)
                else:
                    displayTemp[new_prefix] = value
                    # print(f"{new_prefix}: {item}")
        return displayTemp
    
    displayTemp = displayJSON(dataJSON)
    
    #from UtilityModule.displayFormat import displayDict
    #displayDict(displayTemp)

    return displayTemp

def saveJson(filename, output):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(output)

def fileCsvOutputWriteline(filename, headers, data):
    file_exists = os.path.exists(filename)

    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        if not file_exists:
            csvwriter.writerow(headers)
        
        csvwriter.writerow(data)

def getSubdirectories(folderPath):
    subdirectories = []
    for item in os.listdir(folderPath):
        item_path = os.path.join(folderPath, item)
        if os.path.isdir(item_path):
            subdirectories.append(item)
    return subdirectories
