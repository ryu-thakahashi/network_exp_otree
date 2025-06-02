from network_pd import *
import pytest


class TestGetNeighborFunc:
    network_list = [i for i in range(8)]

    def test_get_neighbors_2(self):
        expected_neighbors = [3, 5]
        assert get_neighbors(len(self.network_list), 4, k=2) == expected_neighbors

    def test_get_neighbors_4(self):
        expected_neighbors = [0, 1, 3, 4]
        assert get_neighbors(len(self.network_list), 2, k=4) == expected_neighbors

    def test_get_neighbors_6(self):
        expected_neighbors = [7, 0, 1, 3, 4, 5]
        assert get_neighbors(len(self.network_list), 2, k=6) == expected_neighbors


class TestGetNeiActionsFunc:
    action_list = [0, 0, 0, 1, 1, 0, 1, 0]

    def test_get_nei_actions_2(self):
        expected_actions = [0, 0]
        assert get_neighbors_actions(self.action_list, p_pos=1, k=2) == expected_actions
        expected_actions = [0, 1]
        assert get_neighbors_actions(self.action_list, p_pos=2, k=2) == expected_actions
        expected_actions = [1, 1]
        assert get_neighbors_actions(self.action_list, p_pos=5, k=2) == expected_actions

    def test_get_nei_actions_4(self):
        expected_actions = [0, 0, 0, 1]
        assert get_neighbors_actions(self.action_list, p_pos=1, k=4) == expected_actions
        expected_actions = [0, 0, 1, 1]
        assert get_neighbors_actions(self.action_list, p_pos=2, k=4) == expected_actions
        expected_actions = [1, 1, 1, 0]
        assert get_neighbors_actions(self.action_list, p_pos=5, k=4) == expected_actions

    def test_get_nei_actions_6(self):
        expected_actions = [1, 0, 0, 0, 1, 1]
        assert get_neighbors_actions(self.action_list, p_pos=1, k=6) == expected_actions
        expected_actions = [0, 0, 0, 1, 1, 0]
        assert get_neighbors_actions(self.action_list, p_pos=2, k=6) == expected_actions
        expected_actions = [0, 1, 1, 1, 0, 0]
        assert get_neighbors_actions(self.action_list, p_pos=5, k=6) == expected_actions


class TestCalcPayoffFunc:
    action_list = [0, 0, 0, 1, 1, 0, 1, 0]

    def test_calc_payoff_k2_bc2(self):
        payoff = calc_payoff(self.action_list, p_pos=2, k=2, bc_ratio=2)
        assert payoff == 2
        payoff = calc_payoff(self.action_list, p_pos=5, k=2, bc_ratio=2)
        assert payoff == 4
        payoff = calc_payoff(self.action_list, p_pos=6, k=2, bc_ratio=2)
        assert payoff == -2

    def test_calc_payoff_k2_bc4(self):
        payoff = calc_payoff(self.action_list, p_pos=2, k=2, bc_ratio=4)
        assert payoff == 4
        payoff = calc_payoff(self.action_list, p_pos=5, k=2, bc_ratio=4)
        assert payoff == 8
        payoff = calc_payoff(self.action_list, p_pos=6, k=2, bc_ratio=4)
        assert payoff == -2

    def test_calc_payoff_k2_bc6(self):
        payoff = calc_payoff(self.action_list, p_pos=2, k=2, bc_ratio=6)
        assert payoff == 6
        payoff = calc_payoff(self.action_list, p_pos=5, k=2, bc_ratio=6)
        assert payoff == 12
        payoff = calc_payoff(self.action_list, p_pos=6, k=2, bc_ratio=6)
        assert payoff == -2
