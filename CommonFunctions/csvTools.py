import CommonFunctions.formatTools as q
import csv

def checkPlaytimeCSV(username):
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


def updatePlaytime(username, additionalMinutes, reset = False):
    
    #q.sendLogMessage(f"Updating {username}'s playtime by {additionalMinutes} minutes")
    
    with open("StoredData/hours.csv", mode="r") as csvf:
        csvReader = csv.DictReader(csvf)
        
        data = list(csvReader)

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
        fieldnames = ['username', 'minutesplayed']
        
        csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
        
        csvWriter.writeheader()
        csvWriter.writerows(data)