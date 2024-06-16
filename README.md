# SABM: Shall We Team Up

![Workflow](https://github.com/wuzengqing001225/SABM_ShallWeTalk/blob/main/IMG/workflow_overview.jpg?raw=true)

This repository is the source code for our paper **[Shall We Team Up: Exploring Spontaneous Collaborations of Competing LLM Agents](https://arxiv.org/abs/2402.12327)**. In this work, we investigate whether LLM-empowered agents can achieve *spontaneous cooperation in a competitive environment* and explore its patterns through interdisciplinary case studies, including the **Keynesian Beauty Contest** (Game Theory), **Bertrand Competition** (Economics), and **Emergency Evacuation** (Behavioral Science).

This work is realized based on a novel Agent-Based Modeling framework we proposed: Smart Agent-Based Modeling (SABM).

**[Smart Agent-Based Modeling: On the Use of Large Language Models in Computer Simulations](https://arxiv.org/abs/2311.06330)**.

## Setup

Please make sure you have the valid OpenAI API key for GPT-4 model. Otherwise, you may need to apply for one before you test our codes.

***Please do not commit your API key to GitHub, or share it with anyone online.**

### Keynesian Beauty Contest

To reproduce the results in the paper, please place your OpenAI API key in the ```configAPIKey.json``` file and then run the following command.

```bash
python mainKBC.py
```

The `configSimulation["runs"]` controls the total runs of simulation.

You can also modify the `configSimulation["reward rules"]` variable to observe different agent performances under various reward rules.

You may change the simulation settings in ```configEnv.py``` file.

### Bertrand Competition

To reproduce the results in the paper, please run the following command.

```bash
python SABM_Economics_Main.py
```

The ```Base Model``` folder contains the basic settings for the Bertrand competition with and without communication as discussed in the paper, while the ```Model with Uncooperative Persona``` folder includes the settings for the uncooperative persona with communication.

You may also utilize the GUI of this case study to configure simulation parameters, including modifying the agents' personas and enabling communication between them.

Please place your OpenAI API key in the ```SABM_Economics_Main.py``` file (lines 21-22). You can use the same API key for ```my_apikey1``` and ```my_apikey2```.


### Emergency Evacuation

To reproduce the results in the paper, please run the following command.

```bash
python main_emergency_evacuation.py --task <task_id>
```

The `<task_id>` can be one of the following options: [1, 2, 3]. Each task id corresponds to a specific setting in the paper:

Task 1: w/o communication; Task 2: w/ communication; Task 3: w/ communication + uncooperative persona.

Additionally, if you would like to specify a seed, the number of humans, and add obstacles in the environment, you may want to run the following command.

```bash
python main_emergency_evacuation.py --task <task_id> --seed <seed> --num_humans <num_humans> --need_obstacle
```

Please place your OpenAI API key in the ```apikey.token``` file.

## Citation

If you find our work useful, please give us credit by citing:

(1) Shall We Team Up paper
```bibtex
@misc{wu2024shall,
      title={Shall We Talk: Exploring Spontaneous Collaborations of Competing LLM Agents}, 
      author={Zengqing Wu and Shuyuan Zheng and Qianying Liu and Xu Han and Brian Inhyuk Kwon and Makoto Onizuka and Shaojie Tang and Run Peng and Chuan Xiao},
      year={2024},
      eprint={2402.12327},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```

(2) SABM Framework
```bibtex
@misc{wu2023smart,
      title={Smart Agent-Based Modeling: On the Use of Large Language Models in Computer Simulations}, 
      author={Zengqing Wu and Run Peng and Xu Han and Shuyuan Zheng and Yixin Zhang and Chuan Xiao},
      year={2023},
      eprint={2311.06330},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
