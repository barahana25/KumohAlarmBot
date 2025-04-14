import discord
import asyncio
import traceback
from datetime import datetime
from bot.utils.database import *
from bot import LOGGER, BOT_NAME_TAG_VER, color_code


async def send_error(bot, error) -> None:
    """ 에러 발생 시 전송 """
    channel_id_list = channelDataDB().get_on_channel("error")
    if channel_id_list is not None:
        # 채널아이디별 메시지 전송
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            try:
                embed = discord.Embed(title=f"에러 발생", description='', color=color_code)
                embed.add_field(name="에러 발생 시간", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
                embed.add_field(name="에러 발생 위치", value=error, inline=False)
                embed.add_field(name="에러 발생 내용", value=traceback.format_exc(), inline=False)

                # embed.set_footer(text=BOT_NAME_TAG_VER)
                await target_channel.send(embed=embed)

            except Exception:
                LOGGER.error(traceback.format_exc())