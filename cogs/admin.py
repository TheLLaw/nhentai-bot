from discord.ext import commands
import discord
import os
from utils import *


class Admin(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="blacklist", aliases=["bl"], hidden=True)
    async def _blacklist(self, ctx: commands.Context, user: discord.Member):
        if not ctx.author.id in get_mods():
            return
        if await check_blacklist(user):
            await ctx.reply("User is already blacklisted.")
            return
        await add_blacklist(user)
        await ctx.reply("User was blacklisted.")
        try:
            await user.send(
                "You were blacklisted from using all of my features by a mod. Talk to any bot moderator to see if you can get your name out of the blacklist... or you can always just get someone to lick you..")
        except discord.Forbidden:
            pass

    @commands.command(name="whitelist", aliases=["wl"], hidden=True)
    async def _whitelist(self, ctx: commands.Context, user: discord.Member):
        if not ctx.author.id in get_mods():
            return
        if not await check_blacklist(user):
            await ctx.reply("User isn't blacklisted.")
            return
        await remove_blacklist(user)
        await ctx.reply("User was whitelisted.")
        try:
            await user.send("You were whitelisted, that means you can use all of my features again!")
        except discord.Forbidden:
            pass

    @commands.command(name="madd", hidden=True)
    async def _madd(self, ctx, member: discord.Member):
        mods = get_mods()
        if ctx.author.id in mods:
            with open("mods.json", "w") as f:
                mods.append(member.id)
                data = {"mods": mods}
                json.dump(data, f)
        return

    @commands.command(name="mods", hidden=True)
    async def _mods(self, ctx):
        raw_mods = get_mods()
        if ctx.author.id in raw_mods:
            mods = []
            for mod in raw_mods:
                mods.append(str(mod))
            await ctx.send(f'{", ".join(mods)}', delete_after=5)
        return

    @commands.command(name="exit", aliases=["e"], hidden=True)
    async def _exit(self, ctx):
        if ctx.author.id in get_mods():
            await ctx.message.delete()
            os._exit(0)
        return


def setup(bot):
    bot.add_cog(Admin(bot))
