# -*- coding: utf-8 -*-
from libmediathek4 import lm4
import resources.lib.jsonparser as jsonParser
parser = jsonParser.parser()




class audiothek(lm4):
	def __init__(self):
		self.defaultMode = 'main'

		self.modes = {
			'main': self.main,
			'listMostPlayed': self.listMostPlayed,
			'listFeaturedPlaylists': self.listFeaturedPlaylists,
			'listFeaturedProgramSets': self.listFeaturedProgramSets,
			'listPrograms': self.listPrograms,
			'listCategories': self.listCategories,
			'listProgramSets': self.listProgramSets,
			'listItems': self.listItems,
			'playAudio': self.playAudio,
		}	

		self.playbackModes = {
			'playAudio':self.playAudio,
		}

	def main(self):
		l = []
		l.append({'metadata':{'name':self.translation(32138)}, 'params':{'mode':'listMostPlayed'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(32137)}, 'params':{'mode':'listFeaturedPlaylists'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(32135)}, 'params':{'mode':'listCategories'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(32136)}, 'params':{'mode':'listFeaturedProgramSets'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(32132)}, 'params':{'mode':'listPrograms'}, 'type':'dir'})
		return {'items':l,'name':'root'}
		
	def listMostPlayed(self):
		return parser.parseMostPlayed()
		
	def listFeaturedPlaylists(self):
		return parser.parseFeaturedPlaylists()
		
	def listFeaturedProgramSets(self):
		return parser.parseFeaturedProgramSets()

	def listPrograms(self):
		self.sortAZ()
		return parser.parsePrograms()
		
	def listCategories(self):
		return parser.parseCat()
		
	def listProgramSets(self):
		return parser.parseProgramSets(self.params['url'])
		
	def listItems(self):
		return parser.parseItems(self.params['url'])
		
	def playAudio(self):
		return {'media':[{'url':self.params['url'], 'type':'video', 'stream':'MP4'}]}
			
o = audiothek()
o.action()