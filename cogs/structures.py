# structures.py
# Comet Assistant generated cog for Structures system
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Dict, List

import discord
from discord.ext import commands

@dataclass(frozen=True)
class Structure:
    key: str
    name: str
    difficulty: int
    xp_bonus: int
    coins_bonus: int
    drop_bonus_percent: int
    description: str

STRUCTURES: Dict[str, Structure] = {
    # Common Plains
    "Village": Structure(
        "Village", "Village", 1, 5, 10, 2,
        "Peaceful settlement with basic supplies."
    ),
    "Windmill": Structure(
        "Windmill", "Windmill", 2, 4, 8, 1,
        "Grinding structure with stored grain."
    ),
    "Abandoned Farm": Structure(
        "Abandoned Farm", "Abandoned Farm", 2, 6, 12, 2,
        "Overgrown fields with lingering loot."
    ),
    # Common Forest
    "Treehouse": Structure(
        "Treehouse", "Treehouse", 3, 8, 15, 3,
        "Hidden canopy hideout."
    ),
    "Ranger Camp": Structure(
        "Ranger Camp", "Ranger Camp", 2, 6, 10, 2,
        "Outpost with survival gear."
    ),
    "Mossy Ruins": Structure(
        "Mossy Ruins", "Mossy Ruins", 3, 10, 18, 4,
        "Ancient stones reclaimed by nature."
    ),
    # Uncommon Desert
    "Desert Temple": Structure(
        "Desert Temple", "Desert Temple", 4, 15, 25, 5,
        "Sandstone monument guarding treasures."
    ),
    "Oasis": Structure(
        "Oasis", "Oasis", 3, 10, 20, 3,
        "Life in the wasteland. Respite and rewards."
    ),
    "Sand Ruins": Structure(
        "Sand Ruins", "Sand Ruins", 4, 12, 22, 4,
        "Half-buried remnants from lost age."
    ),
    "Pillar Site": Structure(
        "Pillar Site", "Pillar Site", 3, 10, 18, 3,
        "Carved pillars with forgotten scripts."
    ),
    # Uncommon Snow
    "Igloo": Structure(
        "Igloo", "Igloo", 2, 8, 15, 2,
        "Cozy shelter with emergency caches."
    ),
    "Ice Cavern": Structure(
        "Ice Cavern", "Ice Cavern", 4, 14, 24, 5,
        "Crystalline grotto hiding rare resources."
    ),
    "Frost Tower": Structure(
        "Frost Tower", "Frost Tower", 5, 16, 28, 6,
        "Sentinel tower encased in eternal ice."
    ),
    # Rare Jungle
    "Jungle Ruins": Structure(
        "Jungle Ruins", "Jungle Ruins", 5, 18, 30, 6,
        "Vine-choked temples of ancient civilization."
    ),
    "Overgrown Shrine": Structure(
        "Overgrown Shrine", "Overgrown Shrine", 5, 16, 28, 5,
        "Altar reclaimed by jungle, still potent."
    ),
    "Canopy Bridge": Structure(
        "Canopy Bridge", "Canopy Bridge", 4, 14, 24, 4,
        "Rope and wood suspended high above."
    ),
    "Vine Labyrinth": Structure(
        "Vine Labyrinth", "Vine Labyrinth", 6, 20, 32, 7,
        "Natural maze teeming with danger."
    ),
    # Rare Cave
    "Crystal Chamber": Structure(
        "Crystal Chamber", "Crystal Chamber", 6, 20, 35, 7,
        "Sparkling cavity with rich veins."
    ),
    "Mine Shaft": Structure(
        "Mine Shaft", "Mine Shaft", 5, 16, 28, 6,
        "Abandoned mine with ore and echoes."
    ),
    "Stalagmite Hall": Structure(
        "Stalagmite Hall", "Stalagmite Hall", 5, 18, 30, 6,
        "Grand cavern formation concealing caches."
    ),
    # Epic Volcano
    "Lava Fortress": Structure(
        "Lava Fortress", "Lava Fortress", 7, 25, 45, 8,
        "Basalt stronghold surrounded by molten flows."
    ),
    "Basalt Keep": Structure(
        "Basalt Keep", "Basalt Keep", 7, 24, 42, 8,
        "Fire-resistant tower with forges."
    ),
    "Magma Fissure": Structure(
        "Magma Fissure", "Magma Fissure", 6, 22, 40, 7,
        "Deep crack spewing lava and riches."
    ),
    # Epic Wasteland
    "Ruined Bunker": Structure(
        "Ruined Bunker", "Ruined Bunker", 7, 26, 48, 8,
        "Pre-collapse shelter with equipment."
    ),
    "Ashen City": Structure(
        "Ashen City", "Ashen City", 8, 28, 50, 9,
        "Ghostly metropolis once thriving."
    ),
    "Scorched Obelisk": Structure(
        "Scorched Obelisk", "Scorched Obelisk", 7, 25, 46, 8,
        "Monolith bearing dire warnings."
    ),
    # Rare Skylands
    "Cloud Temple": Structure(
        "Cloud Temple", "Cloud Temple", 6, 20, 36, 7,
        "Floating shrine among clouds."
    ),
    "Sky Bridge": Structure(
        "Sky Bridge", "Sky Bridge", 5, 18, 32, 6,
        "Thin walkway crossing sky islands."
    ),
    "Aerial Nest": Structure(
        "Aerial Nest", "Aerial Nest", 6, 22, 38, 7,
        "Harpy roost with looted trinkets."
    ),
    # Legendary Void
    "Void Castle": Structure(
        "Void Castle", "Void Castle", 10, 40, 80, 12,
        "Fortress suspended in timeless darkness."
    ),
    "Fracture Spire": Structure(
        "Fracture Spire", "Fracture Spire", 9, 36, 70, 11,
        "Twisting tower that breaks reality."
    ),
    "Endless Stair": Structure(
        "Endless Stair", "Endless Stair", 9, 38, 75, 12,
        "Staircase looping through paradoxes."
    ),
}


def pick_structure(keys: List[str]) -> Structure:
    return STRUCTURES[random.choice(keys)]


class StructuresCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="viewstructure")
    async def view_structure_prefix(self, ctx: commands.Context, structure_key: str):
        structure_key = structure_key.title().replace("_", " ")
        if structure_key not in STRUCTURES:
            return await ctx.reply("Unknown structure.")
        s = STRUCTURES[structure_key]
        e = discord.Embed(title=f"Structure: {s.name}", description=s.description, color=0x3498db)
        e.add_field(name="Difficulty", value=str(s.difficulty))
        e.add_field(name="Bonuses", value=f"+{s.xp_bonus} XP, +{s.coins_bonus} coins, +{s.drop_bonus_percent}% drops")
        await ctx.reply(embed=e)

    @discord.app_commands.command(name="viewstructure", description="View details of a structure")
    async def view_structure_slash(self, interaction: discord.Interaction, structure_key: str):
        structure_key = structure_key.title().replace("_", " ")
        if structure_key not in STRUCTURES:
            return await interaction.response.send_message("Unknown structure.", ephemeral=True)
        s = STRUCTURES[structure_key]
        e = discord.Embed(title=f"Structure: {s.name}", description=s.description, color=0x3498db)
        e.add_field(name="Difficulty", value=str(s.difficulty))
        e.add_field(name="Bonuses", value=f"+{s.xp_bonus} XP, +{s.coins_bonus} coins, +{s.drop_bonus_percent}% drops")
        await interaction.response.send_message(embed=e)


async def setup(bot: commands.Bot):
    await bot.add_cog(StructuresCog(bot))
