from NoThanksPlayer import Player
from NoThanksState import State, PlayerState
from random import randint

'''
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
'''

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



# create a new class inheriting features from Player - defined in NoThanksPlayer.py
class ImFineThanks(Player):
    # create init method 
    def __init__( self ):
        # calls init method from player
        Player.__init__( self )
        # give itself a name with the setName method
        self.setName( 'ImFineThanks' )
        
        self.scores = []
        self.gamepenalty = []
        self.lastround = -1
        self.takeCoinCount = []
        self.takesPerGame = []
        

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
        
        # update game stats
        if self.scores == []:
            self.scores.append( self.totalpenalty)

        # 1st call of MyAI in current game
        if self.lastround > state.round:

            self.scores.append( self.totalpenalty)

            if len(self.scores) == 1:
                self.gamepenalty.append( self.scores[0] )
            if len(self.scores) > 1:
                self.gamepenalty.append( self.scores[-1] - self.scores[-2])

        self.lastround = state.round

        #if len(self.scores) == 20:
        #    print(self.gamepenalty)
        #    print(self.takeCoinCount)

        # output of 2 for clear optimal takes
        # output of 1000 for clear optimal no takes
        def decide( self, card, state):
            
            # if state.round == 24: endOfGameStats(self, card, state)

            score = 0
           
            if self.coins <= 0:
                return -10000

            # if card is my neighbour and has no neighbours in any of my opponents collection, get coins on it before taking (whenever possible)
            if myNeighbour(self, card):
                if someonesNeighbour(self, card, state):
                    return -10000
                if coinlessPlayer(self, state):
                    return -10000
                if card.number / (card.coins + 4) < 2.5: 
                    return -10000
                return 10000 # dont take!

            # optimal play at last rounds
            # only take penaltiless card at round 24-n (n=1,2,3), except when there are less than (n+1) players with less coins than me

            if state.round == 24:
                if coinRank(self, state) <= 4:
                    return 10000
            if state.round == 23:
                if coinRank(self, state) <= 3:
                    return 10000
            if state.round == 22:
                if coinRank(self, state) <= 2:
                    return 10000    
            if state.round == 21:
                if coinRank(self, state) <= 1:
                    return 10000
            
            # adapt scoring for state and self variable values
            # penalty I take + expected penalty reduction
            score += card.penalty - card.coins - xNeighbour(self, state, card, 3) 
            score -= ( 20 / self.coins ) * card.coins * pow( (24 - state.round), 2) / 1000
            
            # if score < -2: debug(self, card, state, score)

            return score
        

        if decide( self, card, state) < -3:
            
            self.takeCoinCount.append(self.coins)
            return True
        else:
            return False

def debug(self, card, state, score):
    
    print('score: ' + str(score) )
    print('summation: ' + str (card.penalty - card.coins - xNeighbour(self, state, card, 3) ) )
    print('substraction: ' + str ( ( 20 / self.coins ) * card.coins * pow( (24 - state.round), 2) / 1000) )
    print('round: ' + str(state.round) )
    print('card.penalty: ' + str(card.penalty) )
    print('card.coins: ' + str(card.coins) )
    print('xNeighbour: ' + str(xNeighbour(self, state, card, 3)) )
    print('self.coins: ' + str(self.coins))
    
def consoleTake(self, card, state):
    print('round: ' + str(state.round) )
    print('card.penalty: ' + str(card.penalty) )
    print('card.coins: ' + str(card.coins) )

def endOfGameStats(self, card, state):
    print("-----")
    print("End of game stats:")
    print(self.collection)
    print(self.coins)
      
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

def theirCollection( self, state):
    tc = []
    for i in state.players:
        if i.name != self.name:
            for j in i.collection:
                tc.append(j.number)
    tc.sort()
    return tc

def allDrawnCards( state ):
    ac = []
    for i in state.players:
        for j in i.collection:
            ac.append(j.number)
    ac.sort()
    return ac

def isCardTheir( self, state, n):
    for i in theirCollection( self, state):
        if i == n:
            return True
    return False

def closestNeighbour(self, state, card):
    tc = theirCollection(self, state)
    tc.append(card.number)
    tc.sort()
    ind = tc.index(card.number)

    lowerNeighDistance = 100  
    upperNeighDistance = 100
    lowerNeigh = 0 
    upperNeigh = 0

    if ind > 0:
        lowerNeighDistance = tc[ind] - tc[ind - 1]
        lowerNeigh = tc[ind - 1]

    if ind < len(tc) - 1:
        upperNeighDistance = tc[ind + 1] - tc[ind]
        upperNeigh = tc[ind + 1]

    return [lowerNeighDistance, upperNeighDistance, lowerNeigh, upperNeigh]

def closestNeighbourStatus( self, state, card):
    status = [0, 0]
    lowerNeigh = closestNeighbour(self, state, card)[2]
    upperNeigh = closestNeighbour(self, state, card)[3]
    myCollection = [i.number for i in self.collection]
    if lowerNeigh in myCollection:
        status[0] = 1
    if upperNeigh in myCollection:
        status[1] = 1
    return status    

def pLowerNeighbour(self, state, card):
    probCardGetsPlayed = ( 33 - state.round ) / 33
    closestNeighMe = closestNeighbourStatus( self, state, card)[0]
    distance = closestNeighbour(self, state, card)[0]
    if ( 5 < card.number < 33 ):
        if distance <= 3:
            if closestNeighMe == 1:
                if distance == 2:
                    return probCardGetsPlayed * 1
                return probCardGetsPlayed
            else:
                if distance == 3:
                    return probCardGetsPlayed / 2
                elif distance == 2:
                    return 0
                elif distance == 1:
                    return 0
                else:
                    return 0
    return 0

def pUpperNeighbour(self, state, card):
    probCardGetsPlayed = ( 33 - state.round ) / 33
    closestNeighMe = closestNeighbourStatus( self, state, card)[1]
    distance = closestNeighbour(self, state, card)[1]
    if ( 5 < card.number < 33 ):
        if distance <= 3:
            if closestNeighMe == 1:
                if distance == 2:
                    return probCardGetsPlayed * 1
                return probCardGetsPlayed
            else:
                if distance == 3:
                    return probCardGetsPlayed / 2
                elif distance == 2:
                    return 0
                elif distance == 1:
                    return 0
                else:
                    return 0
    return 0
    
def xNeighbour(self, state, card, r):
    return ( pLowerNeighbour(self, state, card) + pUpperNeighbour(self, state, card) ) * card.number / r
