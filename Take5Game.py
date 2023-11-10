import random

# A Take 5! card
class Card():

    def __init__( self, number = 0 ):
        self.number = number
        self.penalty = 1
        if self.number%10 == 0:
            self.penalty = 3
        elif self.number%10 == 5:
            self.penalty = 2
        if self.number%11 == 0:
            self.penalty = 5
        if self.number == 55:
            self.penalty = 7

    def __str__( self ):
        s = '['+str(self.number)
        for i in range(self.penalty):
            s += '*'
        s += ']'
        return s

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

    def goesToRow( self, rows ):
        rowselect = -1
        for i in range( len( rows ) ):
            if self > rows[i].cards[-1]:
                if rowselect < 0:
                    rowselect = i
                elif rows[i].cards[-1] > rows[rowselect].cards[-1]:
                    rowselect = i
        return rowselect


# The whole deck of Take 5! cards
class Deck():
	
	def __init__( self, decksize=0 ):
		self.maxsize = decksize
		self.cards = []
		for i in range( self.maxsize ):
			self.cards.append( Card( i+1 ) )
			
	def __str__( self ):
		s = ''
		size = len( self.cards )
		for i in range( size ):
			s += str( self.cards[i] )
			if i < size-1:
				s += ','
		return s
		
	def shuffle( self ):
		size = len(self.cards)
		for i in range(size):
			j = random.randrange(i,size)
			self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
			
	def removeCard(self, card):
		if card in self.cards:
			self.cards.remove(card)
			return True
		return False
		
	def popCard( self ):
		return self.cards.pop()
		
	def isEmpty( self ):
		return (len( self.cards ) <= 0)


# A row of Take 5! cards
class Row(Deck):
	
	def __init__( self, maxsize ):
		self.cards = []
		self.maxsize = maxsize
		
	def canAdd( self, card ):
		if self.isEmpty():
			return True
		elif len( self.cards ) >= self.maxsize:
			return False
		elif card > self.cards[-1]:
			return True
		else:
			return False
			
	def addCard( self, card ):
		if self.canAdd( card ):
			self.cards.append( card )
		else:
			print( str( card ) , 'cannot be added to the selected row!' )
			
	def penalty( self ):
		p = 0
		for card in self.cards:
			p += card.penalty
		return p
		
	def size( self ):
		return len( self.cards )
		
	def startNewRow( self, card ):
		self.cards = []
		self.cards.append( card )