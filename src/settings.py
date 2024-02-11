import os
import random
import re
import time
from config import OUTPUT_FOLDER
from database import Database
from static_data import Mode, Role


def set(mode, title = "", video_summary = "", video_path = ""):

    database = _initialize_project()

    if title == "":
        title = str(int(time.time()))
    if database.is_video_title_present(title):
        raise ValueError("すでにそのタイトルの動画が存在します。")

    database.insert_video({
    "video_title": title,
    "mode": mode,
    "video_summary": video_summary,
    "video_path": video_path
    })

    _set_streamer_profiles(database, mode, title)

    return database, title

def _initialize_project():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    database = Database("AICommentaryVision.db")
    database.create_master_data_table()
    database.create_videos_table()
    database.create_streamer_profiles_table()
    database.create_serifs_table()
    database.create_radio_parts_table()

    return database

def _set_streamer_profiles(database:Database, mode, title):

    # データベースにストリーマーのプロフィールを取得
    streamer_profiles = []
    static_streamer_profiles = database.fetch_all_static_streamer_profiles()
    selected_static_streamer_profile = random.choice(static_streamer_profiles)
    streamer_profiles.append(selected_static_streamer_profile)
    # モードが二人用の場合
    if mode is Mode.DUO_RADIO.value or mode is Mode.DUO_GAMEPLAY.value:
        static_streamer_profiles.remove(selected_static_streamer_profile)
        # 二人目のプロフィールを取得
        streamer_profiles.append(random.choice(static_streamer_profiles))
        # データベースから関係性を取得
        relationships = random.choice(database.fetch_all_relationships())
        your_roles = [relationships["your_role2"], relationships["your_role1"]]

    # データベースにストリーマーのプロフィールを登録
    for index, streamer_profile in enumerate(streamer_profiles):
        streamer_profile["role"] = _get_role(mode, index)
        if len(streamer_profiles) == 1:
            streamer_profile["partner_name"] = ""
            streamer_profile["partner_relationship"] = ""
            streamer_profile["your_role"] = ""
        else:
            streamer_profile["partner_name"] = streamer_profiles[1-index]["name"]
            streamer_profile["our_relationship"] = relationships["our_relationship"]
            streamer_profile["your_role"] = your_roles[1-index]

        database.insert_streamer_profile(title, streamer_profile)



def _get_role(mode, index):
    if mode is Mode.DUO_RADIO.value:
        if index == 0:
            return Role.RADIO_PERSONALITY1.value
        else:
            return Role.RADIO_PERSONALITY2.value
    elif mode is Mode.DUO_GAMEPLAY.value:
        if index == 0:
            return Role.COMMENTATOR.value
        else:
            return Role.PLAYER.value
    elif mode is Mode.SOLO_GAMEPLAY.value:
        return Role.RADIO_PERSONALITY.value