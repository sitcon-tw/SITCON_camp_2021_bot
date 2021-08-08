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
    is_in_bot_channel,
    get_group_id_by_bot_channel,
    get_group_id_by_guild,
)


class Escape(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('>>Escape Ready!<<')

    @commands.command()
    @commands.check(is_in_bot_channel)
    async def solve(self, ctx, task_id: str, *, password: str):
        '''
        Log every single submission into database

        Trigger hint if the submitted password is close enough
        '''
        group_id = get_group_id_by_bot_channel(ctx.channel)
        print(f'[+] Group {group_id} solve task_id: {task_id} with password: <{password}>')

        task = get_task_by_id(task_id)

        if task is None:
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

    @solve.error
    async def solve_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(message.COMMAND_USAGE.format(command='/solve <task_id> <password>'))
        if isinstance(error, commands.CheckFailure):
            group_id = get_group_id_by_guild(ctx.guild)
            group = self.bot.get_channel(CONFIG['CHANNEL_BOT'][group_id])
            await ctx.send(message.GO_TO_CHANNEL.format(channel=group.mention))

    @commands.command()
    @commands.check(is_in_bot_channel)
    async def scoreboard(self, ctx):
        '''
        Show current scoreboard

        TODO: frozen before ended
        '''
        res, err = db.get_scoreboard()

        if err is not None:
            await ctx.send(message.UNKNOWN_ERROR)
            return

        table = '''```══════════════════════════════════════════════════════════════════
 Task ID  Point   1️⃣   2️⃣   3️⃣   4️⃣   5️⃣   6️⃣   7️⃣   8️⃣   9️⃣
══════════════════════════════════════════════════════════════════
'''

        table_row = ' {task_id:^7}  {point:^5}   '

        #  table_delimeter = '──────────────────────────────────────────────────────────────────'

        table_footer = '══════════════════════════════════════════════════════════════════```'

        for idx, task in enumerate(get_all_tasks()):
            # would hit the limit of length 2000
            #  if idx:
            #      table += table_delimeter

            row = table_row.format(
                task_id=task['task_id'],
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


def setup(bot):
    bot.add_cog(Escape(bot))
