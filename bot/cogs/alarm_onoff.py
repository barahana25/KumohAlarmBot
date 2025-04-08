import discord
from discord.ext import commands
from discord import app_commands

from bot.utils.database import channelDataDB
from bot import LOGGER, BOT_NAME_TAG_VER, color_code, OWNERS, KumohSquarePage

class AlarmSet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.page_list = KumohSquarePage.name_list() + ["SE_Board", "Hagsigdang"]

    @app_commands.command(name="alarmset", description="알람을 설정합니다.")
    # @option("table", description="알람 소스를 선택하세요", choices=KumohSquarePage.name_list() + ["SE_Board", "Hagsigdang", "faculty_cafeteria", "Purum", "Orum1", "Orum23"])
    # @option("onoff", description="이 채널에서의 알람을 켜거나 끕니다", choices=["ON", "OFF"])
    async def alarmset(self, interaction: discord.Interaction, table: str, onoff: str, name: str = None):
        """ 채널에서 알림을 켜거나 끕니다 """
        # 오너가 아닐 경우 관리자 권한이 있는지 확인
        if interaction.user.id not in OWNERS:
            if not interaction.user.guild_permissions.manage_messages:
                embed=discord.Embed(title="이 명령어는 서버의 관리자만이 사용할 수 있습니다!")
                embed.set_footer(text=BOT_NAME_TAG_VER)
                # return await interaction.respond(embed=embed)
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        # onoff를 소문자로 변환
        onoff = onoff.lower()
        # 채널 알림 상태를 DB에 저장
        channelDataDB().channel_status_set(table, interaction.channel.id, onoff)

        if onoff == "on":
            msg_title = ":green_circle: 이 채널에서 알람을 켰습니다"
        else:
            msg_title = ":red_circle: 이 채널에서 알람을 껐습니다"
        embed=discord.Embed(title="알람 설정", description=msg_title, color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        # await interaction.respond(embed=embed)
        await interaction.response.edit_message(embed=embed)

    @alarmset.autocomplete("table")
    async def alarmset_autocomplete(self, interaction: discord.Interaction, current: str):
        return [name for name in self.page_list if current.lower() in name.lower()]
    



    @app_commands.command(name="alarmstatus")
    # @option("table", description="알람이 켜져있는지 확인할 소스를 선택하세요", choices=KumohSquarePage.name_list() + ["SE_Board", "Hagsigdang", "faculty_cafeteria", "Purum", "Orum1", "Orum23"])
    async def alarmstatus(self, interaction: discord.Interaction, table: str):
        """ 이 채널에서 알람이 켜져있는지 확인합니다. """
        # 채널 알림 상태를 DB에서 불러옴
        on_channel_list = channelDataDB().get_on_channel(table)
        if interaction.channel.id in on_channel_list:
            msg_title = ":green_circle: 이 채널에서 알람이 켜져있습니다."
        else:
            msg_title = ":red_circle: 이 채널에서 알람이 꺼져있습니다."
        embed=discord.Embed(title="채널 알람 상태", description=msg_title, color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        # await interaction.respond(embed=embed)
        await interaction.response.edit_message(embed=embed)
        
    @alarmstatus.autocomplete("table")
    async def alarmstatus_autocomplete(self, interaction: discord.Interaction, current: str):
        return [name for name in self.page_list if current.lower() in name.lower()]
    

async def setup(bot):
    await bot.add_cog(AlarmSet(bot))
    LOGGER.info('AlarmSet loaded!')