import os
import discord
import asyncio
import traceback
import io
import base64

from bot.utils.database import *
from bot.utils.biskit_preview import get_preview
from bot import LOGGER, BOT_NAME_TAG_VER, db_path, biskit_link
from bot.background.send_error import send_error

async def broadcast_biskit(bot):
    """ 비스킷 새 글 알림 전송 """
    if not os.path.exists(db_path):
        await asyncio.sleep(5)
    while True:
        latest_data_id = BiskitDB().get_latest_data_id('biskit')
        # None 이 아닐 경우 반복문 탈출
        if latest_data_id is not None:
            break
        # None 일 경우 5초 대기
        await asyncio.sleep(5)
    await asyncio.sleep(5)

    while True:
        while True:
            now_latest_data_id = BiskitDB().get_latest_data_id('biskit')
            # None 이 아닐 경우 반복문 탈출
            if now_latest_data_id is not None:
                break
            # None 일 경우 5초 대기
            await asyncio.sleep(5)
        if latest_data_id != now_latest_data_id:
            for data_id in range(latest_data_id + 1, now_latest_data_id + 1):
                # get post
                post = BiskitDB().get_database_from_id(data_id)
                # 데이터베이스에 정보가 존재할 경우
                if post is not None:
                    try:
                        post, img_preview_base64, preview = await get_preview(post[1])
                    except: 
                        # 글 수정/삭제되었을 경우 오류 예외처리
                        img_preview_base64 = None
                        preview = None

                    # 메시지 전송
                    if post is not None:
                        LOGGER.info(f"Send msg : {post}")
                        await send_msg(bot, post, preview, img_preview_base64)

            latest_data_id = now_latest_data_id
        await asyncio.sleep(60)

async def send_msg(bot, post: tuple, preview: (str | None), img_preview_base64: (str | None)):
    """ 메시지 전송 """
    try:
        _, post_id, title, author, org, category, period, mileage = post
        

        color = 0x008000

        # 채널 아이디 리스트 가져오기
        channel_id_list = channelDataDB().get_on_channel("biskit")
        # 채널 아이디 리스트가 존재한다면
        if channel_id_list != None:
            # 채널아이디별 메시지 전송
            for channel_id in channel_id_list:
                target_channel = bot.get_channel(channel_id)
                # 메시지 전송에 실패할 경우를 대비해 3번 시도
                for _ in range(3):
                    try:
                        embed=discord.Embed(title=title, description=f"", color=color)
                        
                        embed.add_field(name="카테고리", value=category, inline=True)
                        embed.add_field(name="운영조직", value=org, inline=True)
                        embed.add_field(name="글쓴이", value=author, inline=True)
                        embed.add_field(name="기간", value=period, inline=False)
                        embed.add_field(name="마일리지", value=mileage, inline=True)
                        # embed.add_field(name="중요도", value=important, inline=True)
                        embed.add_field(name="링크", value=f"{biskit_link}?mode=view&articleNo={post_id}&article.offset=0&articleLimit=10", inline=False)
                        
                        # 미리보기 텍스트가 있을 경우
                        if preview:
                            embed.add_field(name="미리보기", value=preview, inline=False)
                        # 이미지 미리보기가 있을 경우
                        if img_preview_base64:
                            img_data = base64.b64decode(img_preview_base64)
                            file = discord.File(io.BytesIO(img_data), filename="image.png")
                            embed.set_image(url="attachment://image.png")
                            # embed.set_image(url=img_preview)

                        # embed.set_footer(text=BOT_NAME_TAG_VER)
                        await target_channel.send(embed=embed, file=file)

                        break
                    except Exception as e:
                        LOGGER.error(traceback.format_exc())
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        try:
            await send_error(bot, channel_id, e)
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            LOGGER.error(f"send_msg() Error : {e}")
        await asyncio.sleep(1200)
