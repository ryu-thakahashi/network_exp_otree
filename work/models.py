from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'work'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    PAYOFFS = {
        ('C', 'C'): (3, 3),
        ('C', 'D'): (0, 5),
        ('D', 'C'): (5, 0),
        ('D', 'D'): (1, 1),
    }

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    delay_seconds = models.FloatField() 
    
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        outcome = (p1.decision, p2.decision)
        p1.payoff, p2.payoff = C.PAYOFFS[outcome]

class Player(BasePlayer):
    decision = models.StringField(
        choices=[('C', 'C(協力する)'), ('D', 'D(裏切る)')],
        label="あなたの選択をしてください。",
        widget=widgets.RadioSelect
    )
    
    decision_time = models.FloatField()
    delay_condition = models.StringField()
    
