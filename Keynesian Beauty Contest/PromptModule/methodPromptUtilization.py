from textwrap import dedent
from UtilityModule.displaySystemInfo import display_error

def readPrompt(command, promptSet):
    prompt = ""

    lines = command.strip().split('\n')

    for line in lines:
        if line == '\n':
            prompt += '\n'
            continue

        commandElements = line.split(' ')
        commandKey = commandElements[0].lower()
        commandValue = ' '.join(commandElements[1:]).strip()
        placeholder = ''

        if '@' in commandValue:
            commandValueTemp = commandValue.split('@')
            commandValue = commandValueTemp[0].strip()
            placeholder = commandValueTemp[1].strip()
        
        matchPromptKey = next((k for k in promptSet if k.endswith(commandKey)), None)
        
        if matchPromptKey:
            if commandValue in promptSet[matchPromptKey].keys():
                promptSubSet = promptSet[matchPromptKey][commandValue]
                if len(promptSubSet) == 1:
                    prompt += list(promptSubSet.values())[0]
                else:
                    promptTemp = ""
                    if "in use" not in promptSubSet.keys() or "ALL" in promptSubSet["in use"]:
                        for k in promptSubSet.keys():
                            if k == 'in use': continue
                            promptTemp += promptSubSet[k] + ' '
                        promptTemp = promptTemp.strip()
                        prompt += promptTemp
                    else:
                        for k in promptSubSet["in use"]:
                            if k not in promptSubSet.keys():
                                display_error("Prompt key not found.", "methodPromptUtilization", "prompt")
                                continue
                            else:
                                promptTemp += promptSubSet[k] + ' '
                        promptTemp = promptTemp.strip()
                        prompt += promptTemp
        
        if placeholder == '': prompt += '\n'
        elif placeholder == 'space': prompt += ' '
        elif placeholder == 'tab': prompt += '\t'
    
    prompt = prompt.strip()
    return prompt

def instantiatePrompt(promptTemplate, promptSet):
    prompt = readPrompt(dedent(promptTemplate['command']), promptSet).format(**promptTemplate['value'])
    return prompt
