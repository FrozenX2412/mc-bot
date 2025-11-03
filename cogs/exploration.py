import discord
import random
from discord.ext import commands

from .mobs import MOB_POOLS
from .chests import CHEST_POOL
from .structures import STRUCTURE_POOLS

class Exploration(commands.Cog):
    """Handles exploration logic"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def explore(self, ctx):
        biome = random.choice(list(STRUCTURE_POOLS.keys()))
        structure = random.choice(STRUCTURE_POOLS[biome])
        mob = random.choice(MOB_POOLS[biome])
        chests = random.choices(CHEST_POOL, k=random.randint(1, 3))
        embed = discord.Embed(title="Exploration Results")
        embed.add_field(name="Biome", value=biome)
        embed.add_field(name="Structure", value=f"{structure['name']} ({structure['effect']})")
        embed.add_field(name="Mob", value=f"{mob['name']} (HP {mob['hp']}, ATK {mob['atk']})")
        chest_summary = "\n".join(f"{c['tier']} Chest" for c in chests)
        embed.add_field(name="Chests", value=chest_summary)
        embed.set_footer(text="Fight the mob and open your chests!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Exploration(bot))
