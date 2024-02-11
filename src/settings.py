import os
import random
import re
import time
from turtle import st
from audio import VoiceGenerator
from config import Session, engine
from model import Base, CueCard, Relationship, StaticStreamerProfile, StreamerProfile, TalkTheme, Video
from static_data import CUE_CARD_DATA, RELATIONSHIP_DATA, STATIC_STREAMER_PROFILES_DATA, TALK_THEME_DATA, Mode, Role
from studio import Studio

def initialize_project():
    # データベースの初期化
    Base.metadata.create_all(engine)
    session = Session()
    
    # 静的データとモデルクラスのマッピング
    static_data_mappings = {
        CueCard: CUE_CARD_DATA,
        TalkTheme: TALK_THEME_DATA,
        Relationship: RELATIONSHIP_DATA,
        StaticStreamerProfile: STATIC_STREAMER_PROFILES_DATA
    }
    # 共通メソッドを使用して静的データを挿入
    for model_class, data_list in static_data_mappings.items():
        _insert_static_data(session, model_class, data_list)
    
    # TTSの初期化
    VoiceGenerator.set_tts()
    
    session.close()

def _insert_static_data(session, model_class, data_list):
    if session.query(model_class).count() == 0:
        for data in data_list:
            model_instance = model_class(**data)
            session.add(model_instance)
        session.commit()

def set(mode, title = "", video_summary = "", video_path = ""):
    # タイトルが空の場合は現在の時間をタイトルにする
    if title == "":
        title = str(int(time.time()))
    session = Session()
    # すでにそのタイトルの動画が存在する場合はエラー
    if session.query(Video).filter(Video.video_title == title).first() is not None:
        raise Exception("すでにそのタイトルの動画が存在します")
    # 動画情報をデータベースに登録    
    video = Video(video_title=title, mode=mode, video_summary=video_summary, video_path=video_path)
    session.add(video)
    session.commit()
    session.close()

    _set_streamer_profiles(mode, title)

    studio = Studio(title)

    return studio

def _set_streamer_profiles(mode, title):
    session = Session()

    # データベースからストリーマーのプロフィールを取得
    streamer_profiles = []
    static_streamer_profiles = session.query(StaticStreamerProfile).all()
    selected_static_streamer_profile = random.choice(static_streamer_profiles)
    streamer_profiles.append(selected_static_streamer_profile)
    # モードが二人用の場合
    if mode is Mode.DUO_RADIO.value or mode is Mode.DUO_GAMEPLAY.value:
        static_streamer_profiles.remove(selected_static_streamer_profile)
        # 二人目のプロフィールを取得
        streamer_profiles.append(random.choice(static_streamer_profiles))
        # データベースから関係性を取得
        relationships = random.choice(session.query(Relationship).all())
        your_roles = [relationships.your_role2, relationships.your_role1]

    # データベースにストリーマーのプロフィールを登録
    for index, temp_streamer_profile in enumerate(streamer_profiles):
        role = _get_role(mode, index)
        if len(streamer_profiles) == 1:
            partner_name = ""
            our_relationship = ""
            your_role = ""
        else:
            partner_name = streamer_profiles[1-index].name
            our_relationship = relationships.our_relationship
            your_role = your_roles[1-index]
        streamer_profile = StreamerProfile(
            video_title=title, 
            name=temp_streamer_profile.name, 
            voicevox_chara=temp_streamer_profile.voicevox_chara, 
            color=temp_streamer_profile.color, 
            role=role, 
            personality=temp_streamer_profile.personality, 
            speaking_style=temp_streamer_profile.speaking_style, 
            partner_name=partner_name, 
            our_relationship=our_relationship, 
            your_role=your_role)
        session.add(streamer_profile)
    session.commit()
    session.close() 

def _get_role(mode, index):
    if mode is Mode.DUO_RADIO.value:
        if index == 0:
            return Role.DUO_RADIO_HOST.value
        else:
            return Role.DUO_RADIO_GUEST.value
    elif mode is Mode.DUO_GAMEPLAY.value:
        if index == 0:
            return Role.DUO_GAME_COMMENTATOR.value
        else:
            return Role.DUO_GAME_PLAYER.value
    elif mode is Mode.SOLO_GAMEPLAY.value:
        return Role.SOLO_PLAYER.value