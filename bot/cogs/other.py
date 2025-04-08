import discord
from discord.ext import commands
import subprocess
from discord import app_commands

from bot import LOGGER, BOT_NAME_TAG_VER, color_code

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="invite")
    async def invite(self, interaction: discord.Interaction):
        """ 봇 초대 링크 전송 """
        link = f'https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=414464789568&scope=bot%20applications.commands'
        embed=discord.Embed(title="초대링크", description=f"봇을 초대할 다른 서버의 관리자라면 [링크]({link})를 클릭하면 됩니다.", color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="uptime")
    async def uptime(self, interaction: discord.Interaction):
        """ 서버 업타임 """
        res = subprocess.check_output("uptime", shell=False, encoding='utf-8')
        embed=discord.Embed(title="Uptime", description="```%s```" %res.replace(',  ', '\n').replace(', ', '\n').replace(': ', ': ')[1:], color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Other(bot))
    LOGGER.info('Other loaded!')