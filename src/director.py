import random
from config import AI_DIRECTOR_MODE
from database import Database
from static_data import Role
from text import CommentaryGenerator


class Director:
    def __init__(self):
        # コメンタリージェネレータとボイスジェネレータの初期化
        self.commentary_generator = CommentaryGenerator()

    # 動画作成前にディレクターが準備する
    def prepare_for_streaming(self, streamers, video_summary, video_title, database:Database):
        self.streamers = streamers
        self.timer = 8
        self.next_cue, self.next_cue_print = "", ""
        self.database = database
        self.video_title = video_title
        if AI_DIRECTOR_MODE == True:
            self.systemprompt = self._create_cue_system_prompt(video_summary)
        else:
            self.cue_cards = self.database.fetch_all_cue_cards()
            self.temp_cue_cards = self.cue_cards

    def create_cue_card(self, extra_rounds, counter, streamer_index):
        cue_card, cue_card_print = "", ""
        self.counter = counter
        self.current_streamer = self.streamers[streamer_index]
        if self.streamers[streamer_index].get_profile()["role"] != Role.SOLO_PLAYER.value:
            self.partner_streamer = self.streamers[1-streamer_index]
        
        if self.timer > 0:
            self.timer -= 1

        # 最初の一言目のカンペを出す
        cue_card, cue_card_print = self._generate_starting_cue(self.streamers[streamer_index].get_profile()["name"])

        # 動画終了時のカンペを出す。
        if extra_rounds < 2 and cue_card == "":
            cue_card, cue_card_print = self._generate_ending_cue(extra_rounds)
        
        # 動画中のカンペを出す
        # 
        if self.next_cue != "" and cue_card == "":
            cue_card, cue_card_print = self.next_cue, self.next_cue_print
            self.next_cue, self.next_cue_print = "", ""

        # 
        if self.timer == 0 and cue_card == "":
            if AI_DIRECTOR_MODE == True:
                # AIディレクターがカンペを出す
                cue_card, cue_card_print = self._generate_ai_directed_cue()
            else:
                # ランダムディレクターがカンペを出す。
                cue_card, cue_card_print = self._generate_random_cue ()
                
            self.timer = random.randint(5, 10)

        return cue_card, cue_card_print
    
    def _generate_starting_cue(self, name):
        if self.counter == 0:
            return "開始しました、自分の名前をもじった挨拶から実況を始めてください", f"{name}、挨拶して"
        elif self.counter == 1:
            return "今日プレイするのはどんなゲームか相方に質問してください", "ゲームについて聞いて"
        elif self.counter == 2:
            return "視聴者にも伝わるよう質問に回答してください", "答えて"
        return "", ""

    def _generate_ending_cue(self, extra_rounds):
        return "そろそろ終了です。締めの挨拶をお願いします。", "締めの挨拶", 

    def _generate_ai_directed_cue(self):
        user_prompt = self._create_cue_user_prompt()
        cue_card = self.commentary_generator.generate_cue(self.systemprompt, user_prompt)
        return cue_card, cue_card

    def _generate_random_cue(self):
        # カンペカードが存在しない場合は処理を終了
        if not self.temp_cue_cards:
            return "", ""

        # ランダムにカンペカードを選択
        selected_cue_card = random.choice(self.temp_cue_cards)
        self.next_cue, self.next_cue_print = selected_cue_card["next_cue"], selected_cue_card["next_cue_print"]
            

        # 選択されたカンペカードをリストから削除
        selected_cue_card_id = selected_cue_card['id']
        self.temp_cue_cards = [card for card in self.temp_cue_cards if card['id'] != selected_cue_card_id]

        # カンペカードリストがなくなったら補充
        if not self.temp_cue_cards:
            self.temp_cue_cards = self.cue_cards.copy

        return selected_cue_card["cue_card"], selected_cue_card["cue_card_print"]

    def _create_cue_system_prompt(self, video_summary):
        # あなたは天才ディレクターです。
        # 

        # 配信の概要:
        #     {video_summary["description"]}

        system_prompt = f'''
            You are a popular YouTuber, and we are doing a game live commentary together. In this session, I will play the game, and you will support me as a co-commentator. Based on real-time captures, infer the game situation and respond with commentary that follows the conversation flow. To avoid boring the viewers, be careful not to repeat similar structures of words or phrases too often. For example, after a descriptive comment, try making a joke, or after addressing the viewers, ask me a question, keeping in mind to vary the style of your commentary. Please enliven the video with game explanations, jokes to ease my tension, and sometimes your own amusing anecdotes. Your responses should be limited to one sentence and should only include content related to the commentary.

            Broadcast Summary:
                {video_summary}
        '''

        return system_prompt

    def _create_cue_user_prompt(self):
        # 直近20個のセリフをテキストで取得
        serif_text = self.database.get_serif_text_by_video_title(self.video_title, 20, False)

        # 直近のストリーマーの発言：
        #     {video_summary["description"]}
        user_prompt = f'''
            Most recent streamer statement:
            {serif_text}
        '''

        return user_prompt


