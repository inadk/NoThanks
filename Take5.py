# Take 5! or 6 Nimmt! Game file

import random
import importlib
import sys
from Take5Game import Deck, Card, Row
from Take5Player import Player
from Take5State import State

# Need to add:
# Handy functions for the players.

DEFAULTLENGTH = 1000
DEFAULTAIS = ["Take5Beginners"]

MAXPLAYERS = 10
STARTHANDSIZE = 10
MAXROWSIZE = 5
NUMROWS = 4
DOTDISPLAY = min( max( int( DEFAULTLENGTH / 10 ), 1 ), 1000 )

# A Play is a combination of a player and a card
class Play():
    
    def __init__( self, player, card ):
        self.player = player
        self.card = card

    def __lt__( self, other ):
        return self.card < other.card

    def __gt__( self, other ):
        return self.card > other.card

    def __le__( self, other ):
        return self.card <= other.card

    def __ge__( self, other ):
        return self.card >= other.card

    def __eq__( self, other ):
        return self.card == other.card

    def __str__( self ):
        return str( self.player )+' plays '+str( self.card )


# A game consists of shuffling and dealing the cards,
# and has methods to play out the game.
# playRound plays one round of the game; it asks all players for a card,
# then updates the table.
class Game():

	def __init__( self, length, players ):
		self.length = length
		self.players = players
		self.rows = []
		
	def startGame( self, selectedplayers ):
		for player in self.players:
			player.reset()
		for player in selectedplayers:
			player.startGame()
		self.deck = Deck( len( selectedplayers ) * STARTHANDSIZE + NUMROWS )
		self.deck.shuffle()
		self.rows = []
		for i in range( NUMROWS ):
			self.rows.append( Row( MAXROWSIZE ) )
		for player in selectedplayers:
			for i in range( STARTHANDSIZE ):
				player.addCard( self.deck.popCard() )
		for row in self.rows:
			row.addCard( self.deck.popCard() )
		if not self.deck.isEmpty():
			print( 'ERROR! Deck should be empty!' )
			
	def endGame( self, selectedplayers ):
		state = State( 10, self.rows, selectedplayers, self.players )
		for player in selectedplayers:
			player.endGame( state )

	def __str__( self ):
		s = ''
		for player in self.players:
			s += str( player ) + '\n'
		for row in self.rows:
			s += str( row ) + '\n'
		return s

	def playRound( self, selectedplayers, number ):
		self.plays = []
		state = State( number, self.rows, selectedplayers, self.players )
		# print state
		for player in selectedplayers:
			card = player.playCard( player.hand, self.rows, state )
			if card not in player.hand:
				card = player.hand[random.randrange( len( player.hand ) )]
			player.lastcard = card
			self.plays.append( Play( player, card ) )
		self.plays.sort()
		for play in self.plays:
			play.player.removeCard( play.card )
			rowselect = play.card.goesToRow( self.rows )
			if rowselect >= 0 and len( self.rows[rowselect].cards ) < MAXROWSIZE:
				self.rows[rowselect].addCard( play.card )
			else:
				if rowselect < 0:
					rowselect = play.player.chooseRow( self.rows, state )
				if rowselect < 0 or rowselect > 3:
					rowselect = random.randrange( 4 )
				for card in self.rows[rowselect].cards:
					play.player.addCardToCollection( card )
				self.rows[rowselect].startNewRow( play.card )

	def statistics( self ):
		print( "NAME                   GAMES  AVERAGE" )
		players.sort()
		for player in self.players:
			print( f"{player.name:20s} {player.games:7d} {player.score():8.3f}" )

	def run( self ):
		for i in range( self.length ):
			if i % DOTDISPLAY == 0:
				print( '.', end="" )
			selectedplayers = []
			if len( self.players ) < MAXPLAYERS:
				selectedplayers = self.players
			else:
				while len( selectedplayers ) < MAXPLAYERS:
					p = self.players[random.randrange( len(self.players) )]
					if p not in selectedplayers:
						selectedplayers.append( p )
			self.startGame( selectedplayers )
			for i in range( STARTHANDSIZE ):
				self.playRound( selectedplayers, i+1 )
				# print
			for player in selectedplayers:
				player.games += 1
				player.totalpenalty += player.penalty()
			self.endGame( selectedplayers )
		print()

# Loads the competitors from the command line arguments
def getCompetitors(argv):
	competitors = []
	for request in argv:
		if '.' in request:
			filename, classname = request.split('.')
		else:
			filename, classname = request, None
		module = importlib.import_module(filename)
		if classname:
			competitors.append(getattr(module, classname))
		else:
			for b in dir(module):
				if hasattr(module, '__all__') and not b in module.__all__: 
					continue
				if b.startswith('__') or b == 'Player': 
					continue
				cls = getattr(module, b)
				try:
					if issubclass(cls, Player):
						competitors.append(cls)
				except TypeError:
					pass
	return competitors


if __name__ == '__main__':
	
	length = DEFAULTLENGTH
	competitors = [] # is a list of the classes that compete
	
	if len(sys.argv) > 1:
		try:
			length = int(sys.argv[1])
		except:
			print( "Usage: Take5.py [<number of games> [<botfiles>]]" )
			sys.exit(1)

	if len( sys.argv ) > 2:
		for i, arg in enumerate(sys.argv[2:]):
			if '/' not in arg: 
				continue
			sys.path.append(arg)
			del sys.argv[2+i]
		competitors = getCompetitors(sys.argv[2:])
			
	if len(competitors) <= 0:
		competitors = getCompetitors( DEFAULTAIS )
		
	players = [] # is a list of instances of competing classes
	for competitor in competitors:
		players.append( competitor() )
		
	game = Game( length, players )
	# print game
	game.run()
	game.statistics()
