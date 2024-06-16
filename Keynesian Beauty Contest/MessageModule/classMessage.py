from typing import List, Dict

class Message():
    cntMessageCount : int = 0

    def __init__(self, message:str, agentOrigin, indexAgentDestination:int = None, indexMessageOrigin:List = None, type:Dict = None, timestampStart:List[int] = None, timestampEnd:List[int] = None, remark:str = None) -> None:
        # Index and status
        Message.cntMessageCount += 1
        self.index : int = self.cntMessageCount

        self.statusActive : bool = True

        # Message properties
        self.message : str = message

        if indexMessageOrigin == None: self.indexMessageOrigin : List = []
        else: self.indexMessageOrigin : List = indexMessageOrigin

        if type == None: self.type : Dict = {"components": "raw"} # An item of type is (Type: Value)
        else: self.type : Dict = type

        if "components" in type.keys():
            if type["components"] in ["raw", "transformed"]:
                self.agentOrigin = agentOrigin # A copy of the agent (need to be destroyed when inactive)
            elif type["components"] == "merged":
                self.agentOrigin = None # Multiple agents

        if indexAgentDestination == None: self.indexAgentDestination : int = 0 # Do not allow multiple destinations (index)
        else: self.indexDestination : int = indexAgentDestination

        self.remark = remark

        # Timestamp [Round, Priority between main types, Priority between subtypes, Priority within type]
        if timestampStart == None: self.timestampStart : List[int] = []
        else: self.timestampStart : List[int] = timestampStart
        if timestampEnd == None: self.timestampEnd : List[int] = []
        else: self.timestampEnd : List[int] = timestampEnd
    
    def updateDestination(self, indexAgentDestination):
        self.indexAgentDestination = indexAgentDestination
    
    def updateType(self, type, reset = False):
        if reset == False:
            for k, v in type.items():
                self.type[k] = v
        else:
            self.type = type
    
    def updateTimestampEnd(self, timestampEnd):
        self.timestampEnd = timestampEnd

    def display(self, content:str = 'message'):
        content = content.lower()
        def displayTimestamp(self):
            displayPaddedNumbers = []
            for index, timestamp in enumerate(self.timestampStart):
                if index == 0: displayPaddedNumbers.append(f'{timestamp:04d}')
                elif index == 1: displayPaddedNumbers.append(f'{timestamp:02d}')
                else: displayPaddedNumbers.append(f'{timestamp:03d}')
            displayTemp = "-".join(displayPaddedNumbers)
            return displayTemp
        
        if content == "index": return self.index
        if content == "message": return self.message
        if content == "timestamp": return displayTimestamp(self)

    def updateStatus(self):
        self.statusActive = False
        self.releaseAgentUnit()
        
    def releaseAgentUnit(self):
        self.agentOrigin = None
