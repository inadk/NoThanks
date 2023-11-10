class PlayerState():
	def __init__( self, name, collection=[], score=0.0, ingame=False, lastcard=None ):
		self.name = name
		self.collection = collection
		self.score = score
		self.ingame = ingame
		self.lastcard = lastcard
	def __str__( self ):
		s = self.name + '\n'
		s += 'Score: %8.3f\n' % self.score
		if self.ingame:
			s += 'in game\n'
		else:
			s += 'not in game\n'
		s += 'Last card played: '
		if self.lastcard is None:
			s += 'None'
		else:
			s += str( self.lastcard )
		s += '\nCollected:\n'
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
	def __init__( self, round, rows, selectedplayers, players ):
		self.players = []
		self.round = round
		self.rows = rows
		for player in players:
			name = player.name
			collection = player.collection
			score = player.score()
			lastcard = player.lastcard
			ingame = False
			if player in selectedplayers:
				ingame = True
			self.players.append( PlayerState( name, collection, score, ingame, lastcard ) )
	def __str__( self ):
		s = 'Round: ' + str( self.round ) + '\nCard rows:\n'
		for row in self.rows:
			s += str( row ) + '\n'
		s += 'Players:\n'
		for player in self.players:
			s += str( player )
		return s
