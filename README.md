# Kumoh alarm

본 repository는 컴퓨터공학과 소프트웨어전공 22학번인 안재범 선배님의 디스코드봇 알리미를 fork하였습니다. (https://github.com/ajb3296/Kumoh-alarm)


## How to use
봇 초대 링크(https://discord.com/oauth2/authorize?client_id=1358754351262208021&permissions=1689384584214592&integration_type=0&scope=bot)
1. /alarmset table {테이블 이름} onoff {ON|OFF}  
봇을 초대한 뒤, 원하는 채널에서 alarmset 명령어를 호출해줍니다.  
테이블 이름 목록  
(1) 금오광장 (학사 안내, 행사 안내, 일반소식)  
(2) 비스킷 (마일리지)  
(3) 컴퓨터공학과 (공지사항)  
(4) 학식당, 교직원식당, 푸름관, 오름1관, 오름23관

3. /alarmstatus  
명령어를 호출하는 채널에서의 알람 상태를 알려줍니다.

4. /scheduleset {ON|OFF}  
학사일정을 이벤트 탭으로 보여줍니다.

5. /schedulestatus  
학사일정 알림 여부를 보여줍니다.

6. 나머지 명령어들은 / 를 눌러 확인할 수 있습니다.


### 디스코드 서버

https://discord.gg/tgMFRQED

## How to install
1. bot 폴더 안에 config.py 파일을 만든다.
2. config.py 파일을 아래와 같이 작성한다.
```python
from bot.sample_config import Config

class Development(Config):
    TOKEN = '토큰'
    OWNERS = [관리자 디스코드 아이디]
    DebugServer = [디버그 서버 id]
    BOT_NAME = "봇 이름"
    BOT_TAG = "#봇태그"
    BOT_ID = 봇아이디
```
`sample_config.py`를 참고하여 만들면 된다.<br>
3. `python3 -m bot` 명령어로 실행한다.
