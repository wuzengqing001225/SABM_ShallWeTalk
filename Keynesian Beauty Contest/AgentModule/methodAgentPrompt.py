promptGroupTemplate = {
    "first player discussion": {
        "type": "player",

        "command": """
        ROLE college student
        RULES background
        RULES rewards
        ACTION discussion settings
        ACTION discussion action
        OUTPUT discussion format
        """,

        "value": {"cntPlayerNumberMinusOne": 23, "rangeLeft": 0, "rangeRight": 100, "rewardType": "dollars", "playerIndex": 1}
    },

    "player discussion": {
        "type": "player",

        "command": """
        ROLE college student
        RULES background
        RULES rewards
        ACTION discussion settings
        HISTORY discussion history format

        ACTION discussion action
        OUTPUT discussion format
        """,

        "value": {"cntPlayerNumberMinusOne": 23, "rangeLeft": 0, "rangeRight": 100, "rewardType": "dollars", "textDiscussion": '''(discussion context)''', "playerIndex": 1}
    },

    "player action first round": {
        "type": "player",

        "command": """
        ROLE college student
        RULES background
        RULES rewards
        ACTION reasoning and answer @space
        """,

        "value": {"cntPlayerNumberMinusOne": 23, "rangeLeft": 0, "rangeRight": 100, "rewardType": "dollars", "playerIndex": 1}
    },
    
    "player action": {
        "type": "player",

        "command": """
        ROLE college student
        RULES background
        RULES rewards
        ACTION discussion settings
        HISTORY discussion history format

        ACTION reasoning and answer @space
        """,

        "value": {"cntPlayerNumberMinusOne": 23, "rangeLeft": 0, "rangeRight": 100, "rewardType": "dollars", "textDiscussion": '''(discussion context)''', "playerIndex": 1}
    }
}
