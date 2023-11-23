import sys
import time
from config import OUTPUT_FOLDER

class Log:
    def __init__(self, log_folder, video_title):
        # ログファイルのパスを生成（日時情報を含む）
        self.current_log_file = f'{log_folder}/{video_title}_log.txt'
        # 空のログファイルを作成
        with open(self.current_log_file, 'w', encoding='utf-8') as file:
            file.write('')

    def write_to_log_file(self, tag, text):
        # ログファイルの内容
        log = f'{tag} :\n{text}\n\n'

        # ログファイルに追記
        with open(self.current_log_file, 'a', encoding='utf-8') as file:
            file.write(log)

def write_error_log(text):
    current_log_file = f'{OUTPUT_FOLDER}/error_{int(time.time())}_log.txt'
    # 空のログファイルを作成
    with open(current_log_file, 'w', encoding='utf-8') as file:
        file.write(text)

def update_dialogue_progress(total_duration_sec, current_time):
    progress_percentage = (current_time / total_duration_sec) * 100
    sys.stdout.write("\rProgress: {:.2f}% ({:.2f}秒/{:.2f}秒)".format(progress_percentage, current_time, total_duration_sec))
    sys.stdout.flush()