import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

from bot.utils.database import channelDataDB
from bot import LOGGER, BOT_NAME_TAG_VER, color_code, OWNERS, KumohSquarePage

class ScheduleAlarmSet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.table = "Schedule"

    @app_commands.command(name="scheduleset")
    @app_commands.choices(onoff=[
        app_commands.Choice(name="ON", value="on"),
        app_commands.Choice(name="OFF", value="off")
    ])
    async def scheduleset(self, interaction: discord.Interaction, onoff: str):
        """ 서버에서 학사일정 연동을 켜거나 끕니다 """

        # 오너가 아닐 경우 관리자 권한이 있는지 확인
        if interaction.user.id not in OWNERS:
            if not interaction.user.guild_permissions.manage_messages:
                embed=discord.Embed(title="이 명령어는 서버의 관리자만이 사용할 수 있습니다!")
                # embed.set_footer(text=BOT_NAME_TAG_VER)
                return await interaction.response.send_message(embed=embed)

        # onoff를 소문자로 변환
        onoff = onoff.lower()
        # 채널 알림 상태를 DB에 저장
        channelDataDB().channel_status_set(self.table, interaction.guild.id, onoff)

        if onoff == "on":
            msg_title = ":green_circle: 이 서버에서 학사일정 연동을 켰습니다"
        else:
            msg_title = ":red_circle: 이 서버에서 학사일정 연동을 껐습니다"
        embed=discord.Embed(title="알람 설정", description=msg_title, color=color_code)

        # embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="schedulestatus")
    async def schedulestatus(self, interaction: discord.Interaction):
        """ 이 서버에서 학사일정 연동이 켜져있는지 확인합니다. """

        # 채널 알림 상태를 DB에서 불러옴
        on_guild_list = channelDataDB().get_on_channel(self.table)
        if interaction.guild.id in on_guild_list:
            msg_title = ":green_circle: 이 서버에서 학사일정 연동이 켜져있습니다."
        else:
            msg_title = ":red_circle: 이 서버에서 학사일정 연동이 꺼져있습니다."
        embed=discord.Embed(title="채널 알람 상태", description=msg_title, color=color_code)

        # embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ScheduleAlarmSet(bot))
    LOGGER.info('ScheduleAlarmSet loaded!')