from calendar import c
import random
from abc import ABC, abstractmethod
from config import AI_DIRECTOR_MODE, MAX_EXTRA_ROUNDS, RADIO_THEME_TALK_NUM
from database import Database
from static_data import Mode, Role
from openai_client  import OpenAIClient 

def create_director_instance(mode, *args, **kwargs):
    """
    GameStreamDirector または RadioDirector のインスタンスを作成する。

    :param mode: class Mode(Enum)のいずれかを指定。
    :param args: コンストラクタに渡す引数。
    :param kwargs: コンストラクタに渡すキーワード引数。
    :return: 指定されたタイプの Director インスタンス。
    """
    if mode == Mode.SOLO_GAMEPLAY.value or mode == Mode.DUO_GAMEPLAY.value:
        return GameStreamDirector(*args, **kwargs)
    elif mode == Mode.DUO_RADIO.value:
        return RadioDirector(*args, **kwargs)
    else:
        raise ValueError("Invalid mode")

class Director(ABC):
    def __init__(self):
        super().__init__()
        # コメンタリージェネレータの初期化
        self.commentary_generator = OpenAIClient()

    # 動画作成前にディレクターが準備する
    def prepare_for_streaming(self, streamers, database:Database):
        self.streamers = streamers
        self.cue_interval = random.randint(8, 12)
        self.next_cue, self.next_cue_print = "", ""
        self.database = database
        self.continue_counter = 3
        if AI_DIRECTOR_MODE == True:
            self.systemprompt = self._create_cue_system_prompt()
        else:
            self.cue_cards = self.database.fetch_all_cue_cards()
            self.temp_cue_cards = self.cue_cards

    def create_cue_card(self, extra_rounds, counter, streamer_index, start_flag, end_flag):
        cue_card, cue_card_print = "", ""
        self.current_streamer = self.streamers[streamer_index]
        if self.streamers[streamer_index].get_profile()["role"] != Role.SOLO_PLAYER.value:
            self.partner_streamer = self.streamers[1-streamer_index]
        
        if self.cue_interval > 0:
            self.cue_interval -= 1

        # 最初の一言目のカンペを出す
        cue_card, cue_card_print = self._generate_starting_cue(start_flag, counter)

        # 動画終了時のカンペを出す。
        if extra_rounds < MAX_EXTRA_ROUNDS and cue_card == "":
            cue_card, cue_card_print = self._generate_ending_cue(end_flag, extra_rounds)
        
        # 連続したカンペがある場合、出す。
        if self.next_cue != "" and cue_card == "":
            cue_card, cue_card_print = self.next_cue, self.next_cue_print
            self.next_cue, self.next_cue_print = "", ""

        # カンペを出す。
        if self.cue_interval == 0 and cue_card == "":
            if AI_DIRECTOR_MODE == True:
                # AIディレクターがカンペを出す
                cue_card, cue_card_print = self._generate_ai_directed_cue()
            else:
                # ランダムディレクターがカンペを出す。
                cue_card, cue_card_print = self._generate_random_cue()
            
            self.current_cue, self.current_cue_print = cue_card, cue_card_print
            self.cue_interval = random.randint(8, 14)
            self.continue_counter = 0

        # カンペを継続して出す
        if AI_DIRECTOR_MODE == True:
            if self.continue_counter == 0:
                self.continue_counter += 1
            elif self.continue_counter < 3:
                cue_card, cue_card_print = f"(the instructions mentioned in the statement {self.continue_counter} items back)"+self.current_cue, self.current_cue_print
                self.continue_counter += 1

        return cue_card, cue_card_print
    
    @abstractmethod
    def _generate_starting_cue(self):
        pass

    @abstractmethod
    def _generate_ending_cue(self, extra_rounds):
        pass
         
    def _generate_ai_directed_cue(self):
        # 今までの会話をデータベースから取り出す
        user_prompt = self._create_cue_user_prompt()
        # AIディレクターがカンペを生成
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

    @abstractmethod
    def _create_cue_system_prompt(self):
        pass

    @abstractmethod
    def _create_cue_user_prompt(self):
        pass
        
    
class GameStreamDirector(Director):
    def prepare_for_gameStream(self, video_title, video_summary):
        self.title = video_title
        self.video_summary = video_summary

    def _generate_starting_cue(self, start_flag, counter):
        if counter == 0:
            return "開始しました、自分の名前をもじった挨拶から実況を始めてください", "挨拶して"
        elif counter == 1:
            return "今日プレイするのはどんなゲームか相方に質問してください", "ゲームについて聞いて"
        elif counter == 2:
            return "視聴者にも伝わるよう質問に回答してください", "答えて"
        return "", ""

    def _create_cue_system_prompt(self):
        # 後で考える

        system_prompt = f'''
            後で考える
       '''

        return system_prompt
    
    def _create_cue_user_prompt(self):
        # 直近20個のセリフをテキストで取得
        serif_text = self.database.get_serif_text_by_video_title(self.title, 20, False)

        # 直近のストリーマーの発言：
        user_prompt = f'''
            Most recent streamer statement:
            {serif_text}
        '''

        return user_prompt
    
class RadioDirector(Director):
    def prepare_for_radio_part(self, index, radio_title, radio_theme):
        self.radio_part_index = index
        self.title = radio_title
        self.radio_theme = radio_theme

    def _generate_starting_cue(self, start_flag, counter):
        if start_flag == True:
            return self._radio_start_cue(counter)
        else:
            return self._radio_after_the_commercial_cue(counter) 

    def _radio_start_cue(self, counter):
        if counter == 0:
            return "ラジオ開始です。挨拶してください", "挨拶して"
        elif counter == 1:
            return "トークテーマを視聴者に伝えて", "今日のテーマ"
        elif counter == 2:
            return "トークテーマに耳なじみのない単語があったら、解説・質問などしてください", "感想"
        return "", ""

    def _radio_after_the_commercial_cue(self, counter):
        if counter == 0:
            return "CM明けです。挨拶してください", "挨拶して"
        elif counter == 1:
            return "次のトークテーマを視聴者に伝えて", "今日のテーマ"
        elif counter == 2:
            return "トークテーマに耳なじみのない単語があったら、解説・質問などしてください", "感想"
        return "", ""

    def _generate_ending_cue(self, end_flag, extra_rounds):
        if end_flag == True:
            return self._radio_end_cue(extra_rounds)
        else:
            return self._radio_before_the_commercial_cue(extra_rounds)

    def _radio_end_cue(self, extra_rounds):
        if extra_rounds == 2:
            return "ラジオ終了です。まとめに入ってください。", "まとめ"
        if extra_rounds == 1:
            return "ラジオ終了です。締めの挨拶をお願いします。", "締めの挨拶"
        elif extra_rounds == 0:
            return "ラジオ最後の一言です。「いいね」と「高評価」を視聴者にお願いしてください", "締めの挨拶"

    def _radio_before_the_commercial_cue(self, extra_rounds):
        if extra_rounds == 2:
            return "このトークテーマがそろそろ終わります。次のテーマに行く前に、まとめに入ってください。", "まとめ"
        if extra_rounds == 1:
            return "まとめを受けた感想を話してください。", "締めの挨拶"
        elif extra_rounds == 0:
            return "CMに入ります。", "締めの挨拶"

    def _create_cue_system_prompt(self):
        # あなたはラジオの天才ディレクターです。
        # 刺激的で面白いラジオを作るために、次の発言者に見せるカンペを考えてください。
        # 話題を変えるために演者に質問したり、面白くなりそうな話題を広げるよう促したりしてください。
        # 返答がそのままカンペとして演者に見せられます。指示のみを40文字以内で簡潔に、演者が理解しやすいように返答してください。

        system_prompt = f'''
            You are a genius radio director. For creating an exciting and engaging radio show, think of cue cards to show the next speaker. Prompt questions to change the subject or to expand on topics that could become interesting. Your responses will be directly shown to the performer as cue cards. Please reply with instructions only, concisely within 40 characters, so that it's easy for the performer to understand.
       '''
        return system_prompt
    
    def _create_cue_user_prompt(self):
        # 直近20個のセリフをテキストで取得
        serif_text = self.database.get_serif_text_by_video_title(self.title, 20, False)

        # 直近のストリーマーの発言：
        user_prompt = f'''
            current theme: {self.radio_theme}
            Most recent streamer statement:
            {serif_text}
        '''
        return user_prompt
    
    def create_talk_theme(self, output_path, image_title):
        if  AI_DIRECTOR_MODE is True:
            # AIでトークテーマを生成
            talk_theme = self._generate_ai_talk_theme()
        else:
            # ランダムでデータベースからトークテーマを取得
            talk_theme = self._generate_random_talk_theme()

        # トークテーマから背景画像を生成
        talk_theme['background_image_url'] = self.commentary_generator.generate_background_image(talk_theme['theme'], output_path, image_title)

        return talk_theme

    def _generate_random_talk_theme(self):
        # トークテーマをデータベースから取得
        all_talk_themes = self.database.fetch_all_talk_themes()
        selected_talk_theme = random.choice(all_talk_themes)
        return selected_talk_theme

    def _generate_ai_talk_theme(self):
        talk_theme = {}
        talk_theme['theme'] = self.commentary_generator.generate_talk_theme()
        talk_theme['theme_jp'] = talk_theme['theme']
        return talk_theme

    def create_summary(self, output_path, title):
        if  AI_DIRECTOR_MODE is True:
            # AIでトークテーマを生成
            summary = self._generate_ai_summary(title)
        else:
            return None

        # トークテーマから背景画像を生成
        summary['background_image_url'] = self.commentary_generator.generate_background_image(summary['theme'], output_path, title)

        return summary

    def _generate_ai_summary(self, title):
        # 今までのトークを取得
        serif_texts = []
        for i in range(RADIO_THEME_TALK_NUM - 1):
            serif_texts.append(self.database.get_serif_text_by_video_title(title + f"_{i}", 0, False))
        summary = {}
        summary['theme'] = self.commentary_generator.generate_radio_summary(serif_texts)
        summary['theme_jp'] = '今日のまとめ'
        return summary
    