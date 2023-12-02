from audio import VoiceGenerator
from log import Log
from static_data import Role
from text import CommentaryGenerator

class Streamer:
    def __init__(self, streamer_profile):
        # コメンタリージェネレータとボイスジェネレータの初期化
        self.commentary_generator = CommentaryGenerator()
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
        
        self.save_folder = save_folder
        self.log = log
        self.log.write_to_log_file("system_prompt", self.system_prompt)

    # partner_messageがある場合は二人での実況、ない場合は一人での実況を意味します。
    def speak(self, file_number, capture_base64_list = None, time_passed = 0.0, cue_card = "", partner_message=None):
        # ユーザープロンプトの作成
        user_prompt_list = self._create_user_prompt(time_passed, partner_message, cue_card)
        for prompt in user_prompt_list:
            self.log.write_to_log_file("user_prompt", prompt)

        # 実況文の生成とログへの出力
        commentary_text = self.commentary_generator.generate_commentary(self.system_prompt, self.previous_messages, user_prompt_list, capture_base64_list)
        self.log.write_to_log_file(f"{file_number} {self.streamer_profile['name']}", commentary_text)  # ログに実況文を記録
        if commentary_text is None:
            return {
                'text': commentary_text
            }

        # メッセージ履歴の更新
        self.previous_messages = CommentaryGenerator.update_previous_messages(self.previous_messages, commentary_text, partner_message)

        # 実況文から音声を生成し、その長さを取得
        commentary_emotion = self.commentary_generator.suppose_emotion(commentary_text)
        self.log.write_to_log_file("感情", commentary_emotion)  # ログに感情を記録
        voice_data = self.voice_generator.generate_voice_from_text(self.save_folder, file_number, commentary_text, self.streamer_profile["voicevox_chara"], commentary_emotion)
        voice_duration = VoiceGenerator.get_audio_duration(voice_data)

        # 辞書形式で結果を返却
        return {
            'name': self.streamer_profile["name"],
            'voicevox_chara': self.streamer_profile["voicevox_chara"],
            'color': self.streamer_profile["color"],
            'text': commentary_text,
            'emotion': commentary_emotion,
            'voice': voice_data,
            'voice_duration': voice_duration
        }
    
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
                Your view of me: {self.streamer_profile["partner_relationship"]}

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
                Your view of me: {self.streamer_profile["partner_relationship"]}

            Broadcast Summary:
                {video_summary}
        '''

        return system_prompt
    
    def _create_user_prompt(self, time_passed, partner_message, cue_card):
        """
        LLMに読ませるためのuserプロンプトリストを作成します。
        
        :param time_passed: 前回のキャプチャからの経過時間（秒単位）。
        :param partner_message: 実況パートナーの前回のメッセージ。
        :param cue_card: スタッフからのメッセージ（カンペ）。
        :return: LLMに読ませるためのuserプロンプトリスト。
        """
        user_prompt_list = []
        if self.streamer_profile["role"] == Role.SOLO_PLAYER:
            if time_passed != 0:
                time_passed_sec = int(time_passed)
                user_prompt_list.append(f"Time has passed: {time_passed_sec} seconds since the last capture.")
        elif partner_message != "":
            user_prompt_list.append(partner_message)
        
        if cue_card:
            user_prompt_list.append(f"[Cue Card from Staff]{cue_card}")

        return user_prompt_list

