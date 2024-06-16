from UtilityModule.displaySystemInfo import display_error

def discussionMerge(agent, indexMsgListDiscussion, dictMessage, network):
    textDiscussion = ""
    # print(indexMsgListDiscussion)

    if agent.index in network["Player"].graph:
        for index in indexMsgListDiscussion:
            msg = dictMessage[index]
            if msg.type["receiveType"] == "Player" and agent.index in network["Player"].graph[msg.agentOrigin.index]:
                if msg.agentOrigin == None:
                    display_error(f"Message origin not found. msg: {msg}", type = 'Message incomplete')
                else:
                    if msg.agentOrigin.index == agent.index:
                        textDiscussion += f"You: {msg.message}\n"
                    else:
                        textDiscussion += f"Player #{msg.agentOrigin.index}: {msg.message}\n"
    
    return textDiscussion