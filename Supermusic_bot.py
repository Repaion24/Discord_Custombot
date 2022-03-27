from unittest import result
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
client = discord.Client()

load_dotenv()
token = os.getenv("TOKEN")
link = os.getenv("LINK")

user = []       #유저가 입력한 노래 정보
musictitle = [] #가공된 노래의 정보 제목
song_queue = [] #가공된 정보의 노래 링크 큐
musicnow = []   #현재 출력중인 노래
userF = []      #유저 정보 저장 배열
userFlist = []  #유저 개인 노래 저장 배열
allplaylist = []    #플레이리스트 배열





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
    else:
        if not vc.is_playing():
            client.loop.create_task(vc.disconnect())



#접속 =================================================================

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("이병 슈퍼봇 근무"))

#봇 event 함수들 =================================================================

@bot.command()
async def 도움말(ctx):
    await ctx.send(embed = discord.Embed(title='도움말',description="""
\n!도움말 -> 뮤직봇의 모든 명령어를 볼 수 있습니다.
\n!야 -> 뮤직봇을 자신이 속한 채널로 부릅니다.
\n!나가 -> 뮤직봇을 자신이 속한 채널에서 내보냅니다.
\n!재생 [노래이름] -> 뮤직봇이 노래를 검색해 틀어줍니다. 만약 노래가 이미 재생중이라면, 대기열에 추가합니다
\n!노래끄기 -> 현재 재생중인 노래를 끕니다.
!일시정지 -> 현재 재생중인 노래를 일시정지시킵니다.
!다시재생 -> 일시정지시킨 노래를 다시 재생합니다.
\n!지금노래 -> 지금 재생되고 있는 노래의 제목을 알려줍니다.
\n!목록 -> 이어서 재생할 노래목록을 보여줍니다.
!목록재생 -> 목록에 추가된 노래를 재생합니다.
!목록초기화 -> 목록에 추가된 모든 노래를 지웁니다.
\n!목록추가 [노래] -> 노래를 대기열에 추가합니다.
!목록삭제 [숫자] -> 대기열에서 입력한 숫자에 해당하는 노래를 지웁니다.""", color = 0x536349))

#봇 event 함수들 =================================================================

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
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send("이병 슈퍼봇! 부르셨습니까!")
    except:
        try:
            await vc.mode_to(ctx.message.author.voice.channel)
        except:
            print('문제없음')

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
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x536349))
        vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send(embed = discord.Embed(title = "재생목록 추가", description = result + "를 재생목록에 추가했어요!", color = 0x536349))
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
        await ctx.send(embed = discord.Embed(title= "목록", description = Text.strip(), color = 0x536349))





@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = musicnow[0] + "을(를) 일시정지 했습니다.", color = 0x536349))
    else:
        await ctx.send("지금 재생중인 노래가 없습니다.")

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("지금 재생중인 노래가 없습니다.")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = musicnow[0]  + "을(를) 다시 재생했습니다.", color = 0x536349))

@bot.command()
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = musicnow[0]  + "을(를) 종료했습니다.", color = 0x536349))
    else:
        await ctx.send("지금 재생중인 노래가 없습니다.")

@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금 재생중인 노래가 없습니다.")
    else:
        await ctx.send(embed = discord.Embed(title = "재생중", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x536349))

@bot.command()
async def 목록추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(embed = discord.Embed(title = "재생목록 추가", description = result + "를 재생목록에 추가했어요!", color = 0x536349))
    global Text
    Text = ""
    for i in range(len(musictitle)):
        Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
    await ctx.send(embed = discord.Embed(title= "목록", description = Text.strip(), color = 0x536349))

@bot.command()
async def 목록삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "목록", description = Text.strip(), color = 0x536349))
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없습니다.")
        else:
            if len(list) < int(number):
                await ctx.send("숫자가 이상합니다.")
            else:
                await ctx.send("숫자를 입력해주세요.")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("목록이 비어있습니다.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "목록", description = Text.strip(), color = 0x536349))

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
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록이 정상적으로 초기화되었습니다.""", color = 0x536349))
    except:
        await ctx.send("목록이 비어있습니다.")

@bot.command()
async def 목록재생(ctx):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("목록이 비어있습니다.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생중입니다.")


#장난감=============================================================================================


@bot.command()
async def 뭐하냐(ctx):
    try:
        if(random.random() > 0.2):
            await ctx.send("죄송합니다!")
        else:
            await ctx.send("총이 더러워서 물로 씻고 있습니다!")
    except:
        await ctx.send("Error")

@bot.command()
async def 복무신조(ctx):
    try:
        if(random.random() > 0.2):
            await ctx.send("우리의 결의!")
        else:
            await ctx.send("죄송합니다! 아직 못 외웠습니다!")
    except:
        await ctx.send("Error")

@bot.command()
async def 아침뭐냐(ctx):
    try:
        if(random.random() > 0.2):
            await ctx.send("쇠미에 쏘야입니다!")
        else:
            await ctx.send("잘 모르겠습니다!")
    except:
        await ctx.send("Error")

@bot.command()
async def 점심뭐냐(ctx):
    try:
        if(random.random() > 0.2):
            await ctx.send("고순조입니다...")
        else:
            await ctx.send("저 오늘 안먹어서 모릅니다")
    except:
        await ctx.send("Error")

@bot.command()
async def 남은군생활(ctx):
    try:
        if(random.random() > 0.2):
            await ctx.send("489일 남았습니다")
        else:
            await ctx.send("그걸 왜 물어보십니까")
    except:
        await ctx.send("Error")

@bot.command()
async def 툭툭치기(ctx):
    try:
        if(random.random() > 0.2):
            await ctx.send("이병 슈퍼봇!")
        else:
            await ctx.send("예?")
    except:
        await ctx.send("Error")






#즐겨찾기 기능 코드, 24시간 돌리는거 아니면 무의미 - 개발중인 코드=============================================================================================

# @bot.command()
# async def 즐겨찾기(ctx):
#     global Ftext
#     Ftext = ""
#     correct = 0
#     global Flist
#     for i in range(len(userF)):
#         if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
#             correct = 1 #있으면 넘김
#     if correct == 0:
#         userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
#         userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듬.
#         userFlist[len(userFlist)-1].append(str(ctx.message.author.name))
        
#     for i in range(len(userFlist)):
#         if userFlist[i][0] == str(ctx.message.author.name):
#             if len(userFlist[i]) >= 2: # 노래가 있다면
#                 for j in range(1, len(userFlist[i])):
#                     Ftext = Ftext + "\n" + str(j) + ". " + str(userFlist[i][j])
#                 titlename = str(ctx.message.author.name) + "님의 즐겨찾기"
#                 embed = discord.Embed(title = titlename, description = Ftext.strip(), color = 0x536349)
#                 embed.add_field(name = "목록에 추가\U0001F4E5", value = "즐겨찾기에 모든 곡들을 목록에 추가합니다.", inline = False)
#                 embed.add_field(name = "플레이리스트로 추가\U0001F4DD", value = "즐겨찾기에 모든 곡들을 새로운 플레이리스트로 저장합니다.", inline = False)
#                 Flist = await ctx.send(embed = embed)
#                 await Flist.add_reaction("\U0001F4E5")
#                 await Flist.add_reaction("\U0001F4DD")
#             else:
#                 await ctx.send("아직 등록한 즐겨찾기가 없습니다.")


# @bot.command()
# async def 즐겨찾기추가(ctx, *, msg):
#     correct = 0
#     for i in range(len(userF)):
#         if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
#             correct = 1 #있으면 넘김
#     if correct == 0:
#         userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
#         userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듦.
#         userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

#     for i in range(len(userFlist)):
#         if userFlist[i][0] == str(ctx.message.author.name):
            
#             options = webdriver.ChromeOptions()
#             options.add_argument("headless")

#             chromedriver_dir = link
#             driver = webdriver.Chrome(chromedriver_dir, options = options)
#             driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
#             source = driver.page_source
#             bs = bs4.BeautifulSoup(source, 'lxml')
#             entire = bs.find_all('a', {'id': 'video-title'})
#             entireNum = entire[0]
#             music = entireNum.text.strip()

#             driver.quit()

#             userFlist[i].append(music)
#             await ctx.send(music + "(이)가 정상적으로 등록되었습니다.")



# @bot.command()
# async def 즐겨찾기삭제(ctx, *, number):
#     correct = 0
#     for i in range(len(userF)):
#         if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
#             correct = 1 #있으면 넘김
#     if correct == 0:
#         userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
#         userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듦.
#         userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

#     for i in range(len(userFlist)):
#         if userFlist[i][0] == str(ctx.message.author.name):
#             if len(userFlist[i]) >= 2: # 노래가 있다면
#                 try:
#                     del userFlist[i][int(number)]
#                     await ctx.send("정상적으로 삭제되었습니다.")
#                 except:
#                      await ctx.send("입력한 숫자가 잘못되었습니다.")
#             else:
#                 await ctx.send("즐겨찾기에 노래가 없습니다.")

# @bot.event
# async def on_reaction_add(reaction, users):
#     if users.bot == 1:
#         pass
#     else:
#         try:
#             await Flist.delete()
#         except:
#             pass
#         else:
#             if str(reaction.emoji) == '\U0001F4E5':
#                 await reaction.message.channel.send("잠시만 기다려주세요. (오래걸림)")
#                 print(users.name)
#                 for i in range(len(userFlist)):
#                     if userFlist[i][0] == str(users.name):
#                         for j in range(1, len(userFlist[i])):
#                             try:
#                                 driver.close()
#                             except:
#                                 print("NOT CLOSED")

#                             user.append(userFlist[i][j])
#                             result, URLTEST = title(userFlist[i][j])
#                             song_queue.append(URLTEST)
#                             await reaction.message.channel.send(userFlist[i][j] + "를 재생목록에 추가했습니다.")
#             elif str(reaction.emoji) == '\U0001F4DD':
#                 await reaction.message.channel.send("-미구현 기능입니다-")


##코드================================================================
bot.run(token)


##개발중인코드=================================================================


# @bot.command()
# async def 목록셔플(ctx):
#     try:
#         global musicnow, user, musictitle,song_queue
#         numbershuffle = len(musicnow) - len(user)
#         for i in range(numbershuffle):
#             shuffles.append(musicnow[0])
#             del musicnow[0]
#         combine = list(zip(user, musicnow, musictitle, song_queue))
#         random.shuffle(combine)
#         a, b, c, d = list(zip(*combine))

#         user = list(a)
#         musicnow = list(b)
#         musictitle = list(c)
#         song_queue = list(d)

#         for i in range(numbershuffle):
#             musicnow.insert(0, shuffles[i])

#         del shuffles[:]
#         await ctx.send("목록이 정상적으로 셔플되었습니다.")
#     except:
#         await ctx.send("셔플할 목록이 없습니다!")



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