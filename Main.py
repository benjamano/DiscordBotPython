import discord
import random
import datetime
import youtube_dl

from itertools import cycle
from discord.ext import commands, tasks

# ^ importing all needed libraries

token = 'nul'

client = commands.Bot(command_prefix = 'oioi ') # Sets the command prefix to the string 'oioi'

status = cycle(['Back from the dead!','Prefix = oioi',"willywillywillywillywilly"])

players = {}

date_of_today = datetime.date.today()




@client.event
async def on_ready():
    print(f'Ping: {round(client.latency * 1000)}ms')
    change_status.start()
    #await client.change_presence(activity=discord.Game(name='Back from the dead!')) # When the bot is started, the status 'Back from the dead!' displays on it's status NOTE: The task names 'change status' now automates this, changing the status every 10 seconds
    print('Logged on as {0}!'.format(client.user)) # States the name and ID of the Client/Bot as it is first initialized 

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))




@client.command()
async def credits(ctx):
    embed = discord.Embed(
        title = 'Credits',
        description = 'Coded by Ben Mercer',
        colour = discord.Colour.blue()
    )
    embed.set_footer(text = 'Thats literally just it')

    await ctx.send(embed=embed)



@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
async def foo(ctx, arg):
    print('Triggered foo')
    await ctx.send(arg)


@client.command(aliases=['8ball','test'])
async def _8ball(ctx, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command(aliases=['ratemywilly'])
async def _willyrate(ctx):
    responses = ["Its 12 inches long",
                "Gigantic.",
                "[Insert girlfriend name here] is very very lucky",
                "Taller than the empire state building",
                "The size of my pinky toe",
                "So so so small",
                "I feel sorry for your girlfriend, its the smallest penis ever",
                "The size of a peanut",
                "You may aswell just chop it off.",
                "It's 5000 inches long!",
                "It's 0.5 inches long."]
    await ctx.send(f'{random.choice(responses)}')
    #^ This picks and random statement to send as a response

#To use this command, in discord type: "oioi dm [user's @] [message]" e.g. "oioi dm @benjamano hello"
@client.command(aliases=['dm'])
async def DM(ctx, user : discord.User, *, msg):
    try:
        await user.send(msg)
        await ctx.send(f':white_check_mark: Your Message has been sent')
        print(msg, "sent to", user,)
    except:
        await ctx.send(':x: Member had their DMs closed, message not sent')




#The code that is commented out are my attempts at allowing it to connect it to a voicechannel and allow it to play music, no luck so far!

#@client.command(pass_context=True)
#async def join(ctx):
    #channel = ctx.message.author.voice.voice_channel
    #await client.join_voice_channel(channel)


#@client.command(pass_context=True)
#async def play(ctx,url):
    #guild = ctx.message.guild
    #voice_client = voice.client
    #player = await voice_client.create_ytdl_player(url)
    #players[server.id] = player
    #player.start()
    

client.run('NzIyODU5MTI4NTQ3OTY3MTAw.G9kisn.FcW3Mnh-OVsD280CSfb0tVF1gy1B51oFqJXL14') # <----- Enter your Bot Token code here (Found in Discord Developer Portal)