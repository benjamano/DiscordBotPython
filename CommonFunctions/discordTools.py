import CommonFunctions.formatTools as q
import CommonFunctions.csvTools as s
import csv
import random



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
        
        history = []
        
        async for message in channel.history(limit=50):
            
            messageData = [message.content, message.id]
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
                
                if emoji_name == "<:upvote:727485131740414002>" and reaction.count > 1:
                    upvoteHistory.append(message)
        
        return upvoteHistory
    
    except Exception as e:
        q.sendLogMessage(f"Error getting history of channel {channelID}: {e}", type="Error")
        return None



async def pickMovie(client):
    try:
    
        q.sendLogMessage("Fetching history of movie suggestions channel")
        
        moviesuggestionschannelID = 1248394904833495160
        
        history = await getHistoryofChannel(moviesuggestionschannelID, client)
        
        if history:
            q.sendLogMessage(f"Got history of channel {moviesuggestionschannelID}", type="Success")
            
            for message in history:
                q.sendLogMessage(f"MessageID: {message[1]}, Contents: {message[0]}", type="Success")
                
            choice = random.choice([message[0] for message in history])
            
            q.sendLogMessage(f"Picked movie: {choice}", type="Success")
            
            return choice
        
        else:
            q.sendLogMessage("Failed to get history of channel, nothing was returned.", type="Error")
            
            return None
        
    except Exception as e:
        q.sendLogMessage(f"Error picking movie: {e}", type="Error")
        
        return None
    
    return None
    
    