import datetime


colors = {
        "Info": "\033[94m",    
        "Warning": "\033[93m", 
        "Error": "\033[91m",  
        "Success": "\033[92m"  
}

def sendLogMessage(message, type="Info", date=True, newline=False):
    
    """Possible types: Info, Warning, Error, Success.
    \ndate : defaults to true, this should be kept true as it will break the look of the log if false.
    \nnewline : defaults to false, if true, will add a new line before the message."""
    
    logtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    messagetosend = ""
    
    reset = "\033[0m"

    color = colors.get(type, "\033[94m")
    
    if newline:
        messagetosend += "\n"
    
    if not date:
        messagetosend += f"| {color}{type}{reset} : {message}"
        
    else:
        messagetosend += f"{logtime} | {color}{type}{reset} : {message}"

    print(messagetosend)
    
    
def newline(withDivider=True, baronly=False):
    
    """withdivider : defaults to true, if true, adds a divider ('+')."""
    
    if baronly:
        print("\t\t    |")
        
        return
    
    if withDivider:
        print("-" * 20 + "+" + "-" * 70)
    
    else:
        print("-" * 91)