import discord
from discord.ext import commands
from discord import app_commands

from bot.utils.database import channelDataDB
from bot import LOGGER, BOT_NAME_TAG_VER, color_code, OWNERS, KumohSquarePage

class AlarmSet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="alarmset", description="알람을 설정합니다.")
    @app_commands.choices(
        table=[
            app_commands.Choice(name=name, value=name) for name in KumohSquarePage.name_list() + ["Hagsigdang", "faculty_cafeteria", "Purum", "Orum1", "Orum23"]
        ]
    )
    @app_commands.choices(
        onoff=[
            app_commands.Choice(name="ON", value="on"),
            app_commands.Choice(name="OFF", value="off")
        ]
    )
    async def alarmset(self, interaction: discord.Interaction, table: str, onoff: str, name: str = None):
        """ 채널에서 알림을 켜거나 끕니다 """

        # 오너가 아닐 경우 관리자 권한이 있는지 확인
        if interaction.user.id not in OWNERS:
            if not interaction.user.guild_permissions.manage_messages:
                embed=discord.Embed(title="이 명령어는 서버의 관리자만이 사용할 수 있습니다!")
                embed.set_footer(text=BOT_NAME_TAG_VER)
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
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="alarmstatus")
    async def alarmstatus(self, interaction: discord.Interaction):
        """ 채널 내에 어느 테이블에서 알람이 켜져있는지 확인합니다. """

        all_table_dic = channelDataDB().get_on_channel_for_all_table()

        # 채널 알림 상태를 DB에서 불러옴
        on_channel_list = []
        msg_title = ""

        for table in all_table_dic:
            if interaction.channel.id in all_table_dic[table]:
                on_channel_list.append(table)
                msg_title += f":green_circle:  {table} \n"
            else:
                msg_title += f":red_circle: {table} \n"
            
        if on_channel_list == []:
            embed=discord.Embed(title="채널 알람 상태", description="모든 채널에서 알람이 꺼져있습니다.", color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await interaction.response.send_message(embed=embed)
        
        embed=discord.Embed(title="채널 알람 상태", description=msg_title, color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.response.send_message(embed=embed)
        
    

async def setup(bot):
    await bot.add_cog(AlarmSet(bot))
    LOGGER.info('AlarmSet loaded!')