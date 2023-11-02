from NoThanksPlayer import Player
from NoThanksState import State, PlayerState
from random import randint

class RandomPlayer(Player):
    def __init__( self ):
        Player.__init__( self )
        self.setName( 'RandomPlayer' )
    def take( self, card, state ):
        if self.coins <= 0:
            return True
        if randint( 0, 3 ) == 1:
            return True
        return False

class LowerPenalty(Player):
    def __init__( self ):
        Player.__init__( self )
        self.setName( 'LowerPenalty' )
    def take( self, card, state ):
        if self.coins <= 0:
            return True
        if self.penaltyWhenTake( card ) <= self.penalty():
            return True
        return False

class CutOff14(Player):
    def __init__( self ):
        Player.__init__( self )
        self.setName( 'CutOff14' )
    def take( self, card, state ):
        if self.coins <= 0:
            return True
        if self.penaltyWhenTake( card ) < self.penalty()+14:
            return True
        return False

class TakeSmall(Player):
    def __init__( self ):
        Player.__init__( self )
        self.setName( 'TakeSmall' )
    def take( self, card, state ):
        if self.coins <= 0:
            return True
        if card.penalty <= 10:
            return True
        return False

class CoinsDependent(Player):
    def __init__( self ):
        Player.__init__( self )
        self.setName( 'CoinsDependent' )
    def take( self, card, state ):
        if self.coins <= 0:
            return True
        # Never take a card if there is a player with less coins
        # Do less-or-equal otherwise if this player is the first
        # one he will take all the cards.
        for player in state.players:
            if self.coins >= player.coins:
                return False
        return True

