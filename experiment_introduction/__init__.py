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


def set_question_form(form_label=""):
    return models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, "正しい"], [0, "誤り"]],
        label=form_label,
    )


class Player(BasePlayer):
    q_1 = set_payoff_form()
    q_2 = set_payoff_form()
    q_3 = set_payoff_form()
    q_4_1 = set_question_form(
        "やりとりを行うたびに、あなたがやりとりをする 4人の相手は変わる"
    )
    q_4_2 = set_question_form(
        "あなたが獲得するポイントは、あなたの選択とつながりのある4人の相手の選択の組み合わせによって決まる"
    )
    q_4_3 = set_question_form("課題の繰り返し回数は、事前にはみなさんには知らされない")


# PAGES
class Introduction(Page):
    pass


class CheckTest(Page):
    form_model = "player"
    form_fields = ["q_1", "q_2", "q_3", "q_4_1", "q_4_2", "q_4_3"]

    @staticmethod
    def error_message(player: Player, values):
        correct_answers = {
            "q_1": 22,
            "q_2": 4,
            "q_3": 6,
            "q_4_1": 0,
            "q_4_2": 1,
            "q_4_3": 1,
        }

        all_correct = True
        for question, answer in correct_answers.items():
            if values[question] != answer:
                all_correct = False
                break

        return "誤りがあります．再度ご回答ください．" if not all_correct else None


page_sequence = [Introduction, CheckTest]
