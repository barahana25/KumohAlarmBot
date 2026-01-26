import discord
import asyncio
import traceback
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

from bot.utils.crawler import getText
from bot.utils.database import *
from bot import LOGGER, BOT_NAME_TAG_VER, color_code

async def broadcast_dorm_food(bot) -> None:
    """ 오늘의 기숙사 식당 메뉴 체크 (최대 3회 재시도) """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    all_links = {
        "Purum": "https://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do",
        "Orum1": "https://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do",
        "Orum23": "https://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do"
    }
    
    notified_dorms = set()
    last_reset_date = datetime.now().date()
    retry_count = 0

    while True:
        now = datetime.now()
        
        # 날짜가 바뀌면 성공 목록과 재시도 횟수 초기화
        if now.date() > last_reset_date:
            notified_dorms.clear()
            last_reset_date = now.date()
            retry_count = 0

        # 실행 조건: 
        # 1. 7시 정각이거나
        # 2. 아직 다 못 보낸 기숙사가 있는데, 재시도 횟수가 3회 미만이고 이미 7시를 지났을 때
        is_time_to_run = (now.hour == 7 and now.minute == 0)
        is_retry_needed = (len(notified_dorms) < len(all_links) and 0 < retry_count < 3)

        if is_time_to_run or is_retry_needed:
            for dorm, url in all_links.items():
                if dorm in notified_dorms:
                    continue  # 이미 성공한 기숙사는 건너뜀

                try:
                    dt = (now - timedelta(days=1)).strftime("%Y-%m-%d")
                    result = await getText(url + "?mode=menuList&srDt=" + dt, header)

                    if result is None:
                        continue

                    parse = BeautifulSoup(result, 'lxml')
                    box = parse.find("table", {"class": "smu-table"})
                    if not box:
                        continue

                    today_menu_list = []
                    rows = box.find("tbody").find_all("tr")
                    weekday_idx = now.weekday()

                    for row in rows:
                        cells = row.find_all("td")
                        if len(cells) > weekday_idx:
                            menu_text = cells[weekday_idx].getText().strip().split("\n")
                            if menu_text[0]: # 메뉴 이름이 존재할 때만 추가
                                today_menu_list.append([menu_text[0], '\n'.join(menu_text[1:]).strip()])

                    if today_menu_list:
                        await send_dorm_food(bot, dorm, today_menu_list)
                        notified_dorms.add(dorm)
                        print(f"[{dorm}] 전송 성공")

                except Exception as e:
                    print(f"[{dorm}] 파싱 에러: {e}")

            # 루프가 한 번 끝난 후, 아직 성공하지 못한 기숙사가 있다면
            if len(notified_dorms) < len(all_links):
                retry_count += 1
                if retry_count < 3:
                    # print(f"일부 실패 ({len(notified_dorms)}/{len(all_links)}). 10초 후 재시도... ({retry_count}/3)")
                    await asyncio.sleep(10) # 10초 딜레이
                    continue
                else:
                    # print(f"3회 재시도 실패. 오늘은 더 이상 조회하지 않습니다.")
                    pass

        # 1분 대기 (7시 0분에 한 번 실행된 후 다음 분으로 넘어가도록 함)
        await asyncio.sleep(60)

async def send_dorm_food(bot, dorm, today_menu: list) -> None:
    """ 기숙사식당 메뉴 전송 """
    dorm_name = {
        "Purum": "푸름관",
        "Orum1": "오름관 1",
        "Orum23": "오름관 2, 3"
    }
    # 채널 아이디 리스트 가져오기
    channel_id_list = channelDataDB().get_on_channel(dorm)
    if channel_id_list is not None:
        # 채널아이디별 메시지 전송
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            try:
                embed = discord.Embed(title=f"오늘의 {dorm_name[dorm]} 식당 메뉴", description='', color=color_code)

                for menu in today_menu:
                    menu_title, menu_content = menu
                    embed.add_field(name=menu_title, value=menu_content, inline=True)

                # embed.set_footer(text=BOT_NAME_TAG_VER)
                await target_channel.send(embed=embed)

            except Exception:
                LOGGER.error(traceback.format_exc())