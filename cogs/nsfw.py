from discord.ext import commands
from discord.ext.commands import Context
import discord
from discord.ui import Button, View
import random
from hentai import Hentai, Utils, Sort
from utils import *


class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, context: Context, exception: commands.errors) -> None:
        if isinstance(exception, commands.CommandError):
            if str(exception).startswith("User is blacklisted from using the bot."):
                await context.reply("You are blacklisted from using any bot command. Please message my creator if this is an error. Thank you.")
                return
        else:
            raise exception

    @commands.command(name="random")
    async def _random(self, ctx):
        if not check_channel(ctx.channel):
            await ctx.reply("Channel must be NSFW to use that command.")
            return
        id = Utils.get_random_id()
        book = Hentai(id)
        await play(ctx, ctx.channel, book)

    @commands.command(name="unsave", aliases=["delete", "remove"])
    async def _unsave(self, ctx, id: int):
        books = await get_save_data(ctx.author)
        if id not in books:
            await ctx.send(f"Book id: {id} is not saved in your collections!")
            return
        await unsave(ctx.author, id)
        await ctx.send(f"Book: {id} was removed from your collections!")        

    @commands.command(name="save", aliases=["record", "add"])
    async def _save(self, ctx, id: int):
        books = await get_save_data(ctx.author)
        if id in books:
            await ctx.send(f"Book id: {id} is already saved in your collections!")
            return
        await save(ctx.author, id)
        await ctx.send(f"Book: {id} was saved in your collections!")

    @commands.user_command(name="Share books!", guild_ids=[849673187222224936])
    async def _share(self, ctx: discord.ApplicationContext, member: discord.Member):
        if not await check_shares(member):
            await ctx.respond(f"{member.name} does not have shares enabled!")
            return
        books = await get_save_data(ctx.author)
        if len(books) == 0:
            await ctx.respond("You have no saved books")
            return
        if len(books) == 1:
            embed = await create_embed(Hentai(books[0]))
            try:
                await member.send(embed=embed)
                await ctx.respond("Shared book with user!")
                return
            except discord.Forbidden:
                await ctx.respond("User has his dms closed!")
        await ctx.respond("Processing...", delete_after=1.5)
        book_number = 0
        view = ShareView(ctx, book_number, books, member)
        doujin = Hentai(books[0])
        embed = await create_embed(doujin)
        await ctx.send(embed=embed, view=view, delete_after=900)

    @commands.command(name="collections", aliases=["saved"])
    async def _saved(self, ctx: commands.Context):
        if not check_channel(ctx.channel):
            await ctx.reply("Channel must be NSFW to use that command.")
            return
        books = await get_save_data(ctx.author)
        if len(books) == 0:
            await ctx.send("You have no saved books!")
            return
        if len(books) == 1:
            book = Hentai(books[0])
            await play(ctx, ctx.channel, book)
            await ctx.message.delete()
        else:            
            book_number = 0
            view = SavedView(ctx, books, book_number)
            doujin = Hentai(books[0])
            embed = await create_embed(doujin)
            await ctx.send(embed=embed, view=view, delete_after=900)

    @commands.command(name="shares")
    async def _shares(self, ctx):
        onoff = await change_shares(ctx.author)
        await ctx.send(f"Successfully turned shares {onoff}!")
    
    @commands.command(name="tagsearch")
    async def _search(self, ctx, *, tag: str):
        if not check_channel(ctx.channel):
            await ctx.reply("Channel must be NSFW to use that command.")
            return
        popular_loli = list(Utils.search_by_query(f'tag:{tag}', sort=Sort.PopularWeek))
        await play(ctx, ctx.channel, random.choice(popular_loli), tag)

    @commands.command(name="hentai")
    async def _search_by_id(self, ctx, id: int):
        if not check_channel(ctx.channel):
            await ctx.reply("Channel must be NSFW to use that command.")
            return
        book = Hentai(id)
        if not book:
            await ctx.send("Book not found!")
            return
        await play(ctx, ctx.channel, book)


    @commands.command(name="info")
    async def _info(self, ctx: commands.Context):
        embed = discord.Embed(title="Info command", description="Bot I made on my freetime, please use!!\nPlease don't judge the code this was my first time working with views and It's obviously a test bot. I made this when pycord announced views and then decided to continue working on it without bothering to use classes cos im lazy.", color = discord.Color.nitro_pink())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Nsfw(bot))