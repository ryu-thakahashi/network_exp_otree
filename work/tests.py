from otree.api import Bot, SubmissionMustFail
import random
import time
from . import pages, models


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield (pages.Intro1)
            yield (pages.Intro2)

        p_id = self.player.id_in_group
        round_odd = self.round_number % 2
        decision = random.choice(["C", "D"])

        time.sleep(random.uniform(3, 7))  # Simulate decision time

        if round_odd and p_id == 1:
            # First mover in odd rounds
            yield (pages.DecisionFirst, {"decision": decision})
        elif not round_odd and p_id == 2:
            # First mover in even rounds
            yield (pages.DecisionFirst, {"decision": decision})

        if not round_odd and p_id == 1:
            # First mover in odd rounds
            yield (pages.DecisionSecond, {"decision": decision})
        elif round_odd and p_id == 2:
            # First mover in even rounds
            yield (pages.DecisionSecond, {"decision": decision})

        yield (pages.Results)
