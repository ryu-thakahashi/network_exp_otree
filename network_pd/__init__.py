from otree.api import *
import time
import random
import otree.channels.utils as channel_utils

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = "network_pd"
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 15
    BC_RATIO = 4
    NEIGHBOR_NUM = 4


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    print("creating_session")

    if subsession.round_number == 1:
        for group in subsession.get_groups():
            print(f"Group {group.id_in_subsession} created")
    else:
        subsession.group_like_round(1)


class Group(BaseGroup):
    dicision_start_time = models.FloatField()
    show_payoffs = models.BooleanField()


class Player(BasePlayer):
    action = models.IntegerField(
        choices=[0, 1],
        label="Choose your action:",
        widget=widgets.RadioSelect,
    )
    confirm_results = models.IntegerField()
    time_out = models.BooleanField(initial=False)
    current_payoff = models.IntegerField(initial=None)

    neighbor_actions = models.StringField(
        label="Neighbor actions",
        initial="",
    )
    neighbor_coop_ratio = models.FloatField()
    neighbor_payoffs = models.StringField(
        label="Neighbor payoffs",
        initial="",
    )
    highest_action = models.IntegerField(
        label="Highest action",
        initial=0,
    )

    show_payoffs = models.BooleanField(label="Show payoffs")

    def get_action(self):
        if self.field_maybe_none("action") in [None, 99]:
            self.action = random.randint(0, 1)
        return self.action


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
    form_model = "player"
    form_fields = ["action"]

    @staticmethod
    def js_vars(player: Player):
        try:
            start_time = player.group.dicision_start_time
        except TypeError:
            start_time = time.time()
            player.group.dicision_start_time = start_time

        return {
            "num_of_k": C.NEIGHBOR_NUM,
            "start_time": start_time,
        }

    @staticmethod
    def get_timeout_seconds(player: Player):
        is_dropped = player.participant.vars.get("is_dropped", False)
        if is_dropped:
            return 5
        return 20

    @staticmethod
    def live_method(player: Player, data):
        player.action = data["action"]

        if player.action == 99:
            player.participant.vars["is_dropped"] = True
        else:
            player.participant.vars["is_dropped"] = False
        return {0: "game_finished"}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_out = timeout_happened
        set_conditions(player.group)

        if timeout_happened:
            player.participant.vars["is_dropped"] = True
        else:
            player.participant.vars["is_dropped"] = False


class DecisionWaitPage(WaitPage):
    template_name = "network_pd/MyWaitPage.html"

    def socket_url(self):
        session_pk = self._session_pk
        page_index = self._index_in_pages
        participant_id = self.participant.id

        res = channel_utils.group_wait_page_path(
            session_pk=session_pk,
            page_index=page_index,
            participant_id=participant_id,
            group_id=self.player.group_id,
        )

        # get decided player number
        decided_count = 0
        for p in self.player.group.get_players():
            # print(f"Player {p.id_in_group} action: {p.field_maybe_none('action')}")
            if p.field_maybe_none("action") is not None:
                decided_count += 1
            elif p.participant.vars.get("is_dropped"):
                decided_count += 1
        if decided_count == C.PLAYERS_PER_GROUP:
            # if all players have decided, mark the group as completed
            self._mark_completed_and_notify(self.player.group)

        return res


class Results(Page):

    @staticmethod
    def live_method(player: Player, data):
        player.confirm_results = data["confirm"]

        if player.confirm_results == 99:
            player.participant.vars["is_dropped"] = True
        else:
            player.participant.vars["is_dropped"] = False
        return {0: "game_finished"}

    @staticmethod
    def get_timeout_seconds(player):
        is_dropped = player.participant.vars.get("is_dropped", False)
        if is_dropped:
            return 10
        return 10

    @staticmethod
    def js_vars(player: Player):
        if player.field_maybe_none("current_payoff") is None:
            set_payoffs(player.group)

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
            "show_payoffs": player.participant.vars.get("show_payoffs"),
            "num_of_k": C.NEIGHBOR_NUM,
        }


class ResultsWaitPage(WaitPage):
    template_name = "network_pd/MyWaitPage.html"

    @staticmethod
    def after_all_players_arrive(group: Group):
        record_start_time(group.subsession)

    def socket_url(self):
        session_pk = self._session_pk
        page_index = self._index_in_pages
        participant_id = self.participant.id

        res = channel_utils.group_wait_page_path(
            session_pk=session_pk,
            page_index=page_index,
            participant_id=participant_id,
            group_id=self.player.group_id,
        )

        # get decided player number
        confirmed_count = 0
        for p in self.player.group.get_players():
            if p.field_maybe_none("confirm_results") is not None:
                confirmed_count += 1
            elif p.participant.vars.get("is_dropped"):
                print(f"\tPlayer {p.id_in_group} is dropped")
                confirmed_count += 1
        if confirmed_count == C.PLAYERS_PER_GROUP:
            # if all players have decided, mark the group as completed
            self._mark_completed_and_notify(self.player.group)

        return res


page_sequence = [
    WaitForAll,
    Decision,
    DecisionWaitPage,
    Results,
    ResultsWaitPage,
]
