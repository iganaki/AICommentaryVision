import datetime
import json
from math import e
import os
from pyexpat import model
import random
import re
import shutil
from tkinter import N
import traceback
from openai import OpenAI
import requests
from config import DATA_FOLDER, DEBUG_FLAG, MESSAGE_HISTORY_LIMIT
import log
import api_utilities

class OpenAIClient:
    def __init__(self):
        self.my_api_key = os.getenv("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.my_api_key)
        self.news_titles = []
        self.words = []

    # 呼ばれるたびに実況文を生成する。
    def generate_commentary(self, system_prompt, previous_messages, user_prompt_list, capture_base64_list):
        messages = self._build_messages(system_prompt, previous_messages, user_prompt_list, capture_base64_list)

        if capture_base64_list != None:
            gpt_model = "gpt-4-vision-preview"
        else:
            gpt_model = "gpt-4-turbo-preview"

        if DEBUG_FLAG:
            contents = ['これはデバッグ用のダミー応答です。いい。改行のテストのため、意図的に長い文章にしています。ご協力感謝します。',
                        'I\'m sorry, his is a dummy response for debugging. Good. It is intentionally long for testing line breaks. Thank you for your cooperation.',
                        'これはデバッグ用のダミー応答です。いい。改行のテストのため、意図的に長い文章にしています。ご協力感謝します。']

            content = random.choice(contents)

            response = {"choices": [{"message": {"content": content}}]}
            new_assistant_message = {"role": "assistant", "content": response["choices"][0]["message"]["content"]}
        else:
            try:
                response = self.client.chat.completions.create(
                    model=gpt_model,
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7,
                )
            except Exception as e:
                log.handle_api_error(e, "GPT4 API呼び出し中にエラーが発生しました", capture_base64=capture_base64_list, user_prompt=user_prompt_list)
                return None
            content = response.choices[0].message.content
            new_assistant_message = {"role": "assistant", "content": content}

        return new_assistant_message["content"]

    # OpenAI APIに渡すメッセージを組み立てる
    def _build_messages(self, system_prompt, previous_messages=[], user_prompt_list=[], capture_base64_list=[], assistant_prompt_list=[]):
        # システムプロンプト付加
        messages = [{"role": "system", "content": system_prompt}]
        
        # 過去のプロンプトリストがあれば付加
        messages.extend(previous_messages)

        # ユーザープロンプトリストがあれば付加
        if user_prompt_list != []:
            # capture_base64 リスト内の各要素に対する画像データの辞書を作成
            image_dicts = []
            if capture_base64_list:
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
                    messages.append({
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}]
                    })

        for prompt in assistant_prompt_list:
            messages.append({
                "role": "assistant",
                "content": prompt
            })

        return messages
    
    def create_voice_paramater(self, text, style_list):
        messages = self._create_voice_paramater_prompt(text, style_list)
        #ダミー回答
        if len(style_list) >= 3:
            normal_ret = [{'voice_emotion': "normal", 'voice_speed': 0.9, 'voice_pitch': 0.9, 'voice_style': style_list[0]},
                        {'voice_emotion': "positive", 'voice_speed': 1.0, 'voice_pitch': 1.0, 'voice_style': style_list[1]},
                        {'voice_emotion': "negative", 'voice_speed': 1.1, 'voice_pitch': 1.1, 'voice_style': style_list[2]}]
        else:
            normal_ret = [{'voice_emotion': "normal", 'voice_speed': 0.9, 'voice_pitch': 0.9, 'voice_style': style_list[0]},
                        {'voice_emotion': "positive", 'voice_speed': 1.0, 'voice_pitch': 1.0, 'voice_style': style_list[0]},
                        {'voice_emotion': "negative", 'voice_speed': 1.1, 'voice_pitch': 1.1, 'voice_style': style_list[0]}]
        normal_ret = random.choice(normal_ret)

        # gpt_model = "gpt-4-turbo-preview"
        gpt_model = "gpt-3.5-turbo-1106"

        if DEBUG_FLAG:
            return normal_ret
        else:
            try:
                response = self.client.chat.completions.create(
                    model=gpt_model,
                    response_format={"type": "json_object"},
                    messages=messages
                )
                try:
                    voice_paramater = json.loads(response.choices[0].message.content)
                except json.JSONDecodeError:
                    log.handle_api_error(e, "JSONモードの戻り値がJSON形式ではありませんでした。", text=text, voice_paramater=response.choices[0].message.content)
                    return normal_ret

            except Exception as e:
                log.handle_api_error(e, "GPT3.5 API呼び出し中にエラーが発生しました", text=text)
                return normal_ret

        return voice_paramater

    def _create_voice_paramater_prompt(self, text, style_list):
        # あなたは音声合成システムに渡すパラメータを作成するアシスタントです。
        # 日本語のセリフから発言者の感情や状況を推測し、パラメータを作成してください。
        # 回答は以下のJSON形式で返してください。
        # 声の感情は"positive"、"normal"、"negative"の３パターンで返します。
        # 声の速さ、声の高さは0.80~1.20までの間で、倍率で返してください。
        # 声のスタイルはstyle_listの中から最適なものを選択します。
        system_prompt = f'''
            You are an assistant responsible for creating parameters to pass to a voice synthesis system. From the Japanese script, infer the speaker's emotions and situation and create parameters. Please return your response in the following JSON format. The emotional tone of the voice should be categorized as "positive", "normal", or "negative". The speed and pitch of the voice should be returned as a ratio, within a range of 0.80 to 1.20. Select the most appropriate voice style from {', '.join(style_list)}.

            {{voice_emotion:, voice_speed:, voice_pitch:, voice_style:}}
        '''
        user_prompt = f"{text}"
        messages = self._build_messages(system_prompt, user_prompt_list=[user_prompt])
        return messages

    @staticmethod
    def classify_text(text, categories):
        # カテゴリのリストが空の場合、Noneを返す
        if not categories:
            return None

        # 各カテゴリに対してテキストをチェックする
        for category in categories:
            if category in text:
                return category

        # テキストに一致するカテゴリがない場合は、カテゴリリストの最初の要素を返す
        return categories[0]
    
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
    
    def generate_cue(self, system_prompt, user_prompt):
        messages = self._build_messages(system_prompt=system_prompt, user_prompt_list=[user_prompt])

        gpt_model = "gpt-4-turbo-preview"

        if DEBUG_FLAG:
            # カンペのリスト
            cues = ['相方のうっかりエピソードを話して', '最近会ったうれしいことを話して', 'ここでボケて']

            # ランダムにカンペを選択
            content = random.choice(cues)
        else:
            try:
                response = self.client.chat.completions.create(
                    model=gpt_model,
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7,
                )
            except Exception as e:
                log.handle_api_error(e, "GPT4 API呼び出し中にエラーが発生しました", system_prompt=system_prompt, user_prompt=user_prompt)
                return 'normal'
            content = response.choices[0].message.content

        return content
    
    # ラジオのトークテーマを生成する
    def generate_talk_theme(self):
        messages = self._create_talk_theme_prompt()

        gpt_model = "gpt-4-turbo-preview"

        if DEBUG_FLAG:
            # ランダムにテーマを選択
            talk_themes = ['月に行ったら何したい？', '最近の夢を教えて', 'お風呂でどこから洗う？']
            content = random.choice(talk_themes)
        else:
            try:
                response = self.client.chat.completions.create(
                    model=gpt_model,
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7,
                )
            except Exception as e:
                log.handle_api_error(e, "トークテーマ生成中にエラーが発生しました", gpt_model=gpt_model)
                return None
            content = response.choices[0].message.content
        return content

    def _create_talk_theme_prompt(self):
        if DEBUG_FLAG == True:
            random_news = "『ヘルダイバー2』先行レビュー。PvEに挑み続けるワイワーーーーイ系協力型TPS。コマンド入力で支援を呼び、エイリアンどもに“500kg”の爆弾を落とせ!! - ファミ通.com"
            random_word = "hellllllll"
        else:
            # ランダムなニュースを取得
            if not self.news_titles:
                self.news_titles = api_utilities.fetch_random_news()

            random_news = random.choice(self.news_titles)

            # 取得したニュースを削除
            self.news_titles.remove(random_news)

            # ランダムな単語を取得
            # random_word = api_utilities.fetch_random_word()
            if not self.words:
                self.words = api_utilities.fetch_random_wiki_word()
            random_word = random.choice(self.words)

            # 取得した単語を削除
            self.words.remove(random_word)

        # ランダムに与えられたニュースと単語を使用して、日本語で20文字程度のラジオのトークテーマを作成してください。
        system_prompt = f'''
            Please create a radio talk theme in Japanese, about 20 characters long, using randomly given news and words. Avoid names of living persons. Make it a general theme that is easy to talk about.
        '''
        user_prompt = f'''
            news: {random_news}
            word: {random_word}
        '''
        messages = self._build_messages(system_prompt=system_prompt, user_prompt_list=[user_prompt])

        log.show_message(f"news_titles_len={len(self.news_titles)}, random_news={random_news}, random_word={random_word}", newline=True)

        return messages

    def generate_radio_summary(self, serif_texts):
        summary = ""
        # トークを見どころを残したまま要約してください。        
        system_prompt = f'''
            Please summarize while leaving the highlights.
        '''
        for index, serif_text in enumerate(serif_texts, start=1):
            messages = self._build_messages(system_prompt=system_prompt, user_prompt_list=[serif_text])

            gpt_model = "gpt-4-turbo-preview"

            if DEBUG_FLAG:
                content = f"{index}個めのトークまとめだよー！"
                summary += content + "\n"
            else:
                try:
                    response = self.client.chat.completions.create(
                        model=gpt_model,
                        messages=messages,
                        max_tokens=300,
                        temperature=0.7,
                    )
                except Exception as e:
                    log.handle_api_error(e, "トークまとめ作成中にエラーが発生しました", gpt_model=gpt_model, messages=messages)
                    return None
                content = response.choices[0].message.content

            summary += f"{index}個めのトーク：" + content + "\n"

        return summary

    def generate_background_image(self, talk_theme, output_path, image_title):
        def try_generate_image(prompt):
            try:
                response = self.client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1792x1024",
                    quality="standard",
                    n=1,
                )
                return response
            except Exception as e:
                log.handle_api_error(e, "dall-e-3呼び出し中にエラーが発生しました", talk_theme=talk_theme, prompt=prompt)
                return None


        if DEBUG_FLAG:
            dummy_png = random.choice(['/images/background/dummy1.png', '/images/background/dummy2.png', '/images/background/dummy3.png']) 
            dummy_image = DATA_FOLDER + dummy_png
            image_filename = os.path.join(output_path, image_title + '.png')
            shutil.copy2(dummy_image, image_filename)
        else:
            prompt = self._create_background_image_prompt(talk_theme)
            response = try_generate_image(prompt)
            
            # エラーコードがcontent_policy_violationの場合、プロンプトを修正して再試行
            if response and 'error' in response and response['error']['code'] == 'content_policy_violation':
                # プロンプトの修正方法をここに実装
                modified_prompt = self._create_background_image_prompt(talk_theme, True)
                response = try_generate_image(modified_prompt)

            if response is None:
                return None

            image_url = response.data[0].url
            response = requests.get(image_url)

            if response.status_code == 200:
                image_filename = os.path.join(output_path, image_title + '.png')
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
            else:
                log.handle_api_error(response.status_code, "生成画像ダウンロード失敗", status_code=response.status_code)
                return None

        return image_filename

    def _create_background_image_prompt(self, talk_theme, more_safe=False):
        image_styles = [
                            "Watercolor", "Oil Painting", "Pencil Sketch", "Charcoal Drawing", "Pop Art",
                            "Abstract Art", "Pixel Art", "Monochrome", "Realistic", "Psychedelic",
                            "Vintage", "Retro Futuristic", "Minimalist", "Surrealism", "Graffiti",
                            "Comic Style", "Geometric", "Neon Art", "Pastel Colors", "Grunge Style",
                            "Documentary Style Photography", "Landscape Photography", "Urban Street Photography",
                            "Portrait Photography", "Vintage Photography", "Black and White Photography",
                            "Macro Photography", "Astrophotography", "Night Scene Photography", "Fashion Photography",
                            "Nature Photography", "Animal Photography", "Underwater Photography", "Sports Photography",
                            "Travel Photography", "Drone Aerial Photography", "Fine Art Photography",
                            "Sunset/Sunrise Photography", "Food Photography", "Abstract Photography",
                            "Cyberpunk", "Steampunk", "Fantasy Art", "Metallic Texture", "Classical Art",
                            "Impressionism", "Expressionism", "Art Nouveau", "Art Deco", "Folk Art",
                            "Fairy Tale Imagery", "Space Theme", "Underwater World", "Futuristic City",
                            "Fantastical Landscape", "Digital Art", "Glitch Art", "Surrealism", "Concept Art",
                            "Environmental Art"
                        ]

        # ランダムにスタイルを選択
        selected_style = random.choice(image_styles)
        
        # ラジオ番組のための背景画像を作成してください。
        # テーマに合った視覚的なイメージを提供してください。
        prompt = f'''
            Please create a background image for a radio show. Provide a visual image that matches the theme.
            talk_theme: {talk_theme}
            image style: {selected_style}
        '''
        if more_safe:
            # ラジオ番組の背景画像を作成してください。
            # テーマに合ったビジュアルイメージを提供してください。
            # 実在の人物名や不適切なワードは無視してください。
            # テーマの本質を象徴する抽象的で芸術的な画像を作成し、テーマに関連するムードや雰囲気をキャプチャしてください。
            # 色や形を使用してテーマの本質を反映させ、直接的な表現を避けて、
            # テーマの一般的な感覚を伝えるビジュアルを作成することに焦点を当ててください。
            prompt = f'''
                Please create a background image for the radio program. Provide a visual image that matches the theme. Ignore any real person names or inappropriate words.Create an abstract and artistic image that symbolizes the essence of the theme, and capture the mood and atmosphere related to the theme. Use colors and shapes to reflect the essence of the theme, avoid direct representations, and focus on creating a visual that conveys the general sense of the theme.
                talk_theme: {talk_theme}
                image style: {selected_style}
            '''

        return prompt


