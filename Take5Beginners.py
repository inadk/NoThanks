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


class LowToHighPenalty1(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'LowToHighPenalty1' )
	def playCard( self, hand, rows, state ):
		cardselect = 0
		for i in range( 1, len(hand) ):
			if hand[i].penalty < hand[cardselect].penalty:
				cardselect = i
		return hand[cardselect]

	
class LowToHighPenalty2(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'LowToHighPenalty2' )
	def playCard( self, hand, rows, state ):
		cardselect = 0
		for i in range( 1, len(hand) ):
			if hand[i].penalty < hand[cardselect].penalty:
				cardselect = i
		return hand[cardselect]


class HighToLowPenalty1(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'HighToLowPenalty1' )
	def playCard( self, hand, rows, state ):
		cardselect = 0
		for i in range( 1, len(hand) ):
			if hand[i].penalty > hand[cardselect].penalty:
				cardselect = i
		return hand[cardselect]

	
class HighToLowPenalty2(LowPenalty):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'HighToLowPenalty2' )
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


# ---------------------------------------------------------------------------------------

class MyAI(Player):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'MyAI' )
		self.outcomeCounter = [0, 0, 0]
		self.penalties = [0]
		self.strategies = [0]


	def startGame(self):
		self.cardsInPlay = [i for i in range(1, 105)]

	def endGame(self, state):
		self.penalties.append(0)
		self.strategies.append(0)
		if self.games == 10000:
			print( self.outcomeCounter)
			print('pick highest score card avg penalty: '  + str( sum(element for flag, element in zip(self.strategies, self.penalties) if flag == 1) / self.strategies.count(1) ) )
			print('pick lowest score card avg penalty: '  + str( sum(element for flag, element in zip(self.strategies, self.penalties) if flag == 2) / self.strategies.count(2) ) )
			print('number of time strategies were applied: ' + str( len(self.strategies)) )
			print('strategy occurences: ' + str( self.strategies.count(1) ) + '; ' + str( self.strategies.count(2) ))

	def playCard( self, hand, rows, state):

		# list available cards
		
		if state.round == 1:
			for i in range(4):
				self.cardsInPlay.remove( rows[i].cards[0].number )

		if state.round > 1:
			for i in state.players:
				self.cardsInPlay.remove( i.lastcard.number )

		# make decision based on card fits with P=1

		def cardsFittingP1():
			cfP1 = []
			for i in range(0,4):
				cfP1.append( [e for e in self.cardsInPlay if e > rows[i].cards[-1].number ][ :( 5 - rows[i].size() ) ] )
			return cfP1
		
		# get list of card number in my hand
		def myHand(self):
			myhand = []
			for i in range(len(self.hand)):
				myhand.append( self.hand[i].number )
			return myhand
		
		myhand = myHand(self)

		def cfP1rows():
			cfP1 = cardsFittingP1()
			result = [[] for _ in range(len(cfP1))]
			for c in myhand:
				for i, sublist in enumerate(cfP1):
					if c in sublist:
						result[i].append(c)
			return result
		
		cfP1r = cfP1rows()
		
		# get penalty tank of rows descending
		def rowRankByPenalty( rows ):
			penaltys = []
			for i in range(4):
				penaltys.append( [i, rows[i].penalty() ] )
			penaltys.sort(key=lambda x: x[1], reverse=True)
			return [sublist[0] for sublist in penaltys]
		
		def cfP1Exists():
			if any( cfP1r ): 
				return True
			return False
		
		def mycfP1s():
			return [i for sublist in cfP1r if sublist for i in sublist]
		
		mycfP1 = mycfP1s()

		def myLowestcfP1():
			if mycfP1:
				return min(mycfP1)
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
		def choosecfP1():
			if myLowestcfP1():
				return myLowestcfP1()


		def logGameData(self, state, rows, hand):
			print( 'round: ' + str( state.round ) )

			print( 'rows[0]: ' + str( rows[0] ) )
			print( 'rows[1]: ' + str( rows[1] ) )
			print( 'rows[2]: ' + str( rows[2] ) )
			print( 'rows[3]: ' + str( rows[3] ) )

			# print( 'rows[0].cards[-1].number: ' + str( rows[0].cards[-1].number ) )
			# print( 'rows[0].size(): ' + str( rows[0].size() ) )

			print( 'myhand: ' + str( myHand(self) ) )
			print( 'cardsFittingP1(): ' + str( cardsFittingP1() ) )
			print( 'cfP1rows(self): ' + str( cfP1rows() ))
			print( 'rowRankByPenalty( rows ): ' + str( rowRankByPenalty( rows ) ))
			print( 'cfP1Exists( self, rows, hand): ' + str( cfP1Exists( ) ) )
			print( 'choosecfP1( self, rows ): ' + str(choosecfP1(  )))
			
			

			#	print(self.cardsInPlay)
			#	print(len(self.cardsInPlay))

		

		def findCardInHandByNumber( self, num ):
			for i in range( len(self.hand) ):
				if self.hand[i].number == num:
					return i
		
		if cfP1Exists( ):
			# print('playing cfP1 from hand at index: ' + str( hand[ findCardInHandByNumber( self, choosecfP1( self, rows ) ) ] ) )
			return hand[ findCardInHandByNumber( self, choosecfP1( ) ) ]

		# ------------------------------------------------------------------------------------------------------------------------------------------
		# if no cards fit any row with P=1

		# get rows with only numbers
		def rowsNumbers( rows ):
			rowsNums = []
			for i in range(4):
				rowsNums.append( [] )
				for j in range( rows[i].size() ):
					rowsNums[i].append( rows[i].cards[j].number )
			return rowsNums
		
		rn = rowsNumbers( rows )

		# get gaps between rows
		def gaps ( ):

			# Step 1: Sort the sublists based on their last element
			sorted_rn = sorted(rn, key=lambda x: x[-1])
			
			# Step 2: Subtract the last element of each sublist from the first element of the next
			differences = []
			for i in range(len(sorted_rn) - 1):
				diff = sorted_rn[i+1][-1] - sorted_rn[i][-1]
				differences.append(diff)

			# Step 3: Subtract the largest last element from 104
			largest_last_element = sorted_rn[-1][-1]
			subtraction_result = 104 - largest_last_element
			differences.append(subtraction_result)

			# Step 4: Map the results back to the original order of sublists
			results = [None] * len(rn)
			for i, sublist in enumerate(rn):
				index_in_sorted = sorted_rn.index(sublist)
				results[i] = differences[index_in_sorted] if index_in_sorted < len(differences) else subtraction_result
			
			return results
		
		rowgaps = gaps ()


		# number of cards in play fitting into gaps
		def amountCardsFitRow( ):
			results = []
			for i in range(4):
				results.append( len( [ c for c in self.cardsInPlay if rows[i].cards[-1].number < c < rows[i].cards[-1].number + rowgaps[i] ] ) )
			return results

		aCFR = amountCardsFitRow( )

		
		# proportion of card fitting into row i from all cards fitting into gaps
		def proportionCardsFitRow( ):
			results = []
			if sum(aCFR) == 0:
					return [0, 0, 0, 0]
			else:
				for i in aCFR:				
					results.append( i / sum(aCFR) )
			return results

		pCFR = proportionCardsFitRow()


		# tells which row card goes to if it goes to any
		def goesToWhichRow():
			results = []
			for i in self.hand:
				rowIndex = None
				for j in range(4):
					if rows[j].cards[-1].number < i.number:
						rowIndex = j
				results.append( rowIndex )
			return results

		gTWR = goesToWhichRow()


		# not important
		# proportion of cards that can be placed in the row and less than mine versus all cards that can be placed in that row
		# calculated for all my cards
		def numberOfCardsBelowMine( self, rows, hand):
			results = []
			for i in range( len(self.hand) ):
				if gTWR[i] != None:
					results.append( len( [ c for c in self.cardsInPlay if rows[ gTWR[i] ].cards[-1].number < c < self.hand[i].number ] ) )
				else:
					results.append( None )
			return results
		
		nCBelowMine = numberOfCardsBelowMine( self, rows, hand)
		
		
		def placesInRow(rows):
			results = []
			for i in rows:
				results.append( 5 - i.size() )
			return results
		
		rowPlaces = placesInRow(rows)
		

		def proportionOfPlacesInRow( ):
			results = []
			for i in rowPlaces:
				if sum(rowPlaces) == 0 :
					return [0, 0, 0, 0]
				else:
					results.append( i / sum(rowPlaces) )
			return results
		
		propRowPlaces = proportionOfPlacesInRow( )
		

		def avgRowPenalty( rows ):
			results = []
			for i in rows:
				results.append( i.penalty() / i.size() )
			return results
		
		avgRP = avgRowPenalty( rows )
		

		def totalAvgRowPenalty( rows ):
			pen = 0
			sizes = 0
			for i in rows:
				pen += i.penalty()
				sizes += i.size()
			return pen / sizes
		
		totAvgRP = totalAvgRowPenalty( rows )
		
		def scoreCards(self, hand, rows):
			scores = []
			for i in range(len(self.hand)):
				if gTWR[i] == None:
					scores.append(0)
				else:
					#if rows[ gTWR[i] ].cards[-1].number == 0:
					#	scores.append(0)
					#if rowPlaces == [0, 0, 0, 0]:
					#	scores.append(0)
					if rowPlaces[ gTWR[i] ] == 0:
						scores.append(0)
					else:
						scores.append( nCBelowMine[i] / rowPlaces[ gTWR[i] ] ) 
						# nCBelowMine[i] / sum(rowPlaces) * rowPlaces[ gTWR[i] ] * rowPlaces[ gTWR[i] ]
			return scores
		
		scr = scoreCards(self, hand, rows)
		
		def getLowScore():
			lowest = 100
			ind = -1
			for i in scr:
				if ( i > 0 and i < lowest ):
					lowest = i
					ind = scr.index(i)
			return [lowest, ind]
		
		glowscr = getLowScore()
		
		def getHighScore():
			highest = 0
			ind = -1
			for i in scr:
				if ( i > 0 and i > highest ):
					highest = i
					ind = scr.index(i)
			return [highest, ind]
		
		ghighscr = getHighScore()

		def logMetrics():
			print('gaps() - ' + str(rowgaps) )
			print('amountCardsFitRow() - ' + str(aCFR) )
			print('proportionCardsFitRow() - ' + str(pCFR) )
			print('goesToWhichRow() - ' + str(gTWR) ) 
			print( 'numberOfCardsBelowMine( self, rows, hand) - ' + str( nCBelowMine ))
			print( 'placesInRow(rows) - ' + str( rowPlaces ))
			print( 'proportionOfPlacesInRow() - ' + str(propRowPlaces))
			print( 'avgRowPenalty( rows ) - ' + str( avgRP ))
			print( 'totalAvgRowPenalty( rows ) - ' + str( totAvgRP ))
			print("scoreCards(rows) - " + str( scr ) ) 
			print("getLowScore() - " + str( glowscr ) ) 
			print("getHighScore() - " + str( ghighscr ) )
			print( '-----' )
		
		#logGameData(self, state, rows, hand)
		#logMetrics()
		#print(scr)

		def penaltiesPerStrategy(self):
			self.penalties.append( self.penalty() - self.penalties[-1] )

		penaltiesPerStrategy(self)

		if ghighscr[0] > 5:
			self.outcomeCounter[0] += 1
			self.strategies.append( 1 )
			return hand[ ghighscr[1] ]
		else:			
			self.outcomeCounter[1] += 1
			self.strategies.append( 2 )
			return hand[ glowscr[1] ]


	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect
	