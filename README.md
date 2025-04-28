# Kumoh Alarm 설치 및 사용 가이드

## 목표
이 문서는 Kumoh Alarm 디스코드 봇을 설치하고, 주요 명령어를 사용하여 원하는 알림 기능을 설정하는 방법을 안내합니다.

## 사전 준비 사항
- Python 3 설치
- Discord 계정 및 서버 관리 권한
- Git 사용 가능
- (Linux/Mac 기준) bash 환경 설정 가능

---

## 설치 방법

### 1. 리포지토리 클론
먼저 원본 리포지토리를 fork하고, 본인 계정으로 클론합니다.

```bash
git clone https://github.com/본인계정/Kumoh-alarm.git
cd Kumoh-alarm
```

### 2. `config.py` 파일 생성
`bot` 폴더 안에 `config.py` 파일을 생성하고, 다음과 같이 작성합니다.

```python
from bot.sample_config import Config

class Development(Config):
    TOKEN = '디스코드 봇 토큰'
    OWNERS = [관리자 디스코드 ID]
    DebugServer = [디버그 서버 ID]
    BOT_NAME = "봇 이름"
    BOT_TAG = "#봇태그"
    BOT_ID = 봇 ID
```
- 참고: `bot/sample_config.py` 파일을 참고하면 됩니다.

### 3. 비스킷 자동 로그인 설정
`utils/biskit_preview.py`에서는 `os.environ`을 사용해 자동 로그인을 설정합니다.

Linux/Mac 기준으로, 홈 디렉터리의 `~/.bashrc` 파일에 다음 내용을 추가합니다:

```bash
export hakbun=학번
export password=비밀번호
```

변경사항을 적용하려면:

```bash
source ~/.bashrc
```

### 4. 봇 실행
아래 명령어로 봇을 실행합니다.

```bash
python3 -m bot
```

---

## 디스코드 봇 사용법

봇 초대 링크: [여기 클릭](https://discord.com/oauth2/authorize?client_id=1358754351262208021&permissions=1689384584214592&integration_type=0&scope=bot)

### 주요 명령어 목록

- `/alarmset table {테이블 이름} onoff {ON|OFF}`  
  → 알림 받을 테이블을 설정합니다.

- `/alarmstatus`  
  → 현재 채널의 알림 설정 상태를 확인합니다.

- `/scheduleset {ON|OFF}`  
  → 학사일정 알림을 설정합니다.

- `/schedulestatus`  
  → 학사일정 알림 상태를 확인합니다.

- `/room building {건물명} classroom {강의실명}`  
  → 오늘 해당 강의실의 수업 일정을 확인합니다.

- `/room_day building {건물명} classroom {강의실명} day {요일}`  
  → 특정 요일의 수업 일정을 확인합니다.

- `/room_ready_now building {건물명} duration {시간}`  
  → 현재 시간 기준으로 비어 있는 강의실을 찾습니다.

> 나머지 명령어는 `/`를 입력해 확인할 수 있습니다.

#### 테이블 이름 목록
- 금오광장 (학사 안내, 행사 안내, 일반 소식)
- 비스킷 (마일리지)
- 컴퓨터공학과 (공지사항)
- 학식당, 교직원식당, 푸름관, 오름1관, 오름23관

---

## 참고: 디스코드 서버
- 공식 서버 링크: [https://discord.gg/tgMFRQED](https://discord.gg/tgMFRQED)

---

## 자주 묻는 질문(FAQ)

**Q. config.py를 만들었는데 봇이 실행되지 않아요.**  
- `TOKEN` 값이 올바른지, `OWNERS`, `DebugServer` 값이 리스트 형태인지 다시 확인하세요.

**Q. bashrc 설정 후에도 자동 로그인이 되지 않아요.**  
- `source ~/.bashrc` 명령어를 실행했는지, 혹은 터미널을 재시작했는지 확인해 주세요.

**Q. 명령어 입력 시 오류가 발생해요.**  
- 디스코드 봇 권한 설정이 제대로 되어 있는지 확인하세요. 필요한 권한: 메시지 읽기/쓰기, 슬래시 명령어 사용.

---
