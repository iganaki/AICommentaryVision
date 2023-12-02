import os
import random
from config import OUTPUT_FOLDER, RADIO_DURATION_SEC, START_TIME
from database import Database
from director import Director
from static_data import Mode
from streamer import Streamer
from movie import VideoProcessor
import log

class Studio:
    def __init__(self, database: Database, title):
        self.database = database

        video_data = database.fetch_video_by_title(title)
        self.video_data = video_data[0]
        streamers = database.fetch_streamer_profiles_by_video_title(title)
        self.streamers = []
        for streamer in streamers:
            self.streamers.append(Streamer(streamer))

        self.director = Director()

        self.title = title
        self.output_path = OUTPUT_FOLDER + "/" + self.title
        self.temp_path = self.output_path + "/temp"
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.temp_path, exist_ok=True)

        self.log = log.Log(self.output_path, title)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.close()

    def create_video(self):
        # ディレクターの準備
        self.director.prepare_for_streaming(self.streamers, self.video_data["video_summary"], self.video_data["video_title"], self.database)

        #  ストリーマーの準備
        for streamer in self.streamers:
            streamer.prepare_for_streaming(self.output_path, self.log, self.video_data["video_summary"])

        self.speak_counter = 0

        # 動画の読み込み
        video_processor = VideoProcessor(self.video_data["video_path"])
        self.log.write_to_log_file("video_path", self.video_data["video_path"])

        if self.video_data["mode"] == Mode.SOLO_GAMEPLAY.value:
            self._create_solo_commentary(video_processor)
        elif self.video_data["mode"] == Mode.DUO_GAMEPLAY.value:
            self._create_duo_commentary(video_processor)
        elif self.video_data["mode"] == Mode.DUO_RADIO.value:
            self._create_duo_radio()
        else:
            raise ValueError("無効なモードです")

        # 動画に実況音声、字幕を付加して保存
        final_video_path = video_processor.add_audio_and_subtitles_to_video(self.output_path, self.title, self.database)
        self.log.write_to_log_file("final_video_path", final_video_path)

        self.log.write_to_log_file("まとめ", self.database.get_serif_text_by_video_title(self.video_data["video_title"], 0, True))

        return final_video_path

    def _create_solo_commentary(self, video_processor:VideoProcessor):
        # 初期化
        total_duration_sec = video_processor.get_duration()
        current_time = START_TIME
        time_passed = 0
        generate_data_list = []

        # current_timeが動画の総時間を超えるまでループ
        while current_time < total_duration_sec:
            
            # 進捗状況を表示
            log.update_dialogue_progress(total_duration_sec, current_time)
            
            # current_timeの動画キャプチャを取得してBASE64変換
            capture_base64_list = [
                # VideoProc.get_video_capture_at_time(current_time-0.5, 1280, 720),
                video_processor.get_video_capture_at_time(current_time, 1280, 720),
                # VideoProc.get_video_capture_at_time(current_time+0.5, 1280, 720)
            ]

            # カンペを生成
            cue_card = self._create_cue_card(current_time)

            # ストリーマーのセリフを生成
            generate_data = self.streamers[0].speak(capture_base64_list, time_passed, cue_card)
            # テキスト生成でエラーが出ていた場合、終了してその時点までの動画を作成
            if generate_data["text"] is None:
                break

            # generate_dataにセリフの入るタイミングを追加して、generate_data_listに追加
            generate_data["start_time_sec"] = current_time
            generate_data_list.append(generate_data)

            # 音声ファイルの再生時間＋ランダムな間をcurrent_timeに加算
            time_passed =  generate_data["voice_duration"] + random.uniform(0.5, 1.5)
            current_time += time_passed

        log.update_dialogue_progress(total_duration_sec, total_duration_sec)

        return generate_data_list

    def _create_duo_commentary(self, video_processor:VideoProcessor):
        # 初期化
        total_duration_sec = video_processor.get_duration()
        current_time = START_TIME
        time_passed = 0
        streamer_toggle = 0
        partner_message = ""
        extra_rounds = 3

        # 動画終了に近くなるまでループ
        while extra_rounds > 0:
            
            # 進捗状況を表示
            log.update_dialogue_progress(total_duration_sec, current_time)

            if total_duration_sec - current_time <= 30.0 and extra_rounds > 0:
                extra_rounds -= 1  # 残りのループ回数を減らす
            
            # current_timeの動画キャプチャを取得してBASE64変換
            capture_base64_list = [
                # VideoProc.get_video_capture_at_time(current_time-0.5, 1280, 720),
                video_processor.get_video_capture_at_time(current_time),
                # VideoProc.get_video_capture_at_time(current_time+0.5, 1280, 720)
            ]

            # カンペを生成
            cue_card, cue_card_print = self.director.create_cue_card(extra_rounds, self.speak_counter, streamer_toggle)

            # ストリーマーのセリフを生成
            generate_data = self.streamers[streamer_toggle].speak(self.speak_counter, capture_base64_list, time_passed, cue_card, partner_message)
            # テキスト生成でエラーが出ていた場合、その時点までの動画を作成するためループ終了
            if generate_data["text"] is None:
                break

            # generate_dataにセリフの入るタイミング、使われたカンペを追加
            generate_data["start_time_sec"] = current_time
            generate_data["cue_card"] = cue_card
            generate_data["cue_card_print"] = cue_card_print

            # 音声ファイルの再生時間＋ランダムな間をcurrent_timeに加算
            time_passed =  generate_data["voice_duration"] + random.uniform(0.5, 1.5)
            current_time += time_passed
            
            # 次のストリーマーへ渡すためにパートナーメッセージとして保存
            partner_message = generate_data["text"]

            # セリフデータをデータベースに挿入
            self.database.insert_serif(self.title, generate_data)
            
            # ストリーマーを切り替え
            streamer_toggle = 1 - streamer_toggle
            self.speak_counter += 1

        log.update_dialogue_progress(total_duration_sec, current_time)

    # ラジオモード（未実装）
    def _create_duo_radio(self):

        # 初期化
        current_time = START_TIME
        time_passed = 0
        generate_data_list = []
        generate_data = {}
        streamer_toggle = 0
        partner_message = ""
        total_duration_sec = RADIO_DURATION_SEC

        # トークテーマを生成（未実装）

        # 裏トークテーマを生成（未実装）

        # 背景画像を生成（未実装）

        while current_time < total_duration_sec:
            
            # 進捗状況を表示
            log.update_dialogue_progress(total_duration_sec, current_time)

            # カンペを生成
            cue_card = self._create_cue_card(current_time)

            # ストリーマーのセリフを生成
            generate_data = self.streamers[streamer_toggle].speak(time_passed=time_passed, cue_card=cue_card, partner_message=partner_message)
            # テキスト生成でエラーが出ていた場合、終了してその時点までの動画を作成
            if generate_data["text"] is None:
                break

            # generate_dataにセリフの入るタイミングを追加して、generate_data_listに追加
            generate_data["start_time_sec"] = current_time
            generate_data_list.append(generate_data)

            # 音声ファイルの再生時間＋ランダムな間をcurrent_timeに加算
            time_passed =  generate_data["voice_duration"] + random.uniform(0.5, 1.5)
            current_time += time_passed
            
            # 次のストリーマーへ渡すためにパートナーメッセージとして保存
            partner_message = generate_data["text"]
            
            # ストリーマーを切り替え
            streamer_toggle = self._chenge_streamer(streamer_toggle)

        log.update_dialogue_progress(total_duration_sec, total_duration_sec)

        return generate_data_list
    
    def _chenge_streamer(self, streamer_toggle):
        # 確率に基づいて数値を変更するかどうかを決定
        if self.consecutive_count == 1:
            # 25%の確率で同じ数字
            change = random.random() < 0.75
        elif self.consecutive_count == 2:
            # 12.5%の確率で同じ数字
            change = random.random() < 0.875
        else:
            # 5%の確率で同じ数字
            change = random.random() < 0.95

        if change:
            streamer_toggle = 1 - streamer_toggle  # 数値の切り替え
            self.consecutive_count = 1
        else:
            self.consecutive_count += 1

        return streamer_toggle
