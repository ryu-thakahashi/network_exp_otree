from otree.api import *
import time
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = "network_pd"
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 5
    BC_RATIO = 4
    NEIGHBOR_NUM = 4


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    print("creating_session")
    if subsession.round_number == 1:
        subsession.group_randomly()
        for p in subsession.get_players():
            p.participant.vars["group_id"] = p.group.id_in_subsession
    else:
        subsession.group_like_round(1)


class Group(BaseGroup):
    dicision_start_time = models.FloatField()


class Player(BasePlayer):
    action = models.IntegerField(
        choices=[0, 1],
        label="Choose your action:",
        widget=widgets.RadioSelect,
    )
    time_out = models.BooleanField(
        initial=False,
    )
    current_payoff = models.IntegerField(
        label="Current payoff",
        initial=0,
    )

    neighbor_actions = models.StringField(
        label="Neighbor actions",
        initial="",
    )
    neighbor_payoffs = models.StringField(
        label="Neighbor payoffs",
        initial="",
    )
    highest_action = models.IntegerField(
        label="Highest action",
        initial=0,
    )


# FUNCTION
def get_neighbors(network_size: int, p_id: int, k: int) -> set:
    half_k = k // 2
    nei_pos = [(p_id + i) % network_size for i in range(-half_k, half_k + 1)]
    nei_pos.remove(p_id)

    return nei_pos


def get_neighbors_actions(act_list: list, p_pos: int, k: int) -> list:
    neighbors = get_neighbors(len(act_list), p_pos, k)
    actions = [act_list[i] for i in neighbors]
    return actions


def get_neighbors_payoffs(payoff_list: list, p_pos: int, k: int) -> list:
    neighbors = get_neighbors(len(payoff_list), p_pos, k)
    payoffs = [payoff_list[i] for i in neighbors]
    return payoffs


def calc_payoff(act_list: list, p_pos: int, k: int, bc_ratio: int) -> float:
    neighbors = get_neighbors(len(act_list), p_pos, k)
    actions = [act_list[i] for i in neighbors]
    return bc_ratio * sum(actions) - len(actions) * act_list[p_pos] + k


def set_payoffs(group: Group) -> None:
    player_list = group.get_players()
    action_list = [p.action for p in player_list]

    for player in player_list:
        p_pos = player.id_in_group - 1
        player.current_payoff = calc_payoff(
            action_list, p_pos, C.NEIGHBOR_NUM, C.BC_RATIO
        )


def record_start_time(subsession: Subsession) -> None:
    group = subsession.get_groups()[0]
    group.dicision_start_time = time.time()


def record_neighbor_actions(player: Player) -> None:
    player_list = player.group.get_players()
    action_list = [p.action for p in player_list]
    nei_actions = get_neighbors_actions(
        action_list, player.id_in_group - 1, C.NEIGHBOR_NUM
    )
    player.neighbor_actions = ",".join([str(a) for a in nei_actions])


def record_neighbor_payoffs(player: Player) -> None:
    player_list = player.group.get_players()
    payoff_list = [p.current_payoff for p in player_list]
    nei_payoffs = get_neighbors_payoffs(
        payoff_list, player.id_in_group - 1, C.NEIGHBOR_NUM
    )
    player.neighbor_payoffs = ",".join([str(a) for a in nei_payoffs])


def record_highest_action(player: Player) -> None:
    player_list = player.group.get_players()
    action_list = [p.action for p in player_list]
    payoff_list = [p.current_payoff for p in player_list]
    nei_actions = get_neighbors_actions(
        action_list, player.id_in_group - 1, C.NEIGHBOR_NUM
    )
    nei_payoffs = get_neighbors_payoffs(
        payoff_list, player.id_in_group - 1, C.NEIGHBOR_NUM
    )
    highest_payoff = max(nei_payoffs)
    if highest_payoff <= player.current_payoff:
        player.highest_action = player.action
    else:
        highest_neighbor_action = nei_actions[nei_payoffs.index(highest_payoff)]
        player.highest_action = highest_neighbor_action


def save_player_data(player: Player):
    record_neighbor_actions(player)
    record_neighbor_payoffs(player)
    record_highest_action(player)


# PAGES
class WaitForAll(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = "record_start_time"


class Decision(Page):
    form_model = "player"
    form_fields = ["action"]
    timeout_seconds = 5

    # @staticmethod
    # def get_timeout_seconds(player):
    #     if player.participant.vars.get("is_dropped"):
    #         return 20
    #     return 1

    @staticmethod
    def js_vars(player: Player):
        return {
            "num_of_k": C.NEIGHBOR_NUM,
            "start_time": player.group.dicision_start_time,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars["is_dropped"] = True
            player.action = random.randint(0, 1)
        player.time_out = timeout_happened


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoffs"


class Results(Page):
    timeout_seconds = 5

    # @staticmethod
    # def get_timeout_seconds(player):
    #     if player.participant.vars.get("is_dropped", False):
    #         return 10
    #     return 1

    @staticmethod
    def js_vars(player: Player):

        save_player_data(player)
        player_list = player.group.get_players()
        action_list = [p.action for p in player_list]
        payoff_list = [p.current_payoff for p in player_list]
        p_pos = player.id_in_group - 1

        return {
            "self_action": player.action,
            "self_payoff": player.current_payoff,
            "actions": get_neighbors_actions(action_list, p_pos, C.NEIGHBOR_NUM),
            "payoffs": get_neighbors_payoffs(payoff_list, p_pos, C.NEIGHBOR_NUM),
            "show_payoffs": True,
            "num_of_k": C.NEIGHBOR_NUM,
        }


page_sequence = [WaitForAll, Decision, ResultsWaitPage, Results]
