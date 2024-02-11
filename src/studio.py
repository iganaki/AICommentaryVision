import os
import random
from config import MAX_EXTRA_ROUNDS, OUTPUT_FOLDER, RADIO_DURATION_SEC, RADIO_SUMMARY_FLAG, RADIO_THEME_TALK_NUM, START_TIME, Session
from director import create_director_instance
from model import RadioPart, Serif, StreamerProfile, Video
from static_data import Mode
from streamer import Streamer
from movie import VideoProcessor
import log

class Studio:
    def __init__(self, title):
        session = Session()

        # 動画情報をデータベースから取得
        video_data = session.query(Video).filter(Video.video_title == title).first()
        self.video_data = video_data

        # ストリーマーのプロフィールをデータベースから取得
        streamer_profiles = session.query(StreamerProfile).filter(StreamerProfile.video_title == title).all()
        self.streamers = []
        for streamer_profile in streamer_profiles:
            self.streamers.append(Streamer(streamer_profile))

        self.director = create_director_instance(self.video_data.mode)

        self.title = title
        self.output_path = OUTPUT_FOLDER + "/" + self.title
        self.temp_path = self.output_path + "/temp"
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.temp_path, exist_ok=True)

        self.log = log.Log(self.output_path, title)

        session.close()

    def create_video(self):
        # 動画処理クラスの初期化
        video_processor = VideoProcessor()

        # ディレクターの準備
        self.director.prepare_for_streaming(self.streamers)

        #  ストリーマーの準備
        for streamer in self.streamers:
            streamer.prepare_for_streaming(self.output_path, self.log, self.video_data.video_summary)

        if self.video_data.mode == Mode.SOLO_GAMEPLAY.value:
            # アップデートできていないので動かない。
            raise ValueError("無効なモードです")
            # self._create_solo_commentary(video_processor)
        elif self.video_data.mode == Mode.DUO_GAMEPLAY.value:
            # 動画の読み込み
            video_processor.add_video(self.video_data.video_path)
            self.log.write_to_log_file("video_path", self.video_data.video_path)
            # 実況文を生成
            self._create_duo_commentary(video_processor)
            # 動画に実況音声、字幕を付加して保存
            final_video_path = video_processor.add_audio_and_subtitles_to_video(self.output_path, self.title)
            self.log.write_to_log_file("final_video_path", final_video_path)
            session = Session()
            self.log.write_to_log_file("まとめ", Serif.get_serif_text_by_video_title(session, self.title, 0, True))
            session.close()
        elif self.video_data.mode == Mode.DUO_RADIO.value:
            # 実況文を生成
            self._create_duo_radio()
            # 動画に実況音声、字幕を付加して保存
            final_video_path = video_processor.create_radio(self.output_path, self.title)
            self.log.write_to_log_file("final_video_path", final_video_path)
            session = Session()
            radio_parts = session.query(RadioPart).filter(RadioPart.video_title == self.title).all()
            for radio_part in radio_parts:
                self.log.write_to_log_file(f"トークテーマ:{radio_part.talk_theme_jp}", Serif.get_serif_text_by_video_title(session, radio_part.part_name, 0, True))
            session.close()
        else:
            raise ValueError("無効なモードです")

        return final_video_path

    # アップデートできていないので動かない。
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
        session = Session()
        # 初期化
        self.speak_counter = 0
        total_duration_sec = video_processor.get_duration()
        current_time = START_TIME
        streamer_toggle = 0
        partner_message = ""
        extra_rounds = MAX_EXTRA_ROUNDS
        self.director.prepare_for_gameStream(self.title, self.video_data.video_summary)

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
            cue_card, cue_card_print = self.director.create_cue_card(extra_rounds, self.speak_counter, streamer_toggle, self.title)

            # ストリーマーのセリフを生成
            generate_data = self.streamers[streamer_toggle].speak(self.speak_counter, capture_base64_list, cue_card, partner_message)
            # テキスト生成でエラーが出ていた場合、その時点までの動画を作成するためループ終了
            if generate_data["text"] is None:
                break

            # generate_dataにセリフの入るタイミング、使われたカンペを追加
            generate_data["start_time_sec"] = current_time
            generate_data["cue_card"] = cue_card
            generate_data["cue_card_print"] = cue_card_print

            # 音声ファイルの再生時間＋ランダムな間をcurrent_timeに加算
            current_time += generate_data["voice_duration"] + random.uniform(0.5, 1.5)
            
            # 次のストリーマーへ渡すためにパートナーメッセージとして保存
            partner_message = generate_data["text"]

            # セリフデータをデータベースに挿入
            Serif.insert_serif(session, self.title, generate_data)
            
            # ストリーマーを切り替え
            streamer_toggle = 1 - streamer_toggle
            self.speak_counter += 1
            session.commit()

        log.update_dialogue_progress(total_duration_sec, current_time)
        session.close()

    # ラジオモード
    def _create_duo_radio(self):
        session = Session()

        for i in range(RADIO_THEME_TALK_NUM):
            # 初期化
            extra_rounds = MAX_EXTRA_ROUNDS
            current_time = START_TIME
            self.speak_counter = 0
            partner_message_list = []
            partner_message = ""
            self.consecutive_count = 1
            streamer_toggle = 0
            [streamer.reset_previous_messages() for streamer in self.streamers]

            if i is (RADIO_THEME_TALK_NUM-1) and RADIO_SUMMARY_FLAG is True:
                log.show_message(f"まとめを生成中...", newline=True)
                # まとめを生成
                summary = self.director.create_summary(self.output_path, self.title)
                if summary['background_image_url'] is None or summary['theme'] is None:
                    break

                # まとめをデータベースに挿入
                radio_part = RadioPart(video_title=self.title, part_name=self.title + "_" + str(i), talk_theme=summary['theme'], talk_theme_jp=summary['theme_jp'], background_image_pass=summary['background_image_url'])
                session.add(radio_part)

                # まとめを各ストリーマーにセット
                [streamer.create_system_prompt_for_radio_summary(radio_part.talk_theme) for streamer in self.streamers]

                # まとめをディレクターにセット
                self.director.prepare_for_radio_part(i, radio_part.part_name, "今日の振り返り")
            else:
                log.show_message(f"トークテーマ{i+1}を生成中...", newline=True)
                # トークテーマを生成
                talk_theme = self.director.create_talk_theme(self.output_path, self.title + "_" + str(i))
                if talk_theme['background_image_url'] is None or talk_theme['theme'] is None:
                    break

                # トークテーマをデータベースに挿入
                radio_part = RadioPart(video_title=self.title, part_name=self.title + "_" + str(i), talk_theme=talk_theme['theme'], talk_theme_jp=talk_theme['theme_jp'], background_image_pass=talk_theme['background_image_url'])
                session.add(radio_part)

                # トークテーマを各ストリーマーにセット
                [streamer.create_system_prompt_for_radio_talk_theme(radio_part.talk_theme) for streamer in self.streamers]

                # トークテーマをディレクターにセット
                self.director.prepare_for_radio_part(i, radio_part.part_name, radio_part.talk_theme)

            # 動画終了に近くなるまでループ
            while extra_rounds > 0:
                
                # 進捗状況を表示
                log.update_dialogue_progress(RADIO_DURATION_SEC, current_time, newline=False)

                if RADIO_DURATION_SEC - current_time <= 30.0 and extra_rounds > 0:
                    extra_rounds -= 1  # 残りのループ回数を減らす
                
                # カンペを生成
                cue_card, cue_card_print = self.director.create_cue_card(extra_rounds, self.speak_counter)

                # ストリーマーのセリフを生成
                generate_data = self.streamers[streamer_toggle].speak(self.speak_counter, cue_card=cue_card, partner_message=partner_message)
                # テキスト生成でエラーが出ていた場合、その時点までの動画を作成するためループ終了
                if generate_data["text"] is None:
                    break

                # generate_dataにセリフの入るタイミング、使われたカンペを追加
                generate_data["start_time_sec"] = current_time
                generate_data["cue_card"] = cue_card
                generate_data["cue_card_print"] = cue_card_print

                # 音声ファイルの再生時間＋ランダムな間をcurrent_timeに加算
                current_time += generate_data["voice_duration"] + random.uniform(0.5, 1.5)

                # セリフデータをデータベースに挿入
                Serif.insert_serif(session, radio_part.part_name, generate_data)
                
                # ストリーマーを切り替え
                # streamer_toggle, streamer_change = self._chenge_streamer(streamer_toggle) # 交互じゃないとうまくいかなかったのでコメントアウト
                streamer_toggle = 1 - streamer_toggle
                partner_message_list.clear()
                partner_message_list.append(generate_data["text"])
                partner_message = partner_message_list
                self.speak_counter += 1

                # 次のストリーマーへ渡すためにパートナーメッセージとして保存
                # if (streamer_change == True):
                #     partner_message_list.clear()
                #     partner_message_list.append(generate_data["text"])
                #     partner_message = partner_message_list
                # else:
                #     partner_message_list.append(generate_data["text"])
                #     partner_message = ""
                session.commit()

            log.update_dialogue_progress(RADIO_DURATION_SEC, current_time, newline=True)
        session.close()
    
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

        return streamer_toggle, change
