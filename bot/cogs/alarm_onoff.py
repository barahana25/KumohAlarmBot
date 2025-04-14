import discord
from discord.ext import commands
from discord import app_commands

from bot.utils.database import channelDataDB
from bot import LOGGER, BOT_NAME_TAG_VER, color_code, OWNERS, KumohSquarePage

kor_table_dic = {"Academic_Information": "학사안내", "Event_Information": "행사안내", "General_News": "일반소식", "ceboard": "컴퓨터공학과 공지사항", "biskit": "비스킷 마일리지", "Hagsigdang": "학식당", "faculty_cafeteria": "교직원식당", "Purum": "푸름관", "Orum1": "오름1관", "Orum23": "오름2,3관", "error": "에러 알림"}
table_list = KumohSquarePage.name_list() + ["biskit", "ceboard", "Hagsigdang", "faculty_cafeteria", "Purum", "Orum1", "Orum23", "error"]

class AlarmSet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="alarmset", description="알람을 설정합니다.")
    @app_commands.choices(
        table=[
            app_commands.Choice(name=kor_table_dic[name], value=name) for name in table_list
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
                # embed.set_footer(text=BOT_NAME_TAG_VER)
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        # onoff를 소문자로 변환
        onoff = onoff.lower()
        # 채널 알림 상태를 DB에 저장
        channelDataDB().channel_status_set(table, interaction.channel.id, onoff)

        if onoff == "on":
            msg_title = f":green_circle: 이 채널에서 {kor_table_dic[table]} 알람을 켰습니다"
        else:
            msg_title = f":red_circle: 이 채널에서 {kor_table_dic[table]} 알람을 껐습니다"
        embed=discord.Embed(title="알람 설정", description=msg_title, color=color_code)

        # embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="alarmstatus")
    async def alarmstatus(self, interaction: discord.Interaction):
        """ 채널 내에 어느 테이블에서 알람이 켜져있는지 확인합니다. """

        all_table_dic = channelDataDB().get_on_channel_for_all_table()
        # 채널 알림 상태를 DB에서 불러옴
        on_channel_list = []
        msg_title = ""

        for table in table_list:
            kor_table = kor_table_dic[table]
            try:
                if interaction.channel.id in all_table_dic[table]:
                    on_channel_list.append(kor_table)
                    msg_title += f":green_circle:  {kor_table} \n"
                else:
                    msg_title += f":red_circle: {kor_table} \n"
            except KeyError:
                msg_title += f":red_circle: {kor_table} \n"
            
        embed=discord.Embed(title="채널 알람 상태", description=msg_title, color=color_code)

        # embed.set_footer(text=BOT_NAME_TAG_VER)
        await interaction.response.send_message(embed=embed)
        
    

async def setup(bot):
    await bot.add_cog(AlarmSet(bot))
    LOGGER.info('AlarmSet loaded!')