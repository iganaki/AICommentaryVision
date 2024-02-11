import math
import time
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image
from httpx import stream
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip, concatenate_videoclips
from config import CUE_CARDS_PRINT_FLAG, CUE_SETTINGS, DATA_FOLDER, RADIO_DURATION_SEC, SUBTITLE_SETTINGS, THEME_SETTINGS
from database import Database
from static_data import Role

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

    def get_video_capture_at_time(self, time_sec, resize_width=None, resize_height=None):
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

    def _wrap_text(self, text, max_chars_per_line):
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

    def add_audio_and_subtitles_to_video(self, save_falder, title, db:Database):
        output_path = f'{save_falder}/movie_{int(time.time())}.mp4'
        generate_data_list = db.fetch_serifs_by_video_title(title)
        # 元の動画を読み込む
        with VideoFileClip(self.video_path) as video:
            original_audio = video.audio

            # 新しい音声クリップを追加するための処理
            audio_clips = [original_audio]
            for generate_data in generate_data_list:
                audio_clip = AudioFileClip(generate_data["voice"]).set_start(generate_data["start_time_sec"])
                audio_clips.append(audio_clip)

            # すべての音声クリップを結合
            final_audio = CompositeAudioClip(audio_clips)

            # ビデオにオーディオを設定
            video = video.set_audio(final_audio)

            subtitle_settings = SUBTITLE_SETTINGS.copy()
            video_height = video.size[1]

            # 字幕と立ち絵を動画に合成
            clips = [video]
            for generate_data in generate_data_list:
                # 立ち絵とカンペの文章を動画に合成
                if generate_data["cue_card_print"]:
                    # 立ち絵の追加
                    image_path = DATA_FOLDER + f'/images/AD/AD1.png'
                    cue_image_position = (50, 50)
                    cue_image_clip = ImageClip(image_path).set_position(('left', 'top')).set_start(generate_data["start_time_sec"]-2.0).set_duration(generate_data["voice_duration"])
                    clips.append(cue_image_clip)

                    # カンペの文章をホワイトボードに載せる
                    wrapped_cue_text = self._wrap_text(generate_data['cue_card_print'], 5) # カンペテキストを改行
                    text_clip = TextClip(
                        wrapped_cue_text, 
                        **CUE_SETTINGS
                    ).set_position((cue_image_position[0], cue_image_position[1] + 20)).set_start(generate_data["start_time_sec"]-2.0).set_duration(generate_data["voice_duration"])
                    clips.append(text_clip)

                # 立ち絵を付加
                if "voicevox_chara" in generate_data and "emotion" in generate_data:
                    image_path = self._get_character_image_path(generate_data["voicevox_chara"], generate_data["emotion"])
                    image_clip = ImageClip(image_path).set_start(generate_data["start_time_sec"]).set_duration(generate_data["voice_duration"])
                    image_clip = self._make_bounce_animation(image_clip, video_height)
                    clips.append(image_clip)
                
                # 字幕を付加
                wrapped_subtitle = self._wrap_text(generate_data["text"], 26) # 字幕テキストを改行
                subtitle_settings["stroke_color"] = generate_data["color"] #字幕の色を設定
                subtitle_clip = TextClip(
                    wrapped_subtitle, 
                    **subtitle_settings
                ).set_position(('center', 'bottom')).set_start(generate_data["start_time_sec"]).set_duration(generate_data["voice_duration"])
                clips.append(subtitle_clip)

            final_clip = CompositeVideoClip(clips)

            # 動画を出力
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        return output_path
    
    def create_radio(self, save_folder, title, db: Database):
        output_path = f'{save_folder}/movie_{int(time.time())}.mp4'
        radio_part_list = db.fetch_radio_parts_by_video_title(title)
        generate_data_list = db.fetch_serifs_by_video_title(title)
        streamer_profile_list = db.fetch_streamer_profiles_by_video_title(title)

        clips = []
        audio_clips = []
        end_time = 0
        subtitle_settings = SUBTITLE_SETTINGS.copy()

        for radio_part in radio_part_list:
            start_time = end_time
            generate_data_list = db.fetch_serifs_by_video_title(radio_part["part_name"])

            # 背景画像の読み込み
            image_path = radio_part["background_image_url"]
            # 各radio_partの総時間を計算
            last_serif = generate_data_list[-1]  # 最後のセリフを取得
            total_duration = last_serif["start_time_sec"] + last_serif["voice_duration"]
            # 背景画像の持続時間を設定
            if image_path:
                image_clip = ImageClip(image_path).set_duration(total_duration).set_start(start_time)
                clips.append(image_clip)

            # 画像の読み込み
            image = cv2.imread(image_path)
            # 画像の高さを取得
            image_height = image.shape[0]

            for index, generate_data in enumerate(generate_data_list):
                # 音声クリップの追加
                audio_clip = AudioFileClip(generate_data["voice"]).set_start(start_time + generate_data["start_time_sec"])
                audio_clips.append(audio_clip)

                # 立ち絵とカンペの文章を動画に合成
                if CUE_CARDS_PRINT_FLAG and generate_data["cue_card_print"]:
                    # 立ち絵の追加
                    image_path = DATA_FOLDER + f'/images/AD/AD1.png'
                    cue_image_position = (50, 50)
                    cue_image_clip = ImageClip(image_path).set_position(('left', 'top')).set_start(start_time + generate_data["start_time_sec"]-2.0).set_duration(generate_data["voice_duration"])
                    clips.append(cue_image_clip)

                    # カンペの文章をホワイトボードに載せる
                    wrapped_cue_text = self._wrap_text(generate_data['cue_card_print'], 5) # カンペテキストを改行
                    text_clip = TextClip(
                        wrapped_cue_text, 
                        **CUE_SETTINGS
                    ).set_position((cue_image_position[0], cue_image_position[1] + 20)).set_start(start_time + generate_data["start_time_sec"]-2.0).set_duration(generate_data["voice_duration"])
                    clips.append(text_clip)

                # streamer_profile_listから["name"]がgenerate_data["name"]と一致するものを取得
                streamer_profile = next((streamer_profile for streamer_profile in streamer_profile_list if streamer_profile["name"] == generate_data["name"]), None)

                # 立ち絵を付加
                if "voicevox_chara" in generate_data and "emotion" in generate_data:
                    location = ('left') if streamer_profile["role"] == Role.RADIO_PERSONALITY1.value else ('right')
                    image_path = self._get_character_image_path(generate_data["voicevox_chara"], generate_data["emotion"], location==('left'))
                    if index + 2 < len(generate_data_list):
                        image_clip = ImageClip(image_path).set_start(start_time + generate_data["start_time_sec"]).set_duration(generate_data_list[index + 2]["start_time_sec"] - generate_data["start_time_sec"])
                    elif index + 1 < len(generate_data_list):
                        image_clip = ImageClip(image_path).set_start(start_time + generate_data["start_time_sec"]).set_duration(generate_data_list[index + 1]["start_time_sec"] - generate_data["start_time_sec"] + generate_data_list[index + 1]["voice_duration"])
                    else:
                        image_clip = ImageClip(image_path).set_start(start_time + generate_data["start_time_sec"]).set_duration(generate_data["voice_duration"])
                    # 画像にアニメーションを付加
                    image_clip = self._make_bounce_animation(image_clip, image_height, location=location)
                    clips.append(image_clip)

                # 字幕を付加
                wrapped_subtitle = self._wrap_text(generate_data["text"], 26) # 字幕テキストを改行
                subtitle_settings["stroke_color"] = generate_data["color"] #字幕の色を設定
                subtitle_clip = TextClip(
                    wrapped_subtitle, 
                    **subtitle_settings
                ).set_position(('center', 'bottom')).set_start(start_time + generate_data["start_time_sec"]).set_duration(generate_data["voice_duration"])
                clips.append(subtitle_clip)

                # パートの終了時間を保存
                end_time = generate_data["start_time_sec"] + generate_data["voice_duration"]    
            
            # テーマのテキストクリップを作成して追加
            talk_theme_text = "テーマ：" + radio_part["talk_theme_jp"]
            text_clip = TextClip(talk_theme_text, **THEME_SETTINGS).set_position(('left', 'top')).set_start(start_time).set_duration(total_duration)
            clips.append(text_clip)

            end_time += start_time+1.0

        final_audio = CompositeAudioClip(audio_clips)
        final_clip = CompositeVideoClip(clips).set_audio(final_audio)

        # 動画を出力
        final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

        return output_path
    
    def _get_character_image_path(self, character, emotion, inversion=False):
        # 不正な感情の場合はnormalにする
        if emotion not in ["normal", "positive", "negative"]:
            emotion = "normal"
        # キャラクターと感情に基づいて立ち絵のパスを決定
        if not inversion:
            image_path = DATA_FOLDER + f'/images/CharacterImages/{character}/{emotion}.png'
        else:
            image_path = DATA_FOLDER + f'/images/CharacterImages/{character}/{emotion}_inversion.png'
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
            # 注意: ここでの 'video_height' は適切なビデオの高さに置き換える必要があります
            bottom_y = video_height - image_clip.size[1] # 画像の高さをビデオの高さから引く

            if 0 <= t <= bounce_duration:
                # サイン関数を使って跳ねる動きをシミュレート
                return (location, bottom_y - bounce_height * math.sin(t / bounce_duration * math.pi)+30)
            else:
                return (location, bottom_y+30)

        return image_clip.set_position(position_func)
