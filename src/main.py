import os
import time
from config import OUTPUT_FOLDER
from database import Database
from static_data import Mode, Role
from studio import Studio


def initialize_project():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    database = Database("AICommentaryVision.db")
    database.create_master_data_table()
    database.create_videos_table()
    database.create_streamer_profiles_table()
    database.create_serifs_table()

    return database

def create_user_gui(database:Database):
    # ユーザーが実況者の人物像、動画の概要、動画のパスを入力するGUIを作成
    # GUI作成と入力受付の関数（未実装）
    mode = Mode.DUO_GAMEPLAY.value
    title = ""
    if title == "":
        title = str(int(time.time()))
    if database.is_video_title_present(title):
        raise ValueError("すでにそのタイトルの動画が存在します。")

    video_summary = "JetIslandというオープンワールドVRゲームをプレイ。今回はダンジョンに潜り、巨大な爬虫類型ボスを倒す"
    # video_summary = "ポピュレーションワンというVRFPSで敵と戦闘中"

    video_path       = "D:/douga/kansei/jetisland002_ori.mp4"
    # video_path       = "D:/douga/kansei/test.mp4"

    database.insert_video({
        "video_title": title,
        "mode": mode,
        "video_summary": video_summary,
        "video_path": video_path
        })

    if mode == Mode.SOLO_GAMEPLAY.value:
        streamer_profile1 = {
            "name": "ずんだもん",
            "voicevox_chara": "ずんだもん",
            "color": "green",
            "role": Role.SOLO_PLAYER.value,
            "personality": "子供っぽい、素直で冒険心のあふれる性格",
            "speaking_style": "日本語話者。一人称は「ボク」、語尾に「～のだ」「～なのだ」をつける"
        }
        database.insert_streamer_profile(title, streamer_profile1)
    elif mode == Mode.DUO_GAMEPLAY.value:
        # streamer_profile1 = {
        #     "name": "めたん",
        #     "voicevox_chara": "四国めたん",
        #     "color": "#FF1493",
        #     "role": Role.COMMENTATOR.value,
        #     "personality": "いつも落ち着いている。穏やかな性格。",
        #     "speaking_style": "日本語話者。一人称は「私」、語尾は「～かしら」「なのよね」などをつける。上品な言葉遣いをする。英語に疎く、外来語はあまり使わない",
        #     "partner_name": "ユキ",
        #     "partner_relationship": "「ユキ」と呼んでいる。かわいい後輩。からかって反応を楽しむ。"
        # }
        # streamer_profile2 = {
        #     "name": "ユキ",
        #     "voicevox_chara": "WhiteCUL",
        #     "color": "#000080",
        #     "role": Role.PLAYER.value,
        #     "personality": "非常に感情豊かで、浮かれたり怖がったりとテンションの浮き沈みが激しい。",
        #     "speaking_style": "日本語話者。一人称は「わたし」、語尾は「～です」「～ます」をつける。慌てると言葉が乱れ、叫んだり、泣き言を言ったりする",
        #     "partner_name": "めたん",
        #     "partner_relationship": "尊敬している先輩。"
        # }
        streamer_profile1 = {
            "name": "中国うさぎ",
            "voicevox_chara": "中国うさぎ",
            "color": "#dc143c ",
            "role": Role.COMMENTATOR.value,
            "personality": "ダウナーで暗めの性格。ゲームは好き",
            "speaking_style": "日本語話者。一人称は「私」。ぼそぼそとしたしゃべり方をする",
            "partner_name": "ずんだもん",
            "partner_relationship": "「ずんだもん」と呼んでいる。ゲーム友達。"
        }
        streamer_profile2 = {
            "name": "ずんだもん",
            "voicevox_chara": "ずんだもん",
            "color": "green",
            "role": Role.PLAYER.value,
            "personality": "ずんだの妖精。明るく活発な性格。ゲームには疎い。",
            "speaking_style": "日本語話者。一人称は「ぼく」、語尾は「～のだ」「～なのだ」をつける。",
            "partner_name": "中国うさぎ",
            "partner_relationship": "「うさぎ」と呼んでいる。友達。よく世話を焼いている"
        }
        database.insert_streamer_profile(title, streamer_profile1)
        database.insert_streamer_profile(title, streamer_profile2)


    return title

def main():
    database = initialize_project()
    title = create_user_gui(database)

    studio = Studio(database, title)
    video_path = studio.create_video()
    
    # 作成した動画ユーザーに返す（未実装）
    # save_and_return_video(final_video_path)

if __name__ == "__main__":
    main()