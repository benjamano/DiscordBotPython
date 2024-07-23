import discord
import random
import datetime
import discord.context_managers
from itertools import cycle
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from mctools import RCONClient, QUERYClient 
import csv
import re

with open("clientkey.txt", "r") as f:
    key = f.readline().strip('\n')
    code = f.readline()
    fileServerIP = f.readline()
    localConnection = f.readline().strip('\n')
    
    f.close()
    
ServerIP = fileServerIP
PORT = 25575
    
token = 'nul'

intents = discord.Intents.all()

client = commands.Bot(command_prefix = 'oioi ', intents = discord.Intents.all(), help_command=None, case_insensitive = True) # Sets the command prefix to the string 'oioi'

allowed_mentions = discord.AllowedMentions(everyone = True)

statuses = cycle(['Back from the dead!','Prefix = oioi',])

date_of_today = datetime.date.today()

RandStuffGeneralID = 731620307659390987
TestServerID = 1001555036976971856

Version = "2.2.9"

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

print(f"Version {Version}\n")


#slash = client.create_group("credits")


@client.event
async def on_ready():
    
    global ServerConn, rcon, qry
    
    ServerConn = False
    
    print(f'\nPing: {round(client.latency * 1000)}ms')
    
    change_status.start()
        
    print("-" * 120)
    print(f'\nLogged in as {client.user}')
    
    try:
        synced = await client.tree.sync()
        
        print(f"\nSynced {len(synced)} command(s)\n")
    
    except Exception as e:
        print(e)
        
    print("-" * 120)
    
    #await client.change_presence(activity=discord.Game(name='Back from the dead!')) # When the bot is started, the status 'Back from the dead!' displays on it's status NOTE: The task names 'change status' now automates this, changing the status every 10 seconds
    
    tries = 0
    
    channel = client.get_channel(TestServerID)
    if channel:
        await channel.send(f" Succesfully Started @ {datetime.datetime.now()} \n {Version} ")
        
    while ServerConn == False:
        try:
            if localConnection == 'True':
                #print(f"Attempting to connect to server at IP {ServerIP}:{PORT}")
            
                rcon = RCONClient('127.0.0.1', port=25575)
                qry = QUERYClient(host='127.0.0.1', port=25565)
                
                if rcon.login('1552'):
                    print("RCON Login Successful!")
                    
                    response = rcon.command('say Crazy Neil is watching....')
                    
                    #print(f"Response: {response}")
                    
                    ServerConn = True
                
                else:
                    raise Exception("Server Connection Failed")
    
        except Exception as e:
            
            tries += 1
            
            if tries > 10:
                print(f"Couldn't connect to server after 10 tries. Waiting for 30 Minutes. ({e})")
                await asyncio.sleep(1800)
            
            elif tries > 4:
                print(f"Couldn't connect to server after 5 tries. Waiting for 5 Minutes. ({e})")
                await asyncio.sleep(300)
            
            else:
                print(f"Couldn't connect to server, probably starting, waiting for 1 minute. ({e})\nTries: ", tries)  
                await asyncio.sleep(60)
            
            print(f"Tries: {tries}\n")
    
    print("-" * 120)
    
    with open("hours.csv", mode="r") as csvf:
        csvReader = csv.DictReader(csvf, ["username", "minutesplayed"])
        
        lineCount = 0
        
        for row in csvReader:
            if lineCount == 0:
                print(f"Column names detected: {" | ".join(row)}")
                lineCount += 1
                
            else:
            
                print(f"\n{row["username"]} has {row["minutesplayed"]} minutes played.")
            lineCount += 1
            
        csvf.close()
    
    print("-" * 120)
    
    try:
        
        print("Attempting to start tasks")
        
        checkPlaytime.start()
            
        resetPlaytime.start()
            
    except Exception as e:
        print("Failed to run a task:", e)
        
    print("-" * 120)


def checkPlaytimeCSV(username):
    shame = False
    
    with open("hours.csv", mode="r") as csvf:
        csvReader = csv.DictReader(csvf)
        
        print("Searching for playtime of user:", username)
        
        for row in csvReader:
            if row['username'] == username:
                playerPlaytime = int(row['minutesplayed'])
                print(f"Found {username} with {playerPlaytime} minutes played")
                break
    
    if playerPlaytime == 360 or playerPlaytime == 420 or playerPlaytime == 480 or playerPlaytime == 540:
        shame = True
    
    print("-" * 120)
    
    return playerPlaytime, shame


#------------------------------------------------------| Task Loops |------------------------------------------------------#


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(statuses)))
    

def updatePlaytime(username, additionalMinutes, reset = False):
    
    print(f"Updating {username}'s playtime by {additionalMinutes} minutes")
    
    with open("hours.csv", mode="r") as csvf:
        csvReader = csv.DictReader(csvf)
        
        data = list(csvReader)

    for row in data:   
        if row['username'] == username and reset == True:
            row['minutesplayed'] = str(0)
            print(f"\nReset {username}'s minutes.")
        
        elif str(username) in str(row["username"]) and reset == False:
            row['minutesplayed'] = str(int(row['minutesplayed']) + additionalMinutes)
            print(f"\nIncreased {username}'s minutes played by {additionalMinutes}\n\tNew Minutes: {row['minutesplayed']} ({(int(row['minutesplayed']))/60} Hours)\n")
    
    with open("hours.csv", mode="w", newline='') as csvf:
        fieldnames = ['username', 'minutesplayed']
        
        csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
        
        csvWriter.writeheader()
        csvWriter.writerows(data)


@tasks.loop(seconds=600)
async def checkPlaytime():
    try:
        qry.start()

        stats = qry.get_full_stats()
        
        if 'players' in stats:
            playerList = stats['players']

        qry.stop()
        
        if len(playerList) > 0:
        
            for player in playerList:

                if ".mattcur" in player:
                    
                    updatePlaytime(".mattcur", 10)
                    
                    result = checkPlaytimeCSV(".mattcur")

                    if result[1]:
                        channel = client.get_channel(RandStuffGeneralID)
                        
                        user = client.get_user(707634111627395222)
                        
                        await channel.send(content=f"{user.mention} has been playing Minecraft for {round(result[0] / 60)} hours, please tell them to touch some grass", allowed_mentions=discord.AllowedMentions(users=True))
                
                elif "Jedi_Maxster" in player:
                    
                    updatePlaytime("Jedi_Maxster", 10)
                    
                    result = checkPlaytimeCSV("Jedi_Maxster")
                     
                    if result[1]:
                        channel = client.get_channel(RandStuffGeneralID)
                        
                        user = client.get_user(643840086114435082)
                        
                        await channel.send(content=f"{user.mention} has been playing Minecraft for {round(result[0] / 60)} hours, please tell them to touch some grass", allowed_mentions=discord.AllowedMentions(users=True))
                
                elif "shortoctopus" in player:
                    
                    updatePlaytime("shortoctopus", 10)
                    
                    result = checkPlaytimeCSV("shortoctopus")
                     
                    if result[1]:
                        channel = client.get_channel(RandStuffGeneralID)
                        
                        user = client.get_user(499289163342938112)
                        
                        await channel.send(content=f"{user.mention} has been playing Minecraft for {round(result[0] / 60)} hours, please tell them to touch some grass", allowed_mentions=discord.AllowedMentions(users=True))
                        
                elif "Rugged_Base" in player:
                    
                    updatePlaytime("Rugged_Base", 10)
                    
                    result = checkPlaytimeCSV("Rugged_Base")
                     
                    if result[1]:
                        channel = client.get_channel(RandStuffGeneralID)
                        
                        user = client.get_user(496388477361979402)
                        
                        await channel.send(content=f"{user.mention} has been playing Minecraft for {round(result[0] / 60)} hours, please tell them to touch some grass", allowed_mentions=discord.AllowedMentions(users=True))
                
                elif "Benjamano" in player:
                    
                    updatePlaytime("Benjamano", 10)
                    
                    result = checkPlaytimeCSV("Benjamano")
                     
                    if result[1]:
                        channel = client.get_channel(RandStuffGeneralID)
                        
                        user = client.get_user(321317643099439104)
                        
                        await channel.send(content=f"{user.mention} has been playing Minecraft for {round(result[0] / 60)} hours, please tell them to touch some grass", allowed_mentions=discord.AllowedMentions(users=True))
        else:
            print("No players to update")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
@tasks.loop(time=datetime.time(hour=0, minute=0))
async def resetPlaytime():
    updatePlaytime(".mattcur", 0, reset=True)
    


#------------------------------------------------------| Commands |------------------------------------------------------#


    
@client.tree.command(name="playersonline")
async def playersonline(interaction: discord.Interaction):
    if ServerConn == False:
        embed = discord.Embed(
            
            title = "No Connection",
            description = f"Connection to server is unavailable, please try again later.",
            colour = discord.Colour.red()
        )
        
        embed.set_footer(text = 'Crazy Neil is running - but there is a problem with the connection to the Minecraft Server')
        
        await interaction.response.send_message(embed=embed,ephemeral=False)
    
    else:
        try:
            qry.start()

            stats = qry.get_full_stats()
            
            if 'players' in stats:
                playerList = stats['players']

            qry.stop()
            
            PlayersOn = ""
            
            if len(playerList) > 0:
                for player in playerList:
                    PlayersOn += f"- {player.strip("[0m")}\n"
                    
            else:
                PlayersOn = "No players online"
            
            qry.stop()
            
            embed = discord.Embed(
                title="Players Online",
                description=f"Players Online:\n{PlayersOn}",
                colour=discord.Colour.green()
            )
            
            await interaction.response.send_message(embed=embed,ephemeral=False)
        
        except Exception as e:
            print(f"Error running Players online command: {e}")
            embed = discord.Embed(
                title="Error",
                description="An error occurred while trying to retrieve the list of players.",
                colour=discord.Colour.red()
            )
            await interaction.response.send_message(embed=embed,ephemeral=False)


@client.tree.command(name="totalplaytime")
async def totalplaytime(interaction: discord.Interaction):
    with open("hours.csv", mode="r") as csvf:
        csvReader = csv.DictReader(csvf)
        
        data = list(csvReader)
        
        playTime = ""
        
        for row in data:
            playTime += str(f"- {row['username']} has played for {round(int(row['minutesplayed'])/60)} hours ({row['minutesplayed']} minutes)\n")
        
        embed = discord.Embed(
            title = "Total Playtime for each player today",
            description = f"Playtime today: \n{playTime}",
            colour = discord.Colour.green()
        )
        
        csvf.close()
        
        await interaction.response.send_message(embed=embed,ephemeral=False)
        
        
@client.command(description="Displays the credits")
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
# @client.command(aliases=['dm'])
# async def DM(ctx, user : discord.User, *, msg):
#     try:
#         await user.send(msg)
        
#         await ctx.send(f':white_check_mark: Your Message has been sent')
        
#         print(msg, "sent to", user,)
#     except:
#         await ctx.send(':x: Member had their DMs closed, message not sent')




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
