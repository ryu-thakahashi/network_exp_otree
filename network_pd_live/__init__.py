from otree.api import *
import time
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = "network_pd_live"
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 5
    BC_RATIO = 6
    NEIGHBOR_NUM = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    show_payoffs = models.BooleanField()


class Player(BasePlayer):
    actions = models.StringField(
        doc="A string of actions taken by the player in the current round, e.g., 'CCDDCC'"
    )

    neighbor_actions = models.StringField(
        label="Neighbor actions",
        initial="",
    )
    neighbor_coop_ratio = models.LongStringField()
    neighbor_payoffs = models.StringField(
        label="Neighbor payoffs",
        initial="",
    )
    highest_actions = models.StringField(
        label="Highest action",
    )
    show_payoffs = models.BooleanField(label="Show payoffs")


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
    action_list = [p.get_action() for p in player_list]

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
    action_list = [p.get_action() for p in player_list]
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


def record_neighbor_coop_ratio(player: Player) -> None:
    player_list = player.group.get_players()
    action_list = [p.get_action() for p in player_list]
    nei_actions = get_neighbors_actions(
        action_list, player.id_in_group - 1, C.NEIGHBOR_NUM
    )
    coop_count = sum(nei_actions)
    if len(nei_actions) > 0:
        player.neighbor_coop_ratio = coop_count / len(nei_actions)
    else:
        player.neighbor_coop_ratio = 0.0


def record_highest_action(player: Player) -> None:
    player_list = player.group.get_players()
    action_list = [p.get_action() for p in player_list]
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


def record_show_payoffs(player: Player) -> None:
    player.show_payoffs = player.participant.vars.get("show_payoffs")


def save_player_data(player: Player):
    player.payoff += player.current_payoff
    record_neighbor_actions(player)
    record_neighbor_coop_ratio(player)
    record_neighbor_payoffs(player)
    record_highest_action(player)
    record_show_payoffs(player)


def set_conditions(group: Group):
    if group.round_number != 1:
        return

    group.show_payoffs = random.choice([True, False])
    for player in group.get_players():
        player.participant.vars["show_payoffs"] = group.show_payoffs


# PAGES
class WaitForAll(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Decision(Page):

    @staticmethod
    def js_vars(player: Player):
        return {"num_of_k": C.NEIGHBOR_NUM}

    @staticmethod
    def live_method(player: Player, data):
        player.action = data["action"]

        if player.action == 99:
            player.participant.vars["is_dropped"] = True
        else:
            player.participant.vars["is_dropped"] = False
        return {0: "game_finished"}


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [WaitForAll, Decision, ResultsWaitPage, Results]
