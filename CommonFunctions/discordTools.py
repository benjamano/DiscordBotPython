import discord
import csv
import random
import asyncio

class DiscordTools:
    def __init__(self, client):
        self.client = client

    async def get_discord_id(self, player):
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

            ben_user_id = 321317643099439104
            
            user = await self.client.fetch_user(ben_user_id)
            
            if user:
                await user.send(f"Player '{player}' does not have a DiscordID stored. To add to the file, type /addid [password] {player} [DiscordID]")
                
                self.send_log_message(f"Sent DM to Ben.", type="Success")
                
            else:
                self.send_log_message(f"User with ID {ben_user_id} not found.", type="Error")

        except Exception as e:
            self.send_log_message(f"Error getting discord ID for {player}: {e}", type="Error")
            
            return None

        self.newline()
        
        return True

    async def get_reactions_by_id(self, message_id, channel_id):
        try:
            channel = self.client.get_channel(channel_id)
            
            message = await channel.fetch_message(message_id)
            
            return message.reactions
        
        except Exception as e:
            self.send_log_message(f"Error getting reactions for message {message_id} in channel {channel_id}: {e}", type="Error")
            
            return None

    async def get_history_of_channel(self, channel_id):
        try:
            channel = self.client.get_channel(channel_id)
            
            self.send_log_message(f"Fetching history of '{channel.name}' channel (50 Messages MAX)")
            
            history = []

            async for message in channel.history(limit=50):
                message_data = [message.content, message.id, message.author.name]
                
                history.append(message_data)

            upvote_history = []
            
            for message in history:
                reactions = await self.get_reactions_by_id(message[1], channel_id)
    
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
            self.send_log_message(f"Error getting history of channel {channel_id}: {e}", type="Error")
            
            return None

    async def pick_movie(self):
        try:
            movie_suggestions_channel_id = 1248394904833495160
            
            history = await self.get_history_of_channel(movie_suggestions_channel_id)
            
            if history:
                self.send_log_message(f"Got history of channel, picking random movie", type="Success")
                
                choice = random.choice([message[0] for message in history])
                
                message_id = [message[1] for message in history if message[0] == choice][0]
                
                user_name = [message[2] for message in history if message[0] == choice][0]
                
                await self.mark_as_watched(message_id, movie_suggestions_channel_id)
                
                self.send_log_message(f"Picked movie: {choice}", type="Success")
                
                return choice, user_name
            
            else:
                self.send_log_message("Failed to get history of channel, nothing was returned.", type="Error")
                
                return None
            
        except Exception as e:
            self.send_log_message(f"Error picking movie: {e}", type="Error")
            
            return None

    async def mark_as_watched(self, message_id, channel_id):
        complete = False
        tries = 0
        while not complete:
            try:
                emoji = "✅"
                message = await self.client.get_channel(channel_id).fetch_message(message_id)
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

    async def send_message(self, message=None, user_id=None, channel_id=None, embed=None, interaction=None):
        try:
            if user_id and not interaction:
                try:
                    user = self.client.fetch_user(user_id)
                    if embed and not message:
                        await user.send_message(embed=embed)
                        return True
                    elif message and not embed:
                        await user.send_message(message)
                        return True
                    else:
                        self.send_log_message(f"Error sending message to user {user_id}: No message or embed provided.", type="Error")
                        return None
                except Exception as e:
                    self.send_log_message(f"Error fetching user {user_id}: {e}", type="Error")
                    return None
            elif channel_id and not interaction:
                try:
                    channel = self.client.get_channel(channel_id)
                    if embed and not message:
                        await channel.send(embed=embed)
                        return True
                    elif message and not embed:
                        await channel.send(message)
                        return True
                except Exception as e:
                    self.send_log_message(f"Error sending message to channel {channel_id}: {e}", type="Error")
                    return None
            elif interaction and not user_id and not channel_id:
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