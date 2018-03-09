import asyncio
import datetime
import json
import logging
import re
import os
from pathlib import Path

import discord
from discord.ext import commands


def config_load():
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, 'data/config.json')
    with open(filepath, 'r', encoding='utf-8-sig') as doc:
        #  Please make sure encoding is correct, especially after editing the config file
        return json.load(doc)


async def run():
    """
    Where the bot gets started. If you wanted to create an database connection pool or other session for the bot to use,
    it's recommended that you create it here and pass it to the bot as a kwarg.
    """

    config = config_load()
    bot = Bot(config=config,
              description=config['description'])
    try:
        await bot.start(config['token'])
    except KeyboardInterrupt:
        await bot.logout()

def check_if_dev(ctx):
    return ctx.message.author.id == 118422640238133249


class CommandCore:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, text: str):
        await ctx.send(text)

    @commands.check(check_if_dev)
    @commands.group(hidden = True, invoke_without_command=True)
    async def source(self, ctx):
        """Developer Commands"""

    @source.command()
    async def loadCommand(self, ctx, name):
        await ctx.send('Attempting command load.')
        commandFile = f'cogs.{name}'
        self.bot.unload_extension(commandFile)
        try:
            self.bot.load_extension(commandFile)
            await ctx.send(f'loaded {commandFile}')
        except Exception as e:
            error = f'{commandFile}\n {type(e).__name__} : {e}'
            await ctx.send(f'failed to load extension {error}')

    @source.command()
    async def reloadAllCommands(self, ctx):
        cogs = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in cogs:
            try:
                commandFile = f'cogs.{extension}'
                self.bot.unload_extension(commandFile)
                self.bot.load_extension(commandFile)
                await ctx.send(f'loaded {extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                await ctx.send(f'failed to load extension {error}')

    @source.command(enabled=False)
    async def createBasicCommand(self, ctx, name: str, *, formattedLogic: str):
        logic = re.sub('[`]', '', formattedLogic)
        className = name[0] + name[1:]
        path = f"./cogs/{name}.py"
        file = os.open(path, os.O_WRONLY|os.O_CREAT)
        os.ftruncate(file, 0)
        source = f"\
import discord\n\
from discord.ext import commands\n\n\
class {className}:\n\
    def __init__(self, bot):\n\
        self.bot = bot\n\n\
{logic}\n\n\
def setup(bot):\n\
    bot.add_cog({className}(bot))\n"
        os.write(file, source.encode())
        os.close(file)

    @source.command(enabled=False)
    async def acceptRaw(self, ctx, name: str, rawSource: str):
        source = re.sub('[`]', '', rawSource)
        path = f'./cogs/{name}.py'
        file = os.open(path, os.O_WRONLY|os.O_CREAT)
        os.ftruncate(file, 0)
        os.write(file, source.encode())
        os.close(file)

    @source.command()
    async def acceptFiles(self, ctx):
        attachments = ctx.message.attachments
        fileNames = [attachment.filename for attachment in attachments]
        fileNamesStr = '[%s]' % ', '.join(map(str, fileNames))
        await ctx.send(f'AttachedFiles: {fileNamesStr}')
        for attachment in attachments:
            path = f'./cogs/{attachment.filename}'
            try:
                await ctx.send(f'Attempting to save {attachment.filename} to {path}')
                await attachment.save(path)
            except Exception as e:
                await ctx.send(f'Failed to save {attachment.filename} to {path}\n Reason={type(e).__name__} : {e}')


    @source.command()
    async def show(self, ctx, module):
        fp = Path(f'cogs/{module}.py')
        fileSource = fp.read_text()
        await ctx.send(f'```{fileSource}```')

    @source.command()
    async def upload(self, ctx, module):
        fp = Path(f'cogs/{module}.py')
        sourceFile = discord.File(fp.open('rb'), filename=fp.name)
        await ctx.send(f'Uploading file', file=sourceFile)

    @source.command()
    async def uploadAll(self, ctx):
        await ctx.send(f'Attempting to upload source files.')
        cogs = [x for x in Path('cogs').glob('*.py')]
        await ctx.send(f'Found: {cogs}')
        while len(cogs) > 0:
            sourceFiles = []
            for i in range(0, 10):
                if len(cogs) > 0:
                    path = cogs.pop()
                    fileObj = path.open('rb')
                    sourceFiles.append(discord.File(fileObj, filename=path.name))
                else:
                    break
            await ctx.send(f'Uploading files', files=sourceFiles)
        await ctx.send(f'Done uploading files.')


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        config = kwargs.pop('config')
        self.prefix = config['prefix']
        super().__init__(
            command_prefix=self.get_prefix_,
            description=kwargs.pop('description')
        )
        self.start_time = None
        self.app_info = None

        self.loop.create_task(self.track_start())
        self.loop.create_task(self.load_all_extensions())

        self.add_cog(CommandCore(self))

    async def track_start(self):
        """
        Waits for the bot to connect to discord and then records the time.
        Can be used to work out uptime.
        """
        await self.wait_until_ready()
        self.start_time = datetime.datetime.utcnow()

    async def get_prefix_(self, bot, message):
        """
        A coroutine that returns a prefix.

        I have made this a coroutine just to show that it can be done. If you needed async logic in here it can be done.
        A good example of async logic would be retrieving a prefix from a database.
        """
        return commands.when_mentioned_or(*self.prefix)(bot, message)

    async def load_all_extensions(self):
        """
        Attempts to load all .py files in /cogs/ as cog extensions
        """
        await self.wait_until_ready()
        await asyncio.sleep(1)  # ensure that on_ready has completed and finished printing
        filepath = os.path.dirname(__file__)
        cogs = [x.stem for x in Path(filepath).joinpath('cogs').glob('*.py')]
        for extension in cogs:
            try:
                self.load_extension(f'cogs.{extension}')
                print(f'loaded {extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                print(f'failed to load extension {error}')
            print('-' * 10)

    async def on_ready(self):
        """
        This event is called every time the bot connects or resumes connection.
        """
        print('-' * 10)
        self.app_info = await self.application_info()
        print(f'Logged in as: {self.user.name}\n'
              f'Using discord.py version: {discord.__version__}\n'
              f'Owner: {self.app_info.owner}\n'
              f'Template Maker: SourSpoon / Spoon#7805')
        print('-' * 10)

    async def on_message(self, message):
        """
        This event triggers on every message received by the bot. Including one's that it sent itself.

        If you wish to have multiple event listeners they can be added in other cogs. All on_message listeners should
        always ignore bots.
        """
        if message.author.bot:
            return  # ignore all bots
        await self.process_commands(message)

    async def on_command_error(self, ctx, exception):
        await ctx.send(f'Failed to execute command.\n Reason={type(exception).__name__} : {exception}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

