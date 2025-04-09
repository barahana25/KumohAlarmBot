import time
import discord
from discord.ext import commands
from discord import app_commands
from bot import LOGGER, BOT_NAME_TAG_VER, color_code

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        """ 핑 속도를 측정합니다. """
        latancy = self.bot.latency
        before = time.monotonic()
        embed=discord.Embed(title="**Ping**", description=f'ping_pong: Pong! WebSocket Ping {round(latancy * 1000)}ms\n:ping_pong: Pong! Measuring...', color=color_code)
        # embed.set_footer(text=BOT_NAME_TAG_VER)
        message = await interaction.response.send_message(embed=embed, ephemeral=True)
        ping = (time.monotonic() - before) * 1000
        embed=discord.Embed(title="**Ping**", description=f':ping_pong: Pong! WebSocket Ping {round(latancy * 1000)}ms\n:ping_pong: Pong! Message Ping {int(ping)}ms', color=color_code)
        # embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
    LOGGER.info('Ping loaded!')