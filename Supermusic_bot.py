import discord
from discord.ext import commands
from pandas import options
from youtube_dl import YoutubeDL
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time
import os
from dotenv import load_dotenv
import random

bot = commands.Bot(command_prefix='!')

user = []
musictitle = []
song_queue = []
musicnow = []
load_dotenv()
token = os.getenv("TOKEN")
link = os.getenv("LINK")

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("이병 슈퍼봇 근무"))


@bot.command()
async def 들어와(ctx):
    try:
        global vc
        if(random.random() > 0.2):
            vc = await ctx.message.author.voice.channel.connect()
            await ctx.send("이병 슈퍼봇! 부르셨습니까!")
        else:
            await ctx.send("응~안가~")
    except:
        try:
            await vc.mode_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("Error")


@bot.command()
async def 나가(ctx):
    try:
        if(random.random() > 0.2):
            await vc.disconnect()
            await ctx.send("이병 슈퍼봇! 편히 쉬십쇼~")
        else:
            await ctx.send("응~안가~")
    except:
        try:
            await vc.disconnect()
        except:
            await ctx.send("Error")


@bot.command()
async def 재생(ctx, *, msg):
    if not vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")


        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = link
        driver = webdriver.Chrome(chromedriver_dir, options= options)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")

@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = entireText + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않네요.")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = entireText  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@bot.command()
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = entireText  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않네요..")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))




## 장난감==============================================================
@bot.command()
async def 뭐하냐(ctx):
    try:
        await ctx.send("죄송합니다!")
    except:
        try:
            await vc.mode_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("총이 더러워서 물로 씻고 있습니다!")

@bot.command()
async def 복무신조(ctx):
    try:
        await ctx.send("우리의 결의!")
    except:
        try:
            await vc.mode_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("죄송합니다! 아직 못 외웠습니다!")

@bot.command()
async def 아침뭐냐(ctx):
    try:
        await ctx.send("쇠미에 쏘야입니다!")
    except:
        try:
            await vc.mode_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("잘 모르겠습니다!")

@bot.command()
async def 점심뭐냐(ctx):
    try:
        await ctx.send("고순조입니다...")
    except:
        try:
            await vc.mode_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("저 오늘 안먹어서 모릅니다.")

@bot.command()
async def 남은군생활(ctx):
    try:
        await ctx.send("489일 남았습니다!")
    except:
        try:
            await vc.mode_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("그걸 왜 물어보십니까?")

@bot.command()
async def 툭툭치기(ctx):
    try:
        await ctx.send("이병 슈퍼봇!")
    except:
        try:
            await vc.mode_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("예?!")




##장난감=================================================================
bot.run(token)



# @bot.command()
# async def 음악(ctx):
#     try:
#         await ctx.send("000 병장님 어떤 음악 틀어드리면 되겠습니까?")
#     except:
#         try:
#             await vc.mode_to(ctx.message.author.voice.channel)
#         except:
#             await ctx.send("제 김상병이 기가지니 뚫다가 망가져서 음악 재생이 안됩니다..")

# @bot.command()
# async def 음악제목(ctx):
#     try:
#         await ctx.send("기가지니~음악제목 틀어줘~")
#     except:
#         try:
#             await vc.mode_to(ctx.message.author.voice.channel)
#         except:
#             await ctx.send("어..기가지니 맛 갔습니다...")