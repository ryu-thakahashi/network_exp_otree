from otree.api import *


def check_data(data, player: BasePlayer):
    print(f"P{player.id_in_group}, data: {data}")


def count_acted_players(player: BasePlayer) -> int:
    group = player.group
    acted_players = [p for p in group.get_players() if p.get_action() is not None]

    return len(acted_players)
