from otree.api import *
from .models import C, Group, Player
import time
import random


# ----------- 導入ページ -----------


class Intro1(Page):
    def is_displayed(self):
        return self.round_number == 1


class Intro2(Page):
    def is_displayed(self):
        return self.round_number == 1


class IntroWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 1

    body_text = "相手の準備を待っています。お待ちください。"


# ----------- First Mover の選択 -----------


class DecisionFirst(Page):
    form_model = "player"
    form_fields = ["decision"]

    def is_displayed(self):
        # 奇数ラウンド: id=1 が先行、偶数ラウンド: id=2 が先行
        if self.round_number % 2 == 1:
            return self.player.id_in_group == 1
        else:
            return self.player.id_in_group == 2

    def before_next_page(self):
        # 各グループに delay_condition を割り当て
        condition = random.choice(["short", "long"])
        for p in self.group.get_players():
            p.delay_condition = condition

    def vars_for_template(self):
        return dict(
            round_number=self.round_number,
            total_rounds=C.NUM_ROUNDS,
        )


# ----------- 後行者が先行者を待つ -----------


class WaitForFirstMover(WaitPage):
    def is_displayed(self):
        return (self.round_number % 2 == 1 and self.player.id_in_group == 2) or (
            self.round_number % 2 == 0 and self.player.id_in_group == 1
        )

    body_text = "このラウンドでは、あなたは後に選択します。相手の選択を待っています。"


# ----------- 後行者に対する遅延導入 -----------


class DelayWaitPage(WaitPage):
    wait_for_all_groups = False

    def is_displayed(self):
        return (self.round_number % 2 == 1 and self.player.id_in_group == 2) or (
            self.round_number % 2 == 0 and self.player.id_in_group == 1
        )

    def after_all_players_arrive(self):
        first_id = 1 if self.round_number % 2 == 1 else 2
        first_player = self.group.get_player_by_id(first_id)

        if first_player.delay_condition == "short":
            delay = random.uniform(3, 7)
        else:
            delay = random.uniform(28, 32)
        # delay = 0.001

        self.group.delay_seconds = delay
        time.sleep(delay)


# ----------- Second Mover の選択 -----------


class DecisionSecond(Page):
    form_model = "player"
    form_fields = ["decision"]

    def is_displayed(self):
        return (self.round_number % 2 == 1 and self.player.id_in_group == 2) or (
            self.round_number % 2 == 0 and self.player.id_in_group == 1
        )

    def vars_for_template(self):
        first_id = 1 if self.round_number % 2 == 1 else 2
        first_player = self.group.get_player_by_id(first_id)

        decision_labels = {"C": "C(協力する)", "D": "D(裏切る)"}

        return dict(
            first_decision=first_player.decision,
            first_decision_label=decision_labels[first_player.decision],  # ← ラベル追加
            delay_shown=round(self.group.delay_seconds, 1),
            round_number=self.round_number,
            total_rounds=C.NUM_ROUNDS,
        )


# ----------- 先行者が後行者を待つ -----------


class WaitForSecondMover(WaitPage):
    def is_displayed(self):
        return (self.round_number % 2 == 1 and self.player.id_in_group == 1) or (
            self.round_number % 2 == 0 and self.player.id_in_group == 2
        )

    body_text = "相手が選択を終えるのを待っています。しばらくお待ちください。"


# ----------- 結果計算 -----------


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoffs"


class Results(Page):
    def vars_for_template(self):
        opponent = self.player.get_others_in_group()[0]
        total_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

        # 選択肢のラベル変換
        decision_labels = {"C": "C(協力する)", "D": "D(裏切る)"}

        return dict(
            round_number=self.round_number,
            my_decision=self.player.decision,
            opponent_decision=opponent.decision,
            my_decision_label=decision_labels[self.player.decision],  # ← 追加
            opponent_decision_label=decision_labels[opponent.decision],  # ← 追加
            my_payoff=self.player.payoff,
            total_payoff=total_payoff,
            total_rounds=C.NUM_ROUNDS,
        )


class ResultsSyncPage(WaitPage):
    wait_for_all_groups = False
    body_text = "次ラウンドの準備中です。しばらくお待ちください。"


class FinalPage(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS  # 最終ラウンドのみ表示

    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.player.in_all_rounds()])
        return dict(total_payoff=total_payoff)


# ----------- ページシーケンス -----------

page_sequence = [
    Intro1,
    Intro2,
    IntroWaitPage,
    DecisionFirst,
    WaitForFirstMover,
    DelayWaitPage,
    DecisionSecond,
    WaitForSecondMover,
    ResultsWaitPage,
    Results,
    ResultsSyncPage,
    FinalPage,
]
