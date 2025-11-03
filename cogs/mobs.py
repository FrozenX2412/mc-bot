# mobs.py
# Comet Assistant generated cog for Mobs and combat
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import discord
from discord.ext import commands

@dataclass(frozen=True)
class MobDrop:
    item: str
    chance: float  # percent
    min_qty: int = 1
    max_qty: int = 1

@dataclass(frozen=True)
class Mob:
    key: str
    name: str
    biome_rarity: str
    attack: int
    health: int
    difficulty: int  # 1-10
    abilities: List[str]
    drops: List[MobDrop]


MOBS: Dict[str, Mob] = {
    # Common
    "Zombie": Mob("Zombie", "Zombie", "Common", 6, 30, 2, ["Infectious Swipe"], [MobDrop("Rotten Flesh", 45, 1, 3), MobDrop("Copper Coin", 30, 2, 6)]),
    "Skeleton": Mob("Skeleton", "Skeleton", "Common", 7, 28, 3, ["Piercing Arrow"], [MobDrop("Bone", 50, 1, 3), MobDrop("Arrow", 30, 3, 6)]),
    "Spider": Mob("Spider", "Spider", "Common", 5, 26, 3, ["Web Snare"], [MobDrop("Silk", 40, 1, 2), MobDrop("Venom Gland", 20, 1, 1)]),
    # Uncommon
    "Husk": Mob("Husk", "Husk", "Uncommon", 9, 40, 4, ["Sand Daze"], [MobDrop("Dried Husk", 40, 1, 2), MobDrop("Iron Scrap", 18, 1, 2)]),
    "Stray": Mob("Stray", "Stray", "Uncommon", 10, 42, 4, ["Frostbite"], [MobDrop("Frost Arrow", 30, 2, 4), MobDrop("Ice Shard", 20, 1, 2)]),
    "Scorpion": Mob("Scorpion", "Scorpion", "Uncommon", 11, 36, 5, ["Poison Sting"], [MobDrop("Scorpion Tail", 25, 1, 1), MobDrop("Chitin", 35, 1, 2)]),
    # Rare
    "Jaguar": Mob("Jaguar", "Jaguar", "Rare", 14, 60, 6, ["Pounce", "Bleed"], [MobDrop("Jaguar Pelt", 35, 1, 1), MobDrop("Fang", 20, 1, 2)]),
    "Cave Spider": Mob("Cave Spider", "Cave Spider", "Rare", 13, 55, 6, ["Poison Bite"], [MobDrop("Toxic Silk", 30, 1, 2), MobDrop("Glow Sac", 18, 1, 1)]),
    "Harpy": Mob("Harpy", "Harpy", "Rare", 12, 58, 6, ["Screech"], [MobDrop("Feather", 38, 2, 4), MobDrop("Wind Essence", 15, 1, 1)]),
    # Epic
    "Fire Golem": Mob("Fire Golem", "Fire Golem", "Epic", 22, 120, 8, ["Lava Slam", "Burning Aura"], [MobDrop("Magma Core", 28, 1, 1), MobDrop("Charred Plate", 22, 1, 2)]),
    "Blaze Captain": Mob("Blaze Captain", "Blaze Captain", "Epic", 20, 110, 8, ["Flame Volley"], [MobDrop("Blaze Rod", 30, 1, 2), MobDrop("Cinder", 20, 2, 4)]),
    "Ash Wraith": Mob("Ash Wraith", "Ash Wraith", "Epic", 19, 105, 8, ["Smoke Veil", "Life Drain"], [MobDrop("Wraith Dust", 25, 1, 2), MobDrop("Ashen Cloth", 25, 1, 2)]),
    # Legendary
    "Phantom King": Mob("Phantom King", "Phantom King", "Legendary", 30, 200, 10, ["Void Rift", "Phantom Lance"], [MobDrop("Void Crown", 10, 1, 1), MobDrop("Phantom Silk", 30, 1, 2)]),
    "Null Shade": Mob("Null Shade", "Null Shade", "Legendary", 26, 180, 9, ["Phase Shift"], [MobDrop("Entropy Crystal", 12, 1, 1), MobDrop("Shadow Fragment", 22, 1, 2)]),
}


def roll_mob(mob_keys: List[str]) -> Mob:
    # simple uniform among provided biome pool; difficulty comes from mob data
    return MOBS[random.choice(mob_keys)]


def simulate_combat(mob: Mob, player_attack: int = 18, player_health: int = 100) -> Tuple[bool, int, int]:
    # Very simple turn-based sim to produce a result; expandable later
    m_hp = mob.health
    p_hp = player_health
    while m_hp > 0 and p_hp > 0:
        # player hits
        m_hp -= max(1, player_attack - mob.difficulty)
        if m_hp <= 0:
            break
        # mob hits
        p_hp -= max(1, mob.attack - 5)
    return (p_hp > 0, max(0, p_hp), max(0, m_hp))


def roll_drops(mob: Mob) -> List[Tuple[str, int]]:
    results: List[Tuple[str, int]] = []
    for d in mob.drops:
        if random.uniform(0, 100) <= d.chance:
            qty = random.randint(d.min_qty, d.max_qty)
            results.append((d.item, qty))
    return results


class MobsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="fightmob")
    async def fight_mob_prefix(self, ctx: commands.Context, mob_key: str):
        mob_key = mob_key.title().replace("_", " ")
        if mob_key not in MOBS:
            return await ctx.reply("Unknown mob.")
        mob = MOBS[mob_key]
        win, p_hp, m_hp = simulate_combat(mob)
        drops = roll_drops(mob) if win else []
        e = discord.Embed(title=f"Encounter: {mob.name}", color=0xe74c3c if not win else 0x2ecc71)
        e.add_field(name="Result", value="Victory" if win else "Defeat")
        e.add_field(name="Player HP", value=str(p_hp))
        e.add_field(name="Mob HP", value=str(m_hp))
        if drops:
            e.add_field(name="Drops", value="\n".join(f"{n} x{q}" for n, q in drops), inline=False)
        await ctx.reply(embed=e)

    @discord.app_commands.command(name="fightmob", description="Fight a mob by key")
    async def fight_mob_slash(self, interaction: discord.Interaction, mob_key: str):
        mob_key = mob_key.title().replace("_", " ")
        if mob_key not in MOBS:
            return await interaction.response.send_message("Unknown mob.", ephemeral=True)
        mob = MOBS[mob_key]
        win, p_hp, m_hp = simulate_combat(mob)
        drops = roll_drops(mob) if win else []
        e = discord.Embed(title=f"Encounter: {mob.name}", color=0xe74c3c if not win else 0x2ecc71)
        e.add_field(name="Result", value="Victory" if win else "Defeat")
        e.add_field(name="Player HP", value=str(p_hp))
        e.add_field(name="Mob HP", value=str(m_hp))
        if drops:
            e.add_field(name="Drops", value="\n".join(f"{n} x{q}" for n, q in drops), inline=False)
        await interaction.response.send_message(embed=e)


async def setup(bot: commands.Bot):
    await bot.add_cog(MobsCog(bot))
