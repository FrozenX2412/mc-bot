# chests.py
# See cogs version in previous file; this is path fix when adding from root.
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import discord
from discord.ext import commands

CoinsRange = Tuple[int, int]
XpRange = Tuple[int, int]

@dataclass(frozen=True)
class LootItem:
    name: str
    chance: float
    min_qty: int = 1
    max_qty: int = 1

@dataclass(frozen=True)
class ChestTier:
    key: str
    display: str
    weights: float
    coins: CoinsRange
    xp: XpRange
    items: List[LootItem]
    special_notes: str = ""

TIERS: Dict[str, ChestTier] = {}

# populate tiers (same data as earlier page write)
TIERS.update({
    "Common": ChestTier(
        key="Common", display="Common Chest", weights=55.0,
        coins=(15, 45), xp=(5, 12),
        items=[LootItem("Wood", 25, 2, 6), LootItem("Stone", 20, 2, 5), LootItem("Leather", 18, 1, 3), LootItem("Small Potion", 15, 1, 2), LootItem("Copper Ore", 12, 1, 3), LootItem("Old Map Fragment", 10, 1, 1)],
        special_notes="Basic supplies and small boosts.",
    ),
    "Rare": ChestTier(
        key="Rare", display="Rare Chest", weights=25.0,
        coins=(40, 110), xp=(10, 25),
        items=[LootItem("Iron Ingot", 22, 1, 3), LootItem("Healing Potion", 18, 1, 2), LootItem("Enchanted Leaf", 14, 1, 2), LootItem("Silver Ore", 14, 1, 3), LootItem("Traveler's Charm", 12, 1, 1), LootItem("Rare Map Fragment", 10, 1, 1)],
        special_notes="Better materials and utility items.",
    ),
    "Epic": ChestTier(
        key="Epic", display="Epic Chest", weights=12.0,
        coins=(120, 260), xp=(25, 60),
        items=[LootItem("Gold Ingot", 22, 1, 3), LootItem("Elixir of Swiftness", 18, 1, 2), LootItem("Jungle Relic", 15, 1, 1), LootItem("Rune Stone", 15, 1, 2), LootItem("Obsidian Shard", 12, 1, 2), LootItem("Epic Map Fragment", 10, 1, 1)],
        special_notes="Valuable crafting and rare relics.",
    ),
    "Mythic": ChestTier(
        key="Mythic", display="Mythic Chest", weights=6.0,
        coins=(260, 520), xp=(60, 120),
        items=[LootItem("Diamond", 20, 1, 2), LootItem("Phoenix Feather", 18, 1, 1), LootItem("Magma Core", 15, 1, 1), LootItem("Void-Touched Gem", 12, 1, 1), LootItem("Ancient Rune", 12, 1, 2), LootItem("Mythic Map Fragment", 10, 1, 1)],
        special_notes="Top-tier mats and powerful curios.",
    ),
    "Legendary Void": ChestTier(
        key="Legendary Void", display="Legendary Void Chest", weights=2.0,
        coins=(600, 1200), xp=(120, 240),
        items=[LootItem("Void Crown", 12, 1, 1), LootItem("Entropy Crystal", 16, 1, 1), LootItem("Phantom Silk", 18, 1, 2), LootItem("Prismatic Core", 14, 1, 1), LootItem("Legendary Rune", 20, 1, 1), LootItem("Legendary Map Fragment", 10, 1, 1)],
        special_notes="Exclusive endgame items and high rewards.",
    ),
})


def weighted_pick_tier(allowed: List[str]) -> ChestTier:
    pool = [TIERS[k] for k in allowed]
    total = sum(t.weights for t in pool)
    r = random.uniform(0, total)
    upto = 0.0
    for t in pool:
        if upto + t.weights >= r:
            return t
        upto += t.weights
    return pool[-1]


def roll_items(tier: ChestTier) -> List[Tuple[str, int]]:
    results: List[Tuple[str, int]] = []
    count = random.randint(1, 3)
    table = tier.items
    total = sum(i.chance for i in table)
    for _ in range(count):
        r = random.uniform(0, total)
        upto = 0.0
        chosen = table[-1]
        for it in table:
            if upto + it.chance >= r:
                chosen = it
                break
            upto += it.chance
        qty = random.randint(chosen.min_qty, chosen.max_qty)
        results.append((chosen.name, qty))
    return results


class ChestsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="openchest")
    async def open_chest_prefix(self, ctx: commands.Context, tier_key: str):
        tier_key = tier_key.title().replace("_", " ")
        if tier_key not in TIERS:
            return await ctx.reply("Unknown chest tier. Try: Common, Rare, Epic, Mythic, Legendary Void")
        tier = TIERS[tier_key]
        coins = random.randint(*tier.coins)
        xp = random.randint(*tier.xp)
        items = roll_items(tier)
        e = discord.Embed(title=f"Opened {tier.display}", color=0xf1c40f)
        e.add_field(name="Coins", value=str(coins))
        e.add_field(name="XP", value=str(xp))
        e.add_field(name="Items", value="\n".join(f"{n} x{q}" for n, q in items), inline=False)
        e.set_footer(text=tier.special_notes)
        await ctx.reply(embed=e)

    @discord.app_commands.command(name="openchest", description="Open a chest by tier key")
    async def open_chest_slash(self, interaction: discord.Interaction, tier_key: str):
        tier_key = tier_key.title().replace("_", " ")
        if tier_key not in TIERS:
            return await interaction.response.send_message("Unknown chest tier. Try: Common, Rare, Epic, Mythic, Legendary Void", ephemeral=True)
        tier = TIERS[tier_key]
        coins = random.randint(*tier.coins)
        xp = random.randint(*tier.xp)
        items = roll_items(tier)
        e = discord.Embed(title=f"Opened {tier.display}", color=0xf1c40f)
        e.add_field(name="Coins", value=str(coins))
        e.add_field(name="XP", value=str(xp))
        e.add_field(name="Items", value="\n".join(f"{n} x{q}" for n, q in items), inline=False)
        e.set_footer(text=tier.special_notes)
        await interaction.response.send_message(embed=e)


async def setup(bot: commands.Bot):
    await bot.add_cog(ChestsCog(bot))
