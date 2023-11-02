from copy import copy
from NoThanksPlayer import Player
from NoThanksGame import Deck, Card

class PlayerState():
    def __init__( self, name, coins, collection=[] ):
        self.name = name
        self.coins = coins
        self.collection = collection
    def __str__( self ):
        s = self.name + '\n'
        s += f'\tCoins: {self.coins}\n'
        s += '\tCollected: '
        if len( self.collection ) <= 0:
            s += 'Nothing\n'
        else:
            for i in range( len( self.collection ) ):
                card = self.collection[i]
                s += str( card )
                if i < len( self.collection )-1:
                    s += ','
                else:
                    s += '\n'
        return s

class State():
    def __init__( self, selectedplayers, players, round ):
        self.players = []
        self.round = round
        for player in selectedplayers:
            name = player.name
            coins = player.coins
            collection = copy( player.collection )
            self.players.append( PlayerState( name, coins, collection ) )
                
    def __str__( self ):
        s = 'Round: '+ str( self.round )
        s += '\nPlayers:\n'
        for player in self.players:
            s += str( player )
        return s

if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    player1 = Player("test1")
    for i in range( 4 ):
        player1.addCardToCollection( deck.popCard() )
    player2 = Player("test2")
    for i in range( 3 ):
        player2.addCardToCollection( deck.popCard() )
    player3 = Player("test3")
    for i in range( 2 ):
        player3.addCardToCollection( deck.popCard() )
    print( player1 )
    print( player2 )
    print( player3 )
    state = State( [player1,player2], [player1,player2,player3], 1 )
    print( state )
