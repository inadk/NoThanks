from Take5 import Player

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
        # take randomly with probability 1/2
        if randint( 0, 2 ) == 1:
            return True
        return False
    