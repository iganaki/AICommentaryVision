import os

# 基本設定
# ------------------------
# 実行スクリプトのディレクトリパス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ディレクトリパス設定
# ------------------
OUTPUT_FOLDER = os.path.join(BASE_DIR, '../output')  # 出力フォルダ
DATA_FOLDER = os.path.join(BASE_DIR, '../data')      # データフォルダ
DATABASE_FOLDER = os.path.join(BASE_DIR, '../db')    # データベースフォルダ

# 機能フラグ設定
# ----------------
DEBUG_FLAG = False            # デバッグモード
EXPERIMENT_FLAG = False       # 実験モード
CUE_CARDS_PRINT_FLAG = False  # カンペ表示
AI_DIRECTOR_MODE = True       # AIディレクターモード

# 動画・ラジオ設定
# ----------------------
START_TIME = 1.5              # 実況開始時間（秒）
MAX_EXTRA_ROUNDS = 3          # 最大追加ラウンド数
RADIO_DURATION_SEC = 180      # ラジオの1パートの時間（秒）
RADIO_THEME_TALK_NUM = 4      # トークテーマ数
RADIO_SUMMARY_FLAG = True     # ラジオのまとめトークをするかどうか

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

