import random
from Take5Game import Card

# A player has an AI to play the game.
# An implementation of Player should at least implement the
# playCard and chooseRow methods.
# playCard selects a card from the Player's hand and returns it; this
# is the card the Player will play.
# chooseRow is called when the player has to take one of the rows; it
# returns the number of the row the player wants (0-3).
# The penalty method tells the player what his current penalty is.
class Player():

    def __init__( self, name="" ):
        self.name = name
        self.hand = []
        self.collection = []
        self.games = 0
        self.totalpenalty = 0
        self.lastcard = None

    def __str__( self ):
        return '['+self.name+','+str( self.penalty() )+\
            ','+str( self.games )+','+str( self.totalpenalty )+']'

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

    def penalty( self ):
        p = 0
        for card in self.collection:
            p += card.penalty
        return p

    def addCard( self, card ):
        self.hand.append( card )
        self.hand.sort()

    def addCardToCollection( self, card ):
        self.collection.append( card )
        self.collection.sort()

    def removeCard( self, card ):
        if card in self.hand:
            self.hand.remove(card)
            return True
        return False

    def playCard( self, hand, rows, state ):
        return hand[random.randrange(0,len( hand ))]

    def chooseRow( self, rows, state ): 
        return random.randrange(0,len(rows))

    def reset( self ):
        self.hand = []
        self.collection = []
        self.lastcard = None

    def startGame( self ):
        pass

    def endGame( self, state ):
        pass
