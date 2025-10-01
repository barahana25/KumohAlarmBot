import os
import discord
import asyncio
import traceback
import io
import base64

from bot.utils.database import *
from bot.utils.ai_preview import get_preview
from bot import LOGGER, BOT_NAME_TAG_VER, db_path, ai_board_link

def check_importance(name: str) -> tuple[int, str]:
    color = 0x008000
    important = ":green_circle: 보통"

    very_important_list =  ["김양현", "컴퓨터공학과 관리자"]
    important_list = ["김진희"]

    for vil in very_important_list:
        if name in vil:
            color = 0xff0000
            important = ":red_circle: 매우 중요"
            break

    if color == 0x008000:
        for il in important_list:
            if name in il:
                color = 0xff7f00
                important = ":orange_circle: 중요"
                break
    
    return color, important

async def broadcast_ai(bot):
    """ AI게시판 새 글 알림 전송 """
    if not os.path.exists(db_path):
        await asyncio.sleep(5)
    while True:
        latest_data_id = aiBoardDB().get_latest_data_id()
        # None 이 아닐 경우 반복문 탈출
        if latest_data_id is not None:
            break
        # None 일 경우 5초 대기
        await asyncio.sleep(5)
    await asyncio.sleep(5)

    while True:
        while True:
            now_latest_data_id = aiBoardDB().get_latest_data_id()
            # None 이 아닐 경우 반복문 탈출
            if now_latest_data_id is not None:
                break
            # None 일 경우 5초 대기
            await asyncio.sleep(5)
        if latest_data_id != now_latest_data_id:
            for data_id in range(latest_data_id + 1, now_latest_data_id + 1):
                # get post
                post = aiBoardDB().get_database_from_id(data_id)
                # 데이터베이스에 정보가 존재할 경우
                if post is not None:
                    try:                        
                        img_preview, preview = await get_preview(post[1])
                        preview = "\n".join(map(str, preview.splitlines()))
                    except: 
                        # 글 수정/삭제되었을 경우 오류 예외처리
                        img_preview = None
                        preview = None

                    # 메시지 전송
                    if post is not None:
                        LOGGER.info(f"Send msg : {post}")
                        await send_msg(bot, post, preview, img_preview)

            latest_data_id = now_latest_data_id
        await asyncio.sleep(60)

async def send_msg(bot, post: tuple, preview: (str | None), img_preview_base64: (str | None)):
    """ 메시지 전송 """
    
    color, important = check_importance(post[3])

    # 채널 아이디 리스트 가져오기
    channel_id_list = channelDataDB().get_on_channel("aiboard")
    # 채널 아이디 리스트가 존재한다면
    if channel_id_list != None:
        # 채널아이디별 메시지 전송
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            # 메시지 전송에 실패할 경우를 대비해 3번 시도
            for _ in range(3):
                try:
                    embed=discord.Embed(title=post[2], description=f"", color=color)
                    embed.add_field(name="글쓴이", value=post[3], inline=True)
                    embed.add_field(name="중요도", value=important, inline=True)
                    embed.add_field(name="링크", value=f"{ai_board_link}?mode=view&articleNo={post[1]}&article.offset=0&articleLimit=10", inline=False)

                    file = None
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
                    if file is not None:
                        await target_channel.send(embed=embed, file=file)
                    else:
                        await target_channel.send(embed=embed)

                    break
                except Exception as e:
                    LOGGER.error(traceback.format_exc())