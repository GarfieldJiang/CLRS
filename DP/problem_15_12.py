import unittest
from collections import namedtuple
import logging


logging.basicConfig(level=logging.WARNING)
Player = namedtuple('Player', 'position vorp sign_cost')


def sign_free_agent_players(players, position_count, budget):
    """
    DP algorithm with O(N * P * X * X) time and O(N * X + P) space, where X == budget, N == position_count,
    and P == len(players).
    :param players: player information list.
    :param position_count: how many positions are available.
    :param budget: The money at my disposal.
    :return: The optimal total VORP and the selected player indices.
    """
    if not players or position_count <= 0 or budget < 0:
        return 0, set()

    p = len(players)
    dp = [[0 for _ in range(0, budget + 1)] for _ in range(0, position_count)]
    sign_flag_matrix = [[-1 for _ in range(0, budget + 1)] for _ in range(0, position_count)]
    for x in range(0, budget + 1):
        player_index = -1
        for player in players:
            player_index += 1
            if player.sign_cost == x and player.position == 0 and dp[0][x] < player.vorp:
                dp[0][x] = player.vorp
                sign_flag_matrix[0][x] = player_index

    for i in range(1, position_count):
        for x in range(0, budget + 1):
            for y in range(0, x + 1):
                prev_sign_flags = _get_sign_flags(i - 1, y, players, sign_flag_matrix)
                last_player_vorp = 0
                last_player_index = -1
                for player_index in range(0, p):
                    player = players[player_index]
                    if prev_sign_flags[player_index] or player.position != i:
                        continue
                    if player.sign_cost == x - y and last_player_vorp < player.vorp:
                        last_player_vorp = player.vorp
                        last_player_index = player_index

                new_vorp = dp[i - 1][y] + last_player_vorp
                if new_vorp > dp[i][x]:
                    dp[i][x] = new_vorp
                    sign_flag_matrix[i][x] = last_player_index

    logging.debug('dp = %s' % dp)
    logging.debug('sign_flag_matrix = %s' % sign_flag_matrix)

    max_vorp = 0
    opt_budget = 0
    for x in range(0, budget + 1):
        if dp[position_count - 1][x] > max_vorp:
            max_vorp = dp[position_count - 1][x]
            opt_budget = x

    sign_flags = _get_sign_flags(position_count - 1, opt_budget, players, sign_flag_matrix)
    sign_flag_set = set()
    for i in range(0, p):
        if sign_flags[i]:
            sign_flag_set.add(i)

    return max_vorp, sign_flag_set


def _get_sign_flags(i, y, players, sign_flag_matrix):
    sign_flags = [False] * len(players)
    z = y
    for j in range(i, -1, -1):
        player_index = sign_flag_matrix[j][z]
        if player_index >= 0:
            sign_flags[player_index] = True
            z -= players[player_index].sign_cost
    return sign_flags


Case = namedtuple('Case', 'desc players position_count budget expected_vorp expected_sign_flags')


class TestSigningFreeAgentPlayers(unittest.TestCase):
    def test_signing_free_agent_players(self):
        cases = (
            Case(
                desc="No players to sign", players=(), position_count=100, budget=1000,
                expected_vorp=0, expected_sign_flags=set()
            ),
            Case(
                desc="No budget", players=(
                    Player(position=0, vorp=100, sign_cost=5),
                ),
                position_count=2, budget=0, expected_vorp=0, expected_sign_flags=set()
            ),
            Case(
                desc="1 player, enough budget", players=(
                    Player(position=0, vorp=100, sign_cost=2),
                ),
                position_count=2, budget=3, expected_vorp=100, expected_sign_flags={0}
            ),
            Case(
                desc="3 player, 2 cheap but good ones", players=(
                    Player(position=0, vorp=1, sign_cost=4),
                    Player(position=1, vorp=100, sign_cost=1),
                    Player(position=2, vorp=100, sign_cost=2),
                ),
                position_count=3, budget=4, expected_vorp=200, expected_sign_flags={1, 2}
            ),
            Case(
                desc="4 player on 2 positions #0", players=(
                    Player(position=0, vorp=100, sign_cost=2),
                    Player(position=0, vorp=110, sign_cost=4),
                    Player(position=1, vorp=100, sign_cost=3),
                    Player(position=1, vorp=80, sign_cost=2),
                ),
                position_count=2, budget=4, expected_vorp=180, expected_sign_flags={0, 3}
            ),
            Case(
                desc="4 player on 2 positions #1", players=(
                    Player(position=0, vorp=100, sign_cost=2),
                    Player(position=0, vorp=110, sign_cost=4),
                    Player(position=1, vorp=100, sign_cost=3),
                    Player(position=1, vorp=80, sign_cost=2),
                ),
                position_count=2, budget=5, expected_vorp=200, expected_sign_flags={0, 2}
            ),
            Case(
                desc="4 player on 2 positions #2", players=(
                    Player(position=0, vorp=100, sign_cost=2),
                    Player(position=0, vorp=110, sign_cost=4),
                    Player(position=1, vorp=100, sign_cost=3),
                    Player(position=1, vorp=80, sign_cost=2),
                ),
                position_count=2, budget=6, expected_vorp=200, expected_sign_flags={0, 2}
            ),
            Case(
                desc="4 player on 2 positions #3", players=(
                    Player(position=0, vorp=100, sign_cost=2),
                    Player(position=0, vorp=110, sign_cost=4),
                    Player(position=1, vorp=101, sign_cost=3),
                    Player(position=1, vorp=80, sign_cost=2),
                ),
                position_count=2, budget=7, expected_vorp=211, expected_sign_flags={1, 2}
            ),
            Case(
                desc="4 player on 2 positions #4", players=(
                    Player(position=0, vorp=100, sign_cost=2),
                    Player(position=0, vorp=110, sign_cost=4),
                    Player(position=1, vorp=100, sign_cost=3),
                    Player(position=1, vorp=80, sign_cost=3),
                ),
                position_count=2, budget=4, expected_vorp=110, expected_sign_flags={1}
            ),
            Case(
                desc="10 player on 5 positions #0", players=(
                    Player(position=0, vorp=100, sign_cost=1),
                    Player(position=0, vorp=10, sign_cost=1),
                    Player(position=0, vorp=10, sign_cost=2),
                    Player(position=0, vorp=10, sign_cost=2),
                    Player(position=1, vorp=10, sign_cost=3),
                    Player(position=1, vorp=10, sign_cost=3),
                    Player(position=2, vorp=10, sign_cost=4),
                    Player(position=2, vorp=11, sign_cost=4),
                    Player(position=3, vorp=12, sign_cost=5),
                    Player(position=4, vorp=11, sign_cost=5),
                ),
                position_count=5, budget=10, expected_vorp=123, expected_sign_flags={0, 7, 8}
            ),
            Case(
                desc="10 player on 5 positions #1", players=(
                    Player(position=4, vorp=100, sign_cost=1),
                    Player(position=4, vorp=10, sign_cost=1),
                    Player(position=4, vorp=10, sign_cost=2),
                    Player(position=4, vorp=10, sign_cost=2),
                    Player(position=3, vorp=10, sign_cost=3),
                    Player(position=3, vorp=10, sign_cost=3),
                    Player(position=2, vorp=10, sign_cost=4),
                    Player(position=2, vorp=11, sign_cost=4),
                    Player(position=1, vorp=12, sign_cost=5),
                    Player(position=0, vorp=11, sign_cost=5),
                ),
                position_count=5, budget=10, expected_vorp=123, expected_sign_flags={0, 7, 8}
            ),
            Case(
                desc="10 player on 5 positions #2", players=(
                    Player(position=4, vorp=10, sign_cost=2),
                    Player(position=4, vorp=15, sign_cost=2),
                    Player(position=4, vorp=20, sign_cost=2),
                    Player(position=4, vorp=20, sign_cost=2),
                    Player(position=3, vorp=19, sign_cost=3),
                    Player(position=3, vorp=19, sign_cost=3),
                    Player(position=2, vorp=40, sign_cost=4),
                    Player(position=2, vorp=21, sign_cost=4),
                    Player(position=1, vorp=50, sign_cost=5),
                    Player(position=0, vorp=21, sign_cost=5),
                ),
                position_count=5, budget=10, expected_vorp=90, expected_sign_flags={6, 8}
            ),
        )

        for case in cases:
            vorp, sign_flags = sign_free_agent_players(case.players, case.position_count, case.budget)
            self.assertEqual(
                (vorp, sign_flags), (case.expected_vorp, case.expected_sign_flags),
                '%s, %s != %s' % (
                    case.desc, (vorp, sign_flags), (case.expected_vorp, case.expected_sign_flags)
                )
            )
