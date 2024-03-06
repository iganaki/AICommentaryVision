from copy import deepcopy
import os
import random
from config import OUTPUT_FOLDER, START_TIME
from director import Director
from listener import Listener
from model import ProgramType, SerifPart, StaticSection, Serif, StreamerProfile, Video, VideoSection, session_scope
from streamer import Streamer
from movie import VideoProcessor
import log
import model

class Studio:
    def __init__(self):
        pass

    def initialize_project(self, title, debug_mode):
        with session_scope() as session:
            # 動画情報をデータベースから取得
            self.video_data = deepcopy(session.query(Video).filter(Video.video_title == title).first())

            # ストリーマーのプロフィールをデータベースから取得
            streamer_profiles = session.query(StreamerProfile).filter(StreamerProfile.video_title == title).all()
            self.streamers = []
            for streamer_profile in streamer_profiles:
                self.streamers.append(Streamer(streamer_profile, debug_mode))

            # 番組情報をデータベースから取得
            self.program_type = deepcopy(session.query(ProgramType).filter(ProgramType.program_name == self.video_data.program_name).first())
            self.sections = deepcopy(session.query(StaticSection).filter(StaticSection.program_name == self.video_data.program_name).order_by(StaticSection.order).all())

        self.director = Director(title, debug_mode)
        self.listener = Listener(debug_mode)
        self.title = title
        self.output_path = OUTPUT_FOLDER + "/" + self.title
        self.temp_path = self.output_path + "/temp"
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.temp_path, exist_ok=True)

        self.log = log.Log(self.output_path, title)

    def create_video(self):
        # 動画処理クラスの初期化
        video_processor = VideoProcessor()

        # ディレクターの準備
        self.director.prepare_for_streaming(self.video_data, self.program_type, self.streamers)

        #  ストリーマーの準備
        for streamer in self.streamers:
            streamer.prepare_for_streaming(self.output_path, self.log)

        # 動画データの作成
        if self.program_type.streamer_num == 1:
            self._create_video_data_for_soro_streamer()
        else:
            self._create_video_data_for_duo_streamer()
            
        # 動画の結合
        final_video_path = video_processor.create_video(self.output_path, self.title)

        # セリフデータをログファイルに書き込む
        with model.session_scope() as session:
            video_sections = session.query(VideoSection).filter(VideoSection.video_title == self.title).all()
            for video_section in video_sections:
                self.log.write_to_log_file(f"{video_section.section_name}", Serif.get_serif_text_by_section(session, self.title, video_section.section_name, 0, True))

        return final_video_path

    # 動画データの作成
    def _create_video_data_for_soro_streamer(self):
        pass # 後で実装

    def _create_video_data_for_duo_streamer(self):
        current_time = START_TIME
        partner_message = ""
        streamer_toggle = 0
        [streamer.reset_previous_messages() for streamer in self.streamers]
        for section in self.sections:
            # 初期化
            end_flag = False
            start_time_sec = current_time
            loop_counter = 0

            self.director.prepare_for_section(self.program_type, section)
            if section.is_reset_conversation_history:
                [streamer.reset_previous_messages() for streamer in self.streamers]

            # セクションの終了条件に達するまでループ
            while end_flag == False:
                # 進捗状況を表示
                if section.end_condition_type == 0:
                    log.update_dialogue_progress_sec(section.end_condition_value, current_time-start_time_sec, newline=False)
                else:
                    log.update_dialogue_progress_num(section.end_condition_value, loop_counter, newline=False)

                # おたよりを生成
                # if current_time > 120:
                #     letter = self.listener.create_letter(radio_part.part_name)
                
                # システムプロンプト、カンペ、終了フラグ判定を生成
                system_prompt, cue_card, end_flag = self.director.create_direction(section, loop_counter, current_time-start_time_sec, streamer_toggle)

                # ストリーマーのセリフを生成
                generate_serif_data, generate_split_serif_data = self.streamers[streamer_toggle].speak(loop_counter, system_prompt=system_prompt, cue_card=cue_card, partner_message=partner_message, start_time_sec=current_time)
                # テキスト生成でエラーが出ていた場合、その時点までの動画を作成するためループ終了
                if generate_serif_data["text"] is None:
                    break

                # generate_serif_dataに使われたカンペを追加
                generate_serif_data["start_time_sec"] = current_time
                generate_serif_data["cue_card"] = cue_card

                # 音声ファイルの再生時間＋ランダムな間をcurrent_timeに加算
                current_time += generate_serif_data["voice_duration"] + random.uniform(0.5, 1.5)

                # セリフデータをデータベースに挿入
                with model.session_scope() as session:
                    serif = Serif.insert_serif(session, self.title, section.section_name, generate_serif_data)
                    SerifPart.insert_serif_parts(session, generate_split_serif_data, serif)
                
                # ストリーマーを切り替え
                streamer_toggle = 1 - streamer_toggle
                partner_message = generate_serif_data["text"]
                loop_counter += 1

            # 動画セクションをデータベースに挿入
            with model.session_scope() as session:
                # 背景画像、BGMを生成
                background_image_path = self.director.create_background_image(section, self.output_path, f"{self.title}_section{section.order}.png", self.video_data)
                background_music_path = self.director.select_background_music(section)
                video_section = VideoSection(video_title=self.title, section_name=section.section_name,
                            order=section.order, start_time_sec=start_time_sec, end_time_sec=current_time, 
                            background_image_path=background_image_path, background_music_path=background_music_path)
                session.add(video_section)

            log.update_dialogue_progress_num(len(self.sections), section.order, newline=True, full_time=current_time)
        session.close()