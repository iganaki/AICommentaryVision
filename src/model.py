from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String

from config import Session

Base = declarative_base()

@contextmanager
def session_scope():
    """セッションのスコープを提供するコンテキストマネージャ"""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# カンペテーブル
class CueCard(Base):
    __tablename__ = 'cue_cards'
    id = Column(Integer, primary_key=True)
    cue_card = Column(String)
    cue_card_print = Column(String)
    next_cue = Column(String)
    next_cue_print = Column(String)

# ラジオトークテーマテーブル
class TalkTheme(Base):
    __tablename__ = 'talk_themes'
    id = Column(Integer, primary_key=True)
    theme = Column(String)
    theme_jp = Column(String)
    
# 静的ストリーマープロフィールテーブル
class StaticStreamerProfile(Base):
    __tablename__ = 'static_streamer_profiles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    voicevox_chara = Column(String)
    color = Column(String)
    personality = Column(String)
    speaking_style = Column(String)

# 関係性テーブル
class Relationship(Base):
    __tablename__ = 'relationships'
    id = Column(Integer, primary_key=True)
    our_relationship = Column(String)
    your_role1 = Column(String)
    your_role2 = Column(String)

# VOICEVOX話者テーブル
class VoiceVoxSpeaker(Base):
    __tablename__ = 'voicevox_speakers'
    id = Column(Integer, primary_key=True)
    speaker_name = Column(String)
    style_name = Column(String)
    style_id = Column(String)

# 動画情報テーブル
class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    video_title = Column(String, unique=True)
    mode = Column(Integer)
    video_path = Column(String)
    video_summary = Column(String)

# ストリーマープロフィールテーブル
class StreamerProfile(Base):
    __tablename__ = 'streamer_profiles'
    id = Column(Integer, primary_key=True)
    video_title = Column(String)
    name = Column(String)
    voicevox_chara = Column(String)
    color = Column(String)
    role = Column(Integer)
    personality = Column(String)
    speaking_style = Column(String)
    partner_name = Column(String)
    our_relationship = Column(String)
    your_role = Column(String)

# セリフテーブル
class Serif(Base):
    __tablename__ = 'serifs'
    id = Column(Integer, primary_key=True)
    video_title = Column(String)
    name = Column(String)
    voicevox_chara = Column(String)
    color = Column(String)
    text = Column(String)
    emotion = Column(String)
    voice = Column(String)
    voice_duration = Column(Float)
    start_time_sec = Column(Float)
    cue_card = Column(String)
    cue_card_print = Column(String)

    @classmethod
    def insert_serif(cls, session, video_title, generate_data):
        serif = cls(video_title=video_title, name=generate_data["name"], voicevox_chara=generate_data["voicevox_chara"], 
                    color=generate_data["color"], text=generate_data["text"], emotion=generate_data["emotion"], 
                    voice=generate_data["voice"], voice_duration=generate_data["voice_duration"], 
                    start_time_sec=generate_data["start_time_sec"], cue_card=generate_data["cue_card"], 
                    cue_card_print=generate_data["cue_card_print"])
        session.add(serif)
        session.commit()
        
    @classmethod
    def get_serif_text_by_video_title(cls, session, video_title, get_len, cue_card_flag):
        serifs = session.query(cls).filter(cls.video_title == video_title).all()

        # 結果を格納するためのリスト
        formatted_serifs = []

        # get_lenが0の場合は全てのレコードを、それ以外は指定された数だけレコードを処理
        if get_len == 0:
            selected_serifs = serifs
        else:
            selected_serifs = serifs[:get_len]

        # 処理するセリフデータ
        for serif in selected_serifs:
            name = serif.name
            text = serif.text
            cue_card = serif.cue_card
            cue_card_print = serif.cue_card_print

            # cue_card_flagがTrueで、cue_cardおよびcue_card_printが空文字列でない場合に追加
            if cue_card_flag and cue_card and cue_card_print:
                formatted_serif = f"{name} : {text} (カンペ：{cue_card_print} [{cue_card}])"
            else:
                formatted_serif = f"{name} : {text}"

            # リストに追加
            formatted_serifs.append(formatted_serif)

        # 処理されたセリフのリストを改行で連結して返す
        return '\n'.join(formatted_serifs)
    
# ラジオパートテーブル
class RadioPart(Base):
    __tablename__ = 'radio_parts'
    id = Column(Integer, primary_key=True)
    video_title = Column(String)
    part_name = Column(String)
    talk_theme = Column(String)
    talk_theme_jp = Column(String)
    background_image_pass = Column(String)
