from math import e
import os
import random
import re
import time
import anthropic
from config import MESSAGE_HISTORY_LIMIT
import log

claude_api_key = os.getenv("CLAUDE_API_KEY", "")
client = anthropic.Anthropic(
    api_key=claude_api_key,
)
class ClaudeClient:
    def __init__(self, debug_mode):
        self.debug_mode = debug_mode
        self.cnt = 0
        
    # 実況文を生成する。
    def generate_commentary(self, system_prompt, previous_messages, user_prompts, capture_base64_images):
        dummy_texts = ['これはデバッグ用のダミー応答です。いい。改行のテストのため、意図的に長い文章にしています。ご協力感謝します。']
        dummy_text = str(self.cnt)+"      "
        self.cnt += 1
        # claude-3-opus-20240229
        # claude-3-sonnet-20240229
        claude_model = "claude-3-opus-20240229"

        commentary = self._generate_text(system_prompt, claude_model, previous_messages=previous_messages, 
                                         user_prompts=user_prompts, capture_base64_images=capture_base64_images, 
                                         dummy_text=dummy_text)
        return commentary
        
    def _generate_text(self, system_prompt, claude_model, max_tokens=300, temperature=0.7, 
                      previous_messages=[], user_prompts=[], capture_base64_images=[], dummy_text="これはデバッグ用のダミー応答です。"):
        messages = self._build_messages(previous_messages=previous_messages, 
                                        user_prompts=user_prompts)
        if self.debug_mode:
            text = dummy_text
            # print(f"Generated text: {text}")
            # raise Exception("Not implemented")
        else:
            max_retries = 100  # 最大再試行回数
            retry_delay = 60  # 再試行までの遅延時間（秒）

            for attempt in range(max_retries):
                try:
                    response = client.messages.create(
                        model=claude_model,
                        system=system_prompt,
                        max_tokens=300,
                        messages=messages
                    )
                    text = response.content[0].text if response.content else None
                    break  # 成功したらループを抜ける
                except Exception as e:
                    # 特定のエラーを捕捉して処理
                    if "Internal server error" in str(e) or "Overloaded" in str(e):
                        print(f"エラー発生、再試行します ({attempt+1}/{max_retries})")
                        time.sleep(retry_delay)  # 設定した時間だけ待機
                    else:
                        log.handle_api_error(e, "CLAUD呼び出し中にエラーが発生しました", system_prompt=system_prompt, gpt_model=claude_model, user_prompts=user_prompts)
                        raise  # 未知のエラーは再試行しない
            else:
                print("最大再試行回数に達しました。処理を中断します。")
                raise

        return text

    # OpenAI APIに渡すメッセージを組み立てる
    def _build_messages(self, previous_messages=[], user_prompts=[]):
        # 過去のプロンプトリストがあれば付加
        messages=[]
        messages.extend(previous_messages)
        if len(previous_messages) == 1 and previous_messages[0]["content"] == "[Cue Card from Staff]番組開始です。まだ物語は開始せず、挨拶をしてください。":
            return previous_messages 

        # ユーザープロンプトリストがあれば付加
        if user_prompts != []:
            # ユーザープロンプトを追加
            content = [{"type": "text", "text": user_prompts[0]}]

            # content を含むメッセージを追加
            messages.append({
                "role": "user",
                "content": content
            })

            if len(user_prompts) > 1:
                # ダミーアシスタントプロンプトを追加
                content = [{"type": "text", "text": "(スタッフのカンペ待ち)"}]

                # content を含むメッセージを追加
                messages.append({
                    "role": "assistant",
                    "content": content
                })
                for prompt in user_prompts[1:]:
                    # ここで各プロンプトに対して行いたい処理を実行
                    messages.append({
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}]
                    })

        return messages
    
    @staticmethod
    def update_previous_messages(previous_messages, assistant_message, partner_message=""):
        if partner_message != "":
            if isinstance(partner_message, list):
                for message in partner_message:
                    previous_messages.append({"role": "user", "content": message})
            elif isinstance(partner_message, str):
                previous_messages.append({"role": "user", "content": partner_message})
        previous_messages.append({"role": "assistant", "content": assistant_message})
        if len(previous_messages) > MESSAGE_HISTORY_LIMIT:
            previous_messages = previous_messages[-MESSAGE_HISTORY_LIMIT:]
        
        return previous_messages
