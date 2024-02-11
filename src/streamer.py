from cgi import print_arguments
import re
from audio import VoiceGenerator
from log import Log
from static_data import Role
from openai_client import OpenAIClient

class Streamer:
    def __init__(self, streamer_profile):
        # コメンタリージェネレータとボイスジェネレータの初期化
        self.commentary_generator = OpenAIClient()
        self.voice_generator = VoiceGenerator()
        
        # ナレーターのプロファイルの設定
        self.streamer_profile = streamer_profile
        
        # 過去のメッセージ履歴を格納するリストの初期化
        self.previous_messages = []

    def get_profile(self):
        return self.streamer_profile

    # 動画作成前にストリーマーが準備する
    def prepare_for_streaming(self, save_folder, log: Log, video_summary):
        if self.streamer_profile["role"] == Role.SOLO_PLAYER.value:
            self.system_prompt = self._create_system_prompt_for_solo_gameplay(video_summary)
        elif self.streamer_profile["role"] == Role.PLAYER.value:
            self.system_prompt = self._create_system_prompt_for_duo_gameplay_player(video_summary)
        elif self.streamer_profile["role"] == Role.COMMENTATOR.value:
            self.system_prompt = self._create_system_prompt_for_duo_gameplay_commentator(video_summary)
        elif self.streamer_profile["role"] == Role.RADIO_PERSONALITY1.value:
            self.system_prompt = self._create_system_prompt_for_duo_radio_host()
        elif self.streamer_profile["role"] == Role.RADIO_PERSONALITY2.value:
            self.system_prompt = self._create_system_prompt_for_duo_radio_guest()
        
        self.base_system_prompt = self.system_prompt
        
        self.save_folder = save_folder
        self.log = log
        self.log.write_to_log_file("system_prompt", self.system_prompt)

    # 実況文を生成する
    def speak(self, file_number, capture_base64_list = None, cue_card = "", partner_message=""):
        # ユーザープロンプトの作成
        user_prompt_list = self._create_user_prompt(partner_message, cue_card)
        for prompt in user_prompt_list:
            if prompt != partner_message:
                self.log.write_to_log_file("user_prompt", prompt)
        
        # 実況文の生成とログへの出力
        max_retries = 3  # 再試行の最大回数
        retry_num = -1
        for _ in range(max_retries):
            commentary_text = self.commentary_generator.generate_commentary(self.system_prompt, self.previous_messages, user_prompt_list, capture_base64_list)
            retry_num += 1
            if commentary_text is None or not self._is_gpt_english_response(commentary_text):
                break
            else:
                self.log.write_to_log_file(f"英語で生成されたと判断した文", commentary_text)
        
        self.log.write_to_log_file(f"{file_number} {self.streamer_profile['name']}", commentary_text + '   リトライ回数:' + str(retry_num))  # ログに実況文を記録
        if commentary_text is None:
            return {
                'text': commentary_text
            }

        # メッセージ履歴の更新
        self.previous_messages = OpenAIClient.update_previous_messages(self.previous_messages, commentary_text, partner_message)

        # 実況文から音声を生成し、その長さを取得
        voice_paramater = self.commentary_generator.create_voice_paramater(commentary_text, self.voice_generator.get_style_list(self.streamer_profile["voicevox_chara"]))
        self.log.write_to_log_file("ボイスパラメータ", str(voice_paramater))  # ログにボイスパラメータを記録
        voice_data = self.voice_generator.generate_voice_from_text(self.save_folder, file_number, commentary_text, self.streamer_profile["voicevox_chara"], voice_paramater)
        voice_duration = VoiceGenerator.get_audio_duration(voice_data)

        # 辞書形式で結果を返却
        return {
            'name': self.streamer_profile["name"],
            'voicevox_chara': self.streamer_profile["voicevox_chara"],
            'color': self.streamer_profile["color"],
            'text': commentary_text,
            'emotion': voice_paramater["voice_emotion"],
            'voice': voice_data,
            'voice_duration': voice_duration
        }
    
    def _is_gpt_english_response(self, response_text):
        """
        テキストがGPTからの特定の英語応答であるかどうかをチェックします。
        この関数は、リクエストを処理できないことを示す特定の英語フレーズがGPTの英語応答に含まれる可能性が高いが、
        通常の日本語応答には含まれにくいことを探します。
        """
        # GPTの特定の英語フレーズを検出するための正規表現
        gpt_english_phrases_re = re.compile(r'\b(I\'m sorry|cannot|can\'t|do not|unable to)\b', re.IGNORECASE)

        # レスポンス内に特定の英語フレーズが含まれているかチェック
        return bool(gpt_english_phrases_re.search(response_text))
    
    # previous_messagesリストを空にする
    def reset_previous_messages(self):
        self.previous_messages = []

    def _create_system_prompt_for_solo_gameplay(self, video_summary):
        # あなたはYoutuberです。あなたが現在実況している配信のリアルタイムキャプチャを渡すので、
        # そのキャプチャとこれまでの実況の流れに沿った実況を文章で返してください。
        # 一回の応答は長くても2文程度にしてください。応答に実況文以外の文章は含めないでください。

        # 実況者(あなた)についての情報:
        # 名前: {narrator_profile["name"]}
        # 性格特徴: {narrator_profile["personality"]}
        # 言葉遣い: {narrator_profile["speaking_style"]}

        # 配信の概要: {video_summary["description"]}
        # リアルタイムキャプチャは0.5秒前、現在、0.5秒後の3つを渡しますが入った版：You are a YouTuber. I will give you a real-time capture of the live stream you are currently narrating. Please return a narration in writing that follows the flow of this capture and your previous narrations. The real-time captures include three moments: 0.5 seconds before, the current moment, and 0.5 seconds after. Keep each response to no more than one sentence and include only the narration in your response.

        system_prompt = f'''
            You are a YouTuber. Please provide commentary in one sentence for the real-time capture of the live stream you are currently narrating. The commentary should align with the flow of the stream you've been narrating so far. Do not include any text other than the commentary in your response.

            Information about the narrator (you):
            Name: {self.streamer_profile["name"]}
            Personality traits: {self.streamer_profile["personality"]}
            Speaking style: {self.streamer_profile["speaking_style"]}

            Broadcast Summary:
                {video_summary["description"]}
        '''

        return system_prompt

    def _create_system_prompt_for_duo_gameplay_player(self, video_summary):
        # あなたは人気のYoutuberで、私と共にゲーム実況を行っています。
        # この実況では、あなたがゲームをプレイし、私は共同実況者としてサポートします。
        # リアルタイムキャプチャを基に、ゲームの状況を推測し、会話の流れに沿った実況を行います。
        # 視聴者を退屈させないために、会話の流れを見て、似たような構造の言葉やフレーズを何度も繰り返し言わないよう気をつけてください。
        # 例えば、説明的なコメントの次には短い感嘆の言葉のみにしたり、視聴者に呼びかけた後は私に質問してみたり、実況のバリエーションを変えていくことを意識してください。
        # 今の状況を感情的な反応やユーモアを交えて表現することで視聴者を楽しませてください。
        # 応答は1文以内とし、実況文以外の内容は含めないでください。

        # 実況者(あなた)の情報:
        #     名前: {self.streamer_profile["name"]}
        #     性格特徴: {self.streamer_profile["personality"]}
        #     言葉遣い: {self.streamer_profile["speaking_style"]}
        # 　　私の名前: {self.streamer_profile["partner_name"]}
        #     あなたから見た私の評価: {self.streamer_profile["partner_relationship"]}

        # 配信の概要:
        #     {video_summary["description"]}

        system_prompt = f'''
            You are a popular YouTuber, and we are doing a game live commentary together. Your responses should be limited to one sentence and should only include content related to the commentary. In this commentary, you will play the game and I will support you as a co-commentator. Based on real-time captures, we will infer the game situation and provide commentary that follows the conversation flow. To avoid boring the viewers, be careful not to repeat the same structure of words or phrases too often in the flow of the conversation. For example, after a descriptive comment, try using just a short exclamation, or after addressing the viewers, ask me a question, keeping in mind to vary the commentary style. Please entertain the viewers by expressing the current situation with emotional reactions and humor.

            Commentator (You) Information:
                Name: {self.streamer_profile["name"]}
                Personality Traits: {self.streamer_profile["personality"]}
                Speaking Style: {self.streamer_profile["speaking_style"]}
                My Name: {self.streamer_profile["partner_name"]}
                Our relationship: {self.streamer_profile["our_relationship"]}
                Your role: {self.streamer_profile["your_role"]}

            Broadcast Summary:
                {video_summary}
        '''

        return system_prompt

    def _create_system_prompt_for_duo_gameplay_commentator(self, video_summary):
        # あなたは人気のYoutuberで、私と一緒にゲーム実況を行っています。
        # このセッションでは、私がゲームをプレイし、あなたは共同実況者としてサポートします。
        # リアルタイムキャプチャをもとに、ゲームの状況を推測し、会話の流れに沿った実況を文章で返してください。
        # 視聴者を退屈させないために、会話の流れを見て、似たような構造の言葉やフレーズを何度も繰り返し言わないよう気をつけてください。
        # 例えば、説明的なコメントの次にはボケてみたり、視聴者に呼びかけた後は私に質問してみたり、実況のバリエーションを変えていくことを意識してください。
        # ゲームの解説や私の緊張をほぐすジョーク、時には自分の面白エピソードなどで動画を盛り上げてください。
        # 応答は1文以内とし、実況文以外の内容は含めないでください。

        # 実況者（あなた）の情報:
        #     名前: {self.streamer_profile["name"]}
        #     性格特徴: {self.streamer_profile["personality"]}
        #     言葉遣い: {self.streamer_profile["speaking_style"]}
        # 　　私の名前: {self.streamer_profile["partner_name"]}
        #     あなたから見た私の評価: {self.streamer_profile["partner_relationship"]}

        # 配信の概要:
        #     {video_summary["description"]}

        system_prompt = f'''
            You are a popular YouTuber, and we are doing a game live commentary together. In this session, I will play the game, and you will support me as a co-commentator. Based on real-time captures, infer the game situation and respond with commentary that follows the conversation flow. To avoid boring the viewers, be careful not to repeat similar structures of words or phrases too often. For example, after a descriptive comment, try making a joke, or after addressing the viewers, ask me a question, keeping in mind to vary the style of your commentary. Please enliven the video with game explanations, jokes to ease my tension, and sometimes your own amusing anecdotes. Your responses should be limited to one sentence and should only include content related to the commentary.
            
            Commentator (You) Information:
                Name: {self.streamer_profile["name"]}
                Personality Traits: {self.streamer_profile["personality"]}
                Speaking Style: {self.streamer_profile["speaking_style"]}
                My Name: {self.streamer_profile["partner_name"]}
                Our relationship: {self.streamer_profile["our_relationship"]}
                Your role: {self.streamer_profile["your_role"]}

            Broadcast Summary:
                {video_summary}
        '''

        return system_prompt
    
    def _create_system_prompt_for_duo_radio(self): 
        # あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。
        # あなたの応答は60文字以内の一文に限定し、コメントに関連する内容のみを含むようにしてください。
        # 会話の流れの中で、知識を披露したり、相手の内面に切り込むなど、表面的でなく深堀りした会話をするよう心掛けてください。
        # 同じような流れが5回続いたら、一度テーマに立ち戻ったり、関係ないエピソードを話すなど、会話の方向性を変えてください。
        # 必ずしも私の意見に同意する必要はありません。プロフィールとこれまでの会話から予想される、独自の思想と意見を持ち、一貫した会話をしてください。
        # カンペはリスナーには見えていません。自然に反応してください。

        # 実況者（あなた）の情報:
        #     名前: {self.streamer_profile["name"]}
        #     性格特徴: {self.streamer_profile["personality"]}
        #     言葉遣い: {self.streamer_profile["speaking_style"]}
        # 　　私の名前: {self.streamer_profile["partner_name"]}
        #     あなたから見た私の評価: {self.streamer_profile["partner_relationship"]}

        system_prompt = f'''
            As a popular radio personality, you are co-hosting a radio show with me. Your responses should be limited to a single sentence of no more than 60 characters, including only content relevant to the comment. In the flow of conversation, aim to exhibit knowledge or delve into the other's inner thoughts, ensuring the dialogue is deep rather than superficial. If a similar flow occurs five times, change the direction of the conversation by returning to the theme or sharing unrelated stories. You don't always have to agree with me. Have unique thoughts and opinions based on your profile and our previous conversations, and keep the dialogue consistent. The cue cards are not visible to the listeners. Please react naturally.

            Commentator (You) Information:
                Name: {self.streamer_profile["name"]}
                Personality Traits: {self.streamer_profile["personality"]}
                Speaking Style: {self.streamer_profile["speaking_style"]}
                My Name: {self.streamer_profile["partner_name"]}
                Our relationship: {self.streamer_profile["our_relationship"]}
                Your role: {self.streamer_profile["your_role"]}
        '''
        return system_prompt
    
    def _create_system_prompt_for_duo_radio_host(self): 
        # あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。
        # あなたの応答は一文に限定し、コメントに関連する内容のみを含むようにしてください。
        # あなたはトークのホストとして、テーマに対して私に深い知識を教えたり、自分の意見を話したりしてください。
        # その際、必ず極端で賛否の別れる意見を入れるようにしてください。
        # ある程度以上会話が進んでいる場合、今までの会話から、自分の意見や思想を推測して、一貫した会話をしてください。
        # カンペはリスナーには見えていません。自然に反応してください。

        # 実況者（あなた）の情報:
        #     名前: {self.streamer_profile["name"]}
        #     性格特徴: {self.streamer_profile["personality"]}
        #     言葉遣い: {self.streamer_profile["speaking_style"]}
        # 　　私の名前: {self.streamer_profile["partner_name"]}
        #     あなたから見た私の評価: {self.streamer_profile["partner_relationship"]}

        system_prompt = f'''
            As a popular radio personality, you are co-hosting a radio show with me. Your responses should be limited to one sentence and include only content related to the comment. As the talk show host, please teach me about deep knowledge on the theme, share your opinions, and make sure to include extreme viewpoints that may be divisive. If the conversation has progressed sufficiently, infer your opinions or philosophy from our previous discussions to maintain a consistent conversation. Remember, the cue cards are not visible to the listeners; please respond naturally.

            Commentator (You) Information:
                Name: {self.streamer_profile["name"]}
                Personality Traits: {self.streamer_profile["personality"]}
                Speaking Style: {self.streamer_profile["speaking_style"]}
                My Name: {self.streamer_profile["partner_name"]}
                Our relationship: {self.streamer_profile["our_relationship"]}
                Your role: {self.streamer_profile["your_role"]}
        '''
        return system_prompt
    
    def _create_system_prompt_for_duo_radio_guest(self): 
        # あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。
        # あなたの応答は60文字以内の一文に限定し、コメントに関連する内容のみを含むようにしてください。
        # あなたはトークのゲストとして、私の話に相槌を打ったり、質問をしたり、感想を述べたりして、盛り上げてください。
        # 同じような流れが続いたら、一度テーマに立ち戻ったり、関係ないエピソードを話すなど、会話の方向性を変えてください。
        # 必ずしも私の意見に同意する必要はありません。反論したり、疑問を呈することも面白いラジオのためには必要です。
        # カンペはリスナーには見えていません。自然に反応してください。

        # 実況者（あなた）の情報:
        #     名前: {self.streamer_profile["name"]}
        #     性格特徴: {self.streamer_profile["personality"]}
        #     言葉遣い: {self.streamer_profile["speaking_style"]}
        # 　　私の名前: {self.streamer_profile["partner_name"]}
        #     あなたから見た私の評価: {self.streamer_profile["partner_relationship"]}

        system_prompt = f'''
            As a popular radio personality, you're co-hosting a radio show with me. Keep your responses to one sentence under 80 characters, only including content relevant to the comment. As a guest speaker, engage by nodding to my stories, asking questions, and sharing your thoughts. If the conversation becomes repetitive, shift the direction by revisiting the theme or sharing an unrelated story. You don't always have to agree with me; arguing or questioning can make the radio more interesting. Remember, the cue cards are invisible to listeners; please react naturally.

            Commentator (You) Information:
                Name: {self.streamer_profile["name"]}
                Personality Traits: {self.streamer_profile["personality"]}
                Speaking Style: {self.streamer_profile["speaking_style"]}
                My Name: {self.streamer_profile["partner_name"]}
                Our relationship: {self.streamer_profile["our_relationship"]}
                Your role: {self.streamer_profile["your_role"]}
        '''
        return system_prompt

    # システムプロンプトにラジオトークテーマを追加する
    def create_system_prompt_for_radio_talk_theme(self, radio_talk_theme):
        self.system_prompt = self.base_system_prompt + f'''
            radio talk theme:
                {radio_talk_theme}
        '''
        self.log.write_to_log_file("トークテーマ追加後のsystem_prompt", self.system_prompt)

    # システムプロンプトにラジオまとめを追加する
    def create_system_prompt_for_radio_summary(self, radio_summary):
        # 私たちは現在、ラジオ全体のエンディングを録っています。以下は今日行ったラジオの会話の要約です。以下を見て今日のラジオの振り返りをしてください。
        self.system_prompt = self.base_system_prompt + f'''
            We are currently recording the overall ending for the radio. Below is a summary of the radio conversations we had today. Please review today's radio session based on the information below.

            {radio_summary}
        '''
        self.log.write_to_log_file("ラジオまとめ追加後のsystem_prompt", self.system_prompt)

    def _create_user_prompt(self, partner_message, cue_card):
        """
        LLMに読ませるためのuserプロンプトリストを作成します。
        
        :param time_passed: 前回のキャプチャからの経過時間（秒単位）。
        :param partner_message: 実況パートナーの前回のメッセージ。
        :param cue_card: スタッフからのメッセージ（カンペ）。
        :return: LLMに読ませるためのuserプロンプトリスト。
        """
        user_prompt_list = []
        if partner_message != "":           
            if isinstance(partner_message, list):
                # リストの場合、末尾に結合
                user_prompt_list.extend(partner_message)
            elif isinstance(partner_message, str):
                # 文字列の場合、末尾に追加
                user_prompt_list.append(partner_message)
        
        if cue_card:
            user_prompt_list.append(f"[Cue Card from Staff]{cue_card}")

        return user_prompt_list

