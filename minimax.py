import itertools
from fishing_game_core.shared import ACTION_TO_STR
from stopwatch import Stopwatch
from search_result import SearchResult



class Minimax:
    def __init__(self):
        pass # TODO


    @classmethod
    def from_initial_data(cls, initial_data):
        return cls() # TODO


    def decide(self, node):
        stopwatch = Stopwatch(num_seconds=0.05) # just below the Kattis time limit
        try:
            for depth in itertools.count(start=1):
                self._cache = {} # {node_hash: SearchResult}
                search_result = self.alpha_beta(node, depth=depth, stopwatch=stopwatch)
        except TimeoutError:
            return ACTION_TO_STR[search_result.move]
    

    def alpha_beta(self, node, depth, stopwatch, alpha=float('-inf'), beta=float('inf')):
        '''Returns a tuple of (best_move_from_this_node, value)'''
        stopwatch.check()
        node_hash = hash_node(node)
        if depth <= 0 or len(node.state.get_fish_positions()) == 0:
            self._cache[node_hash] = SearchResult(move=0, value=self.heuristic(node))
        if node_hash in self._cache:
            return self._cache[node_hash]
        player = max if node.state.player == 0 else min
        children = sorted(
            node.compute_and_get_children(),
            key=self.heuristic,
            reverse=player is max
        )
        result = SearchResult.default(player=player)
        for child in children:
            child_entry = self.alpha_beta(child, depth=depth - 1, stopwatch=stopwatch, alpha=alpha, beta=beta)
            result.fight(child_entry, player=player, challenger_move=child.move)
            if player is max:
                alpha = result.alpha(alpha)
            else:
                beta = result.beta(beta)
            if alpha >= beta:
                break
        self._cache[node_hash] = result
        return result


    def heuristic(self, node):
        player_scores = node.state.get_player_scores()
        score_difference = player_scores[0] - player_scores[1]
        fish_positions = node.state.get_fish_positions()
        if len(fish_positions) == 0:
            return score_difference
        fish_scores = node.state.get_fish_scores()
        hook_positions = node.state.get_hook_positions()
        best_values = {
            player: max(
                fish_scores[fish] / (distance(hook_pos, fish_pos, hook_positions[1 - player][0]) + 1)
                for fish, fish_pos in fish_positions.items()
            )
            for player, hook_pos in hook_positions.items()
        }
        value_difference = best_values[0] - best_values[1]
        return score_difference + value_difference




def hash_node(node):
    state = node.state
    return hash((
        state.player,
        hash_dict(state.player_scores),
        hash_dict(state.player_caught),
        hash_dict(state.hook_positions),
        hash_dict(state.fish_positions)
    ))


def hash_dict(dict):
    return hash(frozenset(dict.items()))


def distance(a, b, barrier):
    '''
    Compute the distance from a to b, wrapping in the x axis.
    Both points should be tuples of (x, y).
    The barrier is the x axis of an unpenetrable barrier.
    '''
    vertical_dist = abs(a[1] - b[1])
    horizontal_dist = abs(a[0] - b[0])
    if a[0] <= barrier <= b[0] or b[0] <= barrier <= a[0]:
        horizontal_dist = 20 - horizontal_dist
    return vertical_dist + horizontal_dist