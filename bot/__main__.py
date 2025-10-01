import discord
import asyncio

from discord.ext import commands
from bot.background.read_ce import read_ce
from bot.background.read_ai import read_ai
from bot.background.broadcast_ce import broadcast_ce
from bot.background.broadcast_ai import broadcast_ai
from bot.background.read_kumoh import read_kumoh
from bot.background.broadcast_kumoh import broadcast_kumoh
from bot.background.read_biskit import read_biskit
from bot.background.broadcast_biskit import broadcast_biskit
from bot.background.schedule import schedule
from bot.background.broadcast_hagsigdang import broadcast_hagsigdang
from bot.background.broadcast_dormitory import broadcast_dorm_food
from bot.background.broadcast_faculty_cafeteria import broadcast_faculty_cafeteria

from bot import LOGGER, TOKEN, EXTENSIONS, BOT_NAME_TAG_VER

async def status_task():
    while True:
        try:
            await bot.change_presence(
                activity = discord.Game ("/help : 도움말"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
            await bot.change_presence(
                activity = discord.Game (f"{len(bot.guilds)}개의 서버에 참여하고 있어요!"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
        except Exception:
            pass

class Bot (commands.Bot):
    def __init__ (self):
        super().__init__(
            command_prefix = "/",
            intents=intents
        )
        self.remove_command("help")
        
        # for i in EXTENSIONS:
        #     self.load_extension("bot.cogs." + i)
    async def setup_hook(self):
        for i in EXTENSIONS:
            # 비동기적으로 cog 로드
            await self.load_extension(f"bot.cogs.{i}")
        await self.tree.sync()
            
    async def on_ready(self):
        LOGGER.info(BOT_NAME_TAG_VER)
        await self.change_presence(
            activity = discord.Game ("/help : 도움말"),
            status = discord.Status.online,
        )
        
        while background_list:
            module_name = list(background_list.keys())[0]
            pass_variable = background_list.pop(module_name)

            if pass_variable:
                asyncio.create_task(globals()[module_name](bot))
            else:
                asyncio.create_task(globals()[module_name]())

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

background_list = {
    "status_task": False,
    "broadcast_ce": True,
    "broadcast_ai": True,
    "broadcast_kumoh": True,
    "broadcast_biskit": True,
    "read_ai": False,
    "read_ce": False,
    "read_kumoh": False,
    "read_biskit": False,
    "schedule": True,
    "broadcast_hagsigdang": True,
    "broadcast_faculty_cafeteria": True,
    "broadcast_dorm_food": True
}

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = Bot()
bot.run(TOKEN)