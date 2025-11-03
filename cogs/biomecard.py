# biomecard.py
# Comet Assistant generated cog for Biome Card system
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import discord
from discord.ext import commands

# Placeholder inventory and economy interfaces (to be implemented by core bot)
class InventoryService:
    async def add_items(self, user_id: int, items: List[Tuple[str, int]]):
        pass

    async def add_currency(self, user_id: int, coins: int):
        pass

    async def add_xp(self, user_id: int, xp: int):
        pass

    async def add_biome_card(self, user_id: int, amount: int = 1):
        pass

    async def consume_biome_card(self, user_id: int, amount: int = 1) -> bool:
        return True


@dataclass
class BiomeInfo:
    name: str
    rarity: str
    chance: float
    description: str
    structures: List[str]
    mobs: List[str]
    chest_types: List[str]
    bonus: Dict[str, int]  # e.g., {"xp": 5, "coins": 10, "drop_bonus": 5}


DEFAULT_BIOMES: List[BiomeInfo] = [
    BiomeInfo(
        name="Plains", rarity="Common", chance=22.0,
        description="Open grasslands with gentle hills and easy encounters.",
        structures=["Village", "Windmill", "Abandoned Farm"],
        mobs=["Zombie", "Skeleton", "Wolf"],
        chest_types=["Common", "Rare"],
        bonus={"xp": 2, "coins": 5, "drop_bonus": 0},
    ),
    BiomeInfo(
        name="Forest", rarity="Common", chance=18.0,
        description="Dense trees and hidden clearings. Watch for ambushes.",
        structures=["Treehouse", "Ranger Camp", "Mossy Ruins"],
        mobs=["Spider", "Zombie", "Witch"],
        chest_types=["Common", "Rare"],
        bonus={"xp": 3, "coins": 5, "drop_bonus": 2},
    ),
    BiomeInfo(
        name="Desert", rarity="Uncommon", chance=12.0,
        description="Harsh sands with buried secrets and temples.",
        structures=["Desert Temple", "Oasis", "Sand Ruins", "Pillar Site"],
        mobs=["Husk", "Scorpion", "Stray"],
        chest_types=["Common", "Rare", "Epic"],
        bonus={"xp": 4, "coins": 10, "drop_bonus": 3},
    ),
    BiomeInfo(
        name="Snow", rarity="Uncommon", chance=11.0,
        description="Frozen tundra with slippery terrain and cold-resistant foes.",
        structures=["Igloo", "Ice Cavern", "Frost Tower"],
        mobs=["Stray", "Polar Bear", "Ice Spirit"],
        chest_types=["Common", "Rare", "Epic"],
        bonus={"xp": 4, "coins": 10, "drop_bonus": 4},
    ),
    BiomeInfo(
        name="Jungle", rarity="Rare", chance=8.0,
        description="Overgrown greenery with rich ruins and agile predators.",
        structures=["Jungle Ruins", "Overgrown Shrine", "Canopy Bridge", "Vine Labyrinth"],
        mobs=["Jaguar", "Poison Dart Frog", "Jungle Spider", "Vine Wraith"],
        chest_types=["Rare", "Epic"],
        bonus={"xp": 6, "coins": 15, "drop_bonus": 6},
    ),
    BiomeInfo(
        name="Cave", rarity="Rare", chance=7.0,
        description="Dark caverns filled with minerals and lurking horrors.",
        structures=["Crystal Chamber", "Mine Shaft", "Stalagmite Hall"],
        mobs=["Cave Spider", "Bat Swarm", "Endermite", "Wardenling"],
        chest_types=["Rare", "Epic"],
        bonus={"xp": 6, "coins": 15, "drop_bonus": 6},
    ),
    BiomeInfo(
        name="Volcano", rarity="Epic", chance=4.0,
        description="Molten peaks with dangerous flows and fiery guardians.",
        structures=["Lava Fortress", "Basalt Keep", "Magma Fissure"],
        mobs=["Fire Golem", "Blaze Captain", "Magma Slime"],
        chest_types=["Epic", "Mythic"],
        bonus={"xp": 8, "coins": 25, "drop_bonus": 8},
    ),
    BiomeInfo(
        name="Wasteland", rarity="Epic", chance=4.0,
        description="Desolate expanse where relics of war grant strange power.",
        structures=["Ruined Bunker", "Ashen City", "Scorched Obelisk"],
        mobs=["Mad Raider", "Toxic Ghoul", "Ash Wraith"],
        chest_types=["Epic", "Mythic"],
        bonus={"xp": 8, "coins": 25, "drop_bonus": 8},
    ),
    BiomeInfo(
        name="Skylands", rarity="Rare", chance=7.0,
        description="Floating isles with thin air and rare treasures.",
        structures=["Cloud Temple", "Sky Bridge", "Aerial Nest"],
        mobs=["Harpy", "Sky Serpent", "Gust Elemental"],
        chest_types=["Rare", "Epic", "Mythic"],
        bonus={"xp": 6, "coins": 20, "drop_bonus": 5},
    ),
    BiomeInfo(
        name="The Void", rarity="Legendary", chance=2.0,
        description="A reality fracture of whispers, shadows, and impossible loot.",
        structures=["Void Castle", "Fracture Spire", "Endless Stair"],
        mobs=["Phantom King", "Null Shade", "Entropy Warden"],
        chest_types=["Mythic", "Legendary Void"],
        bonus={"xp": 12, "coins": 50, "drop_bonus": 12},
    ),
]


def weighted_choice(items: List[BiomeInfo]) -> BiomeInfo:
    total = sum(b.chance for b in items)
    r = random.uniform(0, total)
    upto = 0.0
    for b in items:
        if upto + b.chance >= r:
            return b
        upto += b.chance
    return items[-1]


class BiomeCardCog(commands.Cog):
    def __init__(self, bot: commands.Bot, inventory: InventoryService | None = None):
        self.bot = bot
        self.inventory = inventory or InventoryService()
        self.biomes = DEFAULT_BIOMES

    # Helper: render biome embed
    def _biome_embed(self, user: discord.User | discord.Member, biome: BiomeInfo) -> discord.Embed:
        e = discord.Embed(title=f"Biome Unlocked: {biome.name}", description=biome.description, color=0x2ecc71)
        e.add_field(name="Rarity", value=biome.rarity)
        e.add_field(name="Bonus", value=f"+{biome.bonus['xp']} XP, +{biome.bonus['coins']} coins, +{biome.bonus['drop_bonus']}% drops")
        e.add_field(name="Structures", value=", ".join(biome.structures), inline=False)
        e.add_field(name="Mobs", value=", ".join(biome.mobs), inline=False)
        e.add_field(name="Chest Types", value=", ".join(biome.chest_types), inline=False)
        e.set_footer(text=f"Requested by {user.display_name}")
        return e

    # Prefix command to open a biome card
    @commands.command(name="openbiome", aliases=["open_card", "biomecard"])
    async def open_biome_prefix(self, ctx: commands.Context):
        user_id = ctx.author.id
        has_card = await self.inventory.consume_biome_card(user_id)
        if not has_card:
            return await ctx.reply("You don't have a Biome Card. Buy one in the shop!")

        biome = weighted_choice(self.biomes)
        await self.inventory.add_xp(user_id, biome.bonus.get("xp", 0))
        await self.inventory.add_currency(user_id, biome.bonus.get("coins", 0))

        await ctx.reply(embed=self._biome_embed(ctx.author, biome))

    # Slash command to open a biome card
    @discord.app_commands.command(name="openbiome", description="Open a Biome Card to discover a random biome")
    async def open_biome_slash(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        has_card = await self.inventory.consume_biome_card(user_id)
        if not has_card:
            return await interaction.response.send_message("You don't have a Biome Card. Buy one in the shop!", ephemeral=True)

        biome = weighted_choice(self.biomes)
        await self.inventory.add_xp(user_id, biome.bonus.get("xp", 0))
        await self.inventory.add_currency(user_id, biome.bonus.get("coins", 0))

        await interaction.response.send_message(embed=self._biome_embed(interaction.user, biome))

    # Admin: give biome cards
    @commands.has_permissions(manage_guild=True)
    @commands.command(name="givebiomecard")
    async def give_biome_card(self, ctx: commands.Context, member: discord.Member, amount: int = 1):
        amount = max(1, min(100, amount))
        await self.inventory.add_biome_card(member.id, amount)
        await ctx.reply(f"Gave {amount} Biome Card(s) to {member.display_name}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(BiomeCardCog(bot))
