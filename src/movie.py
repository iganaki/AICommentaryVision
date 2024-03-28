from copy import deepcopy
import math
import os
import time
import cv2
import base64
from io import BytesIO
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip, concatenate_audioclips
from moviepy.audio.fx.all import audio_fadein, audio_fadeout
from config import BACKUP_IMAGE_PATH, CUE_CARDS_PRINT_FLAG, CUE_SETTINGS, DATA_FOLDER, FADE_DURATION_SEC, SUBTITLE_SETTINGS, THEME_SETTINGS, Session
from model import Serif, StreamerProfile, VideoSection
from static_data import Role
import model

class VideoProcessor:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()

    def add_video(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open video {video_path}")
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def get_duration(self):
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = (frame_count / self.fps)

        return duration

    def get_video_frame_as_base64_image(self, time_sec, resize_width=None, resize_height=None):
        # 指定した秒数に対応するフレーム番号を計算
        frame_number = int(time_sec * self.fps)

        # 指定したフレーム番号にジャンプ
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # フレームのキャプチャ
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame at time:", time_sec)
            return None

        # キャプチャしたフレームをPIL画像に変換
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 画像をリサイズ
        if resize_width is not None and resize_height is not None:
            image = image.resize((resize_width, resize_height), Image.Resampling.LANCZOS)

        # PIL画像をBASE64エンコードする
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return img_str

    def get_video_frame_as_pil_image(self, time_sec, save_folder_path, resize_width=None, resize_height=None):
        # 指定した秒数に対応するフレーム番号を計算
        frame_number = int(time_sec * self.fps)

        # 指定したフレーム番号にジャンプ
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # フレームのキャプチャ
        ret, frame = self.cap.read()

        if not ret:
            print("Failed to capture frame at time:", time_sec)
            return None, None

        # キャプチャしたフレームをPIL画像に変換
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 画像をリサイズ
        if resize_width is not None and resize_height is not None:
            image = image.resize((resize_width, resize_height), Image.Resampling.LANCZOS)

        # 保存するファイル名を生成
        file_name = f"{time_sec:04d}.jpg"

        # 保存先のフルパスを生成
        save_path = os.path.join(save_folder_path, file_name)

        # 画像を保存
        image.save(save_path, "JPEG")

        return image, save_path

    def get_frames_from_video(file_path, max_images=20):
        video = cv2.VideoCapture(file_path)
        base64_frames = []
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            _, encoded_frame = cv2.imencode(".jpg", frame)
            base64_frame = base64.b64encode(encoded_frame).decode("utf-8")
            base64_frames.append(base64_frame)
        video.release()

        # 選択する画像の数を制限する
        selected_frames = base64_frames[0::len(base64_frames)//max_images][:max_images]
        return selected_frames

    def _wrap_text(self, text, max_chars_per_line):
        # 既存の改行を取り除く
        text = text.replace('\n', '')
        
        lines = []
        current_line = ""

        for char in text:
            if len(current_line) < max_chars_per_line:
                current_line += char
            else:
                lines.append(current_line)
                current_line = char

        if current_line:
            lines.append(current_line)

        return '\n'.join(lines)

    def add_audio_and_subtitles_to_video(self, save_falder, title):
        output_path = f'{save_falder}/movie_{int(time.time())}.mp4'
        session = Session()
        serifs = session.query(Serif).filter(Serif.video_title == title).all()
        # 元の動画を読み込む
        with VideoFileClip(self.video_path) as video:
            original_audio = video.audio

            # 新しい音声クリップを追加するための処理
            audio_clips = [original_audio]
            for serif in serifs:
                audio_clip = AudioFileClip(serif["voice"]).set_start(serif["start_time_sec"])
                audio_clips.append(audio_clip)

            # すべての音声クリップを結合
            final_audio = CompositeAudioClip(audio_clips)

            # ビデオにオーディオを設定
            video = video.set_audio(final_audio)

            subtitle_settings = SUBTITLE_SETTINGS.copy()
            video_height = video.size[1]

            # 字幕と立ち絵を動画に合成
            clips = [video]
            for serif in serifs:
                # 立ち絵とカンペの文章を動画に合成
                if serif["cue_card_print"]:
                    # 立ち絵の追加
                    image_path = DATA_FOLDER + f'/images/AD/AD1.png'
                    cue_image_position = (50, 50)
                    cue_image_clip = ImageClip(image_path).set_position(('left', 'top')).set_start(serif["start_time_sec"]-2.0).set_duration(serif["voice_duration"])
                    clips.append(cue_image_clip)

                    # カンペの文章をホワイトボードに載せる
                    wrapped_cue_text = self._wrap_text(serif['cue_card_print'], 5) # カンペテキストを改行
                    text_clip = TextClip(
                        wrapped_cue_text, 
                        **CUE_SETTINGS
                    ).set_position((cue_image_position[0], cue_image_position[1] + 20)).set_start(serif["start_time_sec"]-2.0).set_duration(serif["voice_duration"])
                    clips.append(text_clip)

                # 立ち絵を付加
                if "name" in serif and "emotion" in serif:
                    image_path = self._get_character_image_path(serif["name"], serif["emotion"])
                    image_clip = ImageClip(image_path).set_start(serif["start_time_sec"]).set_duration(serif["voice_duration"])
                    image_clip = self._make_bounce_animation(image_clip, video_height)
                    clips.append(image_clip)
                
                # 字幕を付加
                wrapped_subtitle = self._wrap_text(serif["text"], 26) # 字幕テキストを改行
                subtitle_settings["stroke_color"] = serif["color"] #字幕の色を設定
                subtitle_clip = TextClip(
                    wrapped_subtitle, 
                    **subtitle_settings
                ).set_position(('center', 'bottom')).set_start(serif["start_time_sec"]).set_duration(serif["voice_duration"])
                clips.append(subtitle_clip)

            final_clip = CompositeVideoClip(clips)

            # 動画を出力
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        return output_path
       
    def create_video(self, save_folder, title):
        output_path = f'{save_folder}/movie.mp4'
        if os.path.exists(output_path):
            output_path = f'{save_folder}/movie_{int(time.time())}.mp4'
        with model.session_scope() as session:
            video_sections = deepcopy(session.query(VideoSection).filter(VideoSection.video_title == title).order_by(VideoSection.order).all())
            streamer_profiles = deepcopy(session.query(StreamerProfile).filter(StreamerProfile.video_title == title).all())

        clips = []
        audio_clips = []
        subtitle_settings = SUBTITLE_SETTINGS.copy()
        bgm_data = []
        temp_image_path = None
        temp_location = None
        for section in video_sections:
            # bgm_dataが空、または現在のセクションのBGMパスが最後のBGMパスと異なる場合、新しいBGM情報を追加
            if not bgm_data or section.background_music_path != bgm_data[-1]["path"]:
                bgm_data.append({
                    "start_time": section.start_time_sec,
                    "end_time": section.end_time_sec,
                    "path": section.background_music_path
                })
            else:
                # 同じBGMパスの場合、終了時間のみ更新
                bgm_data[-1]["end_time"] = section.end_time_sec

        for bgm in bgm_data:
            bgm_full_path = f"{DATA_FOLDER}/BGM/{bgm['path']}/{bgm['path']}.mp3"
            bgm_full_path = os.path.normpath(bgm_full_path)
            # BGMの読み込み
            full_audio_clip = AudioFileClip(bgm_full_path)
            # 指定された期間でBGMをループさせる
            looped_audio_clip = self._loop_audio_clip(full_audio_clip, bgm["end_time"] - bgm["start_time"])
            # フェードインとフェードアウトを適用
            faded_audio_clip = audio_fadein(looped_audio_clip, FADE_DURATION_SEC)
            faded_audio_clip = audio_fadeout(faded_audio_clip, FADE_DURATION_SEC)
            # 開始時間を設定
            faded_audio_clip = faded_audio_clip.set_start(bgm["start_time"])
            audio_clips.append(faded_audio_clip)

        with model.session_scope() as session:
            for sections_index, section in enumerate(video_sections):
                serifs = session.query(Serif).filter(Serif.video_title == title).filter(Serif.section_name == section.section_name).order_by(Serif.start_time_sec).all()

                # 背景画像の読み込み
                image_path = section.background_image_path
                # 背景画像の持続時間を設定
                if image_path:
                    image_clip = ImageClip(image_path).set_duration(section.end_time_sec - section.start_time_sec).set_start(section.start_time_sec)
                    clips.append(image_clip)

                # 画像の読み込み
                image = cv2.imread(image_path)
                if image is None:
                    image = cv2.imread(BACKUP_IMAGE_PATH)
                # 画像の高さを取得
                image_height = image.shape[0]

                # 前のセクションから続く立ち絵が存在する場合、追加
                if temp_image_path:
                    if len(serifs) > 1:
                        image_clip = ImageClip(temp_image_path).set_duration(serifs[1].start_time_sec - serifs[0].start_time_sec).set_start(serifs[0].start_time_sec)
                    else:
                        image_clip = ImageClip(temp_image_path).set_duration(serifs[0].voice_duration).set_start(serifs[0].start_time_sec)
                    image_clip = self._make_bounce_animation(image_clip, image_height, bounce_duration=0, location=temp_location)
                    clips.append(image_clip)
                    temp_image_path = None

                for index, serif in enumerate(serifs):
                    for part in serif.serif_parts:
                        # 音声クリップの追加
                        audio_clip = AudioFileClip(part.part_voice).set_start(part.start_time_sec)
                        audio_clips.append(audio_clip)

                    # 立ち絵とカンペの文章を動画に合成
                    if CUE_CARDS_PRINT_FLAG and serif.cue_card:
                        # 立ち絵の追加
                        image_path = DATA_FOLDER + f'/images/AD/AD1.png'
                        cue_image_position = (50, 50)
                        cue_image_clip = ImageClip(image_path).set_position(('left', 'top')).set_start(serif.start_time_sec-2.0).set_duration(serif.voice_duration)
                        clips.append(cue_image_clip)

                        # カンペの文章をホワイトボードに載せる
                        wrapped_cue_text = self._wrap_text(serif['cue_card_print'], 5)
                        text_clip = TextClip(
                            wrapped_cue_text, 
                            **CUE_SETTINGS
                        ).set_position((cue_image_position[0], cue_image_position[1] + 20)).set_start(serif.start_time_sec-2.0).set_duration(serif.voice_duration)
                        clips.append(text_clip)

                    # streamer_profilesから.nameserif.nameと一致するものを取得
                    streamer_profile = next((streamer_profile for streamer_profile in streamer_profiles if streamer_profile.name == serif.name), None)

                    for i, part in enumerate(serif.serif_parts):
                        # 立ち絵を付加
                        location = 'left' if streamer_profile.role == Role.DUO_VIDEO_HOST.value or streamer_profile.role == Role.SOLO_VIDEO_HOST.value else 'right'
                        # image_pathの取得
                        image_path = self._get_character_image_path(streamer_profile.character_images_directory , part.emotion, location == 'left')
                        # image_clipの持続時間の設定
                        # このセリフパートが最後のセリフパートでない場合
                        if part.part_order != len(serif.serif_parts) - 1:
                            # 次のセリフパートの開始時間からこのセリフパートの開始時間を引いたものが持続時間
                            duration = serif.serif_parts[i+1].start_time_sec - part.start_time_sec
                        else:
                            # このセクションが最後のセクションでない場合
                            if sections_index != len(video_sections) - 1:
                                # 次の相手のセリフ（1個先のセリフ）が存在しない場合
                                if index + 1 >= len(serifs):
                                    next_section_serifs = session.query(Serif).filter(Serif.video_title == title).filter(Serif.section_name == video_sections[sections_index + 1].section_name).order_by(Serif.start_time_sec).all()
                                    if len(next_section_serifs) > 1:
                                        duration = next_section_serifs[1].start_time_sec - part.start_time_sec
                                    else:
                                        duration = next_section_serifs[0].start_time_sec - part.start_time_sec + next_section_serifs[0].voice_duration
                                    temp_image_path, temp_location = image_path, location
                                # 次の自分のセリフ（2個先のセリフ）が存在しない場合
                                elif index + 2 >= len(serifs):
                                    next_section_serifs = session.query(Serif).filter(Serif.video_title == title).filter(Serif.section_name == video_sections[sections_index + 1].section_name).order_by(Serif.start_time_sec).all()
                                    duration = next_section_serifs[0].start_time_sec - part.start_time_sec
                                else:
                                    duration = serifs[index + 2].start_time_sec - part.start_time_sec
                            # このセクションが最後のセクションの場合
                            else:
                                # 次の相手のセリフ（1個先のセリフ）が存在しない場合
                                if index + 1 >= len(serifs):
                                    duration = part.part_voice_duration
                                # 次の自分のセリフ（2個先のセリフ）が存在しない場合
                                elif index + 2 >= len(serifs):
                                    duration = serifs[index + 1].start_time_sec - part.start_time_sec + serifs[index + 1].voice_duration
                                else:
                                    duration = serifs[index + 2].start_time_sec - part.start_time_sec
                        # ImageClipのインスタンス作成
                        image_clip = ImageClip(image_path).set_start(part.start_time_sec).set_duration(duration)
                        # 画像にアニメーションを付加
                        image_clip = self._make_bounce_animation(image_clip, image_height, location=location)
                        clips.append(image_clip)

                        # 字幕を付加
                        wrapped_subtitle = self._wrap_text(part.part_text, 26)
                        subtitle_settings["stroke_color"] = serif.color
                        subtitle_clip = TextClip(
                            wrapped_subtitle, 
                            **subtitle_settings
                        ).set_position(('center', 'bottom')).set_start(part.start_time_sec).set_duration(part.part_voice_duration)
                        clips.append(subtitle_clip)

        final_audio = CompositeAudioClip(audio_clips)
        final_clip = CompositeVideoClip(clips).set_audio(final_audio)

        # 動画を出力
        final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

        return output_path
    
    def _loop_audio_clip(self, audio_clip, duration):
        """指定された総持続時間に達するまでオーディオクリップをループさせる"""
        looped_clips = []
        current_duration = 0
        while current_duration < duration:
            looped_clips.append(audio_clip)
            current_duration += audio_clip.duration
        # ループしたクリップを結合し、必要な総持続時間にトリミング
        final_clip = concatenate_audioclips(looped_clips).subclip(0, duration)
        return final_clip

    def _get_character_image_path(self, character_images_directory, emotion, inversion=False):
        # 不正な感情の場合はnormalにする
        if emotion not in ["normal", "positive", "negative"]:
            emotion = "normal"
        # キャラクターと感情に基づいて立ち絵のパスを決定
        if not inversion:
            image_path = DATA_FOLDER + f'/{character_images_directory}/{emotion}.png'
        else:
            image_path = DATA_FOLDER + f'/{character_images_directory}/{emotion}_inversion.png'
        return image_path
    
    def _make_bounce_animation(self, image_clip:ImageClip, video_height, bounce_duration=0.3, bounce_height=30, location='right'):
        """
        立ち絵に跳ねるアニメーションを追加する関数

        :param image_clip: ImageClip オブジェクト
        :param bounce_duration: 跳ねる動きの持続時間（秒）
        :param bounce_height: 跳ねる高さ（ピクセル）
        :return: アニメーション付きの ImageClip オブジェクト
        """
        def position_func(t):
            # 画像の下部のy座標を計算（例: ビデオの高さを基にした場合）
            bottom_y = video_height - image_clip.size[1] # 画像の高さをビデオの高さから引く

            if 0 <= t <= bounce_duration:
                # サイン関数を使って跳ねる動きをシミュレート
                return (location, bottom_y - bounce_height * math.sin(t / bounce_duration * math.pi)+30)
            else:
                return (location, bottom_y+30)

        return image_clip.set_position(position_func)
