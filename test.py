from mctools import RCONClient

try:
    rcon = RCONClient('127.0.0.1', port=25575)
    if rcon.login('1552'):
        print("RCON Login Successful!")
        response = rcon.command('say Test command from RCON')
        print(f"Response: {response}")
    else:
        print("RCON Login Failed.")
except Exception as e:
    print(f"RCON Error: {e}")
