from otree.api import *


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


def check_data(data, player: BasePlayer):
    print(f"P{player.id_in_group}, data: {data}")


def count_acted_players(player: BasePlayer) -> int:
    group = player.group
    acted_players = [p for p in group.get_players() if p.get_action() is not None]

    return len(acted_players)


def game_results(player: BasePlayer, action_list, payoff_list) -> dict:
    print(
        f"game_results: player={player.id_in_group}, action_list={action_list}, payoff_list={payoff_list}"
    )
    nei_actions = get_neighbors_actions(
        act_list=action_list, p_pos=player.id_in_group - 1, k=4
    )
    print(f"game_results: nei_actions={nei_actions}")
    nei_payoffs = get_neighbors_payoffs(
        payoff_list=payoff_list, p_pos=player.id_in_group - 1, k=4
    )
    print(f"game_results: nei_payoffs={nei_payoffs}")
    return {
        player.id_in_group: {
            "type": "game_results",
            "show_payoff": player.participant.vars.get("show_payoffs", False),
            "player_payoff": player.current_payoff,
            "player_action": player.get_action(),
            "neighbor_actions": nei_actions,
            "neighbor_payoffs": nei_payoffs,
        }
    }
