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

class HighToLow(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'HighToLow' )
	def playCard( self, hand, rows, state ):
		return hand[-1]

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


class MyAI(Player):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'MyAI' )
		
		self.cardsInPlay = [i for i in range(1, 105)]
		print(self.cardsInPlay)
	def playCard( self, hand, rows, state):
		
		if state.round > 1:
			for i in state.players:
				print( (i.lastcard).number )
				if ( (i.lastcard).number in self.cardsInPlay):
					self.cardsInPlay.remove( (i.lastcard).number )
				else:
					print('card played has been played before: ' + str((i.lastcard).number))
		if state.round == 10: 
			print(self.cardsInPlay)

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
