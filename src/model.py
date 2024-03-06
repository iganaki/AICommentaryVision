from contextlib import contextmanager
from re import I
from turtle import back
from httpx import stream
from numpy import integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from config import Session
from sqlalchemy.orm import relationship

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

## マスターデータ
# 静的ストリーマープロフィールテーブル
class StaticStreamerProfile(Base):
    __tablename__ = 'static_streamer_profiles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stage_name = Column(String)
    tts_chara = Column(String)
    color = Column(String)
    personality = Column(String)
    speaking_style = Column(String)
    character_images_directory = Column(String)

# VOICEVOX話者テーブル
class VoiceVoxSpeaker(Base):
    __tablename__ = 'voicevox_speakers'
    id = Column(Integer, primary_key=True)
    speaker_name = Column(String)
    style_name = Column(String)
    style_id = Column(Integer)

    # テーブルをリセットするメソッド
    @classmethod
    def set_voicevox_speakers_table(cls, session, speakers):
        # データベースに保存する
        for speaker in speakers:
            speaker_name = speaker["name"]
            for style in speaker["styles"]:
                style_name = style["name"]
                style_id = style["id"]
                voicevox_speaker = cls(speaker_name=speaker_name, style_name=style_name, style_id=style_id)
                session.add(voicevox_speaker)
    
    # テーブルを削除するメソッド
    @classmethod
    def delete_voicevox_speakers_table(cls, session):
        # VoiceVoxSpeakerテーブルの全レコードを削除
        session.query(cls).delete()

# Style-Bert-VITS2話者テーブル
class StyleBertVITS2Speaker(Base):
    __tablename__ = 'stylebertvits2_speaker'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer)
    speaker_name = Column(String)
    style_name = Column(String)
    style_id = Column(Integer)

    # テーブルにデータを保存する
    @classmethod
    def set_stylebertvits2_speakers_table(cls, session, speakers):
        # データベースに保存する
        for model_id, speaker in speakers.items():
            speaker_name = list(speaker["spk2id"].keys())[0]  # 'spk2id'から話者名を取得
            for style_name, style_id in speaker["style2id"].items():
                # データベースに保存
                model_style = StyleBertVITS2Speaker(model_id=int(model_id), speaker_name=speaker_name, style_name=style_name, style_id=style_id)
                session.merge(model_style)  # 重複があれば更新

    # テーブルを削除するメソッド
    @classmethod
    def delete_stylebertvits2_speakers_table(cls, session):
        # StyleBertVITS2Speakerテーブルの全レコードを削除
        session.query(cls).delete()

# 番組タイプテーブル
class ProgramType(Base):
    __tablename__ = 'program_types'
    id = Column(Integer, primary_key=True)
    program_name = Column(String, unique=True)
    program_summary = Column(String)
    streamer_num = Column(Integer)
    background_image_type = Column(Integer) # 0:画像,　1:動画
    user_additional_data1_name = Column(String, nullable=True)
    user_additional_data2_name = Column(String, nullable=True)

# セクションテーブル
class StaticSection(Base):
    __tablename__ = 'static_sections'
    id = Column(Integer, primary_key=True)
    program_name = Column(String)
    section_name = Column(String)
    order  = Column(Integer)
    host_speaking_duration = Column(Integer)
    guest_speaking_duration = Column(Integer)
    background_image_type = Column(Integer) # 0:生成, 1:前から継続, 2:指定したorderの背景と同じ, 3:動画
    background_image_order_num = Column(String, nullable=True)
    background_image_prompt = Column(String, nullable=True)
    background_music_type = Column(Integer) # 0:指定, 1:ランダム, 2:前から継続, 3:指定したorderの背景と同じ, 4:なし
    background_music_path = Column(String, nullable=True)
    end_condition_type = Column(Integer) # 0:時間(秒), 1:セリフ数
    end_condition_value = Column(Integer)
    is_reset_conversation_history = Column(Boolean, default=False)

# システムプロンプトテーブル
class SerifSystemPrompt(Base):
    __tablename__ = 'serif_system_prompts'
    id = Column(Integer, primary_key=True)
    program_name = Column(String)
    section_name = Column(String)
    streamer_type = Column(Integer) # 0:ホスト, 1:ゲスト
    text = Column(String)

# カンペシートテーブル
class CueSheet(Base):
    __tablename__ = 'cue_sheets'
    id = Column(Integer, primary_key=True)
    program_name = Column(String)
    section_name = Column(String)
    streamer_type = Column(Integer) # 0:ホスト, 1:ゲスト
    delivery_sequence = Column(Integer, default=0) # 0がランダム、1以上がそのセクションでの順番
    is_ai = Column(Boolean) # AI生成するかどうか
    cue_text = Column(String) # AIプロンプトまたは固定カンペのテキスト
    min_speech_count = Column(Integer, nullable=True)  # ランダム時のセリフ回数の最小値
    max_speech_count = Column(Integer, nullable=True)  # ランダム時のセリフ回数の最大値

## トランザクションデータ
# 動画情報テーブル
class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    program_name = Column(String)
    video_title = Column(String, unique=True)
    user_additional_data1 = Column(String, nullable=True)
    user_additional_data2 = Column(String, nullable=True) 

# ストリーマープロフィールテーブル
class StreamerProfile(Base):
    __tablename__ = 'streamer_profiles'
    id = Column(Integer, primary_key=True)
    video_title = Column(String)
    name = Column(String)
    stage_name = Column(String)
    tts_chara = Column(String)
    color = Column(String)
    role = Column(Integer)
    personality = Column(String)
    speaking_style = Column(String)
    partner_name = Column(String)
    character_images_directory = Column(String)

# セリフテーブル
class Serif(Base):
    __tablename__ = 'serifs'
    id = Column(Integer, primary_key=True)
    video_title = Column(String)
    section_name = Column(String)
    name = Column(String)
    tts_chara = Column(String)
    color = Column(String)
    text = Column(String)
    voice_duration = Column(Float)
    start_time_sec = Column(Float)
    cue_card = Column(String)
    serif_parts = relationship("SerifPart", backref="serif")

    @classmethod
    def insert_serif(cls, session, video_title, section_name, generate_data):
        serif = cls(video_title=video_title, section_name=section_name, 
                    name=generate_data["name"], tts_chara=generate_data["tts_chara"], 
                    color=generate_data["color"], text=generate_data["text"],
                    voice_duration=generate_data["voice_duration"], start_time_sec=generate_data["start_time_sec"], 
                    cue_card=generate_data["cue_card"])
        session.add(serif)
        return serif
        
    @classmethod
    def get_serif_text_by_section(cls, session, video_title, section_name=None, get_len=0, cue_card_flag=False):
        # セクション名が指定されていない場合は全てのセクションのセリフを取得
        if section_name is None:
            serifs = session.query(cls).filter(cls.video_title == video_title).order_by(cls.start_time_sec).all()
        else:
            serifs = session.query(cls).filter(cls.video_title == video_title).filter(cls.section_name == section_name).order_by(cls.start_time_sec).all()

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

            # cue_card_flagがTrueで、cue_cardが空文字列でない場合に追加
            if cue_card_flag and cue_card:
                formatted_serif = f"{name} : {text} (カンペ：{cue_card})"
            else:
                formatted_serif = f"{name} : {text}"

            # リストに追加
            formatted_serifs.append(formatted_serif)

        # 処理されたセリフのリストを改行で連結して返す
        return '\n'.join(formatted_serifs)
    
# 台詞パートテーブル
class SerifPart(Base):
    __tablename__ = 'serif_parts'
    id = Column(Integer, primary_key=True)
    serif_id = Column(Integer, ForeignKey('serifs.id'))
    part_text = Column(String)
    part_voice = Column(String)
    part_voice_duration = Column(Float)
    emotion = Column(String)
    start_time_sec = Column(Float)
    part_order = Column(Integer)

    @classmethod
    def insert_serif_parts(cls, session, generate_split_serif_data, serif: Serif):
        for i, part_data in enumerate(generate_split_serif_data):
            serif_part = cls(serif_id=serif.id, part_text=part_data["text"], 
                             part_voice=part_data["voice_data"], part_voice_duration=part_data["voice_duration"], 
                             emotion=part_data["emotion"], start_time_sec=part_data["start_time_sec"], 
                             part_order=i, serif=serif)
            session.add(serif_part)                                     

# 動画セクションテーブル
class VideoSection(Base):
    __tablename__ = 'video_sections'
    id = Column(Integer, primary_key=True)
    video_title = Column(String)
    section_name = Column(String)
    order = Column(Integer)
    start_time_sec = Column(Float)
    end_time_sec = Column(Float)
    background_image_path = Column(String)
    background_music_path = Column(String)