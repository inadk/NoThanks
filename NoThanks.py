# No Thanks! Game file

import random
import importlib
import sys
from NoThanksGame import Deck, Card
from NoThanksPlayer import Player
from NoThanksState import State

# Need to add:
# Handy functions for the players.

DEFAULTLENGTH = 1000
DEFAULTAIS = ["NoThanksBeginners"]

MAXPLAYERS = 5
DOTDISPLAY = min( max( int( DEFAULTLENGTH / 10 ), 1 ), 1000 )

# A game consists of shuffling and dealing the cards,
# and has methods to play out the game.
class Game():

    def __init__( self, length, players ):
        self.length = length
        self.players = players
        self.deck = None

    def startGame( self, selectedplayers ):
        for player in self.players:
            player.reset()
        for player in selectedplayers:
            player.startGame()
        self.deck = Deck()
        self.deck.shuffle()

    def endGame( self, selectedplayers ):
        state = State( selectedplayers, self.players, 24 )
        for player in selectedplayers:
            player.endGame( state )

    def __str__( self ):
        s = ''
        for player in self.players:
            s += str( player ) + '\n'
        return s

    def playRound( self, selectedplayers, number ):
        card = self.deck.popCard()
        while True:
            state = State( selectedplayers, self.players, number )
            if selectedplayers[0].coins <= 0:
                take = True
            else:
                take = selectedplayers[0].take( card, state )
            if take:
                selectedplayers[0].addCardToCollection( card )
                #state = State( selectedplayers, self.players )
                #print( state )
                break
            selectedplayers[0].coins -= 1
            card.coins += 1
            player = selectedplayers.pop(0)
            selectedplayers.append( player )

    def statistics( self ):
        print( "\nNAME                   GAMES  AVERAGE" )
        players.sort()
        for player in self.players:
            print( f"{player.name:20s} {player.games:7d} {player.score():8.3f}" )

    def run( self ):
        for i in range( self.length ):
            if i % DOTDISPLAY == 0:
                print( '.', end="" )
            selectedplayers = []
            while len( selectedplayers ) < min( len( self.players ), MAXPLAYERS ):
                p = self.players[random.randrange( len(self.players) )]
                if p not in selectedplayers:
                    selectedplayers.append( p )
            number = 0
            self.startGame( selectedplayers )
            while len( self.deck ) > 0:
                number += 1
                self.playRound( selectedplayers, number )
            for player in selectedplayers:
                player.games += 1
                player.totalpenalty += player.penalty()
            self.endGame( selectedplayers )

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
            print( "Usage: NoThanks.py [<number of games> [<botfiles>]]" )
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
    game.run()
    print()
    game.statistics()
