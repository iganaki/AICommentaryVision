import os

# main.py（または実行中のスクリプト）のディレクトリを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# outputフォルダの相対パス
OUTPUT_FOLDER = os.path.join(BASE_DIR, '../output')

# dataフォルダの相対パス
DATA_FOLDER = os.path.join(BASE_DIR, '../data')

# dataフォルダの相対パス
DATABASE_FOLDER = os.path.join(BASE_DIR, '../db')

# debugフラグ
DEBUG_FLAG = True

# 
AI_DIRECTOR_MODE = False

# 実況開始時間（秒）
START_TIME = 3.0

# ラジオ1本の時間
RADIO_DURATION_SEC = 150.0

# 字幕に使用するフォント
SUBTITLE_FONT_Honoka_Shin_Maru_Gothic_R = os.path.join(BASE_DIR, '../data/font/honoka-marugo2-1/Honoka-Shin-Maru-Gothic_R.otf')

# 字幕の設定
SUBTITLE_SETTINGS = {
    'fontsize': 70,
    'color': 'white',
    'stroke_color': 'green',
    'stroke_width': 1,
    'font': SUBTITLE_FONT_Honoka_Shin_Maru_Gothic_R
}

# カンペに使用するフォント
SUBTITLE_FONT_ZenjidoJP_FeltPenLMT = os.path.join(BASE_DIR, "../data/font/Zenjido_PenLMT_1_00/ZenjidoJP-FeltPenLMT.otf")
SUBTITLE_FONT_TekitouPoem = os.path.join(BASE_DIR, "../data/font/TekitouPoem_1034/TekitouPoem.ttf")

# カンペの設定
CUE_SETTINGS = {
    'fontsize': 80,
    'color': 'black',
    'font': SUBTITLE_FONT_TekitouPoem
}

# メッセージ履歴の上限
MESSAGE_HISTORY_LIMIT = 20

# VOICEVOXデータのパス
VOICEVOX_VVID_DATA_CSV = os.path.join(BASE_DIR, '../data/voicevox_speaker_style_ids.csv')
