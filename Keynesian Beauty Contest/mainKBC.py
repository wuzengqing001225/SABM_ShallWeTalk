from configEnv import configEnv
from workflowKBC import simulation
from UtilityModule.utilsDataProcess import formatListtoStr
from UtilityModule.fileInputOutput import generateFileTimestamp, fileCsvOutputWriteline

configSimulation = {
    "runs": 3,
    "reward rules": ["independent"],
}

pathSimulationSet = f"SimulationSet_{generateFileTimestamp(mode = 'minute')}"
pathTopOutputFolder = f'./output/{pathSimulationSet}'

def multipleSimulations():
    for rule in configSimulation["reward rules"]:
        for run in range(1, configSimulation["runs"] + 1):
            configEnvCopy = configEnv.copy()
            configEnvCopy["rewardRule"] = rule
            configEnvCopy["fileOutputGroup"] = f"{pathSimulationSet}/{rule}"
            
            print(f"{rule.capitalize()} Run #{run}")

            configEnvCopy["indexRun"] = run
            keyResults = simulation(configEnvCopy)
        
            fileCsvOutputWriteline(f'{pathTopOutputFolder}/{pathSimulationSet}_overview.csv', ["folder name", "run index", "rule", "variance"], [configEnvCopy["configTimestamp"], configEnvCopy["indexRun"], rule, formatListtoStr(keyResults["variance"])])

def singleSimulation():
    configEnvCopy = configEnv.copy()
    keyResults = simulation(configEnvCopy)

multipleSimulations()
