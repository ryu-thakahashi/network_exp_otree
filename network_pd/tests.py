import random
from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def select_action_randomly(self):
        return random.randint(0, 1)

    def play_round(self):
        # time.sleep(random.uniform(0.1, 0.3))
        yield Decision, dict(action=self.select_action_randomly())
        yield Results

        act_list = [p.action for p in self.group.get_players()]
        p_pos = self.player.id_in_group - 1
        expected_payoff = calc_payoff(act_list, p_pos, C.NEIGHBOR_NUM, C.BC_RATIO)
        assert self.player.current_payoff == expected_payoff
