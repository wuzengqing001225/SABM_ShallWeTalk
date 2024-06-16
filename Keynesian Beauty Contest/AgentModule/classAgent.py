import time
import openai
import anthropic
from typing import List, Dict
import AgentModule.methodAgent as method
import UtilityModule.utilsDataProcess as dataProcess

class Agent:
    cntAgentCount : int = 0

    def __init__(self, type:List[str], indexNetworkGroup:Dict = {}, functionMode:str = 'rule', temperature:float=1.0, model:str='gpt-4o', max_tokens:int=256, api_key:str = ''):
        # Basic Parameters
        Agent.cntAgentCount += 1
        self.index : int = Agent.cntAgentCount
        
        self.type : List[str] = type
        self.functionMode : str = functionMode # rule-based (rule), LLM-based agent (LLM)

        # Network Group
        self.indexNetworkGroup : Dict = indexNetworkGroup # Network name: index
        
        # OpenAI Parameters
        self.model = model
        self.paramModel : Dict = {"temperature" : temperature, "model" : model, "max_tokens" : max_tokens}

        if "gpt" in model:
            self.api_key = api_key
            openai.api_key = api_key
        elif "claude" in model:
            self.api_key = api_key
        
        # Dynamic Parameters
        self.param : Dict = {"discussion": [], "choice": []}
        
    def action(self, message:List, actionType:List, actionTimestamp:List[int], varEnv:Dict, dictMessage:Dict):
        if actionTimestamp[1] == 1:
            responseDiscussion = method.playerDiscussion(self, message, actionType, actionTimestamp, varEnv, dictMessage)
            self.param["discussion"].append(responseDiscussion)
            return
        elif actionTimestamp[1] == 2:
            responseDecision = method.playerAction(self, message, actionType, actionTimestamp, varEnv, dictMessage)
            firstLine, secondLine = dataProcess.splitTextNumberResponses(responseDecision)
            self.param["choice"].append({"reasoning": firstLine, "choice": secondLine})
            if varEnv["verbosity"] == 1: print(f"Player #{self.index}: {secondLine}")
            return
    
    def actionResponse(self, prompt):
        if "gpt" in self.model: return self.actionOpenaiResponse(prompt)
        elif "claude" in self.model: return self.actionAnthropicResponse(prompt)
    
    def actionOpenaiResponse(self, prompt):
        prompt = prompt.strip()
        message = ""

        retries = 3
        backoff_factor = 2
        current_retry = 0

        while current_retry < retries:
            try:
                response = openai.ChatCompletion.create(
                    model=self.paramModel["model"],
                    messages=[
                        # {"role":"system", "content":"You are an assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=self.paramModel["max_tokens"],
                    n=1,
                    temperature=self.paramModel["temperature"],
                    top_p=1
                )
                message = response['choices'][0]['message']['content'].strip()
                return message
            except Exception as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"RateLimitError: Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}")
                    raise e
    
    def actionAnthropicResponse(self, prompt):
        client = anthropic.Anthropic(api_key = self.api_key)

        message = client.messages.create(
            model = self.paramModel["model"],
            max_tokens = self.paramModel["max_tokens"],
            temperature = self.paramModel["temperature"],
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text
    
    def updateIndexGroup(self, indexGroup, reset = False):
        if isinstance(indexGroup, Dict):
            if reset == True:
                self.indexGroup = indexGroup
            else:
                for k, v in indexGroup.items():
                    self.indexGroup[k] = v
        else:
            return
