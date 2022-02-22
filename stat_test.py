import requests
from bs4 import BeautifulSoup
import lxml
import json
from collections import OrderedDict
import math
from dotenv import load_dotenv
import os
import pandas as pd
from pandas import json_normalize #json을 pandas data frame으로 쉽게 바꾸려고


load_dotenv() #load EVN file

API_KEY = os.getenv('apikey') # Get PUBG api key

#API header
header = {
	"Authorization": API_KEY,
	"Accept": "application/vnd.api+json"
}

#case sensitive 피하기 위해 다른 사이트에서 이름 가져오기
def getname(inputname):
	url = f'https://pubg.op.gg/user/{inputname}'
	source_code = requests.get(url, headers ={'User-Agent':'Mozilla/5.0'})
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, 'html.parser')
	nameraw = soup.find(name='div', attrs={'class':'player-summary__name'}).text
	name = nameraw.strip()
	return name

#가져온 이름으로 API request
def getid(name,region):
	url = f'https://api.pubg.com/shards/{region}/players?filter[playerNames]={name}'
	idjson = requests.get(url, headers=header).json() #headers 빠지면 작동 안함
	playerid = idjson['data'][0]['id']
	return playerid

#현재 활성화된 시즌 가져오기
def getseason(region):
	seasonurl = f'https://api.pubg.com/shards/{region}/seasons'
	seasonsource = requests.get(seasonurl, headers=header).json()
	for i in seasonsource['data']:
		if 'pc' in i['id'] and i['attributes']['isCurrentSeason'] == True:
			seasonid = i['id']
	return seasonid

#비경쟁전 솔로 전적
def nonranksolo(msg):
	msg = msg.split()
	namebycase = getname(msg[0])
	seasonid = getseason(msg[1])	
	playerid = getid(msg[0], msg[1])
	region = msg[1]
	url = f'https://api.pubg.com/shards/{region}/players/{playerid}/seasons/{seasonid}'
	statsource = requests.get(url, headers=header).json()
	statdata = statsource['data']['attributes']['gameModeStats']['solo']
	print(statdata)

#경쟁전 솔로 전적
def ranksolo(msg):
	url = f'https://api.pubg.com/shards/{region}/players/{playerid}/seasons/{seasonid}/ranked'
	statsource = requests.get(url, headers=header).json()
	modelist = list(statsource['data']['attributes']['rankedGameModeStats'].keys())
	modedftest = json_normalize(statsource['data']['attributes']['rankedGameModeStats'][modelist[0]])
	print(modedftest)

nonranksolo('Bodeum_ kakao')

# getstat('kakao', 'account.178fea2929b449538f510e51aedbb65b', 1, 'division.bro.official.pc-2018-16')