from discord.ext import commands
import aiosqlite
import discord
import random
from discord import Embed, Guild, Color, File, Interaction, ButtonStyle
from discord.ui import Button, View, button
from hentai import *

async def create_page_embed(book, number: int):
    tags = [i.name for i in book.tag]
    language_tags = [i.name for i in book.language]
    artists = [i.name for i in book.artist]
    urls = [i.url for i in book.artist]
    embed = discord.Embed(title=f"{book.title(Format.Pretty)}", color = discord.Color.purple())
    pages = [i.url for i in book.pages]
    embed.set_image(url=pages[number])
    strings = []
    for index, value in enumerate(artists):
        string = f"[{value}]({urls[index]})"
        strings.append(string)
    description=f"[Click Here]({book.url})\nTags: {', '.join(tags)}\nLanguage tags: {', '.join(language_tags)}\nPages: {book.num_pages}\nArtists: {', '.join(strings)}"
    embed.description = description
    embed.set_footer(text=f"Page Number: {number+1} | Id: {book.id}")
    return embed

async def get_blacklist_data():
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM 'blacklist'")
    users = await cursor.fetchall()
    await conn.commit()
    f_users = []
    for row in users:
        f_users.append(row[0])
    return f_users

async def remove_blacklist(user: discord.User):
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute(f"DELETE FROM 'blacklist' WHERE id = '{user.id}'")
    await conn.commit()

async def add_blacklist(user: discord.User):
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute(f"INSERT INTO 'blacklist' (id) VALUES ('{user.id}')")
    await conn.commit()

async def check_blacklist(user: discord.User):
    users = await get_blacklist_data()
    if user.id in users:
        return True
    else:
        return False

def check_channel(channel):
    if channel.is_nsfw():
        return True
    return False

async def get_share_data():
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM 'shares'")
    users = await cursor.fetchall()
    await conn.commit()
    f_users = []
    for row in users:
        f_users.append(row[0])
    return f_users

async def change_shares(user: discord.User):
    users = await get_share_data()
    if user.id in users:
        await remove_shares(user)
        return "OFF"
    else:
        await add_shares(user)
        return "ON"

async def remove_shares(user: discord.User):
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute(f"DELETE FROM 'shares' WHERE id = '{user.id}'")
    await conn.commit()

async def add_shares(user: discord.User):
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute(f"INSERT INTO 'shares' (id) VALUES ('{user.id}')")
    await conn.commit()

async def check_shares(user: discord.User):
    users = await get_share_data()
    if user.id in users:
        return True
    else:
        return False

async def unsave(user: discord.User, id: int):
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute(f"DELETE FROM '{user.id}' WHERE id = '{id}'")
    await conn.commit()

async def save(user: discord.User, id: int):
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute(f"INSERT INTO '{user.id}' (id) VALUES ('{id}')")
    await conn.commit()

async def create_table_if_not_exists(user: discord.Member):
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute(f'CREATE TABLE IF NOT EXISTS "{user.id}" (id INTEGER)')
    await conn.commit()

async def get_save_data(user: discord.Member):
    await create_table_if_not_exists(user)
    conn = await aiosqlite.connect("database.db")
    cursor = await conn.cursor()
    await cursor.execute(f"SELECT * FROM '{user.id}'")
    rows = await cursor.fetchall()
    await conn.commit()
    doujins = []
    for row in rows:
        doujins.append(row[0])
    return doujins

async def create_embed(book):
    tags = [i.name for i in book.tag]
    language_tags = [i.name for i in book.language]
    artists = [i.name for i in book.artist]
    urls = [i.url for i in book.artist]
    embed = discord.Embed(title=f"{book.title(Format.Pretty)}", color = discord.Color.purple())
    embed.set_image(url=book.cover)
    embed.set_author(name=book.id)
    strings = []
    for index, value in enumerate(artists):
        string = f"[{value}]({urls[index]})"
        strings.append(string)
    description=f"[Click Here]({book.url})\nTags: {', '.join(tags)}\nLanguage tags: {', '.join(language_tags)}\nPages: {book.num_pages}\nArtists: {', '.join(strings)}"
    embed.description = description
    return embed

def get_mods():
    with open("mods.json", "r") as f:
        data = json.load(f)

    return data["mods"]

async def play(ctx, channel: discord.TextChannel, book: Hentai, tag = None):
    page_number = 0
    view = PlayView(ctx, book, page_number, tag)
    embed = await create_page_embed(book, 0)
    await channel.send(embed=embed, view=view, delete_after=900)

async def join_embed(guild: Guild):
    file = File("./resources/logo.png", filename="image.png")
    embed = Embed(title=f"Thanks for adding me to {guild.name}, I'm glad to be here!", description="I'm a bot that interacts with the nhentai API and lets you read doujins inside discord. I have tons of cool features, type `!help` to start using me!\n[Click Here](https://github.com/TheLLaw/)", color=Color.purple())
    embed.set_author(name="Law")
    embed.set_image(url="attachment://image.png")
    return file, embed

class ShareView(View):
    def __init__(self, context, book_number, books, member):
        self.member = member
        self.books = books
        self.book_number = book_number
        self.ctx = context
        super().__init__(timeout=600)

    @button(label="⬅", style=ButtonStyle.blurple)
    async def left_callback(self, button, interaction: Interaction):
        if self.book_number < 1:
            await interaction.response.send_message("First Book!", delete_after=5)
            return
        self.book_number -= 1
        doujin = Hentai(self.books[self.book_number])
        embed = await create_embed(doujin)
        await interaction.response.edit_message(embed=embed, delete_after=900)

    @button(label="Share", style=ButtonStyle.grey)
    async def share_callback(self, button, interaction: Interaction):
        embed = await create_embed(Hentai(self.books[self.book_number]))
        embed.set_footer(text=f"Book shared by {interaction.user}")
        try:
            await self.member.send(embed=embed)
            await interaction.response.send_message("Shared book with user!")
        except discord.Forbidden:
            await interaction.response.send_message("Couldn't share book with user because they have their dms closed.")

    @button(style=ButtonStyle.danger, label="❌")
    async def close_callback(self, button, interaction: Interaction):
        self.stop()
        await interaction.message.delete()
    
    @button(label="➡", style=ButtonStyle.blurple)
    async def right_callback(self, button, interaction: Interaction):
        if (self.book_number+1) == len(self.books):
            await interaction.response.send_message("Last Book!", delete_after=5)
            return
        self.book_number += 1
        doujin = Hentai(self.books[self.book_number])
        embed = await create_embed(doujin)
        await interaction.response.edit_message(embed=embed, delete_after=900)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Don't touch his stuff bro!!!", ephemeral=True)
            return False
        return True

class SavedView(View):
    def __init__(self, context, books, book_number):
        self.ctx = context
        self.books = books
        self.book_number = book_number
        super().__init__(timeout=600)
    
    @button(style=ButtonStyle.blurple, label="⬅")
    async def left_callback(self, button, interaction: Interaction):
        if self.book_number < 1:
            await interaction.response.send_message("First Book!", delete_after=5)
            return
        self.book_number -= 1
        doujin = Hentai(self.books[self.book_number])
        embed = await create_embed(doujin)
        await interaction.response.edit_message(embed=embed, delete_after=900)

    @button(style=ButtonStyle.danger, label="❌")
    async def close_callback(self, button, interaction: Interaction):
        self.stop()
        await interaction.message.delete()

    @button(style=ButtonStyle.grey, label="Unsave")
    async def unsave_callback(self, button, interaction: Interaction):
        await unsave(interaction.user, self.books[self.book_number])
        await interaction.response.send_message(f"Deleted book: {self.books[self.book_number]} from your collections!")

    @button(style=ButtonStyle.green, label="⏯")
    async def play_callback(self, button, interaction: Interaction):
        self.stop()
        book = Hentai(self.books[self.book_number])
        await interaction.message.delete()
        await play(self.ctx, self.ctx.channel, book)

    @button(style=ButtonStyle.blurple, label="➡")
    async def right_callback(self, button, interaction: Interaction):
        if (self.book_number+1) == len(self.books):
            await interaction.response.send_message("Last Book!", delete_after=5)
            return
        self.book_number += 1
        doujin = Hentai(self.books[self.book_number])
        embed = await create_embed(doujin)
        await interaction.response.edit_message(embed=embed, delete_after=900)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Hey don't touch other peoples stuff!!!", ephemeral=True)
            return False
        return True

class PlayView(View):
    def __init__(self, context, book, page_number, tag):
        self.ctx = context
        self.book = book
        self.page_number = page_number
        self.tag = tag
        super().__init__(timeout=600)
    
    @button(style=ButtonStyle.blurple, label="⬅")
    async def left_callback(self, button, interaction: Interaction):
        if (self.page_number-1) < 0:
            await interaction.response.send_message("First page!", delete_after=5)
            return
        self.page_number -= 1
        embed = await create_page_embed(self.book, self.page_number)
        await interaction.response.edit_message(embed=embed, delete_after=900)

    @button(style=ButtonStyle.danger, label="❌")
    async def close_callback(self, button, interaction: Interaction):
        self.stop()
        await interaction.message.delete()


    @button(style=ButtonStyle.blurple, label="🔄")
    async def random_callback(self, button, interaction: Interaction):
        await interaction.message.delete()
        if not self.tag:
            id = Utils.get_random_id()
            self.book = Hentai(id)
            await play(self.ctx, interaction.channel, self.book)
        else:
            popular_loli = list(Utils.search_by_query(f'tag:{self.tag}', sort=Sort.PopularWeek))
            await play(interaction.channel, random.choice(popular_loli))


    @button(style=ButtonStyle.green, label="Save")
    async def save_callback(self, button, interaction: Interaction):
        await create_table_if_not_exists(interaction.user)
        saves = await get_save_data(interaction.user)
        if self.book.id in saves:
            await interaction.response.send_message("Already saved that one!")
            return
        await save(interaction.user, self.book.id)
        await interaction.response.send_message(f"User: {interaction.user} just saved this book.")


    @button(style=ButtonStyle.blurple, label="➡")
    async def right_callback(self, button, interaction: Interaction):
        if (self.page_number+1) > self.book.num_pages:
            await interaction.response.send_message("Last page!", delete_after=5)
            return
        self.page_number += 1
        embed = await create_page_embed(self.book, self.page_number)
        await interaction.response.edit_message(embed=embed, delete_after=900)


    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("hey my man don't interrupt burh my brotha fapin", ephemeral=True)
            return False
        return True