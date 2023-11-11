import cv2
import base64
from io import BytesIO
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip
from config import SUBTITLE_FONT

def load_video_and_get_duration(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return None, None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = (frame_count / fps)

    # 動画キャプチャを返す（まだ解放しない）
    return duration, cap


def get_video_capture_at_time(cap, time_sec):
    # フレームレートを取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 指定した秒数に対応するフレーム番号を計算
    frame_number = int(time_sec * fps)

    # 指定したフレーム番号にジャンプ
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # フレームのキャプチャ
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame at time:", time_sec)
        return None

    # キャプチャしたフレームをPIL画像に変換
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # PIL画像をBASE64エンコードする
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str

def add_audio_and_subtitles_to_video(video_path, generate_data, output_path):
    # 元の動画を読み込む
    video = VideoFileClip(video_path)
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
        subtitle_clip = TextClip(subtitle, fontsize=70, color='white', font=SUBTITLE_FONT).set_position(('center', 'bottom')).set_start(start_time_sec).set_duration(audio_duration)
        clips.append(subtitle_clip)

    final_clip = CompositeVideoClip(clips)

    # 動画を出力
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    return output_path