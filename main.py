import discord
import json
import os
import humanize
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)

# LOG INTO CONSOLE
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Slowdown Message
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):
        natty = humanize.precisedelta(error.retry_after)
        await ctx.send(f"<a:hourglass:857868080435560520> **| Cooldown:** {natty.title()}")
        
#COG COMMANDS
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Loaded cogs.{extension}")
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Unloaded cogs.{extension}")
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Reloaded cogs.{extension}")
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename.startswith('__init__'):
            pass
        client.load_extension(f'cogs.{filename[:-3]}')

#Token
with open('token.json') as f:
    data = json.load(f)
    token = data["TOKEN"]

client.run(token)
