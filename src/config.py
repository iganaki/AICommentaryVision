import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 基本設定
# ------------------------
# 実行スクリプトのディレクトリパス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ディレクトリパス設定
# ------------------
OUTPUT_FOLDER = os.path.join(BASE_DIR, '../output')  # 出力フォルダ
DATA_FOLDER = os.path.join(BASE_DIR, '../data')      # データフォルダ
DATABASE_FOLDER = os.path.join(BASE_DIR, '../db')    # データベースフォルダ

# ディレクトリがない場合は作成
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# データベース設定
# ----------------
database_path = os.path.join(DATABASE_FOLDER, 'database.db')
engine = create_engine(f'sqlite:///{database_path}')
Session = sessionmaker(bind=engine)

# 動画・ラジオ設定
# ----------------------
START_TIME = 1.5              # 実況開始時間（秒）
FADE_DURATION_SEC = 3         # フェード時間（秒）
CUE_CARDS_PRINT_FLAG = False  # カンペ表示
BACKUP_IMAGE_PATH = os.path.join(DATA_FOLDER, '../images/backup.jpg')  # バックアップ画像パス
VIDEO_CAPTURE_INTERVAL = 2   # 動画キャプチャ間隔（秒）
VIDEO_CAPTURE_START_TIME = 10  # 動画キャプチャ開始時間（秒）

# 字幕・カンペ設定
# ----------------
# 字幕用フォント
SUBTITLE_FONT_Honoka_Shin_Maru_Gothic_R = os.path.join(BASE_DIR, '../data/font/honoka-marugo2-1/Honoka-Shin-Maru-Gothic_R.otf')
SUBTITLE_FONT_ZenjidoJP_FeltPenLMT = os.path.join(BASE_DIR, "../data/font/Zenjido_PenLMT_1_00/ZenjidoJP-FeltPenLMT.otf")
SUBTITLE_FONT_TekitouPoem = os.path.join(BASE_DIR, "../data/font/TekitouPoem_1034/TekitouPoem.ttf")

# 字幕設定
SUBTITLE_SETTINGS = {
    'fontsize': 70,
    'color': 'white',
    'stroke_color': 'green',
    'stroke_width': 2,
    'font': SUBTITLE_FONT_Honoka_Shin_Maru_Gothic_R
}

# カンペ設定
CUE_SETTINGS = {
    'fontsize': 80,
    'color': 'black',
    'font': SUBTITLE_FONT_TekitouPoem
}

THEME_SETTINGS = {
    'fontsize': 80,
    'color': 'black',
    'stroke_color': 'white',
    'stroke_width': 2,
    'font': SUBTITLE_FONT_Honoka_Shin_Maru_Gothic_R
}
# その他設定
# --------------
MESSAGE_HISTORY_LIMIT = 20  # メッセージ履歴上限
VOICEVOX_VVID_DATA_CSV = os.path.join(BASE_DIR, '../data/voicevox_speaker_style_ids.csv')  # VOICEVOXデータパス
CLAUDE_FLAG = True  # CLAUDE使用フラグ
