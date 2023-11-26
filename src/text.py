import datetime
import os
import random
import traceback
from openai import OpenAI
from config import DEBUG_FLAG, MESSAGE_HISTORY_LIMIT
import log

class CommentaryGenerator:
    def __init__(self):
        self.my_api_key = os.getenv("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.my_api_key)

    # 呼ばれるたびに実況文を生成する。
    def generate_commentary(self, system_prompt, previous_messages, user_prompt_list, capture_base64_list):
        messages = self._build_messages(system_prompt, previous_messages, user_prompt_list, capture_base64_list)

        if DEBUG_FLAG:
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
                input_values = f"入力値: capture_base64={capture_base64_list}, user_prompt={user_prompt_list}"
                full_error_message = f"{error_message}\n{input_values}\nスタックトレース:\n{stack_trace}"
                print(full_error_message)
                log.write_error_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                log.write_error_log(full_error_message)
                return None
            content = response.choices[0].message.content
            new_assistant_message = {"role": "assistant", "content": content}

        return new_assistant_message["content"]

    # OpenAI APIに渡すメッセージを組み立てる
    def _build_messages(self, system_prompt, previous_messages, user_prompt_list, capture_base64_list):
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(previous_messages)

        # capture_base64 リスト内の各要素に対する画像データの辞書を作成
        image_dicts = [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_string}"} for base64_string in capture_base64_list]

        # ユーザープロンプトを追加
        content = [{"type": "text", "text": user_prompt_list[0]}] + image_dicts

        # content を含むメッセージを追加
        messages.append({
            "role": "user",
            "content": content
        })

        if len(user_prompt_list) > 1:
            for prompt in user_prompt_list[1:]:
                # ここで各プロンプトに対して行いたい処理を実行
                # 例: プロンプトの印刷
                messages.append({
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                })

        return messages
    
    def suppose_emotion(self, text):
        messages = self._create_emotion_prompt(text)

        if DEBUG_FLAG:
            # 感情のリスト
            emotions = ['positive', 'negative', 'normal']

            # ランダムに感情を選択
            content = random.choice(emotions)
        else:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7,
                )
            except Exception as e:
                error_message = f"GPT3.5 API呼び出し中にエラーが発生しました: {e}"
                stack_trace = traceback.format_exc()
                input_values = f"入力値: text={text} 感情値計測"
                full_error_message = f"{error_message}\n{input_values}\nスタックトレース:\n{stack_trace}"
                print(full_error_message)
                log.write_error_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                log.write_error_log(full_error_message)
                return 'normal'
            content = response.choices[0].message.content
        emotion = self._evaluate_emotional_tone(content)
        return emotion
    
    @staticmethod
    def _evaluate_emotional_tone(text):
        if 'normal' in text:
            return 'normal'
        elif 'positive' in text:
            return 'positive'
        elif 'negative' in text:
            return 'negative'
        # 想定外の返答の場合normalにする。
        else:
            return 'normal' 

    @staticmethod
    def _create_emotion_prompt(text):
        # 以下のテキストの感情的なトーンを判断してください。
        # あなたの回答は「ポジティブ」、「ネガティブ」、または「ノーマル」のいずれか一つであるべきです。
        # 感情的なトーンが不明確な場合は、「ノーマル」と回答してください。
        system_prompt = f'''
            Please evaluate the emotional tone of the following text. Your response should be only one of the words 'positive', 'negative', or 'normal'. If the emotional tone is unclear, respond with 'normal'.
            
            Text: "{text}"
        '''
        messages = [{"role": "system", "content": system_prompt}]

        return messages
    
    @staticmethod
    def update_previous_messages(previous_messages, assistant_message, partner_message=None):
        if partner_message != None:
            previous_messages.append({"role": "user", "content": partner_message})
        previous_messages.append({"role": "assistant", "content": assistant_message})
        if len(previous_messages) > MESSAGE_HISTORY_LIMIT:
            previous_messages = previous_messages[-MESSAGE_HISTORY_LIMIT:]
        
        return previous_messages