from tqdm import tqdm
from utils import *
import random
import openai
import prompt
import player
import output
import copy


class GuessTheAverageGame:
    # Main game class to manage the "Guess ⅔ of the Average" game.
    def __init__(self, args):
        self.args = args
        openai.api_key = args["api key"]  # API key for OpenAI
        self.N = args["number of agents"]
        self.max_round = args["max. round"]  # Max rounds of the game
        self.winning_score = args["winning score"]
        self.multi_winner = args["multi. winners allowed"]
        self.record_id = args["record id"]
        self.task_name = args["task name"]
        self.reward_type = args["reward type"]
        self.reward_content = args["reward content"]
        self.rewarding_rule = args["rewarding rule"]
        self.type_codes = args["ability codes"]
        self.persona_codes = args["persona codes"]
        self.players = player.Player.generate_players(self.type_codes, self.persona_codes)
        self.winning_guesses = []  # To track the winning guess of each round
        self.winner_history = []
        self.previous_rounds_history = []
        self.communication_history = []
        self.output_path = f"./output/record_{self.record_id}_task{self.task_name}/"
        self.multi_round = True
        if self.winning_score == 1 and self.multi_winner:
            self.multi_round = False

    def construct_instruction(self, player, round_number, comm_instruction=False):
        instruction = ""
        instruction += prompt.game_background_instruction(self.reward_type, self.rewarding_rule, self.multi_round,
                                                          player.has_knowledge, comm_instruction).format(
            number_of_players=self.N, max_round=self.max_round, winning_score=self.winning_score, reward_content=self.reward_content)
        if comm_instruction:
            instruction += prompt.communication_instruction(round_number, self.multi_round).format(
                round_number=round_number, player_id=player.player_id, persona=player.persona,
                previous_guesses=player.format_history(), previous_talks=self.format_communication())
            print("<<Communication PROMPT>> ", instruction, '\n-------------------------------------------\n')
        else:
            instruction += prompt.decision_instruction(round_number, player.comm_ability, self.multi_round).format(
                round_number=round_number, player_id=player.player_id, persona=player.persona,
                previous_guesses=player.format_history(), communication_history=self.format_communication())
            print("<<Instruction PROMPT>> ", instruction, '\n-------------------------------------------\n')
        return instruction

    # Method to start and manage the game rounds.
    def play_game(self):
        for round_number in tqdm(range(1, self.max_round + 1)):
            round_choices = []
            self.communication_history.append([])
            # Discussion phase
            for i in range(2):
                for player in self.players:
                    if player.comm_ability:
                        game_communication_prompt = self.construct_instruction(player, round_number, comm_instruction=True)
                        response = player.communicate(game_communication_prompt)
                        response = player.format_response(response)
                        player.communication_history.append(response)
                        self.communication_history[-1].append(response)
            # Decision-making phase
            for player in self.players:
                game_instruction_prompt = self.construct_instruction(player, round_number, comm_instruction=False)
                guess, _ = player.guess_with_reason(game_instruction_prompt)
                round_choices.append(guess)

            winner_index, closest = self.determine_winner(round_choices)  # Determine the round winner
            self.previous_rounds_history.append(round_choices)
            self.winner_history.append(winner_index)
            self.winning_guesses.append(closest)

            # Update the score of the winner
            for player in self.players:
                if player.player_id - 1 in winner_index:
                    player.win_history.append(1)
                    player.score += 1
                else:
                    player.win_history.append(0)
                player.win_data.append(closest)

            # Print round results and get post-round feedback
            self.display_round_summary(round_number, winner_index)

            '''
            for player in self.players:
                player.provide_feedback(round_number, round_number == self.max_round, self.api_key)
            '''

            # Check for game end condition
            if max([player.score for player in self.players]) >= self.winning_score:
                print("Winner found!")
                break

        # Output data
        printable_args = copy.deepcopy(self.args)
        printable_args.pop("api key")
        output.log_output_args(self.output_path + f'{self.record_id}_args.json', printable_args)
        output.log_output_player(self.output_path + f'{self.record_id}_player.csv', self.players)
        output.log_output_overview(self.output_path + f'{self.record_id}_overview.csv', self.winner_history,
                                   self.winning_guesses, self.previous_rounds_history, self.players)
        output.log_output_communication(self.output_path + f'{self.record_id}_communication.csv',
                                        self.communication_history, self.previous_rounds_history)

        # Display final game results
        self.display_final_scores()

    # Calculate the average and determine the round winner
    def determine_winner(self, round_choices):
        average = sum(round_choices) / float(len(round_choices))
        target = 2 / 3 * average
        closest = min(round_choices, key=lambda x: abs(target - x))

        if round_choices.count(closest) > 1 and not self.multi_winner:
            return None, None
        else:
            return find_indexes(round_choices, closest), closest

    # Print round results
    def display_round_summary(self, round_number, winner_index):
        print(f"Round {round_number}: Choices = [{self.previous_rounds_history[-1]}]")

        if winner_index is None:
            print(f"Winner = None")
        elif len(winner_index) > 1:
            print(f"Winners = Players {index_to_id(winner_index)}\n")
        else:
            print(f"Winner = Player {winner_index[0] + 1}\n")

        print("Current Scores:")
        for player in self.players:
            print(f"- Player {player.player_id}: {player.score} points")
        print()

    # Display final scores and the winner
    def display_final_scores(self):
        print("\nFinal Scores:")
        for player in self.players:
            print(f"- Player {player.player_id}: {player.score} points")
        winner = max(self.players, key=lambda p: p.score)
        if self.multi_winner:
            winners_ids = [p.player_id for p in self.players if p.score == winner.score]
            print(f"Winners: Players {winners_ids} with {winner.score} points")
        else:
            print(f"Winner: Player {winner.player_id} with {winner.score} points")

    def format_communication(self):
        communication_information = ""
        for record in self.communication_history[-1]:
            communication_information += record + '\n'
        # communication_information = communication_information.rstrip("\n")
        return communication_information