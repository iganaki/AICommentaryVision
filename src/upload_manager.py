import os
import re
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image, ImageDraw, ImageFont
from matplotlib import use
from config import DATA_FOLDER, OUTPUT_FOLDER
from model import StreamerProfile, VideoSection, session_scope

# 動画をアップロードする
def upload_video(video_title, use_shumnail_section=None, thumbnail_path=None, target_platform='youtube'):
    # 動画ファイルのパスを設定
    video_path = OUTPUT_FOLDER + f"/{video_title}/movie.mp4"

    # 動画の説明を設定
    description = create_video_description(video_title)

    # サムネイルを作成
    if use_shumnail_section and not thumbnail_path:
        thumbnail_path = create_thumbnail(video_title, use_shumnail_section, target_platform)

    if target_platform == 'youtube':
        # YouTubeに動画をアップロードする
        youtube_client = YouTubeClient(api_key)
        youtube_client.upload_video(video_path, video_title, description, thumbnail_path)
    elif target_platform == 'niconico':
        # ニコニコ動画に動画をアップロードする
        pass
    elif target_platform == 'twitter':
        # Twitterに動画をアップロードする
        pass
    else:
        raise ValueError("Invalid target platform. Please specify 'youtube' or 'twitter'.")

# サムネイルを作成する
def create_thumbnail(video_title, use_image_section, target_platform='youtube',left_up_text=None, bottom_text=None):
    # サムネイルのサイズを設定
    if target_platform == 'youtube' or target_platform == 'niconico':
        target_size = (1280, 720)
    elif target_platform == 'twitter':
        target_size = (1200, 675)
    else:
        raise ValueError("Invalid target platform. Please specify 'youtube' or 'twitter'.")
    
    # サムネイル画像のパスを設定
    back_ground_image_path = OUTPUT_FOLDER + f"/{video_title}/section{use_image_section}.png"

    # 画像をクロップしてリサイズする
    img = _crop_and_resize_image(back_ground_image_path, target_size)

    # データベースからキャラクター画像パスを取得
    with session_scope() as session:
        character_profiles = [profile[0] for profile in session.query(StreamerProfile.character_images_directory)
                              .filter(StreamerProfile.video_title == video_title).all()]
        
    # キャラクター画像を追加
    img = _add_character_to_image(img, character_profiles)

    # 文字列を追加
    img = _add_text_to_image(img, left_up_text, bottom_text)
        
    # サムネイル画像を保存
    thumbnail_path = OUTPUT_FOLDER + f"/{video_title}/thumbnail.jpg"

    img.save(thumbnail_path, "JPEG", quality=85)

    return thumbnail_path

def _crop_and_resize_image(input_path, target_size=(1280, 720)):
    with Image.open(input_path) as img:
        # 元のアスペクト比を維持しつつ、目標のアスペクト比に近づけるためにクロップする
        original_width, original_height = img.size
        
        # 新しいサイズ（クロップ後）を計算
        target_aspect_ratio = target_size[0] / target_size[1]
        new_height = int(original_width / target_aspect_ratio)
        
        # クロップする領域を計算（中央からクロップ）
        top = (original_height - new_height) / 2
        bottom = (original_height + new_height) / 2
        left = 0
        right = original_width
        
        # クロップ実行
        img_cropped = img.crop((left, top, right, bottom))
        
        # リサイズ実行
        img_resized = img_cropped.resize(target_size, Image.ANTIALIAS)

        return img_resized
    
def _add_character_to_image(img, character_profiles):
    # ホストのみの場合
    host_position_no_guest = (250, 100)  # 中央に近い位置
    host_angle_no_guest = 0

    # ゲストがいる場合
    host_position_with_guest = (100, 100)
    host_angle_with_guest = 15
    guest_position = (400, 100)
    guest_angle = 15

    if character_profiles:
        # 最初のプロファイルをホストとして扱う
        host_character_path = os.path.join(character_profiles[0], "normal.png")
        with Image.open(host_character_path) as host_img:
            if len(character_profiles) == 1:
                # ゲストがいない場合のホスト画像の回転と配置
                rotated_host_img = host_img.rotate(host_angle_no_guest, fillcolor=(0, 0, 0, 0))
                host_position = host_position_no_guest
            else:
                # ゲストがいる場合のホスト画像の回転と配置
                rotated_host_img = host_img.rotate(host_angle_with_guest, fillcolor=(0, 0, 0, 0))
                host_position = host_position_with_guest

            img.paste(rotated_host_img, host_position, rotated_host_img)

        # 2番目のプロファイルが存在する場合、それをゲストとして扱う
        if len(character_profiles) > 1:
            guest_character_path = os.path.join(character_profiles[1], "normal_inversion.png")
            with Image.open(guest_character_path) as guest_img:
                # ゲスト画像の回転と配置
                rotated_guest_img = guest_img.rotate(guest_angle, fillcolor=(0, 0, 0, 0))
                img.paste(rotated_guest_img, guest_position, rotated_guest_img)

    return img

def _add_text_to_image(img, left_up_text, bottom_text):
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()  # デフォルトフォントを使用
    if left_up_text:
        draw.text((10, 10), left_up_text, fill='white', font=font)
    if bottom_text:
        draw.text((10, 700), bottom_text, fill='white', font=font)
    return img

# 動画概要欄のテキストを作成する
def create_video_description(title, description):
    text = ""

    # タグを作成
    tags = ["AI生成", "GPT-4", "自動生成"]
    with session_scope() as session:
        # 動画に使用されるTTSキャラクターの名前を取得
        tts_names = session.query(StreamerProfile.tts_chara).filter(StreamerProfile.video_title == title).distinct().all()
        tts_tags = [tts_name[0] for tts_name in tts_names if tts_name[0]]

        # 基本のタグとTTSキャラクターの名前をタグに追加
        all_tags = tags + tts_tags
        for tag in all_tags:
            text += f"#{tag} "

        # 説明を付加
        text += f"\n\n{description}"

        # 動画に使用される音楽のファイルパスを取得し、重複を除去
        music_paths = session.query(VideoSection.background_music_path).filter(VideoSection.video_title == title).distinct().all()
        music_folders = set(os.path.dirname(path[0]) for path in music_paths if path[0])

        # 動画に使用されるキャラクターの画像が保存されているディレクトリのパスを取得し、重複を除去
        character_image_directories = session.query(StreamerProfile.character_images_directory).distinct().all()
        character_folders = set(path[0] for path in character_image_directories if path[0])

        # 使用素材のライセンス情報を付加
        text += "\n\n【使用素材】\n"
        for folder in music_folders.union(character_folders):
            license_info = _read_license_from_credits(folder)
            text += f"{license_info}\n"

    # 動画概要欄のテキストを保存
    description_path = os.path.join(OUTPUT_FOLDER, f"{title}/video_description.txt")
    with open(description_path, "w", encoding="utf-8") as f:
        f.write(text)

    return text

def _read_license_from_credits(folder_path):
    """指定されたフォルダ内のCredit.txtからライセンス情報を読み込む"""
    credit_file_path = os.path.join(folder_path, 'Credit.txt')
    try:
        with open(credit_file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()  # ファイルの内容を読み込み、前後の空白を削除
    except FileNotFoundError:
        return print("ライセンス情報が見つかりません。")

class YouTubeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    # 動画をアップロードする処理
    def upload_video(self, video_path, upload_title, description, thumbnail_path=None):
        request_body = {
            'snippet': {
                'title': upload_title,
                'description': description
            },
            'status': {
                'privacyStatus': 'public'
            }
        }

        media = MediaFileUpload(video_path)
        response = self.youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        ).execute()

        video_id = response['id']
        print(f"Video uploaded successfully! Video ID: {video_id}")

        # サムネイルを設定する処理
        if thumbnail_path:        
            self._set_thumbnail(video_id, thumbnail_path)

    # サムネイルを設定する処理
    def _set_thumbnail(self, video_id, thumbnail_path):
        media = MediaFileUpload(thumbnail_path)
        self.youtube.thumbnails().set(
            videoId=video_id,
            media_body=media
        ).execute()
        print("Thumbnail set successfully!")
