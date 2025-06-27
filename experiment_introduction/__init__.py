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
        choices=[0, 4, 6, 10, 12, 16, 18, 22, 24, 28],
        label=form_label,
    )


class Player(BasePlayer):
    question_1 = set_payoff_form()
    question_2 = set_payoff_form()
    question_3 = set_payoff_form()


# PAGES
class Introduction(Page):
    pass


class CheckTest(Page):
    form_model = "player"
    form_fields = ["question_1", "question_2", "question_3"]

    @staticmethod
    def error_message(player: Player, values):
        all_correct = True
        if values["question_1"] != 22:
            all_correct = False
        if values["question_2"] != 4:
            all_correct = False
        if values["question_3"] != 6:
            all_correct = False
        return "誤りがあります．再度ご回答ください．" if not all_correct else None


page_sequence = [Introduction, CheckTest]
