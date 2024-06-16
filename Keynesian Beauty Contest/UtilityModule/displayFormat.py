def displayDict(dataDict):
    for k, v in dataDict.items():
        print(f"{k}: {v}")

def displayFirstValueofDictPrefix(data, prefix):
    prefix = prefix.lower()
    for key in data.keys():
        if key.lower().startswith(prefix):
            return key, data[key]
    return None
