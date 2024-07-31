import discord
import csv
import random
import asyncio
import CommonFunctions.formatTools as q

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
                self.send_log_message(f"Found '{player}' in file, skipping record creation", type="info")
                
            else:
                if not await self.create_record(player, 0, 0):
                    self.send_log_message(f"Failed to create record for '{player}'", type="Error")
                    
                    return None

            ben_UserID = 321317643099439104
            
            user = await self.client.fetch_user(ben_UserID)
            
            if user:
                await user.send(f"Player '{player}' does not have a DiscordID stored. To add to the file, type /addid [password] {player} [DiscordID]")
                
                self.send_log_message(f"Sent DM to Ben.", type="Success")
                
            else:
                self.send_log_message(f"User with ID {ben_UserID} not found.", type="Error")

        except Exception as e:
            self.send_log_message(f"Error getting discord ID for {player}: {e}", type="Error")
            
            return None

        self.newline()
        
        return True

    async def getReactionsByID(self, message_id, ChannelID):
        try:
            channel = self.client.get_channel(ChannelID)
            
            message = await channel.fetch_message(message_id)
            
            return message.reactions
        
        except Exception as e:
            self.send_log_message(f"Error getting reactions for message {message_id} in channel {ChannelID}: {e}", type="Error")
            
            return None

    async def getHistoryOfChannel(self, ChannelID):
        try:
            channel = self.client.get_channel(ChannelID)
            
            self.send_log_message(f"Fetching history of '{channel.name}' channel (50 Messages MAX)")
            
            history = []

            async for message in channel.history(limit=50):
                message_data = [message.content, message.id, message.author.name]
                
                history.append(message_data)

            upvote_history = []
            
            for message in history:
                reactions = await self.get_reactions_by_id(message[1], ChannelID)
    
                for reaction in reactions:
                    emoji = reaction.emoji
                    
                    emoji_name = emoji if isinstance(emoji, str) else f"<:{emoji.name}:{emoji.id}>"
                    
                    if emoji_name == "✅" and reaction.count > 0:
                        self.send_log_message(f"Message {message[1]} has been marked as watched, Skipping.", type="Success")
                        pass
                    
                    elif emoji_name == "<:upvote:727485131740414002>" and reaction.count > 1:
                        
                        upvote_history.append(message)
                        
            return upvote_history
        
        except Exception as e:
            self.send_log_message(f"Error getting history of channel {ChannelID}: {e}", type="Error")
            
            return None

    async def pickMovie(self):
        try:
            movie_suggestions_ChannelID = 1248394904833495160
            
            history = await self.get_history_of_channel(movie_suggestions_ChannelID)
            
            if history:
                self.send_log_message(f"Got history of channel, picking random movie", type="Success")
                
                choice = random.choice([message[0] for message in history])
                
                message_id = [message[1] for message in history if message[0] == choice][0]
                
                user_name = [message[2] for message in history if message[0] == choice][0]
                
                await self.mark_as_watched(message_id, movie_suggestions_ChannelID)
                
                self.send_log_message(f"Picked movie: {choice}", type="Success")
                
                return choice, user_name
            
            else:
                self.send_log_message("Failed to get history of channel, nothing was returned.", type="Error")
                
                return None
            
        except Exception as e:
            self.send_log_message(f"Error picking movie: {e}", type="Error")
            
            return None

    async def markAsWatched(self, message_id, ChannelID):
        complete = False
        tries = 0
        while not complete:
            try:
                emoji = "✅"
                message = await self.client.get_channel(ChannelID).fetch_message(message_id)
                await message.add_reaction(emoji)
                self.send_log_message(f"Marked message {message_id} as watched", type="Success")
                complete = True
            except Exception as e:
                tries += 1
                if tries <= 5:
                    self.send_log_message(f"Error marking message {message_id} as watched, may have been run in a different channel, trying again in 10 Seconds ({e})", type="Warning")
                    await asyncio.sleep(10)
                elif tries == 6:
                    self.send_log_message(f"Error marking message {message_id} as watched, max tries reached, aborting. ({e})", type="Error")
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
                        self.send_log_message(f"Error sending message to user {UserID}: No message or embed provided.", type="Error")
                        return None
                except Exception as e:
                    self.send_log_message(f"Error fetching user {UserID}: {e}", type="Error")
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
                    self.send_log_message(f"Error sending message to channel {ChannelID}: {e}", type="Error")
                    return None
            elif interaction and not UserID and not ChannelID:
                if embed and not message:
                    try:
                        await interaction.response.send_message(embed=embed)
                        return True
                    except Exception as e:
                        self.send_log_message(f"Error sending interaction message with embed: {e}", type="Error")
                        return None
                elif message and not embed:
                    try:
                        await interaction.response.send_message(message)
                        return True
                    except Exception as e:
                        self.send_log_message(f"Error sending interaction message: {e}", type="Error")
                        return None
            else:
                self.send_log_message(f"Error sending message: No valid parameters provided.", type="Error")
        except Exception as e:
            self.send_log_message(f"Error sending message: {e}", type="Error")
            return None