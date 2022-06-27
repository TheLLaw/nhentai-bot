import os
from discord.ext.commands import Context, Command
from utils import Bot, check_blacklist
from discord.ext.commands import CommandError

bot = Bot()


@bot.before_invoke
async def check(ctx: Context):
    if await check_blacklist(ctx.author):
        raise CommandError("User is blacklisted from using the bot.")
    else:
        pass


@bot.after_invoke
async def delete_message(ctx: Context):
    if type(ctx.command) == Command:
        await ctx.message.delete()
    

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


bot.run("watCGwastdaiytwcwafawtwtpotwbiGAaPaS!")
