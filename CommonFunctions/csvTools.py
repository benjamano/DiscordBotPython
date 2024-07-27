import CommonFunctions.formatTools as q
import csv


async def checkPlaytimeCSV(username):
    try:
        shame = False
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            q.newline(baronly=True)
            
            q.sendLogMessage(f"Searching for playtime of user: {username}")
            
            for row in csvReader:
                if row['username'] == username:
                    playerPlaytime = int(row['minutesplayed'])
                    q.sendLogMessage(f"Found {username} with {playerPlaytime} minutes played", type="Success")
                    break
        
        if playerPlaytime == 360 or playerPlaytime == 420 or playerPlaytime == 480 or playerPlaytime == 540:
            shame = True
        
        q.newline()
        
        return playerPlaytime, shame
    
    except Exception as e:
        q.sendLogMessage(f"Error checking playtime of {username}: {e}", type="Error")
        return None, None


async def updatePlaytime(username, additionalMinutes, reset = False):
    
    try:
    
        #q.sendLogMessage(f"Updating {username}'s playtime by {additionalMinutes} minutes")
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            data = list(csvReader)
            
        if (username not in [row['username'] for row in data]) and username != "":
            q.sendLogMessage(f"Could not find username '{username}' in file, notifying Ben through DMs", type="Warning")
            
            return None
        
        if any(row['username'] == username and str(row['discorduserid']) == "0" for row in data):
            q.sendLogMessage(f"Discord ID is empty for user: {username}, getting Discord ID through Ben using DMs", type="Warning")
            
            return None

        for row in data:
            if row['username'] == username and reset == True:
                row['minutesplayed'] = str(0)
                q.newline(baronly=True)
                q.sendLogMessage(f"Reset {username}'s minutes.", type="Success")
            
            elif str(username) in str(row["username"]) and reset == False:
                row['minutesplayed'] = str(int(row['minutesplayed']) + additionalMinutes)
                q.sendLogMessage(f"Increased {username}'s minutes played by {additionalMinutes}", type="Success")
                q.sendLogMessage(f"New Minutes: {row['minutesplayed']} ({(int(row['minutesplayed']))/60} Hours)", type="Info")
        
        with open("StoredData/hours.csv", mode="w", newline='') as csvf:
            fieldnames = ['username', 'minutesplayed', 'discorduserid']
            
            csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
            
            csvWriter.writeheader()
            csvWriter.writerows(data)
            
        return True
    
    except Exception as e:
        q.sendLogMessage(f"Error updating {username}'s playtime: {e}", type="Error")
        return "Error"

async def getUserID(player):
    try:
        q.sendLogMessage(f"Searching for userID of player: {player}")
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            data = list(csvReader)
        
        for row in data:
            if row['username'] == player:
                q.sendLogMessage(f"Found {player} with userID: {row['discorduserid']}", type="Success")
                return row['discorduserid']
            
        q.sendLogMessage(f"Could not find {player} in file.", type="Warning")
        
        return None
    
    except Exception as e:
        q.sendLogMessage(f"Error finding userID of {player}: {e}", type="Error")
        return None

async def updateRecord(playername, discordID):
    try:
        q.sendLogMessage(f"Updating '{playername}' discord ID to '{discordID}'")
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            data = list(csvReader)
            
        for row in data:
            if row['username'] == playername and row['discorduserid'] == "0":
                row['discorduserid'] = discordID
                #q.sendLogMessage(f"Updated '{playername}' discord ID to '{discordID}'", type="Success")
        
        with open("StoredData/hours.csv", mode="w", newline='') as csvf:
            fieldnames = ['username', 'minutesplayed', 'discorduserid']
            
            csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
            
            csvWriter.writeheader()
            csvWriter.writerows(data)
            
        csvf.close()
            
        return True
    
    except Exception as e:
        q.sendLogMessage(f"Error updating {playername}'s discord ID: {e}", type="Error")
        return False

async def createRecord(playername, minutesplayed, discordID):
    try:
        q.sendLogMessage(f"Creating record for {playername} with {minutesplayed} minutes played and discord ID {discordID}")
        
        with open("StoredData/hours.csv", mode="a", newline='') as csvf:
            fieldnames = ['username', 'minutesplayed', 'discorduserid']
            
            csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
            
            csvWriter.writerow({'username': playername, 'minutesplayed': minutesplayed, 'discorduserid': discordID})
            
        return True

    except Exception as e:
        q.sendLogMessage(f"Error creating record for {playername}: {e}", type="Error")
        return False