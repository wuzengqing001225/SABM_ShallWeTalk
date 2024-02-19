# from .community import Community
import numpy as np

class Agent:
    """
    Base class of agent. 
    Each agent by default has its id (related to the order of creation), name, and context_history (a dictionary of context and its corresponding message)
    context_history has the following structure:
    context_history = {
        "round0": {
            "chatgroup_name_1": {
                "prompt": prompt for LLM,
                "response": generated by LLM
            },
            "chatgroup_name_2": {
                "prompt": prompt for LLM,
                "response": generated by LLM
            }, ...},
        "round1": [{
            ...
        }, ...]
    }
    
    """
    def __init__(self, id: int, name: str, seed=0):
        self.id = id
        self.name = name
        self.seed = seed
        self.context_history = {}
        self.communities = []
        self.chatgroups = []
        self.rng = np.random.default_rng(seed=seed)

    def reset(self):
        self.context_history = {}

    def record(self, round, chatgroup_name, prompt, response):
        if f"round{round}" not in self.context_history:
            self.context_history[round] = {}
        self.context_history[round][chatgroup_name] = {
            "prompt": prompt,
            "response": response
        }
    
    def get_context_history(self, round: int = None, chatgroup_name: str = None):
        if round is not None:
            if chatgroup_name is not None:
                # Both round and chatgroup_name are specified
                return self.context_history[f"round{round}"][chatgroup_name]
            else:
                # Only round is specified
                return self.context_history[f"round{round}"]
        else:
            if chatgroup_name is not None:
                # Only chatgroup_name is specified
                context_history = {}
                for round in self.context_history:
                    if chatgroup_name in self.context_history[round]:
                        context_history[f"round{round}"] = self.context_history[f"round{round}"][chatgroup_name]
                return context_history

        # Both round and chatgroup_name are None
        return self.context_history

    def add_community(self, community):
        if community in self.communities:
            raise ValueError(f"Agent {self.name} is already in community {community.name}.")
        self.communities.append(community)
    
    def add_chatgroup(self, chatgroup):
        if chatgroup in self.chatgroups:
            raise ValueError(f"Agent {self.name} is already in chatgroup {chatgroup.name}.")
        self.chatgroups.append(chatgroup)

    def in_community(self, community):
        return community in self.communities

    def in_chatgroup(self, chatgroup):
        return chatgroup in self.chatgroups
    
    def __repr__(self):
        return f"agent {self.name} (id = {self.id})"
    
    def __str__(self):
        return self.__repr__() + f" communities: {self.communities}"

    def get_rivals(self, community=None):
        rivals = ""
        if community is None:
            for com in self.communities:
                rival_agents = com.get_alias_agents()
                rivals += f"community {com.name}: {rival_agents}\n"
        else:
            rival_agents = community.get_alias_agents()
            rivals += f"community {community.name}: {rival_agents}\n"

        return rivals
    
    def get_aliases(self, community=None):
        aliases = ""
        if community is None:
            for com in self.communities:
                alias_agents = com.get_alias_agents()
                aliases += f"community {com.name}: {alias_agents}\n"
        else:
            alias_agents = community.get_alias_agents()
            aliases += f"community {community.name}: {alias_agents}\n"

        return aliases

"""
Create your own agent class below, and inherit from Agent class.
"""