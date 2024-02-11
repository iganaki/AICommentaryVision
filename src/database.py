import os
from re import S
import sqlite3
from config import DATABASE_FOLDER

from static_data import CUE_CARD_DATA, RELATIONSHIP_DATA, STATIC_STREAMER_PROFILES_DATA, TALK_THEME_DATA

class Database:
    def __init__(self, db_name):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        os.makedirs(DATABASE_FOLDER, exist_ok=True)
        database_path = os.path.join(current_directory, '..', 'db', db_name)
        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row

    def create_master_data_table(self):
        with self.conn:
            # カンペテーブル
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS cue_cards (
                    id INTEGER PRIMARY KEY,
                    cue_card TEXT,
                    cue_card_print TEXT,
                    next_cue TEXT,
                    next_cue_print TEXT
                )
            ''')
            # データが存在するか確認し、存在しない場合はデータを追加
            if not self.is_setup_database_table_present("cue_cards"):
                self.setup_cue_card_table()

            # トークテーマテーブル
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS talk_themes (
                    id INTEGER PRIMARY KEY,
                    theme TEXT,
                    theme_jp TEXT
                )
            ''')

            # データが存在するか確認し、存在しない場合はデータを追加
            if not self.is_setup_database_table_present("talk_themes"):
                self.setup_talk_theme_table()

            # ストリーマープロフィールテーブル
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS static_streamer_profiles (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    voicevox_chara TEXT,
                    color TEXT,
                    personality TEXT,
                    speaking_style TEXT
                )
            ''')

            # データが存在するか確認し、存在しない場合はデータを追加
            if not self.is_setup_database_table_present("static_streamer_profiles"):
                self.setup_static_streamer_profiles_table()

            # 関係性テーブル
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY,
                    our_relationship TEXT,
                    your_role1 TEXT,
                    your_role2 TEXT
                )
            ''')

            # データが存在するか確認し、存在しない場合はデータを追加
            if not self.is_setup_database_table_present("relationships"):
                self.setup_relationship_table()

            # 別のマスタテーブルもここに書く
                
    # データが存在するか確認
    def is_setup_database_table_present(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM ' + table_name)
        count = cursor.fetchone()[0]  # 最初のカラムの値を取得
        cursor.close()
        return count > 0

    # 初期化時にまとめて追加
    def setup_cue_card_table(self):
        with self.conn:
            self.conn.executemany('INSERT INTO cue_cards (cue_card, cue_card_print, next_cue, next_cue_print) VALUES (?, ?, ?, ?)', CUE_CARD_DATA)
            
    # 個別追加用
    def insert_cue_card(self, cue_card_data):
        with self.conn:
            self.conn.execute('INSERT INTO cue_cards (cue_card, cue_card_print, next_cue, next_cue_print) VALUES (?, ?, ?, ?)', cue_card_data)

    # まとめて取得
    def fetch_all_cue_cards(self):
        query = 'SELECT * FROM cue_cards'
        return self._fetch_data(query)
    
    # 初期化時にまとめて追加
    def setup_talk_theme_table(self):
        with self.conn:
            self.conn.executemany('INSERT INTO talk_themes (theme, theme_jp) VALUES (?, ?)', TALK_THEME_DATA)

    # まとめて取得
    def fetch_all_talk_themes(self):
        query = 'SELECT * FROM talk_themes'
        return self._fetch_data(query)
    
    # 初期化時にまとめて追加
    def setup_static_streamer_profiles_table(self):
        with self.conn:
            self.conn.executemany('INSERT INTO static_streamer_profiles (name, voicevox_chara, color, personality, speaking_style) VALUES (?, ?, ?, ?, ?)', STATIC_STREAMER_PROFILES_DATA)

    # まとめて取得
    def fetch_all_static_streamer_profiles(self):
        query = 'SELECT * FROM static_streamer_profiles'
        return self._fetch_data(query)
    
    # 初期化時にまとめて追加
    def setup_relationship_table(self):
        with self.conn:
            self.conn.executemany('INSERT INTO relationships (our_relationship, your_role1, your_role2) VALUES (?, ?, ?)', RELATIONSHIP_DATA)

    # まとめて取得
    def fetch_all_relationships(self):
        query = 'SELECT * FROM relationships'
        return self._fetch_data(query)
    
    def create_videos_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY,
                    video_title TEXT UNIQUE,
                    mode INTEGER,
                    video_path TEXT,
                    video_summary TEXT
                )
            ''')
             # インデックスの作成
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_video_title ON videos (video_title)')

    def insert_video(self, video_data):
        with self.conn:
            self.conn.execute('''
                INSERT INTO videos (video_title, mode, video_path, video_summary) 
                VALUES (?, ?, ?, ?)
            ''', (
                video_data["video_title"],
                video_data["mode"],
                video_data["video_path"],
                video_data["video_summary"]
            ))
    
    def fetch_video_by_title(self, video_title):
        query = 'SELECT * FROM videos WHERE video_title = ?'
        return self._fetch_data(query, (video_title,))
    
    def create_streamer_profiles_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS streamer_profiles (
                    id INTEGER PRIMARY KEY,
                    video_title TEXT,
                    name TEXT,
                    voicevox_chara TEXT,
                    color TEXT,
                    role INTEGER,
                    personality TEXT,
                    speaking_style TEXT,
                    partner_name TEXT,
                    our_relationship TEXT,
                    your_role TEXT
                )
            ''')
             # インデックスの作成
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_video_title ON streamer_profiles (video_title)')

    def insert_streamer_profile(self, video_title, profile):
        with self.conn:
            self.conn.execute('''
                INSERT INTO streamer_profiles 
                (video_title, name, voicevox_chara, color, role, personality, speaking_style, partner_name, our_relationship, your_role) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video_title,
                profile["name"],
                profile["voicevox_chara"],
                profile["color"],
                profile["role"],  # Enum の値を使用
                profile["personality"],
                profile["speaking_style"],
                profile["partner_name"],
                profile["our_relationship"],
                profile["your_role"]
            ))
      
    def fetch_streamer_profiles_by_video_title(self, video_title):
        query = 'SELECT * FROM streamer_profiles WHERE video_title = ?'
        return self._fetch_data(query, (video_title,))
    
    def create_serifs_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS serifs (
                    id INTEGER PRIMARY KEY,
                    video_title TEXT,
                    name TEXT,
                    voicevox_chara TEXT,
                    color TEXT,
                    text TEXT,
                    emotion TEXT,
                    voice TEXT,
                    voice_duration REAL,
                    start_time_sec REAL,
                    cue_card TEXT,
                    cue_card_print TEXT
                )
            ''')
             # インデックスの作成
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_video_title ON serifs (video_title)')

    # 1セリフデータを挿入
    def insert_serif(self, video_title, generate_data):
        with self.conn:
            self.conn.execute('''
                INSERT INTO serifs (video_title, name, voicevox_chara, color, text, emotion, voice, voice_duration, start_time_sec, cue_card, cue_card_print)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (video_title, generate_data["name"], generate_data["voicevox_chara"], generate_data["color"], generate_data["text"], generate_data["emotion"], generate_data["voice"], generate_data["voice_duration"], generate_data["start_time_sec"], generate_data["cue_card"], generate_data["cue_card_print"]))

    def get_serif_text_by_video_title(self, video_title, get_len, cue_card_flag):
        # 指定したvideo_titleのセリフデータを取得
        serifs = self.fetch_serifs_by_video_title(video_title)

        # 結果を格納するためのリスト
        formatted_serifs = []

        # get_lenが0の場合は全てのレコードを、それ以外は指定された数だけレコードを処理
        if get_len == 0:
            selected_serifs = serifs
        else:
            selected_serifs = serifs[:get_len]

        # 処理するセリフデータ
        for serif in selected_serifs:
            name = serif['name']
            text = serif['text']
            cue_card = serif['cue_card']
            cue_card_print = serif['cue_card_print']

            # cue_card_flagがTrueで、cue_cardおよびcue_card_printが空文字列でない場合に追加
            if cue_card_flag and cue_card and cue_card_print:
                formatted_serif = f"{name} : {text} (カンペ：{cue_card_print} [{cue_card}])"
            else:
                formatted_serif = f"{name} : {text}"

            # リストに追加
            formatted_serifs.append(formatted_serif)

        # 処理されたセリフのリストを改行で連結して返す
        return '\n'.join(formatted_serifs)


    # 指定したvideo_titleのセリフデータをすべて取得
    def fetch_serifs_by_video_title(self, video_title):
        query = 'SELECT * FROM serifs WHERE video_title = ?'
        return self._fetch_data(query, (video_title,))
    
    # 指定したvideo_titleのセリフデータが存在しないことを確認
    def is_video_title_present(self, video_title):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM serifs WHERE video_title = ?', (video_title,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    
    # 指定したvideo_titleのセリフデータをすべて削除
    def delete_serifs_by_video_title(self, video_title):
        with self.conn:
            self.conn.execute('DELETE FROM serifs WHERE video_title = ?', (video_title,))

    # ラジオパートテーブルを作成
    def create_radio_parts_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS radio_parts (
                    id INTEGER PRIMARY KEY,
                    video_title TEXT,
                    part_name TEXT,
                    talk_theme TEXT,
                    talk_theme_jp TEXT,
                    background_image_url TEXT
                )
            ''')
             # インデックスの作成
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_video_title ON radio_parts (video_title)')

    # ラジオパートを挿入
    def insert_radio_part(self, video_title, part_name, talk_theme):
        with self.conn:
            self.conn.execute('''
                INSERT INTO radio_parts (video_title, part_name, talk_theme, talk_theme_jp, background_image_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (video_title, part_name, talk_theme['theme'], talk_theme['theme_jp'], talk_theme['background_image_url']))

    # 指定したvideo_titleのラジオパートをすべて取得
    def fetch_radio_parts_by_video_title(self, video_title):
        query = 'SELECT * FROM radio_parts WHERE video_title = ?'
        return self._fetch_data(query, (video_title,))

    def _fetch_data(self, query, params=None, fetch_all=True):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall() if fetch_all else None
        cursor.close()
        return [dict(row) for row in rows]

    # データベースの終了処理
    def close(self):
        self.conn.close()