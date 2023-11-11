import os
import random
import time
import movie
import audio
import text
from config import OUTPUT_FOLDER, START_TIME, TEMP_FOLDER

def main():
    # 出力するフォルダが存在しない場合は作成
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    # ユーザーが実況者の人物像、動画の概要、動画のパスを入力するGUIを作成
    # GUI作成と入力受付の関数（未実装）
    # narrator_profile, video_summary, video_path = create_gui_and_get_user_input()
    narrator_profile = {
        "name": "ずんだもん",
        "personality": "子供っぽい、素直で冒険心のあふれる性格",
        "speaking_style": "一人称は「ボク」、語尾に「～のだ」「～なのだ」をつける"
    }
    video_summary = {
        "description": "JetIslandというオープンワールドVRゲームの一人称視点の録画"
    }
    video_path       = "D:/douga/kansei/jetisland2.mp4"

    text.write_to_log_file("video_path", video_path, True)

    # キャプチャをとるために動画を読み込んで、動画時間(ミリ秒)を返す。
    total_duration_sec, cap = movie.load_video_and_get_duration(video_path)
    
    # ユーザーから渡された実況者の人物像、動画の概要を使用してシステムプロンプトを作成
    system_prompt = text.create_system_prompt(narrator_profile, video_summary)

    # current_timeを初期化
    current_time = 0.0

    generate_data = []

    # current_timeが動画の総時間を超えるまでループ
    while current_time < total_duration_sec:
        if current_time < START_TIME:
            # 初回の場合、実況開始の挨拶も含めた実況文を作るためのユーザープロンプト作成
            user_prompt = text.create_subsequent_prompt(0, isFirst=True)
            # 0秒からスタートだと違和感があるので、初期動画経過時間を設定
            current_time = START_TIME
        else:
            # 2回目以降の場合、実況文を作るためのユーザープロンプト作成
            user_prompt = text.create_subsequent_prompt(time_passed, isFirst=False)
            pass

        # current_timeの動画キャプチャを取得してBASE64変換
        capture_base64 = movie.get_video_capture_at_time(cap, current_time)

        # キャプチャとプロンプトをGPT 4Vに渡して実況文を生成
        commentary = text.generate_commentary(capture_base64, system_prompt, user_prompt)

        # 実況文からVOICEVOXを使用して音声を生成し、音声ファイルパスを返す。
        audio_path = audio.generate_audio_from_text(commentary)

        # 実況文、音声ファイルパス、current_timeの値を配列(generate_data)に格納
        generate_data.append((commentary, audio_path, current_time))

        # current_timeと動画の総時間を使用してプログレスバーを表示
        # プログレスバーを更新する関数（未実装）
        # update_progress_bar(current_time, total_duration)

        # 音声ファイルの再生時間＋ランダムな間をcurrent_timeに加算
        audio_duration_sec = audio.get_audio_duration(audio_path)
        time_passed =  audio_duration_sec + random.uniform(0.5, 1.5)
        current_time += time_passed

    # キャプチャをとるために読み込んだ動画情報を解放
    cap.release()

    text.reset_previous_messages()

    # generate_data配列を使用して動画に実況音声、字幕を付加して保存
    final_video_path = f'{OUTPUT_FOLDER}/movie_{int(time.time())}.mp4'
    movie.add_audio_and_subtitles_to_video(video_path, generate_data, final_video_path)

    # 作成した動画ユーザーに返す（未実装）
    # save_and_return_video(final_video_path)
    text.write_to_log_file("final_video_path", final_video_path)


if __name__ == "__main__":
    main()