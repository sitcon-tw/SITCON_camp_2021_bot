from discord.ext import commands
import os

from config import CONFIG


bot = commands.Bot(command_prefix='/')


# TODO: permissions
@bot.command()
async def load(ctx, extension):
    if os.path.isfile(f'./commands/{extension}.py'):
        bot.load_extension(f'commands.{extension}')
        await ctx.send(f'loaded extension \'{extension}\'!')
    else:
        await ctx.send(f'extension \'{extension}\' not found!')


# TODO: permissions
@bot.command()
async def unload(ctx, extension):
    if os.path.isfile(f'./commands/{extension}.py'):
        bot.unload_extension(f'commands.{extension}')
        await ctx.send(f'unloaded extension \'{extension}\'!')
    else:
        await ctx.send(f'extension \'{extension}\' not found!')


# TODO: permissions
@bot.command()
async def reload(ctx, extension):
    if os.path.isfile(f'./commands/{extension}.py'):
        bot.reload_extension(f'commands.{extension}')
        await ctx.send(f'reloaded extension \'{extension}\'!')
    else:
        await ctx.send(f'extension \'{extension}\' not found!')


if __name__ == '__main__':
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            bot.load_extension(f'commands.{filename[:-3]}')

    bot.run(os.getenv('TOKEN') or CONFIG['TOKEN'])
