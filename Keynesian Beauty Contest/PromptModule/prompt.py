promptSet = {
"prompt role": {
    "college student": {"default role": "You are a college student participating in a number guessing game with other {cntPlayerNumberMinusOne} players. You are player #{playerIndex}."}
},

"prompt rules": {
    "background": {
        "in use": ["ALL"],

        "guess range": "You need to choose a number between {rangeLeft} and {rangeRight}.",
        "target number definition": "The player whose number is closest to 2/3 of the average guess of all players wins.",
        "multiple win rule": "Multiple players can win.",
    },

    "rewards": {
        "in use": ["default reward", "independent reward"],

        "hint": "In an extreme case, if all players choose the same number, everyone wins.",
        "default reward": "If only you win, you will earn 100 {rewardType}.",

        "independent reward": "If multiple players win, each winner gets 100 {rewardType}.",
        "amplified reward": "If multiple players win, each winner gets M multiplied by 100 {rewardType}, where M is the number of winners.",
        "exclusive reward": "But do note that if multiple players win, no one receives any {rewardType}.",
    }
},

"prompt history": {
    "discussion history format":{
        "in use": ["previous discussion"],

        "labeled discussion": "If exists, your previous remarks are marked as 'You:'.",
        "previous discussion": "Discussion so far:\n'''{textDiscussion}'''"
    }
},

"prompt action": {
    "discussion settings": {
        "in use": ['discussion settings', 'default'],
        
        "discussion settings": "Before selecting your number, you will discuss the game with other players. You can use these discussions to formulate a strategy. You can reveal your strategy during the discussion, but you do not have to follow it when making your final decision. Feel free to discuss anything,",
        
        "default": "and you do not need to follow other's idea.",
        "explicit": "and make cooperation with each other through this discussion.",
    },
    
    "discussion action": {"discussion action": "Now it's your turn to speak. Please share your thoughts concisely in one sentence."}, # GPT 4
    # "discussion action": {"discussion action": "Now it's your turn to speak. Please share your thoughts concisely in one English sentence. Think deeply instead of simply giving your choice."}, # Claude 3

    "reasoning and answer": {
        "in use": ["instruction", "action abstract", "action details"],

        "explicit": "You must cooperate with other players.",
        "uncooperative": "You don't like to cooperate with other players.",

        "instruction": "Based on the discussion with other players,",
        "action abstract": "please choose your number.",
        "action details": "For the first line, state your reasoning concisely for your choice (only in one sentence), and choose an integer between 0 and 100 in the second line."
    }
},

"prompt output": {
    "discussion format": {"format": "Response directly without using format like 'Player #1:'."},
    "number": {"number": "For the second line, only reply the number for your choice (e.g., 12)."},
},
}
