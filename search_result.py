class SearchResult:
    '''The result of seraching one node - its estimated value and the move to take in it'''
    def __init__(self, move, value):
        self.move = move
        self.value = value
    

    @classmethod
    def default(cls, player):
        return cls(move=0, value=float('-inf') if player is max else float('inf'))
    

    def fight(self, challenger, player, challenger_move):
        challenger_wins = challenger.value > self.value if player is max else challenger.value < self.value
        if challenger_wins:
            self.move = challenger_move
            self.value = challenger.value
    

    def alpha(self, alpha):
        return max(self.value, alpha)
    

    def beta(self, beta):
        return min(self.value, beta)