import csv
import player
from typing import List
from utils import *
import json


def log_output_player(csv_filename:str, players:List[player.Player]):
    def format_win(flag, closest_number):
        if flag == 0: return f'Lose (Closest: {closest_number})'
        else: return 'Win'

    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Player ID', 'Persona', 'Round', 'Choice', 'Result','Reasoning', 'Score'])
        
        for p in players:
            score_count = 0
            for game_round in range(len(p.choice_history)):
                if p.win_history[game_round] == 1: score_count += 1
                writer.writerow([p.player_id, p.persona_code, game_round + 1, p.choice_history[game_round], format_win(p.win_history[game_round], p.win_data[game_round]), p.reason_history[game_round], score_count])


def log_output_args(json_filename:str, args):
    with open(json_filename, 'w') as file:
        json.dump(args, file, indent=4)


def log_output_overview(csv_filename:str, winner_history, winning_guesses, previous_rounds_history, players:List[player.Player]):
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Round', 'Winning Guess']
        for p in players:
            header.append(f"{p.player_id} ({p.persona_code})")
        header.append('Round Average')
        header.append('Winner')
        writer.writerow(header)

        for game_round in range(len(winning_guesses)):
            write_row = []
            write_row.append(game_round + 1)
            write_row.append(winning_guesses[game_round])
            for d in previous_rounds_history[game_round]:
                write_row.append(d)
            write_row.append(round(sum(previous_rounds_history[game_round]) / float(len(previous_rounds_history[game_round])), 3))
            if winner_history[game_round] == None:
                write_row.append('Tie')
            else:
                write_row.append(index_to_id(winner_history[game_round]))
            writer.writerow(write_row)

def log_output_communication(csv_filename:str, communication_history, previous_rounds_history):
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Round', 'Communication'])
        
        for game_round in range(len(communication_history)):
            for player_number in range(len(communication_history[game_round])):
                writer.writerow([game_round + 1, communication_history[game_round][player_number]])
                # writer.writerow([game_round + 1, communication_history[game_round][player_number], previous_rounds_history[game_round][player_number]])
