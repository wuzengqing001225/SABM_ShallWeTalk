from PromptModule.methodPromptUtilization import instantiatePrompt
from AgentModule.methodAgentPrompt import promptGroupTemplate
from PromptModule.prompt import promptSet
import UtilityModule.displaySystemInfo as display
from typing import List, Dict
from MessageModule.classMessage import Message
import copy

promptGroup = copy.deepcopy(promptGroupTemplate)

def playerDiscussion(agent, message:List, actionType:List, actionTimestamp:List[int], varEnv:Dict, dictMessage:Dict):
    if len(message) > 0:
        textDiscussion = message[0]
    else:
        textDiscussion = ""
    
    if textDiscussion == "" or textDiscussion == None:
        promptTemplate = promptGroup["first player discussion"]
    else:
        promptTemplate = promptGroup["player discussion"]
        promptTemplate["value"]["textDiscussion"] = textDiscussion
    
    promptTemplate["value"]["cntPlayerNumberMinusOne"] = varEnv["cntAgent"] - 1
    promptTemplate["value"]["rangeLeft"] = varEnv["guessRange"][0]
    promptTemplate["value"]["rangeRight"] = varEnv["guessRange"][1]
    promptTemplate["value"]["rewardType"] = varEnv["rewardType"]
    promptTemplate["value"]["playerIndex"] = agent.index
    
    if "LLM" in agent.functionMode and "LLM" in actionType:
        prompt = instantiatePrompt(promptTemplate, promptSet)
        response = agent.actionResponse(prompt)
    else:
        prompt = "[Discussion phase]"
        response = "[Rule-based agent] N/A"
    
    if varEnv["verbosity"] >= 2: display.display("Prompt", prompt, 'i')

    actionTimestampPrompt = copy.deepcopy(actionTimestamp)
    actionTimestampPrompt[3] = 1
    dictMessage[Message.cntMessageCount] = Message(prompt, copy.copy(agent), None, None, {"components": "raw", "purpose": "discussion", "type": "prompt", "receiveType": "Player"}, actionTimestampPrompt)
    
    if varEnv["verbosity"] >= 2: display.display(agent, response, 'o')

    actionTimestampResponse = copy.deepcopy(actionTimestamp)
    actionTimestampResponse[3] = 2
    dictMessage[Message.cntMessageCount] = Message(response, copy.copy(agent), None, None, {"components": "raw", "purpose": "discussion", "type": "response", "receiveType": "Player"}, actionTimestampResponse)
    
    return response

def playerAction(agent, message:List, actionType:List, actionTimestamp:List[int], varEnv:Dict, dictMessage:Dict):
    if len(message) > 0:
        textDiscussion = message[0]
    else:
        textDiscussion = ""
    
    if actionTimestamp[0] == 0:
        promptTemplate = promptGroup["player action first round"]
        promptSet["prompt action"]["reasoning and answer"]["in use"] = ["action abstract", "action details"]
    else:
        promptTemplate = promptGroup["player action"]
        promptSet["prompt action"]["reasoning and answer"]["in use"] = ["uncooperative", "instruction", "action abstract", "action details"]
        promptTemplate["value"]["textDiscussion"] = textDiscussion

    promptTemplate["value"]["cntPlayerNumberMinusOne"] = varEnv["cntAgent"] - 1
    promptTemplate["value"]["rangeLeft"] = varEnv["guessRange"][0]
    promptTemplate["value"]["rangeRight"] = varEnv["guessRange"][1]
    promptTemplate["value"]["rewardType"] = varEnv["rewardType"]
    promptTemplate["value"]["playerIndex"] = agent.index

    if "LLM" in agent.functionMode and "LLM" in actionType:
        prompt = instantiatePrompt(promptTemplate, promptSet)
        response = agent.actionResponse(prompt)
    else:
        prompt = "[Decision phase]"
        import random
        decision = random.randint(promptTemplate["value"]["rangeLeft"], promptTemplate["value"]["rangeRight"])
        response = f"[Rule-based agent]\n{decision}"
    
    if varEnv["verbosity"] >= 2: display.display("Prompt", prompt, 'i')
    
    actionTimestampPrompt = copy.deepcopy(actionTimestamp)
    actionTimestampPrompt[3] = 1
    dictMessage[Message.cntMessageCount] = Message(prompt, copy.copy(agent), None, None, {"components": "raw", "purpose": "decision", "type": "prompt", "receiveType": "Player"}, actionTimestampPrompt)
    
    if varEnv["verbosity"] >= 2: display.display(agent, response, 'o')

    actionTimestampResponse = copy.deepcopy(actionTimestamp)
    actionTimestampResponse[3] = 2
    dictMessage[Message.cntMessageCount] = Message(response, copy.copy(agent), None, None, {"components": "raw", "purpose": "decision", "type": "response", "receiveType": "Player"}, actionTimestampResponse)

    return response
