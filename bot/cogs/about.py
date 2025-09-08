import discord
from discord.ext import commands
from discord import app_commands

from bot import LOGGER, BOT_NAME_TAG_VER, color_code

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="about")
    async def about(self,interaction: discord.Interaction):
        """ 봇에 대한 소개 """
        embed=discord.Embed(title="봇 정보", description="금오공대의 여러가지 정보를 알려주는 봇입니다.", color=color_code)
        embed.add_field(name="개발자", value="25학번", inline=True)
        embed.add_field(name="관련 링크", value="[Github](https://github.com/barahana25/Kumoh-alarm)", inline=True)
        # embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(About(bot))
    LOGGER.info('About loaded!')