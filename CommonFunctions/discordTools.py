import CommonFunctions.formatTools as q
import CommonFunctions.csvTools as s
import csv
import random
import asyncio


async def getDiscordID(player, client):
    try:
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            data = list(csvReader)
        
        if any(player == row['username'] for row in data):
            q.sendLogMessage(f"Found '{player}' in file, skipping record creation", type="info")
        
        else:
            if not await s.createRecord(player, 0, 0):
                q.sendLogMessage(f"Failed to create record for '{player}'", type="Error")
                return None
            
        BenUserID = 321317643099439104
        
        user = await client.fetch_user(BenUserID)
        
        if user:
            await user.send(f"Player '{player}' does not have a DiscordID stored. To add to the file, type /addid [password] {player} [DiscordID]")
            
            q.sendLogMessage(f"Sent DM to Ben.", type="Success")
            
        else:
            q.sendLogMessage(f"User with ID {BenUserID} not found.", type="Error")
    
    except Exception as e:
        q.sendLogMessage(f"Error getting discord ID for {player}: {e}", type="Error")
        return None
    
    q.newline()
    
    return True



async def getReactionsbyID(messageID, channelID, client):
    try:
        channel = client.get_channel(channelID)
        
        message = await channel.fetch_message(messageID)
        
        reactions = message.reactions
        
        return reactions
    
    except Exception as e:
        q.sendLogMessage(f"Error getting reactions for message {messageID} in channel {channelID}: {e}", type="Error")
        return None
    
    
    
async def getHistoryofChannel(channelID, client):
    try:
        channel = client.get_channel(channelID)
        
        q.sendLogMessage(f"Fetching history of '{channel.name}' channel (50 Messages MAX)")
        
        history = []
        
        async for message in channel.history(limit=50):
            
            messageData = [message.content, message.id, message.author.name]
            history.append(messageData)
        
        upvoteHistory = []
        
        for message in history:
            reactions = await getReactionsbyID(message[1], channelID, client)
            
            for reaction in reactions:
                emoji = reaction.emoji
                
                if isinstance(emoji, str):
                    emoji_name = emoji 
                    
                else:
                    emoji_name = f"<:{emoji.name}:{emoji.id}>" 
                    
                if emoji_name == "✅" and reaction.count > 0:
                    q.sendLogMessage(f"Message {message[1]} has been marked as watched, Skipping.", type="Success")
                    pass
                
                elif emoji_name == "<:upvote:727485131740414002>" and reaction.count > 1:
                    upvoteHistory.append(message)
        
        return upvoteHistory
    
    except Exception as e:
        q.sendLogMessage(f"Error getting history of channel {channelID}: {e}", type="Error")
        return None



async def pickMovie(client):
    try:
        
        moviesuggestionschannelID = 1248394904833495160
        
        history = await getHistoryofChannel(moviesuggestionschannelID, client)
        
        if history:
            q.sendLogMessage(f"Got history of channel, picking random movie", type="Success")
            
            # for message in history:
            #     q.sendLogMessage(f"MessageID: {message[1]}, Contents: {message[0]}", type="Success")
            choice = random.choice([message[0] for message in history])
            
            messageID = [message[1] for message in history if message[0] == choice][0]
            
            userName = [message[2] for message in history if message[0] == choice][0]
            
            await markAsWatched(messageID, moviesuggestionschannelID, client)
        
            q.sendLogMessage(f"Picked movie: {choice}", type="Success")
            
            return choice, userName
        
        else:
            q.sendLogMessage("Failed to get history of channel, nothing was returned.", type="Error")
            
            return None
        
    except Exception as e:
        q.sendLogMessage(f"Error picking movie: {e}", type="Error")
        
        return None
    
    return None
    


async def markAsWatched(messageID, channelID, client):
    complete = False
    tries = 0
    
    while complete == False:

        try:
            emoji = "✅"
            
            message = await client.get_channel(channelID).fetch_message(messageID)
            
            await message.add_reaction(emoji)
            
            q.sendLogMessage(f"Marked message {messageID} as watched", type="Success")
            
            complete = True    
        
        except Exception as e:
            tries += 1
            
            if tries <= 5:
                q.sendLogMessage(f"Error marking message {messageID} as watched, may have been run in a different channel, trying again in 10 Seconds ({e})", type="Warning")
                
                await asyncio.sleep(10)
            
            elif tries == 6:
                q.sendLogMessage(f"Error marking message {messageID} as watched, max tries reached, aborting. ({e})", type="Error")
                
                return 
            
async def sendMessage(client, message=None, UserID=None, ChannelID=None, embed=None, interaction=None):
    try:
        if UserID and not interaction:
            try:
                user = client.fetch_user(UserID)
                
                if embed and not message:
                    await user.send_message(embed=embed)
                    
                    return True
                
                elif message and not embed:
                    await user.send_message(message)
                    
                    return True
                
                else:
                    q.sendLogMessage(f"Error sending message to user {UserID}: No message or embed provided.", type="Error")
                    
                    return None
            
            except Exception as e:
                q.sendLogMessage(f"Error fetching user {UserID}: {e}", type="Error")
                return None
            
        elif ChannelID and not interaction:
            try:
                channel = client.get_channel(ChannelID)
                
                if embed and not message:
                    await channel.send(embed=embed)
                    
                    return True
                
                elif message and not embed:
                    await channel.send(message)
                    
                    return True
            
            except Exception as e:
                q.sendLogMessage(f"Error sending message to channel {ChannelID}: {e}", type="Error")
                
                return None
        
        elif interaction and not UserID and not ChannelID:
            
            if embed and not message:
                try:
                    await interaction.response.send_message(embed=embed)
                    
                    return True
                
                except Exception as e:
                    q.sendLogMessage(f"Error sending interaction message with embed: {e}", type="Error")
                    return None
            
            elif message and not embed:
                try:
                
                    await interaction.response.send_message(message)
                    
                    return True

                except Exception as e:
                    q.sendLogMessage(f"Error sending interaction message: {e}", type="Error")
                    return None
                    
        else:
            q.sendLogMessage(f"Error sending message: No valid parameters provided.", type="Error")
            
    except Exception as e:
        q.sendLogMessage(f"Error sending message: {e}", type="Error")
        
        return None