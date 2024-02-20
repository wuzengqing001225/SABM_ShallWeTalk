import copy
import datetime
import time
import os
import json
from protocol import GuessTheAverageGame
from utils import *
import random



def core_task(args):
    args["record id"] = f"{datetime.date.today().strftime('%y%m%d')}_{time.strftime('%H%M')}"

    makedirs(f"./output/record_{args['record id']}_task{args['task name']}")
    print("The PID of the current process is:", os.getpid())
    printable_args = copy.deepcopy(args)
    printable_args.pop("api key")
    print("The parameters are:\n", printable_args)

    game = GuessTheAverageGame(args)
    game.play_game()

def run_task(args, subtask="3-1", task_label=""):
    local_args = copy.deepcopy(args)
    # local_args["ability codes"] = [f"A{subtask[-1]}"] * local_args["number of agents"]

    # persona_types = [format(number, '05b') for number in list(range(32))]
    # persona_counts = [1] * len(persona_types)
    # local_args["persona codes"] = []
    # for code, count in zip(persona_types, persona_counts):
    #     local_args["persona codes"] += [code] * count

    if args["persona dist."] == "all-agreeable":
        persona_types = ["Agreeable"]
    elif args["persona dist."] == "all-disagreeable":
        persona_types = ["Disagreeable"]
    elif args["persona dist."] == "all-none":
        persona_types = ["None"]
    elif args["persona dist."] == "mixed":
        persona_types = ["Agreeable", "Disagreeable", "None"]
    else:
        raise ValueError("Persona distribution undefined")

    local_args["persona codes"] = persona_types * (local_args["number of agents"] // len(persona_types))
    random.shuffle(local_args["persona codes"])
    local_args["number of agents"] = len(local_args["persona codes"])
    local_args["ability codes"] = [f"A{subtask[-1]}"] * local_args["number of agents"]

    local_args["task name"] = subtask + task_label

    core_task(local_args)


def test_with_gpt3_5(args):
     local_args = copy.deepcopy(args)
     local_args["number of agents"] = 5
     local_args["ability codes"] = ["A6"] * local_args["number of agents"]
     local_args["persona codes"] = ["11111", "11110", "11100", "11000", "10000"]
     local_args["task name"] = "(test)"
     local_args["winning score"] = 1
     core_task(local_args)


if __name__ == "__main__":


    with open("config.json") as file:
        args = json.load(file)

    for i in range(1):
        # for persona_dist in [
        #     "all-agreeable",
        #     "all-disagreeable",
        #     "mixed"
        # ]:
        #     args["persona dist."] = persona_dist
        #     args["rewarding rule"] = "amplified"
        #     run_task(args, subtask="3-5", task_label=f"({args['reward type']}_{args['persona dist.']})")

        # args["persona dist."] = "all-none"
        # args["rewarding rule"] = "amplified"
        # run_task(args, subtask="1-1", task_label=f"({args['reward type']}_{args['rewarding rule']})")

        for rule in [
            "amplified",
            # "nothing",
            # "independent"
        ]:
            args["persona dist."] = "all-none"
            args["rewarding rule"] = rule
            run_task(args, subtask="1-2", task_label=f"({args['reward type']}_{args['rewarding rule']})")

