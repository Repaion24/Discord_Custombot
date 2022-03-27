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

load_dotenv()
token = os.getenv("TOKEN")
link = os.getenv("LINK")

user = []       #유저가 입력한 노래 정보
musictitle = [] #가공된 노래의 정보 제목
song_queue = [] #가공된 정보의 노래 링크 큐
musicnow = []   #현재 출력중인 노래


def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = link
    driver = webdriver.Chrome(chromedriver_dir, options = options)
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL


def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx)) 


def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))




#봇 event 함수들 =================================================================

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("이병 슈퍼봇 근무"))


@bot.command()
async def 야(ctx):
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

        musicnow.insert(0,entireText)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")

@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = musicnow[0] + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않네요.")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = musicnow[0]  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@bot.command()
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = musicnow[0]  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않네요..")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))

@bot.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(embed = discord.Embed(title = "재생목록 추가", description = result + "를 재생목록에 추가했어요!", color = 0x00ff00))

@bot.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어 삭제할 수 없어요!")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다!")
            else:
                await ctx.send("숫자를 입력해주세요!")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@bot.command()
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록이 정상적으로 초기화되었습니다. 이제 노래를 등록해볼까요?""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")

@bot.command()
async def 목록재생(ctx):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있어요!")


# 장난감=============================================================================================


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