from copy import copy
from NoThanksGame import Deck, Card

# A player has an AI to play the game.
# An implementation of Player should at least implement the take() method.
# This method returns True or False; if True, the player takes the card 
# that the method gets as parameter and also gets all the coins on it.
# If False, the player puts one of their coins on the card and the option
# to take it goes to the next player. If the player has no coins left,
# the take() method will not be called, but the player gets the card
# automatically.
# The penalty method tells the player what their current penalty is.
class Player():

    def __init__( self, name="" ):
        self.name = name
        self.coins = 11
        self.collection = []
        self.games = 0
        self.totalpenalty = 0

    def __repr__( self ):
        return f'[{self.name},{self.penalty()},{self.coins},{self.collection},{self.games},{self.totalpenalty}]'

    def __eq__( self, other ):
        self.score() == other.score() and self.name == other.name and self.id == other.id

    def __lt__( self, other ):
        return self.score() < other.score() or \
            (self.score() == other.score() and self.name < other.name ) or \
            (self.score() == other.score() and self.name == other.name and self.id < other.id)
            
    def __ge__( self, other ):
        return not self < other

    def __le__( self, other ):
        return self == other or self < other

    def __gt__( self, other ):
        return not self <= other

    def score( self ):
        if self.games <= 0:
            return 0.0
        return float( self.totalpenalty ) / float( self.games )

    def setName( self, name ):
        self.name = name

    def penalty( self, collection=None, coins=0 ):
        if collection == None:
            collection = self.collection
            coins = self.coins
        p = 0
        for i in range( len( collection ) ):
            if i > 0:
                if collection[i].number == collection[i-1].number+1:
                    continue
            p += collection[i].penalty
        p -= coins
        return p

    def addCardToCollection( self, card ):
        self.collection.append( card )
        self.collection.sort()
        self.coins += card.coins
        card.coins = 0

    def reset( self ):
        self.collection = []
        self.coins = 11
        
    # This method tells you what your penalty will be if you take 
    # the given card.
    def penaltyWhenTake( self, card ):
        copycollection = copy( self.collection )
        copycollection.append( card )
        copycollection.sort()
        return self.penalty( copycollection, self.coins+card.coins )

    # The take() method should ONLY return True or False, to indicate whether the
    # player wants to take the card. The method should NOT make any changes to
    # the player state! Changes to the number of coins and the collection of
    # cards are made by the main program! 
    def take( self, card, state ):
        return True

    def startGame( self ):
        pass

    def endGame( self, state ):
        pass

if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    player = Player("test")
    for i in range( 5 ):
        player.addCardToCollection( deck.popCard() )
    print( player )
    card = deck.popCard()
    card.coins = 10
    print( player.penaltyWhenTake( card ) )
    player.addCardToCollection( card )
    print( player )