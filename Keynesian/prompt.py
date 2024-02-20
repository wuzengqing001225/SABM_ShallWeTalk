game_rule = {
#     "singleRound": "Welcome to the game. \
# You will be asked to choose a number between 0-100. \
# The player(s) whose guess is the closest to 2/3 of the average of all the players' guesses \
# will win the game. \
# If all the players choose the same number, they all will win the game.\n",

    "singleRound": "Welcome to the game. \
You players will be asked to choose a number between 0 and 100.\n\
The player(s) who select a number closest to 2/3 of the average of all selected numbers (compared with the choices of other players) will win the game.\n",

    "multiRound": "Welcome to the game. \
We will play at most {max_round} rounds of gaming. \
At each round, you will be asked to choose a number between 0-100. \
The player(s) whose guess is the closest to 2/3 of the average of all the players' guesses \
will win this round and earn one score. \
Finally, the player(s) who first earned {winning_score} scores will win the game.\n",
}

reward = "You will earn {reward_content} as a reward if you win the game alone.\n"

no_reward = "No rewards will be granted to winners.\n"

base_rewarding_rule = {
    "none": "This is a voluntary test. " + no_reward,

    "money": "You players are gambling in a casino. " + reward,

    "exam mark": "You players are college students. " + reward,

    "ticket": "You players are customers of a travel company. "
              "Now the company is holding a festival for rewarding customers. " + reward,

    "sentence reduction": "You are a prisoner. " + reward,
}

multi_winners_rewarding_rule = {
    "independent":
        "If multiple players win the game together, each winner will obtain an independent reward.\n"
        "That is, each winner will earn {reward_content}.\n",
    "nothing":
        "If multiple players win the game together, no one will obtain a reward.\n"
        "That is, only by winning alone can one earn {reward_content}.\n",
        # "If there are multiple winners, no one will obtain a reward.\n"
        # "That is, if M players win the game, no reward will be granted for them.\n",
    "amplified":
        "If multiple players win the game together, each winner will obtain an amplified reward "
        "that is scaled based on the number of winners.\n"
        "That is, if M players win the game, each winner will earn M*{reward_content}.\n",
    # "allocation": "If there are multiple winners, the reward will be uniformly allocated among winners.",
    # "allocation-": "If there are m winners, the reward will be decreased by m*10% and "
    #                "and then be uniformly allocated among winners.",
    # "allocation+": "If there are m winners, the reward will be increased by m*10% "
    #                "and then be uniformly allocated among winners.",
    # "unfair": "If there are multiple winners, only the winner with smallest ID will obtain the reward.",
}

# communication_rule = "Before selecting a number, \
# all players are allowed to discuss the game together, taking two turns to speak. \
# In each turn, the players can present their ideas one by one. \
# (However, you don't need to truthfully report your ideas.)\n"

communication_rule = "Before selecting a number, \
all players are allowed to discuss the game together, taking two turns to speak. \
In each turn, the players can present their ideas one by one.\n"

# Knowledge
game_knowledge = "The number above 66 is not possible. \
Players guessing numbers higher than 66 show that they have absolutely no clue about what is going on in the game. \
They can be classified as layer zero. The idea of the first layer of players is: \
Assuming that the distribution of people who select numbers is uniform, then the final average number should be 50. \
2/3 of 50 is 33. Therefore, I should choose 33 to maximize my probability of winning. \
The idea of the second level player is: \
Assuming that most people think like the player above, then the average of these numbers in the end is not 50, but 33. \
Multiply 33 by 2/3 to get 22. Therefore, if you want to win the game, the more rational choice is 22 instead of 33. \
Go for deeper layers!\n"

# game_knowledge = {
#     "closest": "The number above 66 is not possible. \
# Players guessing numbers higher than 66 show that they have absolutely no clue about what is going on in the game. \
# They can be classified as layer zero. The idea of the first layer of players is: \
# Assuming that the distribution of people who select numbers is uniform, then the final average number should be 50. \
# 2/3 of 50 is 33. Therefore, I should choose 33 to maximize my probability of winning. \
# The idea of the second level player is: \
# Assuming that most people think like the player above, then the average of these numbers in the end is not 50, but 33. \
# Multiply 33 by 2/3 to get 22. Therefore, if you want to win the game, the more rational choice is 22 instead of 33. \
# Go for deeper layers!\n",
#     "farthest": "The idea of the first layer of players is: \
# Assuming that the distribution of people who select numbers is uniform, then the final average number should be 50. \
# 2/3 of 50 is 33. Therefore, I should choose 100 to maximize my probability of winning. \
# The idea of the second level player is: \
# Assuming that most people think like the player above, then the average of these numbers in the end is not 50, but 100. \
# Multiply 100 by 2/3 to get 66. Therefore, if you want to win the game, the more rational choice is 0 instead of 100. \
# Go for deeper layers!\n"
# }



def game_background_instruction(reward_type, rewarding_rule, multi_round=False, has_knowledge=False, comm_ability=False):
    instruction = ""

    if multi_round:
        instruction += game_rule["multiRound"]
    else:
        instruction += game_rule["singleRound"]

    instruction += base_rewarding_rule[reward_type]
    if reward_type != "None":
        instruction += multi_winners_rewarding_rule[rewarding_rule]

    if comm_ability:
        instruction += communication_rule

    if has_knowledge:
        instruction += game_knowledge
    instruction += "\n"

    return instruction


# Descriptions for each persona type
persona_details = {
    # "Extraversion": {
    #     "0": "shy, quiet, reserved, passive, solitary, moody, joyless",
    #     "1": "warm, gregarious, assertive, sociable, excitement seeking, active, spontaneous, optimistic, talkative"
    # },
    # "Emotional stability": {
    #     "0": "neurotic, anxious, depressed, self-conscious, oversensitive, vulnerable",
    #     "1": "calm, even-tempered, reliable, peaceful, confident"
    # },
    # "Agreeableness": {
    #     "0": "unfriendly, selfish, suspicious, uncooperative, malicious",
    #     "1": "trustworthy, friendly, considerate, generous, helpful, altruistic"
    # },
    # "Conscientiousness": {
    #     "0": "disorganised, impulsive, unreliable, careless, forgetful",
    #     "1": "competent, disciplined, dutiful, achievement striving, deliberate, careful, orderly"
    # },
    # "Openness to experience": {
    #     "0": "narrow-minded, conservative, ignorant, simple",
    #     "1": "creative, intellectual, imaginative, curious, cultured, complex"
    # },
    "Agreeable": "an agreeable player participating the number-choosing game",
    "Disagreeable": "a disagreeable player participating the number-choosing game",
    "None": "a player participating the number-choosing game"
}

round_beginning = "We are now going to play Round {round_number}.\n"

# persona = "Player {player_id}, you are {persona}.\n"

choice_history = "Your previous guesses were: {previous_guesses}\n"


# Communication
# communication_rule = "You are now allowed to simply exchange your ideas in one paragraph with other players in your group before you choose a number. \
# You can say explicitly, such as 'I think I will select 28.' You don't need to indicate your identity in the response. \
# The number you disclosed in communication, however, may not be consistent with your final choice.\n"


communication_request = "Let's start discussion:\n{previous_talks}\
Player {player_id}, you are {persona}. Please speak.\n\
(Please present your ideas as concisely as possible. \
You may state your strategy explicitly, e.g., 'I will select X.' \
You don't need to indicate your identity in the response.)"



def communication_instruction(round_number, multi_round=False):
    instruction = ""

    if multi_round:
        instruction += round_beginning
        if round_number > 1:
            instruction += choice_history

    instruction += communication_request

    return instruction


communication_history = "This is a record of your previous discussions:\n<<{communication_history}>>\n"

choice_request = "Player {player_id}, you are {persona}.\n\
Please enter your choice of number between 0 and 100 on the first line \
(reply with a number only, without any text, e.g., '100'), \
and provide a brief explanation of your choice on the second line.\n"

# choice_request = "Player {player_id}, you are {persona}.\n\
# Please output your reasoning about the number selection on the first line \
# and enter your choice of number between 0 and 100 on the second line \
# (reply with a number only, without any text, e.g., '100').\n"

def decision_instruction(round_number, comm_ability=False, multi_round=False):
    instruction = ""
    # instruction += persona

    if multi_round:
        instruction += round_beginning
        if round_number > 1:
            instruction += choice_history

    if comm_ability:
        instruction += communication_history

    instruction += choice_request
    return instruction

