import json
from bot import Bot


if __name__ == '__main__':
    tkns = {}

    with open("tokens.json", 'r') as tFile:
        tkns = json.load(tFile)

    options = {
        "client_id": tkns["twitch"]["client_id"],
        "irc_token": tkns["twitch"]["auth_token"],
        "initial_channels": ["anniebot"],
        "nick": tkns["twitch"]["nick"],
        "prefix": "!",
        "riot_key": tkns["riot"]["key"]
    }
    bot = Bot(**options)
    bot.run()
