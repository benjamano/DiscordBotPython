import asyncio
import subprocess

async def RestartServer(rcon, seconds = 120):
    """Restarts the server in a set amount of seconds, reopening the start.bat shortcut after 30 seconds.
    Seconds defaults to 120 if no input detected."""
    
    try:
        
        await rcon.sendCommand(f"say Server restarting in {seconds/60} minutes. ({seconds} seconds)")
        
        await asyncio.sleep(seconds)
        
        await rcon.sendCommand("stop")
        
        await asyncio.sleep(30)
        
        subprocess.Popen([r"C:\Users\benme\Documents\GitHub\Discord-Bot-Python\start - Shortcut.lnk"])
        
    except Exception as e:
        print(f"Error restarting server: {e}")
        
        return False
    
    return True