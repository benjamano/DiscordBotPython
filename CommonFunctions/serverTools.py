import asyncio
import subprocess
import CommonFunctions.formatTools as q

class ServerTools:
    def __init__(self, rcon):
        self.rcon = rcon
        q.sendLogMessage("Server Tools Initialized, RCON initialised", type="Success")

    async def RestartServer(self, seconds = 120):
        """Restarts the server in a set amount of seconds, reopening the start.bat shortcut after 30 seconds.
        Seconds defaults to 120 if no input detected."""
        
        try:
            
            await self.rcon.command(f"say Server restarting in {seconds/60} minutes. ({seconds} seconds)")
            
            await asyncio.sleep(seconds)
            
            await self.rcon.command("stop")
            
            await asyncio.sleep(30)
            
            subprocess.Popen([r"C:\Users\benme\Documents\GitHub\Discord-Bot-Python\start - Shortcut.lnk"])
            
        except Exception as e:
            print(f"Error restarting server: {e}")
            
            return False
        
        return True