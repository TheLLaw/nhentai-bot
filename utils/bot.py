import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord import Intents
from discord.ext.commands import Context
from discord import Guild
from utils import join_embed


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(
            command_prefix=when_mentioned_or("!"),
            description="A bot that interacts with nhentai's API",
            intents=Intents.all()
        )

    async def on_ready(self):
        print("Log number 3128: You clod!!")

    async def on_guild_join(self, guild: Guild):
        file, embed = await join_embed(guild)
        channels = guild.channels
        try:
            for channel in channels:
                if isinstance(channel, discord.TextChannel):
                    try:
                        await channel.send(file=file, embed=embed)
                        return
                    except discord.Forbidden:
                        pass
                else:
                    continue
        except Exception as pink:
            pass
