import os
import time
import traceback
from openai import OpenAI
from config import OUTPUT_FOLDER

# グローバル変数でログファイルのパスを保持
current_log_file = None

class CommentaryGenerator:
    def __init__(self, debug_flag, narrator_profile, video_summary):
        self.previous_messages = []
        self.my_api_key = os.getenv("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.my_api_key)
        self.debug_flag = debug_flag
        self.system_prompt = self._create_system_prompt(narrator_profile, video_summary)

    # 呼ばれるたびに実況文を生成する。
    def generate_commentary(self, user_prompt, capture_base64_list):
        messages = self._build_messages(capture_base64_list, user_prompt)

        if self.debug_flag:
            response = {"choices": [{"message": {"content": "これはデバッグ用のダミー応答です。あああああああああああああああああああああ。あいいいいいいいいいいい。改行のテストのため、意図的に長い文章にしています。ご協力感謝します。"}}]}
            new_assistant_message = {"role": "assistant", "content": response["choices"][0]["message"]["content"]}
        else:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7,
                )
            except Exception as e:
                error_message = f"API呼び出し中にエラーが発生しました: {e}"
                stack_trace = traceback.format_exc()
                input_values = f"入力値: capture_base64={capture_base64_list}, user_prompt={user_prompt}"
                full_error_message = f"{error_message}\n{input_values}\nスタックトレース:\n{stack_trace}"
                print(full_error_message)
                write_to_log_file("OpenAI API Error", full_error_message)
                return None
            content = response.choices[0].message.content
            new_assistant_message = {"role": "assistant", "content": content}

        self._update_previous_messages(user_prompt, new_assistant_message)
        self._trim_messages_history()
        write_to_log_file("new_assistant_message", new_assistant_message["content"])

        return new_assistant_message["content"]

    # OpenAI APIに渡すメッセージを組み立てる
    def _build_messages(self, capture_base64_list, user_prompt):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.previous_messages)

        # capture_base64 リスト内の各要素に対する画像データの辞書を作成
        image_dicts = [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_string}"} for base64_string in capture_base64_list]

        # ユーザープロンプトを追加
        content = [{"type": "text", "text": user_prompt}] + image_dicts

        # content を含むメッセージを追加
        messages.append({
            "role": "user",
            "content": content
        })
        return messages
    
    # 保持しているメッセージリストを更新
    def _update_previous_messages(self, user_prompt, assistant_message):
        # userは履歴に必要ない気がするのでいったんコメントアウト。
        # new_user_message = {"role": "user", "content": user_prompt}
        # self.previous_messages.append(new_user_message)
        self.previous_messages.append(assistant_message)

    # 直近の5組のuserとassistantのメッセージだけを保持
    def _trim_messages_history(self):
        if len(self.previous_messages) > 7:
            self.previous_messages = self.previous_messages[-7:]
    
    @staticmethod
    def _create_system_prompt(narrator_profile, video_summary):
        # あなたはYoutuberです。あなたが現在実況している配信のリアルタイムキャプチャを渡すので、
        # そのキャプチャとこれまでの実況の流れに沿った実況を文章で返してください。
        # リアルタイムキャプチャは0.5秒前、現在、0.5秒後の3つを渡します。
        # 一回の応答は長くても2文程度にしてください。応答に実況文以外の文章は含めないでください。

        # 実況者(あなた)についての情報:
        # 名前: {narrator_profile["name"]}
        # 性格特徴: {narrator_profile["personality"]}
        # 言葉遣い: {narrator_profile["speaking_style"]}

        # 配信の概要: {video_summary["description"]}
        # 3つ渡す版：You are a YouTuber. I will give you a real-time capture of the live stream you are currently narrating. Please return a narration in writing that follows the flow of this capture and your previous narrations. The real-time captures include three moments: 0.5 seconds before, the current moment, and 0.5 seconds after. Keep each response to no more than one sentence and include only the narration in your response.

        system_prompt = f'''
            You are a YouTuber. Please provide commentary in one sentence for the real-time capture of the live stream you are currently narrating. The commentary should align with the flow of the stream you've been narrating so far. Do not include any text other than the commentary in your response.

            Information about the narrator (you):
            Name: {narrator_profile["name"]}
            Personality traits: {narrator_profile["personality"]}
            Speaking style: {narrator_profile["speaking_style"]}

            Summary of the stream: {video_summary["description"]}
        '''

        write_to_log_file("system_prompt", system_prompt)

        return system_prompt

    @staticmethod
    def create_user_prompt(time_passed, isFirst=True):
        time_passed_sec = int(time_passed)
        user_prompt = ""
        if isFirst:
            user_prompt = "At the beginning of the stream, greet the viewers watching the live broadcast and then start your narration."
        else:
            user_prompt = f"前回のキャプチャから{time_passed_sec}秒経過しました。"

        write_to_log_file("user_prompt", user_prompt)

        return user_prompt

def create_log_file(video_title='nontitle'):
    global current_log_file
    # ログファイルのパスを生成（日時情報を含む）
    current_log_file = f'{OUTPUT_FOLDER}/{video_title}_log_{int(time.time())}.txt'
    # 空のログファイルを作成
    with open(current_log_file, 'w', encoding='utf-8') as file:
        file.write('')
    return current_log_file

def write_to_log_file(tag, text):
    global current_log_file
    # 現在のログファイルパスを確認
    if current_log_file is None:
        # ログファイルが存在しない場合、新しいログファイルを作成
        current_log_file = create_log_file()

    # ログファイルの内容
    log = f'{tag} :\n{text}\n\n'

    # ログファイルに追記
    with open(current_log_file, 'a', encoding='utf-8') as file:
        file.write(log)