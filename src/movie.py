import math
import time
import cv2
import base64
from io import BytesIO
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip
from config import DATA_FOLDER, OUTPUT_FOLDER, SUBTITLE_SETTINGS

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open video {video_path}")
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()

    def get_duration(self):
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = (frame_count / self.fps)

        return duration

    def get_video_capture_at_time(self, time_sec, resize_width, resize_height):
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

    def add_audio_and_subtitles_to_video(self, save_falder, generate_data_list):
        output_path = f'{save_falder}/movie_{int(time.time())}.mp4'
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
                # 立ち絵を付加
                if "voicevox_chara" in generate_data and "emotion" in generate_data:
                    image_path = self._get_character_image_path(generate_data["voicevox_chara"], generate_data["emotion"])
                    image_clip = ImageClip(image_path).set_position("right").set_start(generate_data["start_time_sec"]).set_duration(generate_data["voice_duration"])
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
    
    def _get_character_image_path(self, character, emotion):
        # キャラクターと感情に基づいて立ち絵のパスを決定
        image_path = DATA_FOLDER + f'/images/CharacterImages/{character}/{emotion}.png'
        return image_path
    
    def _make_bounce_animation(self, image_clip:ImageClip, video_height, bounce_duration=0.3, bounce_height=30):
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
                return ('right', bottom_y - bounce_height * math.sin(t / bounce_duration * math.pi))
            else:
                return ('right', bottom_y)

        return image_clip.set_position(position_func)
