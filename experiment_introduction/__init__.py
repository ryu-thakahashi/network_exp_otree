from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = "experiment_introduction"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def set_payoff_form(form_label=""):
    return models.IntegerField(
        choices=[0, 6, 12, 18, 24, 4, 10, 16, 22, 28],
        label=form_label,
    )


class Player(BasePlayer):
    offer_1 = set_payoff_form()
    offer_2 = set_payoff_form()
    offer_3 = set_payoff_form()
    offer_4 = set_payoff_form()


# PAGES
class Introduction(Page):
    pass


class CheckTest(Page):
    form_model = "player"
    form_fields = ["offer_1", "offer_2"]

    @staticmethod
    def error_message(player: Player, values):
        all_correct = True
        if values["offer_1"] != 0:
            all_correct = False
        if values["offer_2"] != 6:
            all_correct = False
        return "Please check your answers again." if not all_correct else None


page_sequence = [Introduction, CheckTest]
