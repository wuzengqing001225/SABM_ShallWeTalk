from AgentModule.classAgent import Agent
from AgentModule.classNetwork import Network
from MessageModule.classMessage import Message
import UtilityModule.displaySystemInfo as display
from UtilityModule.utilsDataProcess import generateShuffleList, selectKeysfromDict, findActiveIndexList, caluRoundifFloat, formatListtoStr
from UtilityModule.utilsCaseSpecificProcess import caluWinner
from UtilityModule.fileCaseSpecificIO import fileLogOutput, fileOverviewOutput, fileMessageOutput
from UtilityModule.plotCaseSpecific import plotVariance
from MessageModule.methodMerge import discussionMerge
from UtilityModule.fileConfigSave import fileConfigSetup
from typing import List, Dict
from PromptModule.prompt import promptSet
from UtilityModule import fileInputOutput
import numpy as np

def simulation(configEnv):
    # Init class
    Agent.cntAgentCount = 0
    Message.cntMessageCount = 0

    # Init simulation parameters
    runMode = configEnv["runMode"]
    N = configEnv["cntAgent"]
    configEnv["configTimestamp"] = fileInputOutput.generateFileTimestamp()

    # Global agent dictionaries
    agent : Dict = {}
    network : Dict = {}
    dictMessage : Dict = {}
    network["Player"] = Network()
    keyResults = {"variance": []}
    
    # Prompt display and Config save
    promptSet["prompt rules"]["rewards"]["in use"][-1] = f'{configEnv["rewardRule"]} reward'
    promptOutput = display.promptDisplay(configEnv)
    pathOutputFolder = fileConfigSetup(promptSet, promptOutput, configEnv)

    # Init agents and network
    for cnt in range(1, N + 1):
        agent[Agent.cntAgentCount] = Agent(['Player'], {"Player": cnt}, runMode, temperature = configEnv["temperature"], model = configEnv["model"], max_tokens = configEnv["maxToken"], api_key=configEnv["configAPIKey"])

        network["Player"].graphAddNode(cnt)
        network["Player"].graphConnect(cnt, mode = 'all')
    
    if configEnv["verbosity"] == 3:
        network["Player"].plotGraph()
    
    # Definition of procedures
    procedures = {
        "Discussion phase": {"index": 1, "sub": "index", "order": {"prompt": 1, "response": 2}},
        "Decision phase": {"index": 2, "sub": "idnex", "order": {"prompt": 1, "response": 2}},
    }
    
    # Main simulation
    indexMsgListDiscussion = []
    textDiscussion = ""

    for round in range(0, configEnv["maxRound"]):
        if configEnv["verbosity"] >= 0: display.display_round(round)
        
        ## Shuffle agent order
        orderRoundAction = generateShuffleList(N)
        
        ## Variables of environment and settings
        varEnv = selectKeysfromDict(configEnv, ["cntAgent", "guessRange", "rewardType", "rewardRule", "runMode", "verbosity"])
        varEnv["round"] = round

        ## Discussion phase (No discussion phase in round 0)
        if round != 0:
            for indexOrder, order in enumerate(orderRoundAction):
                indexMsgListDiscussion = findActiveIndexList(dictMessage, {"purpose": "discussion", "type": "response"})
                textDiscussion = discussionMerge(agent[order], indexMsgListDiscussion, dictMessage, network)
                
                agent[order].action([textDiscussion], [runMode], [round, procedures["Discussion phase"]["index"], indexOrder + 1, -1], varEnv, dictMessage)

        ## Decision phase
        for indexOrder, order in enumerate(orderRoundAction):
            indexMsgListDiscussion = findActiveIndexList(dictMessage, {"purpose": "discussion", "type": "response"})
            textDiscussion = discussionMerge(agent[order], indexMsgListDiscussion, dictMessage, network)

            agent[order].action([textDiscussion], [runMode], [round, procedures["Decision phase"]["index"], indexOrder + 1, -1], varEnv, dictMessage)
        
        ## Decision phase - Result calculation
        roundData = {"round": round, "discussion": [], "reasoning": [], "choice": [], "result": [], "variance": 0}
        for index in range(1, N + 1):
            roundData["choice"].append(agent[index].param["choice"][-1]["choice"])
            roundData["reasoning"].append(agent[index].param["choice"][-1]["reasoning"])
            if round != 0:
                roundData["discussion"].append(agent[index].param["discussion"][-1])
        
        avgChoices, avgTwoThird, indexWinner = caluWinner(roundData["choice"])
        roundData["result"] = [caluRoundifFloat(avgChoices, 4), caluRoundifFloat(avgTwoThird, 4), formatListtoStr(indexWinner)]

        roundData["variance"] = caluRoundifFloat(np.var(roundData["choice"]), 2)
        keyResults["variance"].append(roundData["variance"])

        ## Data output
        fileLogOutput(f"{pathOutputFolder}/agent_action_log.csv", roundData, N)
        fileOverviewOutput(f"{pathOutputFolder}/overview.csv", roundData, N)

        ## Destroy dynamic objects
        print()
    
    # Data output
    ## Message Data
    fileMessageOutput(f"{pathOutputFolder}/message.csv", dictMessage)

    ## Plot results
    print(keyResults["variance"])
    plotVariance(keyResults["variance"], f"{pathOutputFolder}/variance.pdf", varEnv)

    display.display_results(0)
    return keyResults

# Single run
if __name__ == "__main__":
    from configEnv import configEnv
    keyResults = simulation(configEnv)
