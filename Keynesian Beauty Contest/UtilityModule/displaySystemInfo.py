def promptDisplay(configEnv):
    from AgentModule.methodAgentPrompt import promptGroupTemplate
    from PromptModule.methodPromptUtilization import instantiatePrompt
    from PromptModule.prompt import promptSet

    promptOutput = {}

    for k, v in promptGroupTemplate.items():
        prompt = instantiatePrompt(v, promptSet)
        promptOutput[k.capitalize()] = prompt
        if configEnv["verbosity"] != 0: print(f"<<Prompt>> # {k.capitalize()}\n{prompt}\n")

    return promptOutput

def display(agent, prompt:str, type:str):
    if isinstance(agent, str):
        if type == 'i':
            print(f"<<PROMPT>> {agent.capitalize()}: {prompt}")
        elif type == 'o':
            print(f"<<RESPONSE>> {agent.capitalize()}: {prompt}")
    
    else:
        agentType = ""
        if len(agent.type) == 1:
            agentType = agent.type[0].capitalize()
        else:
            agentType = ",".join(agent.type)
            agentType = agentType.capitalize()
        
        if type == 'i':
            print(f"<<PROMPT>> Agent #{agent.index} [{agentType}]: {prompt}")
        elif type == 'o':
            print(f"<<RESPONSE>> Agent #{agent.index} [{agentType}]: {prompt}")

def display_error(message:str, position = '', type = 'default'):
    if type == 'default':
        if position == '':
            print(f'[Error] {message}')
        else:
            print(f'[Error] {message} @ {position}')
    else:
        print(f'[{type} Error] {message} @ {position}')

def display_results(return_value = 0):
    if return_value == 0:
        print('Simulation Completed')
    if return_value == -1:
        print('Simulation Completed (interrupted)')

def display_variables(var_name, var, round = 0, display_round = False):
    if display_round == False:
        print(f'{var_name}: {var}')
    else:
        print(f'#{round}: {var_name}: {var}')

def display_round(round = 0):
    print(f'Round #{round}')

def display_results_timeseries(key_indicator:dict):
    print("\n=================")
    if 'task' in key_indicator.keys():
        print("# Task")
        for k, v in key_indicator['task'].items():
            print(f"{k}: {v}")
        print()
    if 'round' in key_indicator.keys():
        print(f"# Round: {key_indicator['round'][0]}")
        if len(key_indicator['round']) > 1:
            for item_index in range(1, len(key_indicator['round']), 2):
                print(f"{key_indicator['round'][item_index]}: ")
                for i in key_indicator['round'][item_index + 1]:
                    print(i, end = ' ')
                print()
