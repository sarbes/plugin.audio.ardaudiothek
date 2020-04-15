# -*- coding: utf-8 -*-
import requests
import copy

base = 'https://audiothek.ardmediathek.de'

header = 	{
			'Accept':'application/hal+json',
			'User-Agent':'okhttp/3.3.0',
			'Accept-Encoding':'gzip',
			}

class parser():
	def __init__(self):
		self.result = {'content':'songs','items':[],'pagination':{'currentPage':0}}
		self.template = {'params':{}, 'metadata':{'art':{}}, 'type':'dir'}

		self.width = '640'
		self.aspect = '16x9'
				
	def parseMostPlayed(self):
		j = requests.get(base,headers=header).json()
		self._grepItems(j['_embedded']['mt:mostPlayed']['_embedded']['mt:items'])
		return self.result
		
	def parseFeaturedPlaylists(self):
		j = requests.get(base,headers=header).json()
		self._grepEditorialCollections(j['_embedded']['mt:featuredPlaylists']['_embedded']['mt:editorialCollections'])
		return self.result
		
	def parseFeaturedProgramSets(self):
		j = requests.get(base,headers=header).json()
		self._grepProgramSets(j['_embedded']['mt:featuredProgramSets']['_embedded']['mt:programSets'])
		return self.result

	def parseCat(self):
		#response = libMediathek.getUrl(base+'/editorialcategories'+'?limit=100',header)
		j = requests.get(base+'/editorialcategories',headers=header).json()
		self._grepEditorialCategories(j['_embedded']['mt:editorialCategories'])
		return self.result

	def parseProgramSets(self,url):
		j = requests.get(url+'?limit=100',headers=header).json()
		self._grepProgramSets(j['_embedded']['mt:programSets'])
		return self.result
		
	def parseItems(self,url):#TODO: date
		j = requests.get(url+'?limit=100',headers=header).json()
		self._grepItems(j['_embedded']['mt:items'])
		return self.result
		
	def parsePrograms(self):
		j = requests.get(base+'/organizations',headers=header).json()
		for channel in j['_embedded']['mt:organizations']:
			publicationServices = channel['_embedded']['mt:publicationServices']
			if isinstance(publicationServices, dict):
				channelName = channel['_embedded']['mt:publicationServices']['title']
				#channelIcon = channel['_embedded']['mt:publicationServices']['_links']['mt:image']['href'].replace('{ratio}','1x1').replace('{width}','512')
				channelIcon = channel['_embedded']['mt:publicationServices']['_links']['mt:image']['href'].format(ratio='1x1', width='512')
				self.template = {'params':{'channel':channelName}, 'metadata':{'art':{'icon':channelIcon}}, 'type': 'dir'}
				self._grepProgramSets(channel['_embedded']['mt:publicationServices']['_embedded']['mt:programSets'])
			else:
				for publicationService in publicationServices:
					channelName = publicationService['title']
					channelIcon = publicationService['_links']['mt:image']['href'].format(ratio='1x1', width='512')
					self.template = {'params':{'channel':channelName}, 'metadata':{'art':{'icon':channelIcon}}, 'type': 'dir'}
					try:
						self._grepProgramSets(publicationService['_embedded']['mt:programSets'])
					except: pass
		return self.result
		
		
	def _grepItems(self,j):
		for item in j:
			d = {'params':{'mode':'playAudio'}, 'metadata':{'art':{}}, 'type':'video'}
			d['metadata']['name'] = item['title']
			d['metadata']['plot'] = item['synopsis']
			d['metadata']['duration'] = item['duration']
			d['metadata']['art']['thumb'] = item['_links']['mt:image']['href'].format(ratio='16x9', width='640')
			d['params']['url'] = item['_links']['mt:bestQualityPlaybackUrl']['href']
			self.result['items'].append(d)
		return 

	def _grepEditorialCategories(self,j):
		for item in j:
			d = {'params':{'mode':'listProgramSets'}, 'metadata':{'art':{}}, 'type':'dir'}
			d['metadata']['name'] = item['title']
			d['metadata']['art']['thumb'] = item['_links']['mt:image']['href'].format(ratio='16x9', width='640')
			d['params']['url'] = base + '/editorialcategories/' + item['id']
			self.result['items'].append(d)
		return 
		
	def _grepEditorialCollections(self,j):
		for item in j:
			d = {'params':{'mode':'listItems'}, 'metadata':{'art':{}}, 'type':'dir'}
			d['metadata']['name'] = item['title']
			d['metadata']['plot'] = item['synopsis']
			d['metadata']['numberOfElements'] = item['numberOfElements']
			d['metadata']['art']['thumb'] = item['_links']['mt:image']['href'].format(ratio='16x9', width='640')
			d['params']['url'] = base + '/editorialcollections/' + item['id']
			self.result['items'].append(d)
		return 
		
	def _grepProgramSets(self,j):
		for item in j:
			d = copy.deepcopy(self.template)
			d['metadata']['name'] = item['title']
			if 'synopsis' in item:
				d['metadata']['plot'] = item['synopsis']
			d['metadata']['numberOfElements'] = item['numberOfElements']
			d['metadata']['art']['thumb'] = item['_links']['mt:image']['href'].format(ratio='1x1', width='640')
			d['params']['url'] = base + '/programsets/' + item['id']
			d['params']['mode'] = 'listItems'
			self.result['items'].append(d)
		return 
		