import time
import cv2
import base64
from io import BytesIO
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip
from config import OUTPUT_FOLDER, SUBTITLE_SETTINGS

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

    def add_audio_and_subtitles_to_video(self, generate_data):
        output_path = f'{OUTPUT_FOLDER}/movie_{int(time.time())}.mp4'
        # 元の動画を読み込む
        with VideoFileClip(self.video_path) as video:
            original_audio = video.audio

            # 新しい音声クリップを追加するための処理
            audio_clips = [original_audio]
            for _, audio_file, start_time_sec in generate_data:
                audio_clip = AudioFileClip(audio_file).set_start(start_time_sec)
                audio_clips.append(audio_clip)

            # すべての音声クリップを結合
            final_audio = CompositeAudioClip(audio_clips)

            # ビデオにオーディオを設定
            video = video.set_audio(final_audio)

            # 字幕と動画を合成
            clips = [video]
            for subtitle, audio_file, start_time_sec in generate_data:
                audio_duration = AudioFileClip(audio_file).duration
                # ここで字幕テキストを改行する
                wrapped_subtitle = self._wrap_text(subtitle, 26)
                subtitle_clip = TextClip(
                    wrapped_subtitle, 
                    **SUBTITLE_SETTINGS
                ).set_position(('center', 'bottom')).set_start(start_time_sec).set_duration(audio_duration)
                clips.append(subtitle_clip)

            final_clip = CompositeVideoClip(clips)

            # 動画を出力
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        return output_path
