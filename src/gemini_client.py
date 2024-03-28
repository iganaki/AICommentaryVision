from math import e
from multiprocessing import dummy
import os
import random
import re
import time
import anthropic
import log
import google.generativeai as genai

GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
class GeminiClient:
    def __init__(self, debug_mode):
        self.debug_mode = debug_mode
        self.cnt = 0
        
    # 実況文を生成する。
    def generate_capture_description(self, system_prompt, game_video_capture_path):
        # 実況文を生成
        response = self._generate_text(system_prompt, "gemini-pro", text_duration=300, temperature=0.7)
        commentary_text = response
        return commentary_text
        
        
    def _generate_text(self, system_prompts, claude_model, text_duration=300, temperature=0.7, 
                      previous_messages=[], partner_message="", cue_card="", dummy_text="これはデバッグ用のダミー応答です。"):
        system_prompt = "\n".join(system_prompts)
        messages = self._build_messages(previous_messages=previous_messages, 
                                        partner_message=partner_message, cue_card=cue_card)
        if self.debug_mode:
            text = dummy_text
            expected_role = "user"
            for message in messages:
                if message["role"] != expected_role:
                    raise ValueError(f"roleが交互になっていません。{message['role']}が連続しています。{messages}")
                expected_role = "assistant" if expected_role == "user" else "user"
        else:
            max_retries = 100  # 最大再試行回数
            retry_delay = 60  # 再試行までの遅延時間（秒）
            gemini_pro = genai.GenerativeModel("gemini-pro")

            for attempt in range(max_retries):
                try:
                    response = response = gemini_pro.generate_content(
                        model=claude_model,
                        system=system_prompt,
                        max_tokens=text_duration+100 if text_duration != 0 else 1024,
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
                        log.handle_api_error(e, "CLAUD呼び出し中にエラーが発生しました", system_prompt=system_prompt, gpt_model=claude_model, partner_message=partner_message, cue_card=cue_card)
                        raise  # 未知のエラーは再試行しない
            else:
                print("最大再試行回数に達しました。処理を中断します。")
                raise

        return text

    # Claude3 APIに渡すメッセージを組み立てる
    def _build_messages(self, previous_messages=[], partner_message="", cue_card=""):
        # 過去のプロンプトリストがあれば付加
        messages=[]
        messages.extend(previous_messages)

        # パートナーメッセージがあれば追加
        if partner_message != "":
            content = [{"type": "text", "text": partner_message}]
            messages.append({
                "role": "user",
                "content": content
            })

        # パートナーメッセージとカンペがあれば間にダミーアシスタントプロンプトを追加
        if cue_card != "" and partner_message != "":
            content = [{"type": "text", "text": "(スタッフのカンペ待ち)"}]
            messages.append({
                "role": "assistant",
                "content": content
            })
        
        # カンペがあれば追加
        if cue_card != "":
            content = [{"type": "text", "text": cue_card}]
            messages.append({
                "role": "user",
                "content": content
            })

        return messages

