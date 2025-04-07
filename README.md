# Kumoh alarm

본 repository는 컴퓨터공학과 소프트웨어전공 22학번인 안재범 선배님의 디스코드봇 알리미를 fork하였습니다. (https://github.com/ajb3296/Kumoh-alarm)

## 봇 초대

https://discord.com/oauth2/authorize?client_id=1358754351262208021&permissions=1689384584214592&integration_type=0&scope=bot

### 디스코드 서버

https://discord.gg/65qwcUXS

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
