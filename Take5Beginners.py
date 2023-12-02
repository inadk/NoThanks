from Take5Player import Player
from Take5State import State, PlayerState
import random


class RandomPlayer(Player):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'RandomPlayer' )
	def playCard( self, hand, rows, state ):
		return hand[random.randrange(0,len( hand ))]
	def chooseRow( self, rows, state ):
		return random.randrange(0,len(rows))


class LowPenalty(RandomPlayer):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'LowPenalty' )
	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect

class LowToHigh(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'LowToHigh' )
	def playCard( self, hand, rows, state ):
		return hand[0]
	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect

class HighToLow(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'HighToLow' )
	def playCard( self, hand, rows, state ):
		return hand[-1]
	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect

class LowToHighPenalty(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'LowToHighPenalty' )
	def playCard( self, hand, rows, state ):
		cardselect = 0
		for i in range( 1, len(hand) ):
			if hand[i].penalty < hand[cardselect].penalty:
				cardselect = i
		return hand[cardselect]
	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect

class HighToLowPenalty(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'HighToLowPenalty' )
	def playCard( self, hand, rows, state ):
		cardselect = 0
		for i in range( 1, len(hand) ):
			if hand[i].penalty > hand[cardselect].penalty:
				cardselect = i
		return hand[cardselect]
	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect
	
class AvoidPenalty(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'AvoidPenalty' )
	def playCard( self, hand, rows, state ):
		cardselect = -1
		rowselect = -1
		i = 0
		# Try to find a card that goes into a row without giving a penalty
		while i < len(hand):
			rowselect = hand[i].goesToRow( rows )
			if rowselect >= 0:
				cardselect = i
				break
			i += 1
		# Now try to find a card that goes in a row as short as possible
		for i in range( cardselect+1, len(hand) ):
			newrow = hand[i].goesToRow( rows )
			if newrow < 0:
				continue
			if rows[newrow].size() < rows[rowselect].size():
				rowselect = newrow
				cardselect = i
		# If all cards seem to give a penalty, play a random one
		if cardselect < 0:
			return hand[random.randrange(0,len( hand ))]
		return hand[cardselect]
	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect


# ---------------------------------------------------------------------------------------

class MyAI(Player):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'MyAI' )

	def playCard( self, hand, rows, state):
		
		if state.round == 1:
			self.cardsInPlay = [i for i in range(1, 105)]

		if state.round > 1:
			for i in state.players:
				self.cardsInPlay.remove( i.lastcard.number )

		def cardsFittingP1():
			cfP1 = []
			for i in range(0,4):
				cfP1.append( [e for e in self.cardsInPlay if e > rows[i].cards[-1].number ][ :( 5 - rows[i].size() ) ] )
			return cfP1
		
		def myHand(self):
			myhand = []
			for i in range(len(self.hand)):
				myhand.append( self.hand[i].number )
			return myhand 

		def cfP1rows(self):
			cfP1 = cardsFittingP1()
			myhand = myHand(self)
			result = [[] for _ in range(len(cfP1))]
			for c in myhand:
				for i, sublist in enumerate(cfP1):
					if c in sublist:
						result[i].append(c)
			return result
		
		def rowRankByPenalty( rows ):
			penaltys = []
			for i in range(4):
				penaltys.append( [i, rows[i].penalty() ] )
			penaltys.sort(key=lambda x: x[1], reverse=True)
			return [sublist[0] for sublist in penaltys]
		
		def cfP1Exists( self, rows, hand ):
			cfP1r = cfP1rows(self)
			if any( cfP1r ): 
				return True
			return False
		
		def mycfP1s(self):
			cfP1r = cfP1rows(self)
			return [i for sublist in cfP1r if sublist for i in sublist]
			
			if flat_list:
				return min(flat_list)
			else:
				return None
			
		def myLowestcfP1(self):
			li = mycfP1s(self)
			if li:
				return min(li)
			else:
				return None

		'''
		# from P1 fitting cards choose card that fits highest penalty row, choose lowest such card
		def choosecfP1( self, rows ):
			cfP1r = cfP1rows(self)
			if any( cfP1r ):
				rrbp = rowRankByPenalty( rows )
				for i in range(0, 4):
					if cfP1r[ rrbp[i] ]:
						return cfP1r[ rrbp[i] ][0]
		'''

		# from P1 fitting cards choose lowest card 
		def choosecfP1( self, rows ):
			if myLowestcfP1(self):
				return myLowestcfP1(self)


		def logData(self, state, rows, hand):
			print( 'round: ' + str( state.round ) )

			print( 'rows[0]: ' + str( rows[0] ) )
			print( 'rows[1]: ' + str( rows[1] ) )
			print( 'rows[2]: ' + str( rows[2] ) )
			print( 'rows[3]: ' + str( rows[3] ) )

			# print( 'rows[0].cards[-1].number: ' + str( rows[0].cards[-1].number ) )
			# print( 'rows[0].size(): ' + str( rows[0].size() ) )

			print( 'myhand: ' + str( myHand(self) ) )
			print( 'cardsFittingP1(): ' + str( cardsFittingP1() ) )
			print( 'cfP1rows(self): ' + str( cfP1rows(self) ))
			print( 'rowRankByPenalty( rows ): ' + str( rowRankByPenalty( rows ) ))
			print( 'cfP1Exists( self, rows, hand): ' + str( cfP1Exists( self, rows, hand) ) )
			print( 'choosecfP1( self, rows ): ' + str(choosecfP1( self, rows )))
			
			print( '-----' )

			#	print(self.cardsInPlay)
			#	print(len(self.cardsInPlay))

		# logData(self, state, rows, hand)

		def findCardInHandByNumber( self, num ):
			for i in range( len(self.hand) ):
				if self.hand[i].number == num:
					return i

		if cfP1Exists( self, rows, hand ):
			# print('playing cfP1 from hand at index: ' + str( hand[ findCardInHandByNumber( self, choosecfP1( self, rows ) ) ] ) )
			return hand[ findCardInHandByNumber( self, choosecfP1( self, rows ) ) ]
			
		return hand[-1]

	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect
	