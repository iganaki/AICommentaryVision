import os

# main.py（または実行中のスクリプト）のディレクトリを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# outputフォルダの相対パス
OUTPUT_FOLDER = os.path.join(BASE_DIR, '../output')

# tempフォルダのパスの相対パス
TEMP_FOLDER = f"{OUTPUT_FOLDER}/temp"

# 字幕に使用するフォント
SUBTITLE_FONT = os.path.join(BASE_DIR, '../data/honoka-marugo2-1/Honoka-Shin-Maru-Gothic_R.otf')

# debugフラグ
DEBUG_FLAG = False

# 実況開始時間（秒）
START_TIME = 3.0