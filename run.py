import json
from bot import Bot


if __name__ == '__main__':
    tkns = {}

    with open("tokens.json", 'r') as tFile:
        tkns = json.read(tFile)

    options = {
        "client_id": tkns["client_id"],
        "irc_token": tkns["auth_token"],
        "initial_channels": ["annie_butt"],
        "nick": tkns["nick"],
        "prefix": "!"
    }
    bot = Bot()
    bot.run()
