# https://discordapp.com/oauth2/authorize?&client_id=474673164652380161&scope=bot

import discord
from discord.ext import commands

from config import TWBotConfig as conf
from BattleNetApi import BattleNetApi

api = BattleNetApi()
bot = commands.Bot(command_prefix=conf.prefix)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}/{bot.user.id}")    

@bot.command()
async def affix():
    af = api.get_affix()
    affixes = []
    for a in af:
        level = a[0]
        name = a[1]
        affixes.append(f"{name} at level {level}")
    say = await code_block(affixes)
    await bot.say(say)

async def code_block(string_array):
    cb = "```\n"
    for s in string_array:
        cb += s + '\n'
    cb += "```"
    return cb

bot.run(conf.TOKEN)
