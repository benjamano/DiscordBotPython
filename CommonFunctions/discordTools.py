import discord
import csv
import random
import asyncio
import CommonFunctions.formatTools as q
import CommonFunctions.csvTools as s

class DiscordTools:
    def __init__(self, client):
        self.client = client
        q.sendLogMessage("Discord Tools Initialized, client initialised", type="Success")

    async def getDiscordID(self, player):
        try:
            with open("StoredData/hours.csv", mode="r") as csvf:
                csv_reader = csv.DictReader(csvf)
                
                data = list(csv_reader)
                
            if any(player == row['username'] for row in data):
                q.sendLogMessage(f"Found '{player}' in file, skipping record creation", type="info")
                
            else:
                if not await s.createRecord(player, 0, 0):
                    q.sendLogMessage(f"Failed to create record for '{player}'", type="Error")
                    
                    return None

            ben_UserID = 321317643099439104
            
            user = await self.client.fetch_user(ben_UserID)
            
            if user:
                await user.send(f"Player '{player}' does not have a DiscordID stored. To add to the file, type /addid [password] {player} [DiscordID]")
                
                q.sendLogMessage(f"Sent DM to Ben.", type="Success")
                
            else:
                q.sendLogMessage(f"User with ID {ben_UserID} not found.", type="Error")

        except Exception as e:
            q.sendLogMessage(f"Error getting discord ID for {player}: {e}", type="Error")
            
            return None

        self.newline()
        
        return True

    async def getReactionsByID(self, message_id, ChannelID):
        try:
            channel = self.client.get_channel(ChannelID)
            
            message = await channel.fetch_message(message_id)
            
            return message.reactions
        
        except Exception as e:
            q.sendLogMessage(f"Error getting reactions for message {message_id} in channel {ChannelID}: {e}", type="Error")
            
            return None

    async def getHistoryOfChannel(self, ChannelID):
        try:
            channel = self.client.get_channel(ChannelID)
            
            q.sendLogMessage(f"Fetching history of '{channel.name}' channel (50 Messages MAX)")
            
            history = []

            async for message in channel.history(limit=50):
                message_data = [message.content, message.id, message.author.name]
                
                history.append(message_data)

            upvote_history = []
            
            for message in history:
                reactions = await self.getReactionsByID(message[1], ChannelID)
    
                for reaction in reactions:
                    emoji = reaction.emoji
                    
                    emoji_name = emoji if isinstance(emoji, str) else f"<:{emoji.name}:{emoji.id}>"
                    
                    if emoji_name == "✅" and reaction.count > 0:
                        q.sendLogMessage(f"Message {message[1]} has been marked as watched, Skipping.", type="Info")
                        pass
                    
                    elif emoji_name == "<:upvote:727485131740414002>" and reaction.count > 1:
                        
                        upvote_history.append(message)
                        
            return upvote_history
        
        except Exception as e:
            q.sendLogMessage(f"Error getting history of channel {ChannelID}: {e}", type="Error")
            
            return None

    async def pickMovie(self):
        try:
            movieSuggestionsChannelID = 1248394904833495160
            
            history = await self.getHistoryOfChannel(movieSuggestionsChannelID)
            
            if history:
                q.newline(baronly=True)
                
                q.sendLogMessage(f"Got history of channel, picking random movie", type="Success")
                
                choice = random.choice([message[0] for message in history])
                
                messageID = [message[1] for message in history if message[0] == choice][0]
                
                userName = [message[2] for message in history if message[0] == choice][0]
                
                await self.markAsWatched(messageID, movieSuggestionsChannelID)
                
                q.sendLogMessage(f"Picked movie: {choice}", type="Success")
                
                return choice, userName
            
            else:
                q.sendLogMessage("Failed to get history of channel, nothing was returned.", type="Error")
                
                return None
            
        except Exception as e:
            q.sendLogMessage(f"Error picking movie: {e}", type="Error")
            
            return None

    async def markAsWatched(self, messageID, ChannelID):
        complete = False
        tries = 0
        while not complete:
            try:
                emoji = "✅"
                message = await self.client.get_channel(ChannelID).fetch_message(messageID)
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

    async def sendMessage(self, message=None, UserID=None, ChannelID=None, embed=None, interaction=None):
        try:
            if UserID and not interaction:
                try:
                    user = self.client.fetch_user(UserID)
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
                    channel = self.client.get_channel(ChannelID)
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