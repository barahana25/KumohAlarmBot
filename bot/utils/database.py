"""

ceboard:
    ID, articleNo, title, author

"""

import sqlite3

from bot import db_path, channel_db_path, KumohSquarePage

class ceBoardDB():
    def __init__(self):
        self.db_path = db_path
        self.board_name = "ceboard"

    def set_database(self, tr_list: list) -> None:
        """ 데이터베이스에 데이터 추가 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        # Create table if it doesn't exist
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.board_name} (id integer PRIMARY KEY AUTOINCREMENT, articleNo int, title text, author text)")

        # add se board data
        for tr in tr_list:
            board_id = tr[0]
            title = tr[1]
            author = tr[2]
            
            try:
                cur.execute(f"SELECT * FROM {self.board_name} WHERE articleNo=:Id", {"Id": board_id})
                temp = cur.fetchone()
            except:
                temp = None
            if temp is None:
                cur.execute(f"INSERT INTO {self.board_name} (articleNo, title, author) VALUES(?, ?, ?)", (board_id, title, author))
        con.close()

    def get_database(self) -> list | None:
        """ 모든 데이터베이스 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {self.board_name} ORDER BY id")
        except:
            con.close()
            return None
        temp = cur.fetchall()
        con.close()
        return temp
    
    def get_database_from_id(self, id: int) -> tuple[int, int, str, str, str] | None:
        """ id로 데이터베이스 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {self.board_name} WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            con.close()
            return None
        temp = cur.fetchone()
        con.close()
        return temp

    def get_latest_data_id(self) -> int | None:
        """ 마지막 행 id 리턴 """
        all_db = self.get_database()
        if all_db is None:
            return None
        else:
            return all_db[-1][0]

class aiBoardDB():
    def __init__(self):
        self.db_path = db_path
        self.board_name = "aiboard"

    def set_database(self, tr_list: list) -> None:
        """ 데이터베이스에 데이터 추가 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        # Create table if it doesn't exist
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.board_name} (id integer PRIMARY KEY AUTOINCREMENT, articleNo int, title text, author text)")

        # add se board data
        for tr in tr_list:
            board_id = tr[0]
            title = tr[1]
            author = tr[2]
            
            try:
                cur.execute(f"SELECT * FROM {self.board_name} WHERE articleNo=:Id", {"Id": board_id})
                temp = cur.fetchone()
            except:
                temp = None
            if temp is None:
                cur.execute(f"INSERT INTO {self.board_name} (articleNo, title, author) VALUES(?, ?, ?)", (board_id, title, author))
        con.close()

    def get_database(self) -> list | None:
        """ 모든 데이터베이스 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {self.board_name} ORDER BY id")
        except:
            con.close()
            return None
        temp = cur.fetchall()
        con.close()
        return temp
    
    def get_database_from_id(self, id: int) -> tuple[int, int, str, str, str] | None:
        """ id로 데이터베이스 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {self.board_name} WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            con.close()
            return None
        temp = cur.fetchone()
        con.close()
        return temp

    def get_latest_data_id(self) -> int | None:
        """ 마지막 행 id 리턴 """
        all_db = self.get_database()
        if all_db is None:
            return None
        else:
            return all_db[-1][0]

class KumohSquareDB():
    def __init__(self):
        # 기존 DB에 테이블 얹어서 사용
        # id, postid, link, category, title, author
        self.db_path = db_path

    def set_database(self, tr_list: list) -> None:
        """ 데이터베이스에 데이터 추가 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()

        # 금오광장 게시판 데이터 추가
        for tr in tr_list:
            # 변수 설정
            board_name, post_num, post_link, category, title, author = tr
            # 테이블 없으면 생성
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {board_name} (id integer PRIMARY KEY AUTOINCREMENT, 
                                                                    postid int,
                                                                    link text,
                                                                    category text,
                                                                    title text,
                                                                    author text)
            """)

            # SQL 텍스트 처리
            title = title.replace("'", "''")
            author = author.replace("'", "''")
            
            try:
                cur.execute(f"SELECT * FROM {board_name} WHERE postid=:Id", {"Id": post_num})
                temp = cur.fetchone()
            except:
                temp = None
            # 데이터베이스에 없으면 추가
            if temp is None:
                cur.execute(f"INSERT INTO {board_name} (postid, link, category, title, author) VALUES(?, ?, ?, ?, ?)", (post_num, post_link, category, title, author))
        con.close()

    def get_database(self, table: str) -> list | None:
        """ 해당 테이블의 데이터베이스 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {table} ORDER BY id")
        except:
            con.close()
            return None
        temp = cur.fetchall()
        con.close()
        return temp
    
    def get_database_from_id(self, table: str, id: int) -> tuple[int, int, str, str, str, str] | None:
        """ id로 데이터 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {table} WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            con.close()
            return None
        temp = cur.fetchone()
        con.close()
        return temp

    def get_latest_data_id(self, table: str) -> int | None:
        """ 테이블의 마지막 행 id 리턴 """
        all_db = self.get_database(table)
        if all_db is None:
            return None
        else:
            return all_db[-1][0]
    
    def get_all_latest_data_ids(self) -> dict[str, int]:
        """ 모든 테이블의 마지막 행 id 리턴 """
        all_ids = {}
        for table in KumohSquarePage.name_list():
            latest_data = self.get_latest_data_id(table)
            if latest_data is not None:
                all_ids[table] = latest_data
        return all_ids # {table_name: id}

class BiskitDB():
    def __init__(self):
        # 기존 DB에 테이블 얹어서 사용
        # id, postid, link, category, title, author
        self.db_path = db_path
        self.board_name = "biskit"

    def set_database(self, tr_list: list) -> None:
        """ 데이터베이스에 데이터 추가 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        # 테이블 없으면 생성
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.board_name} (id integer PRIMARY KEY AUTOINCREMENT, 
                                                                postid int,
                                                                title text,
                                                                org text)
        """)

        # 비스킷 게시글 데이터 추가
        for tr in tr_list:
            # 변수 설정
            post_id, title, org = tr

            # SQL 텍스트 처리
            title = title.replace("'", "''")
            
            try:
                cur.execute(f"SELECT * FROM {self.board_name} WHERE postid=:Id", {"Id": post_id})
                temp = cur.fetchone()
            except:
                temp = None
            # 데이터베이스에 없으면 추가
            if temp is None:
                cur.execute(f"INSERT INTO {self.board_name} (postid, title, org) VALUES(?, ?, ?)", (post_id, title, org))
        con.close()

    def get_database(self, table: str) -> list | None:
        """ 해당 테이블의 데이터베이스 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {table} ORDER BY id")
        except:
            con.close()
            return None
        temp = cur.fetchall()
        con.close()
        return temp
    
    def get_database_from_id(self, id: int) -> tuple[int, int, str, str, str, str] | None:
        """ id로 데이터 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {self.board_name} WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            con.close()
            return None
        temp = cur.fetchone()
        con.close()
        return temp

    def get_latest_data_id(self, table: str) -> int | None:
        """ 테이블의 마지막 행 id 리턴 """
        all_db = self.get_database(table)
        if all_db == []:
            return None
        else:
            return all_db[-1][0]

class channelDataDB():
    def __init__(self):
        self.db_path = channel_db_path

    def channel_status_set(self, table: str, id: int, status: str) -> None:
        """ 채널 알림설정 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        # Create table if it doesn't exist
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (id integer PRIMARY KEY, onoff text)")
        try:
            cur.execute(f"SELECT * FROM {table} WHERE id=:id", {"id": id})
            a = cur.fetchone()
        except:
            a = None
        if a is None:
            # add channel set
            cur.execute(f"INSERT INTO {table} VALUES(?, ?)", (id, status))
        else:
            # modify channel set
            cur.execute(f"UPDATE {table} SET onoff=:onoff WHERE id=:id", {"onoff": status, 'id': id})
        con.close()

    def get_on_channel(self, table: str) -> list[int] | None:
        """ 테이블의 모든 알람설정 되어있는 채널 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM {table} ORDER BY id")
        except sqlite3.OperationalError:
            return None
        temp = cur.fetchall()
        con.close()

        on_channel = []
        for channel in temp:
            if channel[1] == "on":
                on_channel.append(channel[0])
        return on_channel

    def get_on_channel_for_all_table(self) -> dict[str, list[int]]:
        """ 모든 테이블의 알람설정 되어있는 채널 가져오기 """
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM sqlite_master WHERE type='table'")
            all_table = cur.fetchall()
        except sqlite3.OperationalError:
            return None
        all_table_list = [table[1] for table in all_table]
        on_channel = {}
        for table in all_table_list:
            on_channel[table] = self.get_on_channel(table)
        con.close()
        return on_channel

if __name__ == "__main__":
    db_path = "ce_board.db"
    channel_db_path = "channel.db"
    post_list = [(80000, '제목1', '글쓴이1'), (80001, '제목2', '글쓴이2')]
    ceBoardDB().set_database(post_list)