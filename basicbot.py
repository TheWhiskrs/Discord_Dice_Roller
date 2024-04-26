# basicbot.py Used for rolling dice in D&D
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('discord_token')

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    guild_count = 0
    for guild in client.guilds:
        print(f'{guild.id} (name: {guild.name})')
        guild_count = guild_count + 1
    print('DnD Dice Roller is in', str(guild_count), "servers.")


@client.command()
async def roll(ctx, *, text: str):
        count, _, text = text.partition('d')
        size, _, bonus = text.partition('+')
        if bonus == '':
            bonus = 0
        try:
            count = int(count)
            size = int(size)
            bonus = int(bonus)
            await _roll(ctx, count, size, bonus)
        except ValueError:
            print('Please enter dice as XdY or XdY+Z')
            error = (f'Please enter dice as XdY or XdY+Z')
            await ctx.send(error)


async def _roll(ctx, count, size, bonus):
    rolls = [random.randint(bonus + 1, bonus + size) for i in range(count)]  # Random generator from bonus + 1 to dice total + bonus
    embed = discord.Embed(title=f'Dice for {count}d{size}+{bonus}')
    embed.description = '\n'.join((f'#{i}: **{roll}**' for i, roll in enumerate(rolls)))
    embed.add_field(name='Total', value=f'{sum(rolls)}')
    await ctx.send(embed=embed)

client.run(TOKEN)
