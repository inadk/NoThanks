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


# -----------------------------------------------------------------------------------
# create a new class inheriting features from Player - defined in NoThanksPlayer.py
class MyAI(Player):
    # create init method 
    def __init__( self ):
        # calls init method from player
        Player.__init__( self )
        # give itself a name with the setName method
        self.setName( 'MyAI' )

# create at least one method
# take.take
# decide whether take or not to take the card
# card is an object of type Card, which is the card that is on offer
# state is an object of type State, overview of everything known about the current game
# - list of players (<state>.players - in seating order, current player first in list
# - name for each player - <player>.name
# - coins a player have - <player>.coins
# - cards collected by player -  <player>.collection - ordered from low to high
# round attribute 1-24
# thus hidden pile size is 24-roundnumber
# take must return True/False
# True - take cards with coins, flip new, next player
# False - put a coin, next player
# if no coins for player, take is not called - automatically takes cards and coins

    def take( self, card, state ):

        if self.coins <= 0:
            return True

        takeNeighbour(self, card, state)

        roundSpecificAction(self, state, card)

        whenFewCoins(self, card, state, 4, 16, 4)

        goodCoinPenaltyRatio(card, 2)
        
        # if xPenalty(self, card, state) >= 0:
        #     return True
    
        return False

    
# functions

# very important ones
# 1.
def roundSpecificAction(self, state, card):
    if self.penaltyWhenTake( card ) >= self.penalty():
        if state.round == 21:
            if coinRank(self, state) <= 1:
                return False
        if state.round == 22:
            if coinRank(self, state) <= 2:
                return False
        if state.round == 23:
            if coinRank(self, state) <= 3:
                return False
        if state.round == 24:
            return False
        
# 2.
def dataCollector(card, state):
    if state.round == 1:
        cardsInPlay = [i for i in range(3, 36)]
    cardsInPlay.remove(card.number)

# 3.
# if card is not my collection and not in any of my neighbours collection, get coins on it before taking (whenever possible)
def takeNeighbour(self, card, state):
    if myNeighbour(self, card):
        if someonesNeighbour(self, card, state):
            return True
        if coinlessPlayer(self, state):
            return True
        if card.number / (card.coins + 4) < 2.5:
            return True
        return False

# 4.
def whenFewCoins(self, card, state, ncoins, untilState, r):
    if self.coins <= ncoins and state.round <= untilState:
        if card.coins >= ( card.number / r ):
            return True
# 5.        
def goodCoinPenaltyRatio(card, r):
    if card.coins >= ( card.number / r ):
        return True
    return False


def someonesNeighbour( self, card, state):
    for i in state.players:
        if i.name != self.name:
            for j in i.collection:
                if (card.number + 1  == j.number) or (card.number -1  == j.number):
                    return True
    return False
        
def myNeighbour(self, card):
    if self.penaltyWhenTake( card ) <= 0:
        return True
    return False

def coinlessPlayer( self, state):
    for i in state.players:
        if i != self.name:
            if i.coins == 0:
                return True
            False

def coinRank(self, state):
    cr = 0
    for i in state.players:
        if i.coins >= self.coins:
            cr += 1
    return cr

def numberOfNthNeighboursAtThem(self, card, state, n):
    counter = 2
    for i in state.players:
        for j in i.collection:
            if (card.number + n  == j.number) or (card.number -n  == j.number):
                counter -= 1
    return counter

def numberOfNthNeighboursAtMe(self, card, n):
    counter = 0
    for i in self.collection:
        if (card.number + 1  == i.number) or (card.number -n  == i.number):
            counter += 1
    return counter

def uncertainty(state):
    counter = 0
    for i in state.players:
        counter += pow(i.coins, 2)
    return 5*11*11 / counter 

def xPenalty(self, card, state):
    n1them = numberOfNthNeighboursAtThem(self, card, state, 1)
    n1me = numberOfNthNeighboursAtMe(self, card, 1)
    n2them = numberOfNthNeighboursAtThem(self, card, state, 2)
    n2me = numberOfNthNeighboursAtMe(self, card, 2)
    deckSize = 24 - state.round
    
    xPR = card.number * (deckSize / (deckSize + 9) ) * (2 - n1them) * n2me * (1 - n2them / 4) * uncertainty(state) - card.number + card.coins
    
    if xPR >= 0:
        print("Round: " + str(state.round))
        print("xPR: " + str(xPR) + ", uncertainty: " + str(uncertainty(state)))
        print("Card: " + str(card.number) + ', Coins: ' + str(card.coins))
        print("n1them" + str(n1them) + ", n1me: " + str(n1me) + "n2them" + str(n2them) + ", n2me: " + str(n2me))
        print("My collection: " + str(self.collection))
        print("------")

    return xPR
