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
        # take randomly with probability 1/3
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
        #  take only if that action doesn't increase penalty
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
        # take if that action has a penalty < 14
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
        # take only if card penalty <= 10
        # that is card number <= 10
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
        # checking if player is first is not implemented here
        for player in state.players:
            if self.coins >= player.coins:
                return False
        return True

