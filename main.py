# -*- coding: utf-8 -*-

#  MODULES / LIBRARIES  ##############################################################################################

from asyncore import read
from email.iterators import body_line_iterator
import discord
from discord.ext import commands
import re
from datetime import datetime


#  SETTING UP  #######################################################################################################

bot = commands.Bot(command_prefix=('гб!', 'гборд!', 'гуглборд!', 'gb!', 'gboard!', 'googleboard!'),intents=discord.Intents.all())
bot.remove_command( 'help' )

with open('token.txt', encoding='utf-8') as f:
    token = f.readline()


#  BOT EVENTS  #######################################################################################################

@bot.event
async def on_ready():
    print("Successfuly logged in as GBoard Bot!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed123= discord.Embed( title="Кажется, вы ввели **не всю команду**.", description=f'_Чтобы узнать больше о командах, введите **гб!хелп**_\n_Ошибка (для разработчиков):_ `{error}`', color=discord.Color.red() )
        embed123.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
        embed123.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send(embed = embed123)

    elif isinstance(error, commands.CommandNotFound):
        embed123= discord.Embed( title="Кажется, **такой команды нет**.", description=f'_Чтобы узнать больше о командах, введите **гб!хелп**_\n_Ошибка (для разработчиков):_ `{error}`',  color=discord.Color.red() )
        embed123.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
        embed123.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send(embed = embed123)

    else:
        embed123= discord.Embed( title="**Ошибка!**", description=f'`{error}`',  color=discord.Color.red() )
        embed123.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
        embed123.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send(embed = embed123)


#  BOT COMMANDS  #####################################################################################################

@bot.command(aliases=['хелп', 'help', 'помощь'])
async def _help(ctx):
    embed = discord.Embed( title = '**Помощь:**', description=":point_down: Смотри ниже :point_down:", color=discord.Color.green())
    await ctx.reply(embed = embed)
    embed = discord.Embed( title = '**Префиксы:**', description="`гб!`, `гборд!`, `гуглборд!`, `gb!`, `gboard!`, `googleboard!`", color=discord.Color.green())
    await ctx.send(embed = embed)
    embed = discord.Embed( title = '**Команды:**', description="`хелп`/`помощь`/`help` - Показывает помощь\n\n`закрепить <текст фрагмента>`/`закреп <текст фрагмента>`/`pin <текст фрагмента>` - Закрепляет фрагмент с указанным текстом\n`открепить <номер фрагмента>`/`откреп <номер фрагмента>`/`unpin <номер фрагмента>` - Открепляет фрагмент под указанным номером\n`показать`/`фрагм`/`показатьфрагменты`/`show`/`showpins` - Показывает все закреплённые фрагменты\n\n`отправить <текст сообщения>`/`отправитьсообщение <текст сообщения>`/`отпр <текст сообщения>`/`send <текст сообщения>`/`sendmessage <текст сообщения>` - Отправляет сообщение от имени бота\n`анонотправить <текст сообщения>`/`анонотправитьсообщение <текст сообщения>`/`анонотпр <текст сообщения>`/`anonsend <текст сообщения>`/`anonsendmessage <текст сообщения>` - Отправляет сообщение от имени бота без указания вашего ника\n`сообщения <кол-во (необязательно)>`/`чат <кол-во (необязательно)>`/`messages <кол-во (необязательно)>`/`chat <кол-во (необязательно)>` - Показывает недавно отправленные сообщения\n`сообщение <номер сообщения>`/`показатьсообщение <номер сообщения>`/`сообщ <номер сообщения>`/`message <номер сообщения>`/`showmessage <номер сообщения>`/`msg <номер сообщения>` - Показывает информацию о выбранном сообщении", color=discord.Color.green())
    await ctx.send(embed = embed)
    embed = discord.Embed(title = '**Информация:**', description = '**Сайт:** https://sites.google.com/view/gboard-bot/main\n**Исходный код:** https://github.com/moontr3/gboard_bot\n**Создатель:** @moontr3',color=discord.Color.green())
    embed.set_author( name = "Бот: " + bot.user.name, icon_url = bot.user.avatar_url )
    embed.set_footer( text = "Запросил: " + ctx.author.name, icon_url = ctx.author.avatar_url )
    await ctx.send(embed = embed)


@bot.command(aliases=['pin', 'закрепить', 'закреп'])
async def _pin(ctx, *, text=None):
    with open('pins.txt', encoding='utf-8') as f:
        count = sum(1 for _ in f) + 1

    lineerr = False
    x=0
    with open('pins.txt', encoding='utf-8') as f:
        line = f.readlines()
        for i in range(count):
            try:
                if line[x] == text+"\n":
                    lineerr = True
                    break
                x += 1
            except:
                break

    if text == None:
        embed = discord.Embed( title = '**Фрагмент** не может быть закреплён.', description=f'Вы не ввели текст фрагмента для закрепления.\n_Эта команда работает так: **гб!закрепить <текст фрагмента>**_', color=discord.Color.red())
    elif "\n" in text:
        embed = discord.Embed( title = '**Фрагмент** не может быть закреплён.', description=f'Фрагмент может содержать только одну строку текста (не может быть мультистрочным).\n_Эта команда работает так: **гб!закрепить <текст фрагмента>**_', color=discord.Color.red())
    elif lineerr == True:
        embed = discord.Embed( title = '**Фрагмент** не может быть закреплён.', description=f'Фрагмент с таким текстом уже сужествует (номер фрагмента: `{x+1}`).\n_Эта команда работает так: **гб!закрепить <текст фрагмента>**_', color=discord.Color.red())
    else:
        with open('pins.txt', "a", encoding="utf-8") as f:
            f.write(str(text)+"\n")
        embed = discord.Embed( title = '**Фрагмент** закреплён!', description=f'Текст фрагмента (`{text}`) закреплён под номером `{count}`.\n_Чтобы удалить фрагмент, введите команду **гб!открепить <номер фрагмента>**_', color=discord.Color.green())
    embed.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
    embed.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    await ctx.reply(embed = embed)

@bot.command(aliases=['unpin', 'открепить', 'откреп'])
async def _unpin(ctx, number=None):
    with open('pins.txt', encoding='utf-8') as f:
        count = sum(1 for _ in f)

    if int(number) <= count and int(number) >= 1:
        x = ''
        with open('pins.txt', encoding='utf-8') as f:
            lines = f.readlines()

        with open('pins.txt', encoding='utf-8') as f:
            for i in range(int(number)):
                x = f.readline()

        pattern = re.compile(re.escape(x))

        with open('pins.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                result = pattern.search(line)
                if result is None:
                    f.write(line)

        x = x.rstrip("\n")

        if number == None:
            embed = discord.Embed( title = '**Фрагмент** не может быть откреплён.', description=f'Вы не ввели номер фрагмента для удаления.\n_Эта команда работает так: **гб!открепить <номер фрагмента>**_', color=discord.Color.red())
        else:
            embed = discord.Embed( title = '**Фрагмент** откреплён!', description=f'Номер фрагмента `{number}` (`{x}`) откреплён.\n_Чтобы закрепить фрагмент, введите команду **гб!закрепить <текст фрагмента>**_', color=discord.Color.green())
    else:
        embed = discord.Embed( title = '**Фрагмент** не может быть откреплён.', description=f'Номер фрагмента некорректный (всего фрагментов: `{count}`, указанный фрагмент: `{number}`).\n_Эта команда работает так: **гб!открепить <номер фрагмента>**_', color=discord.Color.red())
    embed.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
    embed.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    await ctx.reply(embed = embed)

@bot.command(aliases=['show', 'показать', 'showpins', 'показатьфрагменты', 'фрагм'])
async def _show(ctx):
    with open('pins.txt', encoding='utf-8') as f:
        count = sum(1 for _ in f)
    n=1
    x=""
    with open('pins.txt', 'r', encoding='utf-8') as f:
        for i in range(int(count)):
            x += f"`#{n}` "+f.readline() 
            n+=1
    if count != 0:
        embed = discord.Embed( title = '**Закреплённые фрагменты:**', description=x, color=discord.Color.green())
    else:
        embed = discord.Embed( title = '**Закреплённые фрагменты:**', description="_Закреплённых фрагментов нету!_\n_Чтобы узнать больше, введите **гб!хелп**_", color=discord.Color.green())
    embed.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
    embed.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    await ctx.reply(embed = embed)

@bot.command(aliases=['отправить', 'отправитьсообщение', 'send', 'sendmessage', 'отпр'])
async def _send(ctx, *, msg):
    datenow = str(datetime.today().date())
    listdate = datenow.split("-")
    dateready = f"{listdate[2]}.{listdate[1]}.{listdate[0]}"
    timenow = str(datetime.today().time())
    listtime = timenow.split(".")
    timeready = listtime[0]

    await ctx.message.delete()
    if "\n" in msg:
        embed = discord.Embed( title = '**Сообщение не отправлено**', description=f"Сообщение может содержать только одну строку текста (не может быть мультистрочным).\n\n_Чтобы просмотреть историю сообщений, введите **гб!сообщения**_", color=discord.Color.red())
    else:
        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(f"**{ctx.author.name}** _({dateready}, {timeready})_ : {msg}\n")
        embed = discord.Embed( title = '**Сообщение отправлено**', description=f"{msg}\n_Чтобы просмотреть историю сообщений, введите **гб!сообщения**_", color=discord.Color.green())
    embed.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
    embed.set_footer( text = "Отправитель: "+ctx.author.name, icon_url = ctx.author.avatar_url )
    await ctx.send(embed = embed)  

@bot.command(aliases=['анонотправить', 'анонотправитьсообщение', 'anonsend', 'anonsendmessage', 'анонотпр'])
async def _anonsend(ctx, *, msg):
    datenow = str(datetime.today().date())
    listdate = datenow.split("-")
    dateready = f"{listdate[2]}.{listdate[1]}.{listdate[0]}"
    timenow = str(datetime.today().time())
    listtime = timenow.split(".")
    timeready = listtime[0]

    await ctx.message.delete()
    if "\n" in msg:
        embed = discord.Embed( title = '**Анонимное сообщение не отправлено**', description=f"Сообщение может содержать только одну строку текста (не может быть мультистрочным).\n\n_Чтобы просмотреть историю сообщений, введите **гб!сообщения**_", color=discord.Color.red())
    else:
        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(f"**Аноним** _({dateready}, {timeready})_ : {msg}\n")
        embed = discord.Embed( title = '**Анонимное сообщение отправлено**', description=f"{msg}\n\n_Чтобы просмотреть историю сообщений, введите **гб!сообщения**_", color=discord.Color.green())
    embed.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
    embed.set_footer( text = "Анонимное сообщение")
    await ctx.send(embed = embed)  

@bot.command(aliases=['сообщения', 'messages', 'чат', 'chat'])
async def _msghistory(ctx, dur = 15):
    ready = ''
    with open('messages.txt', encoding='utf-8') as f:
        count = sum(1 for _ in f)
    x = count-int(dur)
    with open('messages.txt', encoding='utf-8') as f:
        line = f.readlines()
        if int(dur) <= count:
            for i in range(int(dur)):
                ready += f"`#{x}` "+line[x]
                x+=1
        else:
            ready = f"Не удалось загрузить все сообщения (всего сообщений: {count-1})."
    embed = discord.Embed( title = f'**Сводка сообщений** (последние {dur})', description=f"{ready}\n\n_Чтобы отправить сообщение, введите **гб!отправить <текст сообщения>**_", color=discord.Color.green())
    embed.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
    embed.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)  

@bot.command(aliases=['сообщение', 'message', 'показатьсообщение', 'showmessage', 'сообщ', 'msg'])
async def _showmsg(ctx, dur):
    ready = ''
    with open('messages.txt', encoding='utf-8') as f:
        count = sum(1 for _ in f)-1
    with open('messages.txt', encoding='utf-8') as f:
        line = f.readlines()
        if int(dur) <= count:
            ready += line[int(dur)]
        else:
            ready = f"Не удалось загрузить сообщение (всего сообщений: {count})."
    embed = discord.Embed( title = f'**Сообщение {dur}**', description=f"{ready}\n\n_Чтобы отправить сообщение, введите **гб!отправить <текст сообщения>**_", color=discord.Color.green())
    embed.set_author( name = bot.user.name, icon_url = bot.user.avatar_url )
    embed.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)  


#  BOT INITIALIZATION  ###############################################################################################

bot.run(token)


###########################################
#                                         #
#       This bot made by @moontr3         #
#  https://github.com/moontr3/gboard_bot  #
#                                         #
#    You CANNOT replace or remove this    #
#    text if you want to use this bot     #
#     if you didn't change the code!      #
#                                         #
###########################################