import os

# main.py（または実行中のスクリプト）のディレクトリを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# outputフォルダの相対パス
OUTPUT_FOLDER = os.path.join(BASE_DIR, '../output')

# debugフラグ
DEBUG_FLAG = True

# 一人実況かどうか
SOLO_GAMEPLAY_MODE = 0
DUO_GAMEPLAY_MODE = 1
DUO_RADIO_MODE = 2

# 役割
SOLO_PLAYER = 0
PLAYER = 1
COMMENTATOR = 2

# 実況開始時間（秒）
START_TIME = 3.0


RADIO_DURATION_SEC = 150.0

# 字幕に使用するフォント
SUBTITLE_FONT = os.path.join(BASE_DIR, '../data/honoka-marugo2-1/Honoka-Shin-Maru-Gothic_R.otf')

# 字幕の設定
SUBTITLE_SETTINGS = {
    'fontsize': 70,
    'color': 'white',
    'stroke_color': 'green',
    'stroke_width': 1,
    'font': SUBTITLE_FONT
}

# メッセージ履歴の上限
MESSAGE_HISTORY_LIMIT = 10

VOICEVOX_VVID_DATA_CSV = os.path.join(BASE_DIR, '../data/voicevox_speaker_style_ids.csv')
