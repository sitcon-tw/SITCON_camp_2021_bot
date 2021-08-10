from discord.ext import commands
import os

from config import CONFIG


bot = commands.Bot(command_prefix='/')


if __name__ == '__main__':
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            bot.load_extension(f'commands.{filename[:-3]}')

    bot.run(os.getenv('TOKEN') or CONFIG['TOKEN'])
