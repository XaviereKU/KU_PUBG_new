import discord
from dotenv import load_dotenv
import stats
from discord.ext import commands
import os
from bs4 import BeautifulSoup
import requests

load_dotenv(verbose=True) #load EVN file

bot_token = os.getenv('token') # Get discord bot token
apikey = os.getenv('apikey') # Get PUBG api key

#API header
header = {
	"Authorization": apikey,
	"Accept": "application/vnd.api+json"
}

statusurl = 'https://api.pubg.com/status'
status = str(requests.get(statusurl))
if status == '<Response [200]>':
	season = stats.getseason(header)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	game = discord.Game('배그도우미')
	await bot.change_presence(status=discord.Status.idle, activity=game)
	print('Ready and Go')

# @bot.command()
# async def test(ctx):
# 	await ctx.send('test')

@bot.command(name='구인', aliases=['구직', 'ㄱㅇ', 'ㄱㅈ']) #구인 명령어 반응, aliases에 있는 명령어를 쳐도 작동
async def recruit(ctx, arg1):
	vc = ctx.author.voice
	if vc != None:
		currentmemnum = len(vc.channel.members)
		currentvcchan = vc.channel.name
		recruitnum = int(arg1)
		msg = f'{currentvcchan}에서 {recruitnum}명 구인합니다!'
		await ctx.send(msg)

@bot.command(name = 'test') #작동 테스트
async def _text(ctx):
	await ctx.send('test')

@bot.command(name = '공카') #PUBG 공식 카페 링크
async def cafe(ctx):
	link = 'https://goo.gl/n45ZBj'
	msg = f'공카 주소 : {link}'
	await ctx.send(msg)

@bot.command(name = '전적') # PUBG game record
async def record(ctx,arg1,arg2,arg3):
	if status == '<Response [200]>':
		text = message.content
		result = stats.getstat(text,header,season)
		if type(result) == str:
			await channel.send(result)
		else:
			await channel.send(embed=result)
	else:
		await channel.send('서버 오류. 잠시 후 다시 시도해 주세요.')
bot.run(bot_token)