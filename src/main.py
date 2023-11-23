import os
from config import DEBUG_FLAG, DUO_GAMEPLAY_MODE, COMMENTATOR, OUTPUT_FOLDER, PLAYER, SOLO_GAMEPLAY_MODE, SOLO_PLAYER
from studio import Studio


def initialize_folders():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def create_user_gui():
    # ユーザーが実況者の人物像、動画の概要、動画のパスを入力するGUIを作成
    # GUI作成と入力受付の関数（未実装）
    mode = DUO_GAMEPLAY_MODE
    title = ""
    if mode == SOLO_GAMEPLAY_MODE:
        streamer_profile1 = {
            "name": "ずんだもん",
            "voicevox_chara": "ずんだもん",
            "color": "green",
            "role": SOLO_PLAYER,
            "personality": "子供っぽい、素直で冒険心のあふれる性格",
            "speaking_style": "日本語話者。一人称は「ボク」、語尾に「～のだ」「～なのだ」をつける"
        }
        streamer_profile2 = None
    elif mode == DUO_GAMEPLAY_MODE:
        streamer_profile1 = {
            "name": "めたん",
            "voicevox_chara": "四国めたん",
            "color": "#FF1493",
            "role": COMMENTATOR,
            "personality": "いつも落ち着いている。穏やかな性格。",
            "speaking_style": "日本語話者。一人称は「私」、語尾は「～かしら」「なのよね」などをつける。上品な言葉遣いをする。英語に疎く、外来語はあまり使わない",
            "partner_name": "ユキ",
            "partner_relationship": "「ユキ」と呼んでいる。かわいい後輩。からかって反応を楽しむ。"
        }
        streamer_profile2 = {
            "name": "ユキ",
            "voicevox_chara": "WhiteCUL",
            "color": "#000080",
            "role": PLAYER,
            "personality": "非常に感情豊かで、テンションの浮き沈みが激しい。",
            "speaking_style": "日本語話者。一人称は「わたし」、語尾は「～です」「～ます」をつける。慌てると言葉が乱れ、叫んだり、泣き言を言ったりする",
            "partner_name": "めたん",
            "partner_relationship": "尊敬している先輩。"
        }

    video_summary = {
        "description": "JetIslandというオープンワールドVRゲームの初見プレイ"
    }
    # video_summary = {
    #     "description": "ポピュレーションワンというVRFPSで敵と戦闘中"
    # }
    video_path       = "D:/douga/kansei/jetisland2.mp4"
    # video_path       = "D:/douga/kansei/test.mp4"

    return mode, title, video_path, video_summary, streamer_profile1, streamer_profile2

def main():
    initialize_folders()
    mode, title, video_path, video_summary, streamer_profile1, streamer_profile2= create_user_gui()

    studio = Studio(mode, title, streamer_profile1, streamer_profile2)
    video_path = studio.create_video(video_summary, video_path)
    
    # 作成した動画ユーザーに返す（未実装）
    # save_and_return_video(final_video_path)

if __name__ == "__main__":
    main()