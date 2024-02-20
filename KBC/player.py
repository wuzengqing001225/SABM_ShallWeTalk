from agent import Agent
import prompt
from utils import extract_last_number

models = {
    # "gpt-4": "gpt-4-0613",
    "gpt-4": "gpt-4-0314",
    "gpt-3": "gpt-3.5-turbo-0613"
}

class Player(Agent):
    # Initializes each Player with a unique ID, persona, and score.
    def __init__(self, player_id, persona_code, ability_code="A1", temperature=1.0, max_tokens=256):
        self.ability_code = ability_code
        self.model = None
        self.comm_ability = None
        self.has_knowledge = None
        self.decode_ability()
        Agent.__init__(self, temperature, self.model, max_tokens)
        self.player_id = player_id  # Unique identifier for the player
        self.persona_code = persona_code
        self.persona = prompt.persona_details[self.persona_code]
        # self.decode_persona()      # Persona assigned to the player
        self.score = 0              # Score of the player
        self.choice_history = []    # History of the player's choices
        self.win_history = []       # 0: Lose, 1: Win
        self.reason_history = []
        self.win_data = []
        self.communication_history = []

    def decode_persona(self):
        if self.persona_code == "None":
            self.persona = prompt.persona_details["None"]
            return
        persona_components = []
        for dim, level in zip(prompt.persona_details.keys(), self.persona_code):
            persona_components.append(prompt.persona_details[dim][level])

        self.persona = ", ".join(persona_components)

    def decode_ability(self):
        if self.ability_code == "A1":
            self.model = models["gpt-4"]
            self.comm_ability = False
            self.has_knowledge = False
        elif self.ability_code == "A2":
            self.model = models["gpt-3"]
            self.comm_ability = False
            self.has_knowledge = False
        elif self.ability_code == "A3":
            self.model = models["gpt-4"]
            self.comm_ability = False
            self.has_knowledge = True
        elif self.ability_code == "A4":
            self.model = models["gpt-4"]
            self.comm_ability = True
            self.has_knowledge = True
        elif self.ability_code == "A5":
            self.model = models["gpt-4"]
            self.comm_ability = True
            self.has_knowledge = False
        elif self.ability_code == "A6":
            self.model = models["gpt-3"]
            self.comm_ability = True
            self.has_knowledge = False
        else:
            raise ValueError("Unknown ability code")

    # Format guess history
    def format_history(self):
        history_prompt = ""
        for i, j, k in zip(self.choice_history, self.win_history, self.win_data):
            if j == 0: history_prompt += f"{i} (Lose, the closest number was {k}), "
            else: history_prompt += f"{i} (Win), "
        history_prompt += f"where you won {self.win_history.count(1)} time(s)."
        return history_prompt
    
    # def format_persona(self):
    #     def get_key(dict, value):
    #         return [k for k, v in dict.items() if v == value][0]
    #
    #     return get_key(prompt.persona_details, self.persona)

    def format_response(self, response):
        response = f"Player {self.player_id}: {response}"
        print("<<Response>>", response, '\n-------------------------------------------\n')
        # print(f"Player {self.player_id} ({self.format_persona()}): {response}\n")
        return response

    ### FIX
    # Generates and prints feedback based on the round and game status.
    def provide_feedback(self, round_number, is_final_round):
        feedback_prompt = self.generate_feedback_prompt(round_number, is_final_round)
        feedback = self.get_gpt4_response(feedback_prompt)
        print(f"{feedback_prompt}\nPlayer {self.player_id} ({self.persona}): {feedback}")

    # Generates feedback prompt based on the round number and if it's the final round.
    def generate_feedback_prompt(self, round_number, is_final_round):
        if is_final_round:
            return f"Player {self.player_id} ({self.persona}), the game has ended. Please share how you feel about the game."
        else:
            return f"Player {self.player_id} ({self.persona}), after Round {round_number}, how do you feel about the outcome and your choice?"

    def guess_with_reason(self, game_instruction_prompt):
        response = []
        while len(response) < 2:
            response = self.communicate(game_instruction_prompt).split('\n')
            response = [s for s in response if s != ""]

        guess_ = response[0].strip()
        try:
            guess = int(guess_)
        except ValueError:
            print(f"Invalid guess: {guess_}\n")
            guess = extract_last_number(guess_)

        reason = response[1].strip()

        self.choice_history.append(guess)
        self.reason_history.append(reason)
        self.format_response(response=response)

        return guess, reason

    @staticmethod
    def generate_players(ability_codes, persona_codes):
        players = []
        for i in range(len(persona_codes)):
            p = Player(i + 1, persona_codes[i], ability_code=ability_codes[i])
            players.append(p)

        return players

