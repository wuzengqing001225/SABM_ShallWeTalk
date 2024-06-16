import os
import json
from UtilityModule.fileInputOutput import saveJson

def fileConfigSetup(promptSet, promptOutput, configEnv):
    if configEnv["runMode"] != "LLM": pathModelName = "RuleBased"
    else: pathModelName = configEnv["model"]

    if "fileOutputGroup" in configEnv.keys() and configEnv["fileOutputGroup"] != "" and configEnv["fileOutputGroup"] != None:
        pathOutputFolder = f'./output/{configEnv["fileOutputGroup"]}/Record_{configEnv["configTimestamp"]}_{pathModelName}'
        if "indexRun" in configEnv.keys() and configEnv["indexRun"] != 0:
            pathOutputFolder += f'_{configEnv["indexRun"]}'
    else:
        pathOutputFolder = f'./output/Record_{configEnv["configTimestamp"]}_{pathModelName}'
    os.makedirs(pathOutputFolder, exist_ok=True)

    os.makedirs(f"{pathOutputFolder}/config/", exist_ok=True)
    processedPromptSet = convertPrompttoJSON(promptSet)
    saveJson(f"{pathOutputFolder}/config/config_prompt_components.json", json.dumps(processedPromptSet, indent=4, ensure_ascii=False))
    processedConfigEnv = convertConfigtoJSON(configEnv)
    saveJson(f"{pathOutputFolder}/config/config_main_setting.json", json.dumps(processedConfigEnv, indent=4, ensure_ascii=False))
    saveJson(f"{pathOutputFolder}/config/config_prompt.json", json.dumps(promptOutput, indent=4, ensure_ascii=False))

    return pathOutputFolder

def convertPrompttoJSON(setPrompt):
    output = {}

    for main_key, main_value in setPrompt.items():
        output[main_key] = {}
        for second_key, second_value in main_value.items():
            if "in use" in second_value:
                in_use = second_value["in use"]
                if in_use == ["ALL"]:
                    output[main_key][second_key] = list(second_value.keys())
                    output[main_key][second_key].remove("in use")
                else:
                    output[main_key][second_key] = in_use
            else:
                if len(second_value) == 1:
                    output[main_key][second_key] = list(second_value.keys())[0]
                else:
                    output[main_key][second_key] = list(second_value.keys())
    
    return output

def convertConfigtoJSON(configEnv):
    processedConfigEnv = {}
    for k, v in configEnv.items():
        if 'apikey' in k.lower():
            processedConfigEnv[k] = v[-4:]
        else:
            processedConfigEnv[k] = v
    
    return processedConfigEnv
