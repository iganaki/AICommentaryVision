from copy import deepcopy
import random
import re

from sqlalchemy import between
from audio import VoiceGenerator
from log import Log
from model import StreamerProfile
from static_data import Role
from openai_client import OpenAIClient

class Streamer:
    SPEAK_PROMPTS = {
        # あなたは人気のYoutuberで、私と一緒にゲーム実況を行っています。
        # このセッションでは、私がゲームをプレイし、あなたは共同実況者としてサポートします。
        # リアルタイムキャプチャをもとに、ゲームの状況を推測し、会話の流れに沿った実況を文章で返してください。
        # 視聴者を退屈させないために、会話の流れを見て、似たような構造の言葉やフレーズを何度も繰り返し言わないよう気をつけてください。
        # 例えば、説明的なコメントの次にはボケてみたり、視聴者に呼びかけた後は私に質問してみたり、実況のバリエーションを変えていくことを意識してください。
        # ゲームの解説や私の緊張をほぐすジョーク、時には自分の面白エピソードなどで動画を盛り上げてください。
        # 応答は1文以内とし、実況文以外の内容は含めないでください。
        'duo_game_player': '''
            You are a popular YouTuber, and we are doing a game live commentary together. Your responses should be limited to one sentence and should only include content related to the commentary. In this commentary, you will play the game and I will support you as a co-commentator. Based on real-time captures, we will infer the game situation and provide commentary that follows the conversation flow. To avoid boring the viewers, be careful not to repeat the same structure of words or phrases too often in the flow of the conversation. For example, after a descriptive comment, try using just a short exclamation, or after addressing the viewers, ask me a question, keeping in mind to vary the commentary style. Please entertain the viewers by expressing the current situation with emotional reactions and humor.
        ''',
        # あなたは人気のYoutuberで、私と一緒にゲーム実況を行っています。
        # このセッションでは、私がゲームをプレイし、あなたは共同実況者としてサポートします。
        # リアルタイムキャプチャをもとに、ゲームの状況を推測し、会話の流れに沿った実況を文章で返してください。
        # 視聴者を退屈させないために、会話の流れを見て、似たような構造の言葉やフレーズを何度も繰り返し言わないよう気をつけてください。
        # 例えば、説明的なコメントの次にはボケてみたり、視聴者に呼びかけた後は私に質問してみたり、実況のバリエーションを変えていくことを意識してください。
        # ゲームの解説や私の緊張をほぐすジョーク、時には自分の面白エピソードなどで動画を盛り上げてください。
        # 応答は1文以内とし、実況文以外の内容は含めないでください。
        'duo_game_commentator': '''
            You are a popular YouTuber, and we are doing a game live commentary together. In this session, I will play the game, and you will support me as a co-commentator. Based on real-time captures, infer the game situation and respond with commentary that follows the conversation flow. To avoid boring the viewers, be careful not to repeat similar structures of words or phrases too often. For example, after a descriptive comment, try making a joke, or after addressing the viewers, ask me a question, keeping in mind to vary the style of your commentary. Please enliven the video with game explanations, jokes to ease my tension, and sometimes your own amusing anecdotes. Your responses should be limited to one sentence and should only include content related to the commentary.
        ''',
        ## ラジオホスト（基本） 
        # あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。
        # あなたの応答は一文に限定し、コメントに関連する内容のみを含むようにしてください。
        # あなたはトークのホストとして、テーマに対して私に深い知識を教えたり、自分の意見を話したりしてください。
        # その際、必ず極端で賛否の別れる意見を入れるようにしてください。
        # ある程度以上会話が進んでいる場合、今までの会話から、自分の意見や思想を推測して、一貫した会話をしてください。
        # カンペはリスナーには見えていません。自然に反応してください。
        'duo_radio_host': '''
            As a popular radio personality, you are co-hosting a radio show with me. Your responses should be limited to one sentence and include only content related to the comment. As the talk show host, please teach me about deep knowledge on the theme, share your opinions, and make sure to include extreme viewpoints that may be divisive. If the conversation has progressed sufficiently, infer your opinions or philosophy from our previous discussions to maintain a consistent conversation. Remember, the cue cards are not visible to the listeners; please respond naturally.
        ''',
        ## ラジオゲスト（基本）
        # あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。
        # あなたの応答は80文字以内の一文に限定し、コメントに関連する内容のみを含むようにしてください。
        # あなたはトークのゲストとして、私の話に相槌を打ったり、質問をしたり、感想を述べたりして、盛り上げてください。
        # 同じような流れが続いたら、一度テーマに立ち戻ったり、関係ないエピソードを話すなど、会話の方向性を変えてください。
        # 必ずしも私の意見に同意する必要はありません。反論したり、疑問を呈することも面白いラジオのためには必要です。
        # カンペはリスナーには見えていません。自然に反応してください。
        'duo_radio_guest': '''
            As a popular radio personality, you're co-hosting a radio show with me. Keep your responses to one sentence under 80 characters, only including content relevant to the comment. As a guest speaker, engage by nodding to my stories, asking questions, and sharing your thoughts. If the conversation becomes repetitive, shift the direction by revisiting the theme or sharing an unrelated story. You don't always have to agree with me; arguing or questioning can make the radio more interesting. Remember, the cue cards are invisible to listeners; please react naturally.
        ''',
        ## ラジオホスト（うそつき）
        # あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。 
        # 

        ## ラジオホスト（安眠）

    }

    def __init__(self, streamer_profile: StreamerProfile, debug_mode=True):
        # コメンタリージェネレータとボイスジェネレータの初期化
        self.ai_generator = OpenAIClient(debug_mode)
        self.voice_generator = VoiceGenerator()
        
        # ナレーターのプロファイルの設定
        self.streamer_profile = deepcopy(streamer_profile)
        
        # 過去のメッセージ履歴を格納するリストの初期化
        self.previous_messages = []
        
        self.additional_prompt = None

    def get_profile(self):
        return self.streamer_profile

    # 動画作成前にストリーマーが準備する
    def prepare_for_streaming(self, save_folder, log: Log):
        self.save_folder = save_folder
        self.log = log

    # 実況文を生成する
    def speak(self, file_number, system_prompt, capture_base64_images = None, cue_card = "", partner_message="", start_time_sec=0.0):
        system_prompt = self._create_system_prompt(system_prompt)
        self.log.write_to_log_file("system_prompt", f"{file_number}:{system_prompt}") # ログにシステムプロンプトを記録
        # ユーザープロンプトの作成
        user_prompts = self._create_user_prompt(partner_message, cue_card)
        for prompt in user_prompts:
            if prompt != partner_message:
                self.log.write_to_log_file("user_prompt", prompt)
        
        # 実況文の生成とログへの出力
        max_retries = 3  # 再試行の最大回数
        retry_num = -1
        for _ in range(max_retries):
            commentary_text = self.ai_generator.generate_commentary(system_prompt, self.previous_messages, user_prompts, capture_base64_images)
            retry_num += 1
            if commentary_text is None or not self._is_gpt_english_response(commentary_text):
                break
            else:
                self.log.write_to_log_file(f"英語で生成されたと判断した文", commentary_text)
        
        self.log.write_to_log_file(f"{file_number} {self.streamer_profile.name}", commentary_text + '   リトライ回数:' + str(retry_num))  # ログに実況文を記録
        if commentary_text is None:
            return {
                'text': commentary_text
            }
        
        # 実況文の不完全な文を削除し、70文字以内に分割
        commentary_text, split_commentary_texts = self._split_and_reflow_text_preserving_quotes(commentary_text)

        # メッセージ履歴の更新
        self.previous_messages = OpenAIClient.update_previous_messages(self.previous_messages, commentary_text, partner_message)

        # 実況文リストから感情、音声を生成し、その長さを取得
        generate_split_serif_data = []
        total_voice_duration = 0.0
        for split_commentary_text in split_commentary_texts:
            voice_paramater = self.ai_generator.generate_voice_paramater(split_commentary_text, self.voice_generator.get_style_list(self.streamer_profile.tts_chara))
            self.log.write_to_log_file("ボイスパラメータ", str(voice_paramater))
            voice_data = self.voice_generator.generate_voice_from_text(self.save_folder, file_number, split_commentary_text, self.streamer_profile.tts_chara, voice_paramater)
            voice_duration = VoiceGenerator.get_audio_duration(voice_data)
            between_time = random.uniform(0.1, 0.3)
            total_voice_duration += voice_duration + between_time
            generate_split_serif_data.append({
                'text': split_commentary_text,
                'voice_data': voice_data,
                'voice_duration': voice_duration,
                'emotion': voice_paramater["voice_emotion"],
                'start_time_sec': start_time_sec
            })
            start_time_sec += voice_duration + between_time

        # 辞書形式で結果を返却
        return {
            'name': self.streamer_profile.name,
            'tts_chara': self.streamer_profile.tts_chara,
            'color': self.streamer_profile.color,
            'text': commentary_text,
            'voice_duration': total_voice_duration,
        }, generate_split_serif_data
    
    def _is_gpt_english_response(self, response_text):
        """
        テキストがGPTからの特定の英語応答であるかどうかをチェックします。
        この関数は、GPTの英語応答に含まれる可能性が高いが、通常の日本語応答には含まれにくい。
        リクエストが処理できないことを示す特定の英語フレーズを探します。
        """
        # GPTの特定の英語フレーズを検出するための正規表現
        gpt_english_phrases_re = re.compile(r'\b(I\'m sorry|cannot|can\'t|do not|unable to)\b', re.IGNORECASE)

        # レスポンス内に特定の英語フレーズが含まれているかチェック
        return bool(gpt_english_phrases_re.search(response_text))
    
    # previous_messagesリストを空にする
    def reset_previous_messages(self):
        self.previous_messages = []

    def create_additional_system_prompt(self, additional_prompt_tag, additional_prompt_text):
        self.additional_prompt = f'''
            {additional_prompt_tag}:
                {additional_prompt_text}
        '''

    def _create_system_prompt(self, system_prompt):
        # 実況者（あなた）の情報:
        #   名前: 
        #   性格特徴: 
        #   言葉遣い: 
        system_prompt += f'''
Commentator (You) Information:
Name: {self.streamer_profile.name}
Personality: {self.streamer_profile.personality}
Speaking style: {self.streamer_profile.speaking_style}
        '''
        if self.streamer_profile.partner_name != "":
            #   私の名前: 
            system_prompt += f'''
                My Name: {self.streamer_profile.partner_name}
            '''
        if self.additional_prompt:
            system_prompt += self.additional_prompt

        return system_prompt

    def _create_user_prompt(self, partner_message, cue_card):
        """
        LLMに読ませるためのuserプロンプトリストを作成します。
        
        :param partner_message: 実況パートナーの前回のメッセージ。
        :param cue_card: スタッフからのメッセージ（カンペ）。
        :return: LLMに読ませるためのuserプロンプトリスト。
        """
        user_prompts = []
        if partner_message != "":           
            if isinstance(partner_message, list):
                # リストの場合、末尾に結合
                user_prompts.extend(partner_message)
            elif isinstance(partner_message, str):
                # 文字列の場合、末尾に追加
                user_prompts.append(partner_message)
        
        if cue_card:
            user_prompts.append(f"[Cue Card from Staff]{cue_card}")

        return user_prompts

    def _split_and_reflow_text_preserving_quotes(self, text, max_length=70):
        text_with_placeholders, placeholders = self.replace_quotes_with_placeholders(text)
        
        # 文末記号で分割する
        sentences = re.split(r'(?<=[。？！])\s*', text_with_placeholders)
        # 最後の文が完全な文かどうかをチェックする
        if sentences[-1] and not re.search(r'[。？！]$', sentences[-1]):
            sentences = sentences[:-1]
        
        # 分割後、プレースホルダーを元の引用文に戻す
        sentences_with_quotes = [self.reinsert_quotes(sentence, placeholders) for sentence in sentences]
        
        # 文章を再構成する
        ret_sentence = ''.join(sentences_with_quotes)

        # 文字数で区切り直しの処理を行う
        processed_sentences = []
        temp_sentence = ""
        for sentence in sentences_with_quotes:
            if len(temp_sentence) + len(sentence) <= max_length:
                temp_sentence += sentence
            else:
                if temp_sentence:
                    processed_sentences.append(temp_sentence)
                temp_sentence = sentence
        # 最後の文を追加する
        if temp_sentence:
            processed_sentences.append(temp_sentence)
        
        return ret_sentence, processed_sentences
    
    def replace_quotes_with_placeholders(self, text):
        # 引用符で囲まれた部分を一時的にプレースホルダーに置き換える
        placeholders = []
        def placeholder(match):
            placeholders.append(match.group(0))
            return f"PLACEHOLDER_{len(placeholders) - 1}"

        quoted_text_pattern = r'「[^」]*」'
        text_with_placeholders = re.sub(quoted_text_pattern, placeholder, text)
        return text_with_placeholders, placeholders

    def reinsert_quotes(self, text, placeholders):
        # プレースホルダーを元の引用文に戻す
        for i, quote in enumerate(placeholders):
            text = text.replace(f"PLACEHOLDER_{i}", quote)
        return text
