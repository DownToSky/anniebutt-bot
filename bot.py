from twitchio.ext import commands
import cassiopeia as cass
from cassiopeia import Summoner, Champion, ChampionMastery
import json
import codecs

class Bot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        riot_key = kwargs.get("riot_key")
        cass.set_riot_api_key(riot_key)

        main_channel = kwargs.get("initial_channels")[0]
        self.sInfo = self.load_stream_info()
        self.championInfo = dict()




    def load_stream_info(self):
        with codecs.open("streaminfo.json", 'r', 'utf-8') as streamFile:
            return json.load(streamFile)
        return None




    async def event_ready(self):
        print(f'Ready | {self.nick}')




    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)



    def get_champion_id(self, name , region):
        if name in self.championInfo:
            return self.championInfo[name]["id"]
        champions = cass.Champions(region=region)
        for ch in champions:
            if name.lower() == ch.name.lower():
                self.championInfo[name] = {"id":ch.id}
                return ch.id


    @commands.command(name='mastery')
    async def my_command(self, ctx):
        if ctx.channel.name in self.sInfo:
            ch_name = ctx.channel.name
            reg = self.sInfo[ch_name]["region"]
            accs = self.sInfo[ch_name]["mastery"]["accounts"]
            chmp_name = self.sInfo[ch_name]["mastery"]["champion"]
            chmp_id = self.get_champion_id(name = chmp_name, region = reg)
            chmp = cass.Champion(name=chmp_name, id=chmp_id, region = reg)


            masteries = list()
            for acc in accs:
                summ = cass.get_summoner(name = acc, region = reg)
                print(summ.id)
                cm = cass.get_champion_mastery(champion=chmp, summoner=summ,
                                            region=reg)
                masteries.append((summ.name, cm.points))
            print(masteries)
            total = format(sum([e[1] for e in masteries]), ",")
            accs = ", ".join([e[0] for e in masteries])
            output = f'@{ctx.author.name} Total mastery points on {chmp_name} \
                        across all acounts ({accs}): {total}'
            await ctx.send(output)
