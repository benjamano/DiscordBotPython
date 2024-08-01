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
import CommonFunctions.formatTools as q
import CommonFunctions.csvTools as s
import CommonFunctions.discordTools as d
import CommonFunctions.serverTools as r
import time

intents = discord.Intents.all()

client = commands.Bot(command_prefix = 'oioi ', intents = discord.Intents.all(), help_command=None, case_insensitive = True) # Sets the command prefix to the string 'oioi'

allowed_mentions = discord.AllowedMentions(everyone = True)

RandStuffGeneralID = 731620307659390987
TestServerID = 1001555036976971856

try:
    
    q.newline()

    with open("StoredData/clientkey.txt", "r") as f:
        q.sendLogMessage("Reading from file clientkey.txt")
        
        key = f.readline().strip('\n')
        code = f.readline()
        ServerIP = f.readline()
        PORT = int(f.readline())
        localConnection = f.readline().strip('\n')
        debugMode = f.readline().strip('\n')
        password = f.readline().strip('\n')
        
        f.close()
        
        q.sendLogMessage("Read from clientkey.txt successfully", type="Success")
    
    q.newline(baronly=True)
        
    with open("StoredData/version.txt", "r") as f:
        q.sendLogMessage("Reading from file version.txt")
        
        VersionNo = f.readline().strip('\n')
        Branch = f.readline().strip('\n')
        
        f.close()
        
        q.sendLogMessage("Read from version.txt successfully", type="Success")
        
    q.newline()

except Exception as e:
    q.sendLogMessage(f"Error reading from files: {e}", type="Error")


#------------------------------------------------------| On Ready |------------------------------------------------------#


@client.event
async def on_ready():
    
    global ServerConn, rcon, qry, ServerIP, PORT, VersionNo, Branch, key, statuses, disc, server
    
    disc = d.DiscordTools(client)
    
    if debugMode == True:
        statuses = cycle([f'Running in Debug mode on branch {Branch}',])
    else:
        statuses = cycle(['Back from the dead!','/help',])
        
    q.newline(withDivider=False)
    
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

    print(f"Version {VersionNo} ({Branch})\n")
        
    ServerConn = False
    
    q.newline()
    
    q.sendLogMessage(f'Ping: {round(client.latency * 1000)}ms')
    
    change_status.start()
        
    q.newline()
    
    q.newline(baronly=True)
    
    q.sendLogMessage(f'Logged in as {client.user}', type="Success")
    
    q.newline(baronly=True)
    
    try:
        synced = await client.tree.sync()
        
        q.sendLogMessage(f"Synced {len(synced)} command(s)", type="Success")
    
    except Exception as e:
        q.sendLogMessage(f"Error syncing command tree: {e}", type="Error")
        
    q.newline(baronly=True)
    
    q.newline()
    
    #await client.change_presence(activity=discord.Game(name='Back from the dead!')) # When the bot is started, the status 'Back from the dead!' displays on it's status NOTE: The task names 'change status' now automates this, changing the status every 10 seconds
    
    tries = 0
    
    embed = discord.Embed(
        title = "Bot Started",
        description = f"Bot has started successfully\nVersion: {VersionNo} ({Branch})",
        colour = discord.Colour.green()
    )
    
    await disc.sendMessage(ChannelID=TestServerID, embed=embed)
        
    while ServerConn == False:
        try:
            if localConnection == 'True':
                #print(f"Attempting to connect to server at IP {ServerIP}:{PORT}")
            
                rcon = RCONClient('127.0.0.1', port=25575)
                qry = QUERYClient(host='127.0.0.1', port=25565)
                
                if rcon.login('1552'):
                    q.sendLogMessage("RCON Login Successful!", type="Success")
                    
                    response = rcon.command('say Crazy Neil is watching....')
                    
                    #print(f"Response: {response}")
                    
                    server = r.ServerTools(rcon)
                    
                    ServerConn = True
                
                else:
                    raise Exception("Server Connection Failed")
            else:
                q.sendLogMessage("Bot is starting outside of the network, skipping RCON connection.", type="Warning")
                break
    
        except Exception as e:
            
            tries += 1
            
            if tries > 10:
                q.sendLogMessage(f"Couldn't connect to server after 10 tries. Waiting for 30 Minutes. ({e})", type="Error")
                await asyncio.sleep(1800)
            
            elif tries > 4:
                q.sendLogMessage(f"Couldn't connect to server after 5 tries. Waiting for 5 Minutes. ({e})", type="Warning")
                await asyncio.sleep(300)
            
            else:
                q.sendLogMessage(f"Couldn't connect to server, probably starting, waiting for 1 minute. ({e})", type="Warning")  
                await asyncio.sleep(60)
            
            q.sendLogMessage(f"Tries: {tries}")
            q.newline(baronly=True)
    
    q.newline()
    
    with open("StoredData/hours.csv", mode="r") as csvf:
        csvReader = csv.DictReader(csvf, ["username", "minutesplayed","discorduserid"])

        lineCount = 0
        
        for row in csvReader:
            if lineCount == 0:
                q.sendLogMessage(f"Column names detected: {" | ".join(row)}")
                
            else:
                q.sendLogMessage(f"{row["username"]} has {row["minutesplayed"]} minutes played, and a discord ID of {row["discorduserid"]}.")
                
            lineCount += 1
            
        csvf.close()
    
    q.newline()
    
    try:
        
        q.sendLogMessage("Attempting to start tasks")
        
        checkPlaytime.start()
            
        resetPlaytime.start()
        
        notifyPlaytime.start()
        
        q.sendLogMessage("Tasks started successfully", type="Success")
            
    except Exception as e:
        q.sendLogMessage(f"Failed to run a task: {e}", type="Error")



#--------------------------------------------------| Functions / Classes |-------------------------------------------------#



class RestartButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Restart Server", style=discord.ButtonStyle.green, custom_id="btnRestartServer")

    async def callback(self, interaction: discord.Interaction):
        view = self.view
      
        userID = interaction.user.id
        
        if userID == 321317643099439104:
            q.sendLogMessage(f"Restart Button clicked by Ben, Restarting Server...", type="Success")
            
            if localConnection == 'True':
                try:
                    if await r.RestartServer(120):
                        return True
                    
                    else:
                        q.sendLogMessage("Failed to restart server", type="Error")
                        
                        return None
                
                except Exception as e:
                    q.sendLogMessage(f"Error restarting server: {e}", type="Error")
                    
                    return None
                
            else:
                q.sendLogMessage("Bot is outside of the network RCON connection unavailable, skipping server restart.", type="Warning")
                
                return None
                    
        elif userID not in view.clicked_users:
            view.clicked_users.add(userID)
          
            remaining_users = 2 - len(view.clicked_users)
            
            if len(view.clicked_users) == 2:
                q.sendLogMessage("Restart Button clicked by two different users! Restarting Server...", type="Success")
              
                view.clicked_users.clear()
                
                await interaction.response.edit_message(content="Restart Button clicked by two different users! Restarting server in 2 minutes.")
                
                if localConnection == 'True':
                    try:
                        if await r.RestartServer(120):
                            return True
                     
                        else:
                            q.sendLogMessage("Failed to restart server", type="Error")
                           
                            return None
                  
                    except Exception as e:
                        q.sendLogMessage(f"Error restarting server: {e}", type="Error")
                        
                        return None
                    
                else:
                    q.sendLogMessage("Bot is outside of the network RCON connection unavailable, skipping server restart.", type="Warning")
                    
                    return None
           
            else:
                q.sendLogMessage(f"Restart Button clicked by {len(view.clicked_users)} people. {remaining_users} more people required to trigger restart.", type="Info")
                
                await interaction.response.edit_message(content=f"Restart Button clicked by {len(view.clicked_users)} people. {remaining_users} more people required to trigger restart.")
        
        else:
            await interaction.response.send_message("You've already clicked the button! Waiting for another user.", ephemeral=True)


class RestartView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.clicked_users = set()
        self.add_item(RestartButton())


#------------------------------------------------------| Task Loops |------------------------------------------------------#



@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(statuses)))
    

@tasks.loop(time=datetime.time(hour=22, minute=30))    
async def notifyPlaytime():
    q.sendLogMessage("Notifying playtime...")
    
    try:
        channel = client.get_channel(RandStuffGeneralID)
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            data = list(csvReader)
            
            playTime = ""
            
            playersignored = 0
            
            for row in data:
                if row["minutesplayed"] != '0':
                    playTime += str(f"- {row['username']} has played for {round((int(row['minutesplayed'])/60),1)} hours ({row['minutesplayed']} minutes)\n")
                else:
                    playersignored += 1
            
            embed = discord.Embed(
                title = "Total Playtime for each player today",
                description = f"Playtime today: \n{playTime}",
                colour = discord.Colour.green()
            )
        
            embed.set_footer(text = f"{playersignored} {'players have' if playersignored > 1 else 'player has'} not played today")
            
            csvf.close()
            
        await channel.send(embed=embed)
        
    except Exception as e:
        q.sendLogMessage(f"Error notifying playtime: {e}", type="Error")
    

@tasks.loop(seconds=600)
async def checkPlaytime():
    try:
        
        q.newline()
        
        if ServerConn == False:
            q.sendLogMessage("No server connection available, skipping playtime check.", type="Error")
            
            return
        
        qry.start()

        stats = qry.get_full_stats()
        
        if 'players' in stats:
            playerList = stats['players']

        qry.stop()
        
        if len(playerList) > 0:
        
            for player in playerList:
                
                player = player.strip("[0m")
                
                if not await s.updatePlaytime(player, 10):
                        await disc.getDiscordID(player, client)
        else:
            q.sendLogMessage("No players to update, none online")
    
    except Exception as e:
        q.sendLogMessage(f"An error occurred while checking playtime: {e}", type="Error")
        
        
@tasks.loop(time=datetime.time(hour=0, minute=0))
async def resetPlaytime():
    await s.updatePlaytime(".mattcur", 0, reset=True)
    await s.updatePlaytime("Jedi_Maxster", 0, reset=True)
    await s.updatePlaytime("shortoctopus", 0, reset=True)
    await s.updatePlaytime("Rugged__Base", 0, reset=True)
    await s.updatePlaytime("Benjamano", 0, reset=True)

    
    #ug await channel.send(content=f"{user.mention} has been playing Minecraft for {round((result[0] / 60),1)} hours, please tell them to touch some grass", allowed_mentions=discord.AllowedMentions(users=True))
#------------------------------------------------------| Commands |------------------------------------------------------#



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        q.sendLogMessage(f"{ctx.author} sent a command that doesn't exist: '{ctx.message.content}'", type="Error")
        
        await ctx.send("Command not found. Please use a valid command. Use `/help` for a list of commands.")
    
    else:
        q.sendLogMessage(f"Error occured while running command {ctx.command} run by {ctx.author} : Error: {error}", type="Error")
        
        await ctx.send("An error occurred. Please try again later.")


@client.tree.command(name="restartserver", description="Restarts the Minecraft Server")
async def restartServer(interaction: discord.Interaction):
    try:
        q.newline()
        
        q.sendLogMessage(f"Restart button command triggered by {interaction.user}", type="Warning")
        
        await interaction.response.send_message("To restart the server, click the button below", view=RestartView())
    
    except Exception as e:
        q.sendLogMessage(f"Error sending restart button: {e}", type="Error")
        
        await interaction.response.send_message(f"Error restarting server, try again later.", ephemeral=True)


@client.tree.command(name="movieswatched", description="Displays a list of all movies watched")
async def moviesWatched(interaction: discord.Interaction):
    pass

        
@client.tree.command(name="selectmovie", description="Selects a random movie from the 'Movie Suggestions' channel")
async def selectMovie(interaction: discord.Interaction):
    try:
        q.newline()
        
        try:
            start_time = time.time()
            
        except Exception as e:
            q.sendLogMessage(f"Error starting timer: {e}", type="Error")
        
        #await interaction.response.send_message("Selecting a movie...", ephemeral=False)
        
        await interaction.response.defer(thinking=True)
        
        selection, userName = await disc.pickMovie()
        
        if selection:
            embed = discord.Embed(
                title = "The movie selected is:",
                description = f"{str(selection).title()} requested by {userName}",
                colour = discord.Colour.random()
            )
            
            await s.addToWachedMovies(selection, requestUser=userName)
                
            try:
                end_time = time.time()
                duration = end_time - start_time
                
                embed.set_footer(text = f"Time taken to process request: {round(duration, 2)} seconds")
            
            except:
                q.sendLogMessage(f"Error setting footer: {e}", type="Error")
            
            await interaction.followup.send(embed=embed)
            
        else:
            q.sendLogMessage("An error occurred while selecting a movie, no movie was returned!", type="Error")
            await interaction.followup.send("An error occurred while selecting a movie, please try again later.", ephemeral=True)
    
    except Exception as e:
        q.sendLogMessage(f"An error occured while selecting a movie: {e}", type="Error")
        try:
            await interaction.followup.send(f"An error occurred while selecting a movie, please try again later. ({e})", ephemeral=True)
        except:
            pass


@client.tree.command(name="addid", description="Ben Only")
@app_commands.describe(inputpassword="Password", inputname="Name", inputuserid="UserID")
async def addId(interaction:discord.Interaction,*, inputpassword: str, inputname: str, inputuserid: str):
    try:
        q.newline()
        
        if inputpassword == password:
            if inputname != "" and inputuserid != "" and inputuserid != 0 and len(str(inputuserid)) == 18:
                q.sendLogMessage(f"User '{interaction.user}' has succesfully logged in.")
                
                if not await s.updateRecord(inputname, int(inputuserid)):
                    q.sendLogMessage(f"Failed to update record for {inputname}", type="Error")
                    await interaction.response.send_message("Failed to update record, check logs for more info.", ephemeral=True)
                    
                q.sendLogMessage(f"User {interaction.user} has added/updated {inputname} with a Discord ID of {inputuserid}", type="Success")
                await interaction.response.send_message(f"Successfully added/updated {inputname} with a Discord ID of {inputuserid}", ephemeral=True)
            
            else:
                q.sendLogMessage(f"User {interaction.user} tried to enter invalid data", type="Warning")
                await interaction.response.send_message("Invalid data was entered.", ephemeral=True)
        
        else:
            q.sendLogMessage(f"User {interaction.user} tried to run the add ID command with the wrong password", type="Warning")
            await interaction.response.send_message("Incorrect Password, You do not have access to this.", ephemeral=True)
    
    except Exception as e:
        q.sendLogMessage(f"Error running Add ID command: {e}", type="Error")
        
    q.newline()

@client.tree.command(name="help", description="Displays a list of all possible commands")
async def help(interaction:discord.Interaction):
    #TODO: Add a help command that lists all the commands and their descriptions
    
    try:
        embed = discord.Embed(
            title = "Help",
            description = "List of all commands",
            colour = discord.Colour.blue()
        )
        
        embed.add_field(name="Commands", value="`/playersonline` - Displays a list of all players online\n`/totalplaytime` - Displays the total playtime for each player today\n`selectmovie` - Randomly selects a movie from the 'movie suggestions' channel\n`/credits` - Displays the credits\n`/ping` - Pings the bot\n`/8ball` - Ask the 8ball a question\n`/willyrate` - Rates your willy\n`/howgayami` - How gay are you?", inline=False)
        
        await disc.sendMessage(interaction=interaction, embed=embed)
        
        #await interaction.response.send_message(embed=embed,ephemeral=False)
    
    except Exception as e:
        q.sendLogMessage(f"Error running help command: {e}", type="Error")


@client.tree.command(name="playersonline", description="Displays a list of all players currently on the Minecraft Server")
async def playersonline(interaction: discord.Interaction):
    if ServerConn == False:
        try:
            embed = discord.Embed(
                
                title = "No Connection",
                description = f"Connection to server is unavailable, please try again later.",
                colour = discord.Colour.red()
            )
            
            embed.set_footer(text = 'Crazy Neil is running - but there is a problem with the connection to the Minecraft Server')
            
            await interaction.response.send_message(embed=embed,ephemeral=False)
                
        except Exception as e: 
            q.sendLogMessage(f"Couldn't send the 'No connection to server' message: {e}", type="Error")
    
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
            
            embed.set_footer(text = f'Ping: {round(client.latency * 1000)}ms')
            
            await interaction.response.send_message(embed=embed,ephemeral=False)
        
        except Exception as e:
            q.sendLogMessage(f"Error running Players online command: {e}", type="Error")
            
            try:
                
                embed = discord.Embed(
                    title="Error",
                    description="An error occurred while trying to retrieve the list of players.",
                    colour=discord.Colour.red()
                )
                await interaction.response.send_message(embed=embed,ephemeral=False)
            
            except Exception as e:
                q.sendLogMessage(f"Error while sending error message via discord: {e}", type="Error")


@client.tree.command(name="totalplaytime", description="Displays the total playtime for each player on the Minecraft Server today")
async def totalplaytime(interaction: discord.Interaction):
    try:
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            data = list(csvReader)
            
            playTime = ""
            
            playersignored = 0
            
            for row in data:
                if row["minutesplayed"] != '0':
                    playTime += str(f"- {row['username']} has played for {round((int(row['minutesplayed'])/60),1)} hours ({row['minutesplayed']} minutes)\n")
                else:
                    playersignored += 1
        
        embed = discord.Embed(
            title = "Total Playtime for each player today",
            description = f"Playtime today: \n{playTime}",
            colour = discord.Colour.green()
        )
        
        embed.set_footer(text = f"{playersignored} {'players have' if playersignored > 1 else 'player has'} not played today")
        
        csvf.close()
        
        await interaction.response.send_message(embed=embed,ephemeral=False)
    
    except Exception as e:
        q.sendLogMessage(f"Error running total playtime command: {e}", type="Error")
        
        
@client.tree.command(name="credits", description="Displays the credits")
async def credits(interaction: discord.Interaction):
    try:
        embed = discord.Embed(
            title = 'Credits',
            description = 'Coded by Ben Mercer',
            colour = discord.Colour.blue()
        )
        
        embed.set_footer(text = 'Hold the applause!')

        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        q.sendLogMessage(f"Error running credits command: {e}", type="Error")


#This command allows a user to ask a question to an 8ball and picks a random response.
@client.tree.command(name="8ball", description="Ask the 8ball a question....")
@app_commands.describe(question="Ask the 8ball a question")
async def eightBall(interaction: discord.Interaction, *, question: str):
    
    if question:
    
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
                    "Very doubtful.",
                    "No.",
                    "No chance.",
                    "Not a chance in hell.",
                    "No way.",
                    "You're joking right?",
                    "You're having a laugh.",
                    "You're having a giraffe.",
                    "You're having a bubble.",
                    "You're having a bubble bath.",
                    "You're having a bubble and squeak.",
                    "You're having a bubble and squeak with a side of mash.",
                    "You're having a bubble and squeak with a side of mash and gravy.",
                    "You're having a bubble and squeak with a side of mash, gravy and peas.",
                    "You're having a bubble and squeak with a side of mash, gravy, peas and a yorkshire pudding.",
                    "You're having a bubble and squeak with a side of mash, gravy, peas, a yorkshire pudding and a sausage.",
                    "You're having a bubble and squeak with a side of mash, gravy, peas, a yorkshire pudding, a sausage and a roast chicken.",
                    "You're having a bubble and squeak with a side of mash, gravy, peas, a yorkshire pudding, a sausage, a roast chicken and a beef joint.",
                    "You're having a bubble and squeak with a side of mash, gravy, peas, a yorkshire pudding, a sausage, a roast chicken, a beef joint and a lamb joint.",
                    "You're having a bubble and squeak with a side of mash, gravy, peas, a yorkshire pudding, a sausage, a roast chicken, a beef joint, a lamb joint and a pork joint.",
                    ]
        
        embed = discord.Embed(
            title = 'The 8ball answers....',
            description = f'{random.choice(responses)}',
            colour = discord.Colour.purple()
        )
        
        embed.set_footer(text = f"Question '{question}' asked by {interaction.user}")
            
        await interaction.response.send_message(embed=embed, ephemeral=False)
    
    else:
        await interaction.response.send_message("Please ask a question", ephemeral=True)


@client.tree.command(name="ratemywilly", description="Neil will rate your willy")
async def willyRate(interaction: discord.Interaction):
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
    
    embed = discord.Embed(
        title = 'Neil has rated your willy....',
        description = f'{random.choice(responses)}',
        colour = discord.Colour.random()
    )
        
    await interaction.response.send_message(embed=embed, ephemeral=False)


@client.tree.command(name='howgayami', description="Neil will rate how gay you are")
async def howgay(interaction: discord.Interaction):
    responses = ["very Gay",
                "too Gay",
                r"100% Gay",
                r"0% Gay",
                r"69% Gay",
                "as gay as Elliot Pomroy",
                "not gay at all",
                "James Charles 2.0",
                "as Gay as Matt C-C",
                "Max Brundell"]
    
    embed = discord.Embed(
        title = 'Neil has rated your gayness....',
        description = f'You are {random.choice(responses)}',
        colour = discord.Colour.blurple()
    )
        
    await interaction.response.send_message(embed=embed, ephemeral=False)


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