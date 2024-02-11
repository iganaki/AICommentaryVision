import settings
from static_data import Mode
from studio import Studio

def main():
    mode = Mode.DUO_RADIO.value

    if mode == Mode.DUO_RADIO.value:
        video_summary = ""
        video_path = ""
    else:
        # video_summary = "JetIslandというオープンワールドVRゲームをプレイ。今回はダンジョンに潜り、巨大な爬虫類型ボスを倒す"
        video_summary = "ポピュレーションワンというVRFPSで敵と戦闘中"
        # video_summary = "本格スマホeスポーツのシャドウバースで、ローテーション杯のラウンド2をプレイ。使用デッキはバフドラゴン。相手の使用デッキもバフドラゴンです。"

        # video_path       = "D:/douga/kansei/jetisland002_ori.mp4"
        video_path       = "D:/douga/kansei/test.mp4"
        # video_path       = "D:/douga/kansei/sv_1202.mp4"

    database, title = settings.set(mode, video_summary=video_summary, video_path=video_path)
    studio = Studio(database, title)
    video_path = studio.create_video()
    
    # 作成した動画ユーザーに返す（未実装）
    # save_and_return_video(video_path)

if __name__ == "__main__":
    main()