import asyncio
import subprocess
import CommonFunctions.formatTools as q
import os

class ServerTools:
    def __init__(self, rcon):
        self.rcon = rcon
        q.sendLogMessage("Server Tools Initialized, RCON initialised", type="Success")

    async def RestartServer(self, seconds = 120):
        """Restarts the server in a set amount of seconds, reopening the start.bat shortcut after 30 seconds.
        Seconds defaults to 120 if no input detected."""
        
        try:
            
            self.rcon.command(f"say Server restarting in {seconds/60} minutes. ({seconds} seconds)")
            q.sendLogMessage(f"Server restarting in {seconds/60} minutes. ({seconds} seconds)", type="Info")
            
            await asyncio.sleep(seconds)
            
            self.rcon.command("stop")
            q.sendLogMessage("Server stopped", type="Info")
            
            await asyncio.sleep(30)
            
            os.chdir(r"C:\Users\benme\Desktop\JavaBedrockServer")
            
            os.startfile("start.bat")
            
            q.sendLogMessage("Server restarted", type="Success")
            
        except Exception as e:
            q.sendLogMessage(f"Error restarting server: {e}")
            
            return False
        
        return True