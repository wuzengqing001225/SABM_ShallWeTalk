from UtilityModule import fileInputOutput

configEnv = {
    "description": "Default setting with 24 agents and 4 rounds.",

    # Model
    "model": 'gpt-4-0314',
    # "model": 'claude-3-sonnet-20240229',

    # Common parameters
    ## (4, 3) for debugging, and (24, 4) for default setting
    "cntAgent": 24,
    "maxRound": 4,

    # GPT parameters
    "temperature": 0.7,
    "maxToken": 128,

    # Scenario specific parameters
    "guessRange": (0, 100),
    "rewardType": "dollars",
    "rewardRule": "independent", # Option: ["independent", "amplified", "exclusive"]

    # Simulation config
    "runMode": "LLM", # Option: ["LLM", "rule"]
    "configAPIKey": fileInputOutput.formatConfigAPIKeyExtract(configAPIKeySource = 'GPT.OsakaUniv'),
    "configTimestamp": fileInputOutput.generateFileTimestamp(),
    
    "fileOutputGroup": None, # Option: ["", None, "independent", "amplified", "exclusive"]
    "indexRun": 0, # 0 as default

    "verbosity": 1 # Level: {0: None, 1: Critical, 2: Normal, 3: Verbose}
}
