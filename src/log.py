import datetime
import sys
import time
import traceback
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

# 進捗を表示
def update_dialogue_progress(total_duration_sec, current_time, newline):
    progress_percentage = (current_time / total_duration_sec) * 100
    show_message("Progress: {:.2f}% ({:.2f}秒/{:.2f}秒)".format(progress_percentage, current_time, total_duration_sec), newline=newline)

# 任意のメッセージを表示
def show_message(message, newline=False):
    if newline:
        sys.stdout.write("\r{}\n".format(message))
    else:
        sys.stdout.write("\r{}".format(message))
    sys.stdout.flush()

# APIエラーをハンドル
def handle_api_error(exception, error_message, **input_values):
    error_message = f"{error_message} : {exception}"
    input_values_str = ", ".join(f"{key}={str(value)}" for key, value in input_values.items())
    formatted_input_values = f"入力値: {input_values_str}"
    stack_trace = traceback.format_exc()
    full_error_message = f"{error_message}\n{formatted_input_values}\nスタックトレース:\n{stack_trace}"
    print(full_error_message)
    write_error_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    write_error_log(full_error_message)