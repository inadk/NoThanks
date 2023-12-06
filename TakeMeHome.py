from Take5Player import Player

class TakeMeHome(Player):
	def __init__( self ):
		Player.__init__( self )
		self.setName( 'TakeMeHome' )
		self.outcomeCounter = [0, 0, 0, 0, 0, 0, 0]
		self.gamepenalties = [0]
		self.strategies = []

	def startGame(self):
		self.cardsInPlay = [i for i in range(1, 105)]

	def endGame(self, state):
		self.gamepenalties.append(self.penalty())
		self.gamepenalties.append(0)
		self.strategies.append(0)

        
		# if self.games == 10000:

		# 	self.penalties = [max(self.gamepenalties[i+1] - self.gamepenalties[i], 0) for i in range(len(self.gamepenalties) - 1)]


		# 	print(" ")
		# 	print('Strategies: P1, 6lowest, lowScore, highScore, lowestPenaltyRow, highest')
		# 	print('Avg penalty:  ' 
		#  + "{:.2f}".format( sum(element for flag, element in zip(self.strategies, self.penalties) if flag == 1) / self.strategies.count(1) ) + ', ' 
		#  + "{:.2f}".format( sum(element for flag, element in zip(self.strategies, self.penalties) if flag == 2) / self.strategies.count(2) ) + ', '
		#  + "{:.2f}".format( sum(element for flag, element in zip(self.strategies, self.penalties) if flag == 3) / self.strategies.count(3) ) + ', ' 
		#  + "{:.2f}".format( sum(element for flag, element in zip(self.strategies, self.penalties) if flag == 4) / self.strategies.count(4) ) + ', '  
		#  + "{:.2f}".format( sum(element for flag, element in zip(self.strategies, self.penalties) if flag == 5) / self.strategies.count(5) ) + ', '  
		#  + "{:.2f}".format( sum(element for flag, element in zip(self.strategies, self.penalties) if flag == 6) / self.strategies.count(6) ) )
		# 	print('Occurences: ' 
		#  + "{:.2%}".format( self.strategies.count(1) / ( len(self.strategies) - self.strategies.count(0) ) ) + ', ' 
		#  + "{:.2%}".format( self.strategies.count(2) / ( len(self.strategies) - self.strategies.count(0) )  ) + ', '
		#  + "{:.2%}".format( self.strategies.count(3) / ( len(self.strategies) - self.strategies.count(0) )  ) + ', '
		#  + "{:.2%}".format( self.strategies.count(4) / ( len(self.strategies) - self.strategies.count(0) )  ) + ', ' 
		#  + "{:.2%}".format( self.strategies.count(5) / ( len(self.strategies) - self.strategies.count(0) )  ) + ', ' 
		#  + "{:.2%}".format( self.strategies.count(6) / ( len(self.strategies) - self.strategies.count(0) )  ) )
		# 	#print('Total occurences: ' + str( len(self.strategies) - self.strategies.count(0) ) )
		# 	#print(sum(self.penalties))
		# 	#print(len(self.gamepenalties))


		# 	#print(self.strategies)
		# 	#print(self.penalties)
		

	def playCard( self, hand, rows, state):

		if state.round != 1: 
			self.gamepenalties.append(self.penalty())
		
		if state.round == 1:
			for i in range(4):
				self.cardsInPlay.remove( rows[i].cards[0].number )

		if state.round > 1:
			for i in state.players:
				if i.ingame == True:
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

		# from P1 fitting cards choose card that fits highest penalty row, choose lowest such card
		def choosecfP1( rows ):
			cfP1r = cfP1rows( )
			if any( cfP1r ):
				rrbp = rowRankByPenalty( rows)
				for i in range(0, 4):
					if cfP1r[ rrbp[i] ]:
						return cfP1r[ rrbp[i] ][0]
		
		'''
		# from P1 fitting cards choose lowest card 
		def choosecfP1():
			if myLowestcfP1():
				return myLowestcfP1()
		'''

		# def logGameData(self, state, rows, hand):
		# 	print( 'round: ' + str( state.round ) )

		# 	print( 'rows[0]: ' + str( rows[0] ) )
		# 	print( 'rows[1]: ' + str( rows[1] ) )
		# 	print( 'rows[2]: ' + str( rows[2] ) )
		# 	print( 'rows[3]: ' + str( rows[3] ) )

		# 	# print( 'rows[0].cards[-1].number: ' + str( rows[0].cards[-1].number ) )
		# 	# print( 'rows[0].size(): ' + str( rows[0].size() ) )

		# 	print( 'myhand: ' + str( myHand(self) ) )
		# 	print( 'cardsFittingP1(): ' + str( cardsFittingP1() ) )
		# 	print( 'cfP1rows(self): ' + str( cfP1rows() ))
		# 	print( 'rowRankByPenalty( rows ): ' + str( rowRankByPenalty( rows ) ))
		# 	print( 'cfP1Exists( self, rows, hand): ' + str( cfP1Exists( ) ) )
		# 	print( 'choosecfP1( self, rows ): ' + str(choosecfP1(  )))
			


		# 	#	print(self.cardsInPlay)
		# 	#	print(len(self.cardsInPlay))		

		def findCardInHandByNumber( self, num ):
			for i in range( len(self.hand) ):
				if self.hand[i].number == num:
					return i
		
		if cfP1Exists( ):
			self.outcomeCounter[1] += 1
			self.strategies.append( 1 )			
			return hand[ findCardInHandByNumber( self, choosecfP1( rows ) ) ]

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
			sorted_rn = sorted(rn, key=lambda x: x[-1])
			
			differences = []
			for i in range(len(sorted_rn) - 1):
				diff = sorted_rn[i+1][-1] - sorted_rn[i][-1]
				differences.append(diff)

			largest_last_element = sorted_rn[-1][-1]
			subtraction_result = 104 - largest_last_element
			differences.append(subtraction_result)

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
					if rowPlaces[ gTWR[i] ] == 0:
						scores.append(0)
					else:
						scores.append( nCBelowMine[i] / rowPlaces[ gTWR[i] ]  ) 
						# nCBelowMine[i] / sum(rowPlaces) * rowPlaces[ gTWR[i] ] * rowPlaces[ gTWR[i] ]
						# nCBelowMine[i] - rowPlaces[ gTWR[i] ] * rowPlaces[ gTWR[i] ]
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


		# def logMetrics():
		# 	print('gaps() - ' + str(rowgaps) )
		# 	print('amountCardsFitRow() - ' + str(aCFR) )
		# 	print('proportionCardsFitRow() - ' + str(pCFR) )
		# 	print('goesToWhichRow() - ' + str(gTWR) ) 
		# 	print( 'numberOfCardsBelowMine( self, rows, hand) - ' + str( nCBelowMine ))
		# 	print( 'placesInRow(rows) - ' + str( rowPlaces ))
		# 	print( 'proportionOfPlacesInRow() - ' + str(propRowPlaces))
		# 	print( 'avgRowPenalty( rows ) - ' + str( avgRP ))
		# 	print( 'totalAvgRowPenalty( rows ) - ' + str( totAvgRP ))
		# 	print("scoreCards(rows) - " + str( scr ) ) 
		# 	print("getLowScore() - " + str( glowscr ) ) 
		# 	print("getHighScore() - " + str( ghighscr ) )
		# 	print( '-----' )
			
		# #logGameData(self, state, rows, hand)
		# #logMetrics()
		# #print(scr)
		
		# ------------------------------------------------------------------------------------------------------------------------------------------------------
		# Minimization of penalty collected by low cards
		def lowestRowPenalty():
			rowselect = 0
			for i in range(1,len(rows)):
				if rows[i].penalty() < rows[rowselect].penalty():
					rowselect = i
			return rows[i].penalty()
		
		lowestRP = lowestRowPenalty()
		
		if ( self.cardsInPlay.index( self.hand[0].number ) <= 5 and lowestRP <= 2 ):
			self.outcomeCounter[2] += 1
			self.strategies.append( 2 )
			return hand[0]
		
		
		if glowscr[0] < 2:	
			self.outcomeCounter[3] += 1
			self.strategies.append( 3 )
			return hand[ glowscr[1] ]
		if ghighscr[0] >= 10:
			self.outcomeCounter[4] += 1
			self.strategies.append( 4 )
			return hand[ ghighscr[1] ]
		
		def placesInLowestAvgPenaltyRow():
			rowselect = 0
			smallestp = 30
			for i in range(1,len(rows)):
				if avgRP[i] < smallestp:
					smallestp = avgRP[i]
					rowselect = i
			return [ i, rows[i].size() ]
		
		piLPR = placesInLowestAvgPenaltyRow()
		
		def cardToLowestPenaltyRow():
			for i in range(len(gTWR)):
				if gTWR[i] == piLPR[0]:
					return i
			else:
				return False
		
		ctLPR = cardToLowestPenaltyRow()

		if ctLPR != False and piLPR[1] < 5:
			self.outcomeCounter[5] += 1
			self.strategies.append( 5 )
			return hand[ ctLPR ]
		
		self.outcomeCounter[6] += 1
		self.strategies.append( 6 )
		return hand[-1]
		
	def chooseRow( self, rows, state ):
		rowselect = 0
		for i in range(1,len(rows)):
			if rows[i].penalty() < rows[rowselect].penalty():
				rowselect = i
		return rowselect
	