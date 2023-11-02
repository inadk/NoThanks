import random

# A NoThanks card
class Card():

    def __init__( self, number = 0 ):
        self.number = number
        self.penalty = number
        self.coins = 0

    def __repr__( self ):
        return f'{self.number}'

    def __lt__( self, other ):
        return self.number < other.number

    def __le__( self, other ):
        return self.number <= other.number

    def __gt__( self, other ):
        return self.number > other.number

    def __ge__( self, other ):
        return self.number >= other.number

    def __eq__( self, other ):
        return self.number == other.number


# The whole deck of NoThanks cards
class Deck():

    def __init__( self, decksize=35 ):
        self.maxsize = decksize
        self.cards = []
        for i in range( 3, self.maxsize+1 ):
            self.cards.append( Card( i ) )

    def __repr__( self ):
        s = ''
        size = len( self.cards )
        for i in range( size ):
            s += str( self.cards[i] )
            if i < size-1:
                s += ','
        return s

    def __len__( self ):
        return len( self.cards )

    def shuffle( self ):
        size = len(self.cards)
        for i in range(size):
            j = random.randrange(i,size)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        for i in range( 9 ): # remove 9 random cards
            self.popCard()

    def removeCard(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False

    def popCard( self ):
        return self.cards.pop()

    def isEmpty( self ):
        return (len( self.cards ) <= 0)


if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    print( deck )