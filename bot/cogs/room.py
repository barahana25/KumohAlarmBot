import time
import discord
import datetime
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import app_commands

from bot import LOGGER, BOT_NAME_TAG_VER, color_code
from bot.config import syllabus_2025


def get_classroom_data():
    lecture_list = []

    for lecture in syllabus_2025['ds_out']:
        classroom = lecture['TIME_LCTRM_INFO'] # 강의실
        curriculum = lecture['CRCLM_NM'] # 교육과정
        lecture_name = lecture['SBJCT_NM'] # 강의명
        lecture_code = lecture['SBJCT_CD'] # 과목코드
        professor = lecture['EMPNM'] # 교수명

        if classroom is None:
            continue
        lecture_list.append({
            'classroom': classroom,
            'curriculum': curriculum,
            'lecture_name': lecture_name,
            'lecture_code': lecture_code,
            'professor': professor
        })

    classroom_dict = {}

    for lecture in lecture_list:
        for classroom in lecture['classroom'].split(','):
            date, room = classroom.split('/')
            if room == '':
                continue
            day = date[0]
            time = date[1:]
            if room not in classroom_dict:
                classroom_dict[room] = {}
            if day not in classroom_dict[room]:
                classroom_dict[room][day] = []
            classroom_dict[room][day].append({
                'time': time,
                'curriculum': lecture['curriculum'],
                'lecture_name': lecture['lecture_name'],
                'lecture_code': lecture['lecture_code'],
                'professor': lecture['professor']
            })
    # Sort the dictionary by room number
    classroom_dict = dict(sorted(classroom_dict.items(), key=lambda x: x[0]))

    # Sort the list of lectures in each room by time
    for room, lectures in classroom_dict.items():
        for day, lecture_list in lectures.items():
            classroom_dict[room][day] = sorted(lecture_list, key=lambda x: x['time'])

    # room_list = {'T': '테크노관', 'G': '글로벌관', 'S교육': '', 'DB', 'D', '에디슨', '국제', '본관', '산학', '학군', 'TB', 'GB'}

    room_list = {'T': '테크노관', 'G': '글로벌관', 'D': '디지털관', '에디슨': '에디슨관', '국제': '국제관'}
    building_dict = {}

    for classroom in classroom_dict.keys():
        for room, room_name in room_list.items():
            if room in classroom:
                if room_name not in building_dict:
                    building_dict[room_name] = [classroom]
                if classroom not in building_dict[room_name]:
                    building_dict[room_name].append(classroom)
                break

    # Sort the buildings based on the second character being 'B'
    # for building in building_dict.keys():
    #     buildings = building_dict[building]
    #     sorted_buildings = sorted(buildings, key=lambda x: 0 if len(x) > 1 and x[1] == 'B' else 1)
    #     building_dict[building] = sorted_buildings
    building_dict = dict(sorted(building_dict.items(), key=lambda x: x[0]))

    split_building_dict = dict(sorted(building_dict.items(), key=lambda x: x[0]))

    # classroom을 25개씩 나눠서 building_dict에 넣기
    for building in split_building_dict.keys():
        classroom_list = split_building_dict[building]
        for classroom in enumerate(classroom_list):
            if len(split_building_dict[building]) % 25 == 0:
                split_building_dict[building] = [classroom_list[i:i + 25] for i in range(0, len(classroom_list), 25)]
            else:
                split_building_dict[building] = [classroom_list[i:i + 24] for i in range(0, len(classroom_list), 24)]

    new_building_dict = {}

    # split_building_dict 있는 building의 이름을 split_building_dict[building]안에 있는 리스트의 첫번째 요소와 마지막 요소를 가져와서 "building(split_building_dict[building][0], split_building_dict[building][-1])"로 네이밍하여 각각의 building에 classroom_list를 삽입하여 new_building_dict에 저장
    for building in split_building_dict.keys():
        for classroom_list in split_building_dict[building]:
            if len(split_building_dict[building]) == 1:
                new_building_dict[building] = classroom_list
            else:
                new_building_dict[f"{building}({classroom_list[0]}-{classroom_list[-1]})"] = classroom_list

    return classroom_dict, building_dict, new_building_dict

full_order = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E']
classroom_dict, building_dict, new_building_dict = get_classroom_data()
def find_classroom_empty_time(classroom_dict, classroom, day):
    """ 강의실의 빈 시간 조회 """
    day_dict = {
            0: '월',
            1: '화',
            2: '수',
            3: '목',
            4: '금',
            5: '토',
            6: '일'
        }
    day = day_dict[day]
    empty_time = {'1':None, '2':None, '3':None, '4':None, '5':None, '6':None, '7':None, '8':None, '9':None, 'A':None, 'B':None, 'C':None, 'D':None, 'E':None}
    if classroom in classroom_dict:
        if day not in classroom_dict[classroom]:
            return empty_time
        for lecture in classroom_dict[classroom][day]:
            for time in lecture['time']:
                for i in time:
                    empty_time[i] = lecture['curriculum'] + ' ' + lecture['lecture_name'] + ' ' + lecture['professor']

    return empty_time

def get_current_block():
    """ 현재 시간을 시간표 블록으로 변환 """
    now = datetime.datetime.now().time()
    time_blocks = [
        ('1', (9, 0)), ('2', (10, 0)), ('3', (11, 0)), ('4', (12, 0)),
        ('5', (13, 0)), ('6', (14, 0)), ('7', (15, 0)), ('8', (16, 0)),
        ('9', (17, 0)), ('A', (18, 0)), ('B', (19, 0)), ('C', (20, 0)),
        ('D', (21, 0)), ('E', (22, 0))
    ]

    for i, (block, (hour, minute)) in enumerate(time_blocks):
        block_time = datetime.time(hour, minute)
        if now < block_time:
            return time_blocks[max(0, i - 1)][0]  # 직전 블록으로 간주
    return 'E'  # 늦은 밤이면 마지막 블록 반환

def filter_blocks_after_now(blocks, duration):
    """ 현재 시간 이후 duration시간만큼 연속으로 비어있는 강의실 필터링 """
    now_block = get_current_block()
    now_index = full_order.index(now_block)

    result = {}
    for classroom, block_list in blocks.items():
        for block in block_list:
            # 시작 블록이 정확히 현재 시간 이후인지 확인
            if full_order.index(block[0]) == now_index:
                result.setdefault(classroom, []).append(block)

    return result

def find_classroom_empty_time_by_day_and_hour(classroom_dict, building_dict, building, day, duration):
    """ 강의실의 빈 시간 조회 """
    
    # 요일 번호를 문자로 변환
    day_dict = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    day = day_dict[day]
    empty_time = {}

    if building in building_dict:
        for classroom in building_dict[building]:
            all_time = set(full_order)
            if classroom in classroom_dict:
                if day not in classroom_dict[classroom]:
                    empty_time[classroom] = list(all_time)
                    continue
                for lecture in classroom_dict[classroom][day]:
                    for time in lecture['time']:
                        for i in time:
                            all_time.discard(i)
            empty_time[classroom] = sorted(list(all_time), key=lambda x: full_order.index(x))

    def find_continuous_blocks(time_list, duration):
        """ 연속된 시간 블록을 추출 """
        indices = [full_order.index(t) for t in time_list]
        indices.sort()

        blocks = []
        start = None

        for i, idx in enumerate(indices):
            if start is None:
                start = idx
                continue
            if idx != indices[i - 1] + 1:
                if indices[i - 1] - start + 1 >= duration:
                    span = full_order[start:indices[i - 1]+1]
                    for j in range(len(span) - duration + 1):
                        blocks.append(span[j:j+duration])
                start = idx
        # 마지막 블록 처리
        if start is not None and indices[-1] - start + 1 >= duration:
            span = full_order[start:indices[-1]+1]
            for j in range(len(span) - duration + 1):
                blocks.append(span[j:j+duration])
        return blocks

    result = {}
    for classroom_name, times in empty_time.items():
        if times:  # 시간 리스트가 비어있지 않은 경우에만 진행
            result[classroom_name] = find_continuous_blocks(times, duration)

    return result

class Room(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def classroom_autocomplete(self, interaction: discord.Interaction, current: str):
        """ 건물의 강의실 목록 """
        building = interaction.data['options'][0]['value']
        classroom_list = new_building_dict[building]
        classroom_list = [classroom for classroom in classroom_list if current.lower() in classroom.lower()]
        return [app_commands.Choice(name=classroom, value=classroom) for classroom in classroom_list]

    @app_commands.command(name="room", description="강의실을 선택해주세요.")
    @app_commands.choices(
        building=[
            app_commands.Choice(name=room_name, value=room_name) for room_name in new_building_dict.keys()
        ]
    )
    @app_commands.autocomplete(classroom=classroom_autocomplete)
    async def room(self, interaction: discord.Interaction, building: str, classroom: str):
        """ 비어있는 강의실 시간을 조회합니다. """
        day = datetime.datetime.now().weekday()
        
        empty_time = find_classroom_empty_time(classroom_dict, classroom, day)
        
        # 각 시간대에 대해 아이콘과 수업명을 하나씩 넣기
        empty_time_str = "%s 9:00~9:50 %s\n%s 10:00~10:50 %s\n%s 11:00~11:50 %s\n%s 12:00~12:50 %s\n%s 13:00~13:50 %s\n%s 14:00~14:50 %s\n%s 15:00~15:50 %s\n%s 16:00~16:50 %s\n%s 17:00~17:50 %s\n%s 18:00~18:50 %s\n%s 18:55~19:45 %s\n%s 19:50~20:40 %s\n%s 20:45~21:35 %s\n%s 21:40~22:30 %s"

        # 각 시간대에 대해 아이콘과 수업명을 하나씩 넣기
        values = []
        for key in empty_time.keys():
            val = empty_time.get(key)
            if val is None:
                values.extend([":green_circle:", ""])  # 비어있을 때
            else:
                values.extend([":red_circle:", val])   # 수업이 있을 때

        filled_time_str = empty_time_str % tuple(values)
        
        embed = discord.Embed(title=f"오늘 {building[:building.find('(')]} {classroom} 시간표", description=filled_time_str)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="room_day", description="강의실과 요일을 선택해주세요.")
    @app_commands.choices(
        building=[
            app_commands.Choice(name=room_name, value=room_name) for room_name in new_building_dict.keys()
        ]
    )
    @app_commands.choices(
        day=[
            app_commands.Choice(name="월요일", value=0),
            app_commands.Choice(name="화요일", value=1),
            app_commands.Choice(name="수요일", value=2),
            app_commands.Choice(name="목요일", value=3),
            app_commands.Choice(name="금요일", value=4),
            app_commands.Choice(name="토요일", value=5),
            app_commands.Choice(name="일요일", value=6)
        ]
    )
    @app_commands.autocomplete(classroom=classroom_autocomplete)
    async def room_day(self, interaction: discord.Interaction, building: str, classroom: str, day: int):
        """ 비어있는 강의실 시간을 조회합니다. """
        day_dict = {
            0: '월',
            1: '화',
            2: '수',
            3: '목',
            4: '금',
            5: '토',
            6: '일'
        }
        empty_time = find_classroom_empty_time(classroom_dict, classroom, day)

        # 각 시간대에 대해 아이콘과 수업명을 하나씩 넣기
        empty_time_str = "%s 9:00~9:50 %s\n%s 10:00~10:50 %s\n%s 11:00~11:50 %s\n%s 12:00~12:50 %s\n%s 13:00~13:50 %s\n%s 14:00~14:50 %s\n%s 15:00~15:50 %s\n%s 16:00~16:50 %s\n%s 17:00~17:50 %s\n%s 18:00~18:50 %s\n%s 18:55~19:45 %s\n%s 19:50~20:40 %s\n%s 20:45~21:35 %s\n%s 21:40~22:30 %s"

        # 각 시간대에 대해 아이콘과 수업명을 하나씩 넣기
        values = []
        for key in empty_time.keys():
            val = empty_time.get(key)
            if val is None:
                values.extend([":green_circle:", ""])  # 비어있을 때
            else:
                values.extend([":red_circle:", val])   # 수업이 있을 때

        filled_time_str = empty_time_str % tuple(values)

        embed = discord.Embed(title=f"{day_dict[day]}요일 {building[:building.find('(')]} {classroom} 시간표", description=filled_time_str)

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="room_ready_now", description="건물을 선택해주세요.")
    @app_commands.choices(
        building=[
            app_commands.Choice(name=room_name, value=room_name) for room_name in building_dict.keys()
        ]
    )
    @app_commands.choices(
        duration=[
            app_commands.Choice(name="1시간", value=1),
            app_commands.Choice(name="2시간", value=2),
            app_commands.Choice(name="3시간", value=3),
            app_commands.Choice(name="4시간", value=4),
            app_commands.Choice(name="5시간", value=5),
            app_commands.Choice(name="6시간", value=6),
        ]
    )
    async def room_ready_now(self, interaction: discord.Interaction, building: str, duration: int):
        """ 오늘 n시간이상 비어있는 강의실을 조회합니다. """
        day = datetime.datetime.now().weekday()
        
        blocks = find_classroom_empty_time_by_day_and_hour(classroom_dict, building_dict, building, day, duration)
        filtered = filter_blocks_after_now(blocks, duration)
        
        if not filtered:
            embed = discord.Embed(title=f"{building} 최소 {duration}시간 비어있는 강의실", description="없음")
            await interaction.response.send_message(embed=embed)
            return
        
        empty_time = [classroom for classroom, times in filtered.items()]
        embed = discord.Embed(title=f"{building} 최소 {duration}시간 비어있는 강의실", description=" ".join(empty_time))

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Room(bot))
    LOGGER.info('Room loaded!')
