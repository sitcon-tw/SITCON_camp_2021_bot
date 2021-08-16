from datetime import datetime
from discord.ext import commands

import message
from config import CONFIG
from core.classes import Cog_extension
from database import db
from task import (
    get_all_tasks,
    get_task_by_id,
    get_answer_by_password,
)
from utils import (
    get_group_id_by_bot_channel,
    get_group_id_by_guild,
    BotChannelOnly,
    is_in_bot_channel,
    EscapeNotStarted,
    EscapeEnded,
    is_escape_running,
    ScoreboardFrozen,
    is_scoreboard_available,
)


class Escape(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('>>Escape Ready!<<')

    @commands.command()
    @commands.check(is_in_bot_channel)
    @commands.check(is_escape_running)
    async def solve(self, ctx, task_id: str, *, password: str):
        '''
        Log every single submission into database

        Trigger hint if the submitted password is close enough
        '''
        group_id = get_group_id_by_bot_channel(ctx.channel)
        print(f'[escape] group {group_id} tried to solve {task_id} with <{password}>')

        task = get_task_by_id(task_id)

        if task is None:
            await ctx.send(message.TASK_UNKNOWN)
            return

        if 'available_after' in task:
            now = datetime.now()
            available_after = datetime.fromisoformat(task['available_after'])
            if now < available_after:
                await ctx.send(message.TASK_UNKNOWN)
                return

        res, err = db.get_submissions_statistics(group_id, task_id)
        if err is not None:
            await ctx.send(message.UNKNOWN_ERROR)
            return
        else:
            success_count, failed_count = res

        if success_count > 0:
            await ctx.send(message.TASK_ALREADY_SOLVED)
            return

        if 'max_attempt' in task and failed_count >= task['max_attempt']:
            await ctx.send(message.TASK_NO_ATTEMPT_REMAINED)
            return

        answer = get_answer_by_password(password, task['answers'])

        # answer not acceptable
        if answer is None:
            db.log_submission(group_id, task_id, password, False)
            await ctx.send(task['wrong_message'])
            return

        # log the submission
        if 'log' not in answer or answer['log'] is True:
            db.log_submission(group_id, task_id, password, answer['is_correct'])

        await ctx.send(answer['message'])
        print(f'[escape] group {group_id} solved {task_id}')

    @solve.error
    async def solve_error(self, ctx, error):
        if isinstance(error, EscapeNotStarted):
            return

        if isinstance(error, EscapeEnded):
            await ctx.send(message.ESCAPE_ENDED)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(message.COMMAND_USAGE.format(command='//solve <task_id> <password>'))
            return

        if isinstance(error, BotChannelOnly):
            group_id = get_group_id_by_guild(ctx.guild)
            group = self.bot.get_channel(CONFIG['CHANNEL_BOT'][group_id])
            await ctx.send(message.GO_TO_CHANNEL.format(channel=group.mention))
            return

    @commands.command()
    @commands.check(is_scoreboard_available)
    @commands.check(is_in_bot_channel)
    @commands.check(is_escape_running)
    async def scoreboard(self, ctx):
        '''
        Show current scoreboard

        TODO: frozen before ended
        '''
        res, err = db.get_scoreboard()

        if err is not None:
            await ctx.send(message.UNKNOWN_ERROR)
            return

        tasks = get_all_tasks()

        header = 'Task ID'
        max_task_id_length = max(
            max(map(lambda task: len(task['task_id']), tasks)),
            len(header),
        )
        table = '''```══════════════════════════════════════════════════════════════════
 {header:^{width}}  Point   1️⃣   2️⃣   3️⃣   4️⃣   5️⃣   6️⃣   7️⃣   8️⃣   9️⃣
══════════════════════════════════════════════════════════════════
'''.format(header=header, width=max_task_id_length)
        table = '''``` {header:^{width}}  Point   1️⃣   2️⃣   3️⃣   4️⃣   5️⃣   6️⃣   7️⃣   8️⃣   9️⃣ \n'''.format(header=header, width=max_task_id_length)

        table_row = ' {task_id:^{width}}  {point:^5}   '

        #  table_delimiter = '──────────────────────────────────────────────────────────────────'

        #  table_footer = '══════════════════════════════════════════════════════════════════```'
        table_footer = '```'

        for idx, task in enumerate(tasks):
            # would hit the limit of length 2000
            #  if idx:
            #      table += table_delimiter

            if 'available_after' in task:
                now = datetime.now()
                available_after = datetime.fromisoformat(task['available_after'])
                if now < available_after:
                    continue

            row = table_row.format(
                task_id=task['task_id'],
                width=max_task_id_length,
                point=task['point']
            )

            for group_id in range(1, 10):
                if group_id > 1:
                    row += '   '

                row += {
                    -1: '❌',
                    0: '⬛',
                    1: '⭐',
                }[res[group_id][task['task_id']]]

            table += row + '\n'

        table += table_footer

        await ctx.send(table)

    @scoreboard.error
    async def scoreboard_error(self, ctx, error):
        if isinstance(error, EscapeNotStarted):
            return

        if isinstance(error, EscapeEnded):
            await ctx.send(message.ESCAPE_ENDED)
            return

        if isinstance(error, ScoreboardFrozen):
            await ctx.send(message.SCOREBOARD_FROZEN)
            return


def setup(bot):
    bot.add_cog(Escape(bot))
