import os
import random
from config import DEBUG_FLAG, OUTPUT_FOLDER, START_TIME, TEMP_FOLDER
import movie
import audio
import text


def initialize_folders():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)

def create_user_gui():
    # ユーザーが実況者の人物像、動画の概要、動画のパスを入力するGUIを作成
    # GUI作成と入力受付の関数（未実装）
    # narrator_profile = {
    #     "name": "ずんだもん",
    #     "personality": "子供っぽい、素直で冒険心のあふれる性格",
    #     "speaking_style": "日本語話者。一人称は「ボク」、語尾に「～のだ」「～なのだ」をつける"
    # }
    narrator_profile = {
        "name": "ホワイトカル",
        "personality": "おもしれー女。調子に乗りがちだが、ちょっとしたことでビビりやすい。",
        "speaking_style": "日本語話者。一人称は「わたし」、語尾は「～です」「～ます」をつける。ネットスラングをよく使う。"
    }
    video_summary = {
        "description": "JetIslandというオープンワールドVRゲームの初見プレイ"
    }
    # video_summary = {
    #     "description": "ポピュレーションワンというVRFPSで敵と戦闘中"
    # }
    video_path       = "D:/douga/kansei/jetisland2.mp4"
    # video_path       = "D:/douga/kansei/test.mp4"

    text.create_log_file()
    text.write_to_log_file("video_path", video_path)

    return video_path, narrator_profile, video_summary


def process_video(video_path, narrator_profile, video_summary):
    # キャプチャをとるために動画を読み込んで、動画時間(ミリ秒)を返す。
    VideoProc = movie.VideoProcessor(video_path)
    total_duration_sec= VideoProc.get_duration()

    # 実況文生成のためのインスタンスを生成し、システムプロンプトも作成
    ComGen = text.CommentaryGenerator(DEBUG_FLAG, narrator_profile, video_summary)

    # Voice生成のためのインスタンスを生成。
    VoiceGen = audio.VoiceGenerator(vvid = 24)

    # current_timeを初期化
    current_time = START_TIME
    time_passed = 0

    generate_data = []

    # current_timeが動画の総時間を超えるまでループ
    while current_time < total_duration_sec:
        # ユーザープロンプトを作成
        user_prompt = ComGen.create_user_prompt(time_passed, isFirst=(current_time == START_TIME))

        # current_timeの動画キャプチャを取得してBASE64変換
        capture_base64_list = [
            # VideoProc.get_video_capture_at_time(current_time-0.5, 1280, 720),
            VideoProc.get_video_capture_at_time(current_time, 1280, 720),
            # VideoProc.get_video_capture_at_time(current_time+0.5, 1280, 720)
        ]

        # キャプチャとユーザープロンプトをGPT 4Vに渡して実況文を生成
        commentary = ComGen.generate_commentary(user_prompt, capture_base64_list)
        if commentary == None:
            break

        # 実況文からVOICEVOXを使用して音声を生成し、音声ファイルパスを返す。
        audio_path = VoiceGen.generate_voice_from_text(commentary)

        # 実況文、音声ファイルパス、current_timeの値を配列(generate_data)に格納
        generate_data.append((commentary, audio_path, current_time))

        # current_timeと動画の総時間を使用してプログレスバーを表示
        # プログレスバーを更新する関数（未実装）
        # update_progress_bar(current_time, total_duration)

        # 音声ファイルの再生時間＋ランダムな間をcurrent_timeに加算
        audio_duration_sec = audio.get_audio_duration(audio_path)
        time_passed =  audio_duration_sec + random.uniform(0.5, 1.5)
        current_time += time_passed

    # generate_data配列を使用して動画に実況音声、字幕を付加して保存
    # final_video_path = VideoProc.add_audio_and_subtitles(generate_data)
    final_video_path = VideoProc.add_audio_and_subtitles_to_video(generate_data)

    # 作成した動画ユーザーに返す（未実装）
    # save_and_return_video(final_video_path)
    text.write_to_log_file("final_video_path", final_video_path)

    return generate_data

def main():
    initialize_folders()
    video_path, narrator_profile, video_summary = create_user_gui()
    process_video(video_path, narrator_profile, video_summary)

if __name__ == "__main__":
    main()