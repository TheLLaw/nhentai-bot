import asyncio
from discord.ext import commands
import discord
import random
from discord import Color, option
from discord import ApplicationContext
from aiohttp import ClientSession

guild_ids = [849673187222224936, 948223421953757255]

"""
Sfw commands are slash commands.

"""

class Sfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def make_request(keyword):
        async with ClientSession() as session:
            r = await session.get(f"https://api.waifu.pics/sfw/{keyword}")
            response = await r.json()
        try:
            return response["url"]
        except KeyError:
            return False

    @staticmethod
    async def make_embed(title, image) -> discord.Embed:
        embed = discord.Embed(title=title, color=Color.green())
        embed.set_image(url=image)
        return embed

    @commands.slash_command(name="meme", description="Memes fr!")
    async def _meme(self, ctx: ApplicationContext):
        async with ClientSession() as session:
            r = await session.get("https://meme-api.herokuapp.com/gimme")
        jr = await r.json()
        title = jr["title"]
        url = jr["url"]
        posturl = jr["postLink"]
        subreddit = jr["subreddit"]
        up_votes = jr["ups"]
        author = jr["author"]
        embed = discord.Embed(title=title, description=f"[Click Here]({posturl})", color=Color.green())
        embed.set_image(url=url)
        embed.set_footer(text=f"Made by {author} | Subreddit {subreddit} | {up_votes}👍")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="waifu", description="yes")
    @option(name="waifu_type", description="Waifu typesss", choices=["SFW", "NSFW"])
    async def _waifu(self, ctx: ApplicationContext, waifu_type: str):
        if waifu_type == "NSFW":
            if not ctx.channel.is_nsfw():
                await ctx.respond(f"This isn't an nsfw channel!", ephemeral=True)
                return
            categories = ["waifu", "neko", "trap", "blowjob"]
            await ctx.respond(f"Choose a category. ({', '.join(categories)})")

            def check(m):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=120)
                if msg.content not in categories:
                    await ctx.respond("You didn't choose from the available categories.", ephemeral=True)
                    return
                async with ClientSession() as session:
                    response = await session.get(f"https://api.waifu.pics/{waifu_type.lower()}/{msg.content}")
                    r = await response.json()
                url = r["url"]
                embed = discord.Embed(title="NSFW Waifu", color=Color.dark_purple())
                embed.set_image(url=url)
                await ctx.respond(embed=embed)
            except asyncio.TimeoutError:
                await ctx.respond("You took too long.", ephemeral=True)
                return
        if waifu_type == "SFW":
            categories = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss",
                          "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold",
                          "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe"]
            await ctx.respond(f"Choose a category ({', '.join(categories)})")

            def check(m):
                return m.author.id == ctx.author.id

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=120)
                if msg.content not in categories:
                    await ctx.respond("You didn't choose from the categories.")
                    return
                async with ClientSession() as session:
                    response = await session.get(f"https://api.waifu.pics/{waifu_type.lower()}/{msg.content}")
                    r = await response.json()
                url = r["url"]
                embed = discord.Embed(title="SFW Waifu", color=Color.nitro_pink())
                embed.set_image(url=url)
                await ctx.respond(embed=embed)
            except asyncio.TimeoutError:
                await ctx.respond("You took too long.")
                return

    @commands.slash_command(name="slap", description="Slap someone")
    @option(name="member", description="Choose a victim")
    async def _slap(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("*hugs you and comforts you*")
            return
        url = await Sfw.make_request("slap")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** just slapped {member.name}**", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="kiss", description="Kiss someone")
    @option(name="member", description="... Choose your loved one")
    async def _kiss(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("Weirdo...")
            return
        url = await Sfw.make_request("kiss")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** kissed {member.name}**", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="cuddle", description="Cuddle someone")
    @option(name="member", description="... Choose your loved one")
    async def _cuddle(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("Himself (L)")
            return
        url = await Sfw.make_request("cuddle")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** cuddled with {member.name}**", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="kick", description="Kick someone")
    @option(name="member", description="Choose who ur gonna beat the shit out of")
    async def _kick(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("o-o")
            return
        url = await Sfw.make_request("kick")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** just kicked {member.name}** in the ass", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="hug", description="Kick someone")
    @option(name="member", description="Choose who you're gonna share love with")
    async def _hug(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("***hugs you***")
            return
        url = await Sfw.make_request("hug")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** hugs **{member.name}**", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="lick", description="Lick someone")
    @option(name="member", description="Choose who you are gonna lick...")
    async def _lick(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("o-o")
            return
        chance = random.randint(1, 100)
        if chance == 14:
            embed = discord.Embed(title=f"**{ctx.author.name}** heals **{member.name}**", color = Color.nitro_pink())
            file = discord.File("./resources/easteregg.gif", filename="image.gif")
            embed.set_image(url="attachment://image.gif")
            embed.set_footer(text="A quite rare occurence.")
            await ctx.respond(embed=embed, file=file)
            return
        url = await Sfw.make_request("lick")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** licks **{member.name}**", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="pat", description="Pat someone")
    @option(name="member", description="Choose who you're gonna pat pat in the head")
    async def _pat(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("cringe")
            return
        url = await Sfw.make_request("pat")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** pats **{member.name}** in the head", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="highfive", description="Highfive your best friend")
    @option(name="member", description="your best friend goes here")
    async def _highfive(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("how")
            return
        url = await Sfw.make_request("highfive")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** and **{member.name}** highfive", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="handhold", description="hand hold with someone...")
    @option(name="member", description="ooohh")
    async def _handhold(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("sadge")
            return
        url = await Sfw.make_request("handhold")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** holds hands with **{member.name}**", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="bite", description="Bite someone")
    @option(name="member", description="Choose who ur gonna bite the shit out of")
    async def _bite(self, ctx: ApplicationContext, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.respond("seek medical help")
            return
        url = await Sfw.make_request("bite")
        embed = await Sfw.make_embed(f"**{ctx.author.name}** bites **{member.name}** rawr", url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="invite", description="Invite this beautiful bot to your OWN server")
    async def _invite(self, ctx: ApplicationContext):
        file = discord.File("./resources/logo.png", filename="image.png")
        embed = discord.Embed(title="Invite ME!",
                              description="[Click Here](https://discord.com/api/oauth2/authorize?client_id=819191547597553676&permissions=536401538113&scope=bot%20applications.commands)\nI would love to be in your server!",
                              color=Color.purple())
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text="Made by Law")
        await ctx.respond(embed=embed, file=file)


def setup(bot):
    bot.add_cog(Sfw(bot))
