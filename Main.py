import discord
import random
import datetime
import discord.context_managers
from mcstatus import JavaServer as MC
from itertools import cycle
from discord.ext import commands, tasks
from discord import app_commands
from discord import Colour as c 
import asyncio
from mctools import RCONClient 

with open("clientkey.txt", "r") as f:
    key = f.readline()

HOST = '192.168.1.41'
PORT = 25575

RCONConnection = False

rcon = RCONClient(HOST, port=PORT)

if rcon.login("1552"):
    
    RCONConnection = True
    
token = 'nul'

intents = discord.Intents.all()

client = commands.Bot(command_prefix = 'oioi ', intents = discord.Intents.all(), help_command=None, case_insensitive = False) # Sets the command prefix to the string 'oioi'

allowed_mentions = discord.AllowedMentions(everyone = True)

statuses = cycle(['Back from the dead!','Prefix = oioi',])

players = {}
playerPlaytime = {
    ".mattcur" : 0,
}

date_of_today = datetime.date.today()

RandStuffGeneralID = 731620307659390987
TestServerID = 1001555036976971856


print("""
██████╗░███████╗███╗░░██╗███╗░░░███╗███████╗██████╗░░█████╗░███████╗██████╗░
██╔══██╗██╔════╝████╗░██║████╗░████║██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╦╝█████╗░░██╔██╗██║██╔████╔██║█████╗░░██████╔╝██║░░╚═╝█████╗░░██████╔╝
██╔══██╗██╔══╝░░██║╚████║██║╚██╔╝██║██╔══╝░░██╔══██╗██║░░██╗██╔══╝░░██╔══██╗
██████╦╝███████╗██║░╚███║██║░╚═╝░██║███████╗██║░░██║╚█████╔╝███████╗██║░░██║
╚═════╝░╚══════╝╚═╝░░╚══╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝╚═╝░░╚═╝""")

print("""
░█████╗░██████╗░░█████╗░███████╗██╗░░░██╗███╗░░██╗███████╗██╗██╗░░░░░  ██████╗░░░░░█████╗░
██╔══██╗██╔══██╗██╔══██╗╚════██║╚██╗░██╔╝████╗░██║██╔════╝██║██║░░░░░  ╚════██╗░░░██╔══██╗
██║░░╚═╝██████╔╝███████║░░███╔═╝░╚████╔╝░██╔██╗██║█████╗░░██║██║░░░░░  ░░███╔═╝░░░██║░░██║
██║░░██╗██╔══██╗██╔══██║██╔══╝░░░░╚██╔╝░░██║╚████║██╔══╝░░██║██║░░░░░  ██╔══╝░░░░░██║░░██║
╚█████╔╝██║░░██║██║░░██║███████╗░░░██║░░░██║░╚███║███████╗██║███████╗  ███████╗██╗╚█████╔╝
░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░░╚══╝╚══════╝╚═╝╚══════╝  ╚══════╝╚═╝░╚════╝░""")

print("Version 2.0.2")


#slash = client.create_group("credits")


@client.event
async def on_ready():
    
    global status, server
    
    ServerConn = False
    
    print(f'\nPing: {round(client.latency * 1000)}ms')
    
    change_status.start()
    
    tries = 0
    
    while ServerConn == False:
        
        if tries > 4:
            print("Cannot connect to server after 5 Tries. Stopping.")
            raise ConnectionRefusedError
        
        try:
            server = MC.lookup("192.168.1.41")
            status = server.status()
            
            if status:
                ServerConn = True
        
        except:
            print("Couldn't connect to server, probably starting, waiting.")
            await asyncio.sleep(60)
            
    resp = rcon.command("broadcast Hello RCON!")

    print(f'\n\nLogged in as {client.user}')
    
    try:
        if not checkPlaytime.is_running():
            checkPlaytime.start()
            
        if not resetPlaytime.is_running():
            resetPlaytime.start()
            
    except:
        print("Failed to run a task")
    
    try:
        synced = await client.tree.sync()
        
        print(f"Synced {len(synced)} command(s)")
    
    except Exception as e:
        print(e)
    
    #await client.change_presence(activity=discord.Game(name='Back from the dead!')) # When the bot is started, the status 'Back from the dead!' displays on it's status NOTE: The task names 'change status' now automates this, changing the status every 10 seconds
    
    channel = client.get_channel(TestServerID)
    if channel:
        await channel.send(f" Succesfully Started @ {datetime.datetime.now()} \n Version 2.1.5")



#------------------------------------------------------| Task Loops |------------------------------------------------------#


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(statuses)))
    
    
@tasks.loop(seconds = 600)
async def checkPlaytime():
    TrackingPlayersOnline = []
    status = server.status()
    
    if status.players.sample != None:
        for player in status.players.sample:
            TrackingPlayersOnline.append(player.name)
        
        if ".mattcur" in TrackingPlayersOnline:
            playerPlaytime[".mattcur"] += 600
            
        if playerPlaytime[".mattcur"] > 18000:
            channel = client.get_channel(RandStuffGeneralID)
            
            user = client.get_user(707634111627395222)
            
            await channel.send(content = f"@everyone {user.mention} has been playing Minecraft for {round(playerPlaytime[".mattcur"]/60/60)} Hours, please tell him to touch some grass", allowed_mentions = allowed_mentions)
    
    else:
        print("No players online")
        
        
@tasks.loop(time=datetime.time(hour=0, minute=0))
async def resetPlaytime():
    playerPlaytime[".mattcur"] = 0
    
    print("Playtime has been reset")
    


#------------------------------------------------------| Commands |------------------------------------------------------#


    
@client.command()
async def PlayersOnline(ctx):
    try:
        PlayersOn = ""
        
        status = server.status()
        
        try:
            for player in status.players.sample:
                PlayersOn += str(f"- {player.name}\n")
        
        except:
            PlayersOn = "Nobody!"
            
        embed = discord.Embed(
            title = "Players Online",
            description = f"Players Online: \n{PlayersOn}",
            colour = discord.c.green()
        )
        
    except Exception as e:
        print(f"Error ruinning Players online commande: {e}")
        
    await ctx.send(embed=embed)


@client.command(description="Displays the credits")
async def credits(ctx):
    embed = discord.Embed(
        title = 'Credits',
        description = 'Coded by Ben Mercer',
        colour = discord.c.blue()
    )
    
    embed.set_footer(text = 'Thats literally just it')

    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.tree.command(name="foo")
async def foo(interaction: discord.Interaction):
    await interaction.response.send_message("foo",ephemeral=True)

#This command allows a user to ask a question to an 8ball and picks a random response.
@client.command(aliases=['8ball','test'])
async def _8ball(ctx):
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
    
    await ctx.send(f'{random.choice(responses)}')


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

@client.command(aliases=['howgayami'])
async def howgay(ctx):
    responses = ["Very",
                "Too Gay",
                "100%",
                "0%",
                "69%",
                "As gay as Elliot Pomroy",
                "Not gay at all",
                "James Charles 2.0",]
    
    await ctx.send(f'{random.choice(responses)}')

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
    

client.run(key) # <----- Enter your Bot Token code here (Found in Discord Developer Portal)
