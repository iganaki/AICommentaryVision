import json
from math import e
import os
import random
import shutil
from openai import OpenAI
import requests
from config import DATA_FOLDER
import log

openai_api_key = os.getenv("OPENAI_API_KEY", "")
openai_client = OpenAI(api_key=openai_api_key)
class OpenAIClient:
    def __init__(self, debug_mode):
        self.debug_mode = debug_mode
        
    # 実況文を生成する。
    def generate_commentary(self, system_prompts, previous_messages, user_prompts, capture_base64_images):
        dummy_texts = ['これはデバッグ用のダミー応答です。いい。改行のテストのため、意図的に長い文章にしています。ご協力感謝します。',
                      'I\'m sorry, his is a dummy response for debugging. Good. It is intentionally long for testing line breaks. Thank you for your cooperation.',
                      'これは短いデバッグダミー応答です。',
                      """宇宙太郎、実は昔、さいたま市の星空があまりにも美しいのに心奪われて、自分だけのものにしたいって思っちゃったんすよ。だから、ある夜、星を観測するための大きな望遠鏡を持ち出して、公園で独り占めしてたんす。でも、そこに来たのが小学生の真希ちゃん。真希ちゃんは星が大好きで、毎晩星を見るのが日課だったんすけど、宇宙太郎がいるせいで見れなくなっちゃったんすよね。

真希ちゃんの「星はみんなのものだよ」という一言で、宇宙太郎は自分の間違いに気づいたんす。罪悪感と反省から、宇宙太郎は星空保護活動を始めたんす。さいたま市の星空をより美しく、そして""",
"""
真希ちゃんの一言が全てを変えたんだね。でも、「星はみんなのもの」というシンプルな真実に気づくまで、宇宙太郎はなぜそんなに星を独り占めしたかったんだろう？""",
""" 宇宙太郎が星を独り占めしたかったのは、実は幼い頃からの夢があったからなんすよ。宇宙太郎は子供の頃に父親と一緒に星空を見るのが大好きだったんすけど、父親が急にいなくなっちゃって、その思い出だけが宇宙太郎にとっての宝物だったんす。だから、その思い出を守るために、「星は自分だけのもの」と思い込んでしまったんすよね。

でも、真希ちゃんの一言で、宇宙太郎は気づいたんす。「星はみんなのもの」というシンプルな真実を。そして、星空を共有する喜びが、実は父親との思い出をより美しく、より大切なものに変えるんだってことに。だからこそ、彼は星空保護の活動に情""",
""" あーしもそれ、気になるっすね。星空観察会でのルール違反に対しては、埼玉太郎が考えた対処法があって、それがこの物語のクライマックスにもつながるんですよ。埼玉太郎は、星空の下でのお楽しみを最大限に味わってもらうために、万が一ルールを破った参加者がいた場合は、その人にさいたま市の美しい夜空をもっと深く知ってもらうための特別プログラムを用意していました。
そのプログラムとは、星空ガイドの専門家と一緒に、夜空の星々を詳しく学ぶセッション。ルール違反をした人には、なんと星空の美しさと大切さをもっと深く理解してもらうチャンスを与えるんです。しかし、物語のクライマックスで、ルールを破ったの"""]
        dummy_text = random.choice(dummy_texts)
        if capture_base64_images:
            gpt_model = "gpt-4-vision-preview"
        else:
            gpt_model = "gpt-4-turbo-preview"

        commentary = self._generate_text(system_prompts, gpt_model, previous_messages=previous_messages, 
                                         user_prompts=user_prompts, capture_base64_images=capture_base64_images, 
                                         dummy_text=dummy_text)
        return commentary

    # カンペ文を生成する
    def generate_cue(self, system_prompt, user_prompt):
        dummy_texts = ['相方のうっかりエピソードを話して', '最近会ったうれしいことを話して', 'ここでボケて']
        dummy_text = random.choice(dummy_texts)
        gpt_model = "gpt-4-turbo-preview"
        cue = self._generate_text([system_prompt], gpt_model, user_prompts=[user_prompt], dummy_text=dummy_text)
        return cue
        
    # ラジオのトークテーマを生成する
    def generate_talk_theme(self, system_prompt, user_prompt):
        dummy_texts = ['月に行ったら何したい？', '最近の夢を教えて', 'お風呂でどこから洗う？']
        dummy_text = random.choice(dummy_texts)
        gpt_model = "gpt-4-turbo-preview"
        talk_theme = self._generate_text([system_prompt], gpt_model, user_prompts=[user_prompt], dummy_text=dummy_text)
        return talk_theme

    # ラジオのトークの要約を生成する
    def generate_radio_summary(self, serif_texts):
        summarys = ""
        # トークを見どころを残したまま200文字以内で要約してください。      
        system_prompt = f'''
            Please summarize the talk in 200 characters, leaving the highlights of the talk.
        '''
        gpt_model = "gpt-4-turbo-preview"
        for index, serif_text in enumerate(serif_texts, start=1):
            dummy_text = f"{index}個めのトークまとめだよー！"
            summary = self._generate_text([system_prompt], gpt_model, user_prompts=[serif_text], dummy_text=dummy_text)
            summarys += f"{index}個めのトーク：" + summary + "\n"
        return summarys
    
    # ラジオへのリスナーからのおたよりを生成する
    def generate_lerrer_from_listener(self, system_prompt, user_prompt):
        gpt_model = "gpt-4-turbo-preview"
        dummy_text = "こんにちは、いつも楽しくラジオを聞かせていただいています。"
        letter = self._generate_text([system_prompt], gpt_model, user_prompts=[user_prompt], dummy_text=dummy_text)
        return letter

    def _generate_text(self, system_prompts, gpt_model, max_tokens=300, temperature=0.7, 
                      previous_messages=[], user_prompts=[], capture_base64_images=[], dummy_text="これはデバッグ用のダミー応答です。"):
        messages = self._build_messages(system_prompts, previous_messages=previous_messages, 
                                        user_prompts=user_prompts, capture_base64_images=capture_base64_images)
        
        if self.debug_mode:
            text = dummy_text
        else:
            try:
                response = openai_client.chat.completions.create(
                    model=gpt_model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            except Exception as e:
                log.handle_api_error(e, "GPT4 API呼び出し中にエラーが発生しました", system_prompt=system_prompts, gpt_model=gpt_model, user_prompts=user_prompts)
                return None
            text = response.choices[0].message.content

        return text

    # OpenAI APIに渡すメッセージを組み立てる
    def _build_messages(self, system_prompts, previous_messages=[], user_prompts=[], capture_base64_images=[], assistant_prompts=[]):
        # システムプロンプト付加
        messages = []
        for system_prompt in system_prompts:
            messages.append({"role": "system", "content": system_prompt})
        
        # 過去のプロンプトリストがあれば付加
        messages.extend(previous_messages)

        # ユーザープロンプトリストがあれば付加
        if user_prompts != []:
            # capture_base64 リスト内の各要素に対する画像データの辞書を作成
            image_dicts = []
            if capture_base64_images:
                image_dicts = [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_string}"} for base64_string in capture_base64_images]

            # ユーザープロンプトを追加
            content = [{"type": "text", "text": user_prompts[0]}] + image_dicts

            # content を含むメッセージを追加
            messages.append({
                "role": "user",
                "content": content
            })

            if len(user_prompts) > 1:
                for prompt in user_prompts[1:]:
                    # ここで各プロンプトに対して行いたい処理を実行
                    messages.append({
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}]
                    })

        for prompt in assistant_prompts:
            messages.append({
                "role": "assistant",
                "content": prompt
            })

        return messages
    
    def generate_voice_paramater(self, text, style_list):
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

        voice_paramater = self._generate_json(messages, gpt_model, normal_ret)

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
        messages = self._build_messages([system_prompt], user_prompts=[user_prompt])
        return messages
    
    def _generate_json(self, messages, gpt_model, dummy_json):
        ret_json = dummy_json
        if not self.debug_mode:
            try:
                response = openai_client.chat.completions.create(
                    model=gpt_model,
                    response_format={"type": "json_object"},
                    messages=messages
                )
                try:
                    ret_json = json.loads(response.choices[0].message.content)
                except json.JSONDecodeError:
                    log.handle_api_error(e, "JSONモードの戻り値がJSON形式ではありませんでした。", gpt_model=gpt_model, messages=messages)

            except Exception as e:
                log.handle_api_error(e, "GPT JSONモード呼び出し中にエラーが発生しました", gpt_model=gpt_model, messages=messages)
        return ret_json

    def generate_background_image(self, prompt, output_path, image_title):
        def try_generate_image(prompt):
            try:
                response = openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1792x1024",
                    quality="standard",
                    n=1,
                )
                return response
            except Exception as e:
                log.handle_api_error(e, "dall-e-3呼び出し中にエラーが発生しました", prompt=prompt)

        if self.debug_mode:
            dummy_png = random.choice(['/images/background/dummy1.png', '/images/background/dummy2.png', '/images/background/dummy3.png']) 
            dummy_image = DATA_FOLDER + dummy_png
            image_filename = os.path.join(output_path, image_title + '.png')
            shutil.copy2(dummy_image, image_filename)
        else:
            prompt = self._add_image_style_for_background_image_prompt(prompt)
            response = try_generate_image(prompt)
            
            # エラーコードがcontent_policy_violationの場合、プロンプトを修正して再試行
            if response and 'error' in response and response['error']['code'] == 'content_policy_violation':
                # プロンプトの修正方法をここに実装
                modified_prompt = self._add_image_style_for_background_image_prompt(prompt, True)
                response = try_generate_image(modified_prompt)
                if response and 'error' in response and response['error']['code'] == 'content_policy_violation':
                    modified_prompt = self._add_image_style_for_background_image_prompt(prompt, True, True)
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

    def _add_image_style_for_background_image_prompt(self, base_prompt, more_safe=False, more_more_safe=False):
        image_styles = [
            "Watercolor", "Oil Painting", "Pencil Sketch", "Charcoal Drawing", "Pop Art",
            "Abstract Art", "Pixel Art", "Monochrome", "Realistic", "Psychedelic",
            "Vintage", "Retro Futuristic", "Minimalist", "Surrealism", "Graffiti",
            "Comic Style", "Geometric", "Neon Art", "Pastel Colors", "Grunge Style",
            "Fine Art Photography", "Landscape Photography", "Urban Street Photography",
            "Portrait Photography", "Black and White Photography",
            "Macro Photography", "Astrophotography", "Night Scene Photography", "Fashion Photography",
            "Nature Photography", "Animal Photography", "Underwater Photography", "Sports Photography",
            "Travel Photography", "Drone Aerial Photography",
            "Sunset/Sunrise Photography", "Food Photography", "Abstract Photography",
            "Cyberpunk", "Steampunk", "Fantasy Art", "Metallic Texture", "Classical Art",
            "Impressionism", "Expressionism", "Art Nouveau", "Art Deco", "Folk Art",
            "Fairy Tale Imagery", "Space Theme", "Underwater World", "Futuristic City",
            "Fantastical Landscape", "Digital Art", "Glitch Art", "Concept Art",
            "Environmental Art"
        ]

        # ランダムにスタイルを選択
        selected_style = random.choice(image_styles)
        
        if not more_safe:
            base_prompt += f'''
                image style: {selected_style}
            '''
        elif more_safe:
            # 実在の人物名や不適切なワードは無視してください。
            # テーマの本質を象徴する抽象的で芸術的な画像を作成し、テーマに関連するムードや雰囲気をキャプチャしてください。
            # 色や形を使用してテーマの本質を反映させ、直接的な表現を避けて、
            # テーマの一般的な感覚を伝えるビジュアルを作成することに焦点を当ててください。
            base_prompt += f'''
                Ignore any real person names or inappropriate words.Create an abstract and artistic image that symbolizes the essence of the theme, and capture the mood and atmosphere related to the theme. Use colors and shapes to reflect the essence of the theme, avoid direct representations, and focus on creating a visual that conveys the general sense of the theme.
                image style: {selected_style}
            '''
        elif more_more_safe:
            # ラジオの背景として使用できる。楽し気なイメージを作成してください。
            base_prompt = f'''
                Create an image that can be used as a radio background. Create a cheerful image.
                image style: {selected_style}
            '''

        return base_prompt

