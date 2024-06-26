from copy import deepcopy
import os
import random
from re import L
import re
from config import DATA_FOLDER
from model import CueSheet, ProgramType, Serif, StaticSection, SerifSystemPrompt, Video, VideoSection
from openai_client  import OpenAIClient 
import model
import story
import log
import api_utilities
from static_data import SERIF_SYSTEM_PROMPT_MAIN, Role

class Director():
    def __init__(self, title, debug_mode):
        self.ai_generator = OpenAIClient(debug_mode)
        self.title = title
        self.debug_mode = debug_mode
        self.news_titles = []
        self.words = []

    # 動画作成前にディレクターが準備する
    def prepare_for_streaming(self, video_data:Video, program_type:ProgramType, streamers):
        self.video_mode = program_type.video_mode
        self.story_genre = None
        if self.video_mode == "story":
            self.story_genre = story.select_genre()
        self.streamers = streamers
        self.host_serif_system_prompt2 = ""
        self.guest_serif_system_prompt2 = ""
        for streamer in streamers:
            with model.session_scope() as session:
                serif_system_prompt = session.query(SerifSystemPrompt).filter(SerifSystemPrompt.program_name == program_type.program_name).filter(SerifSystemPrompt.section_name == None).filter(SerifSystemPrompt.streamer_type == streamer.get_profile().role).first()
                print(f"serif_system_prompt={serif_system_prompt}")
                if serif_system_prompt == None:
                    continue
                serif_system_prompt = serif_system_prompt.text
                serif_system_prompt = serif_system_prompt.replace("[user_additional_data1]", video_data.user_additional_data1).replace("[user_additional_data2]", video_data.user_additional_data2)
                if streamer.get_profile().role == Role.DUO_VIDEO_HOST.value or streamer.get_profile().role == Role.SOLO_VIDEO_HOST.value:
                    self.host_serif_system_prompt2 = serif_system_prompt
                else:
                    self.guest_serif_system_prompt2 = serif_system_prompt
        if self.story_genre != None:
            self.host_serif_system_prompt2 += f"\n{story.get_genre_system_prompt(self.story_genre)}"

    # セクション開始時にディレクターが準備する
    def prepare_for_section(self, program_type:ProgramType, section:StaticSection):
        host_serif_system_prompt1, guest_serif_system_prompt1= self._replace_main_serif_system_prompt(program_type, section, SERIF_SYSTEM_PROMPT_MAIN)
        
        self.host_main_serif_system_prompts = [host_serif_system_prompt1, self.host_serif_system_prompt2]
        self.guest_main_serif_system_prompts = [guest_serif_system_prompt1, self.guest_serif_system_prompt2]

    def _replace_main_serif_system_prompt(self, program_type:ProgramType, section:StaticSection, serif_system_prompt: str):
        def speaking_duration_text(duration):
            if duration == 0:
                return ""
            return f"Respond in Japanese within {duration} characters."
        
        host_speaking_duration = speaking_duration_text(section.host_speaking_duration)
        host_serif_system_prompt = serif_system_prompt.replace("[program_name]", program_type.program_name).replace("[program_summary]", program_type.program_summary).replace("[section_name]", section.section_name).replace("[speaking_duration]", host_speaking_duration)
        guest_speaking_duration = speaking_duration_text(section.guest_speaking_duration)
        guest_serif_system_prompt = serif_system_prompt.replace("[program_name]", program_type.program_name).replace("[program_summary]", program_type.program_summary).replace("[section_name]", section.section_name).replace("[speaking_duration]", guest_speaking_duration)
        return host_serif_system_prompt, guest_serif_system_prompt
    
    def create_direction(self, section, loop_counter, current_time, streamer_index):
        # システムプロンプトを生成
        system_prompts = self._create_serif_system_prompt(section, streamer_index)

        # カンペを生成
        cue_card = self._create_cue_card(section, loop_counter, streamer_index)

        # 終了条件をチェック
        end_flag = self._check_end_condition(section, loop_counter, current_time)

        return system_prompts, cue_card, end_flag

    def _create_serif_system_prompt(self, section:StaticSection, streamer_index):
        system_prompts = []
        if streamer_index == Role.SOLO_VIDEO_HOST.value or streamer_index == Role.DUO_VIDEO_HOST.value:
            system_prompts = system_prompts + self.host_main_serif_system_prompts
        else:
            system_prompts = system_prompts + self.guest_main_serif_system_prompts
        # システムプロンプトをデータベースから取得
        with model.session_scope() as session:
            serif_system_prompt = session.query(SerifSystemPrompt).filter(SerifSystemPrompt.program_name == section.program_name).filter(SerifSystemPrompt.section_name == section.section_name).filter(SerifSystemPrompt.streamer_type == streamer_index).first()
            if serif_system_prompt == None:
                return system_prompts
            system_prompts.append(serif_system_prompt.text)
            return system_prompts

    def _create_cue_card(self, section:StaticSection, counter, streamer_index):
        with model.session_scope() as session:
            cue_sheets = deepcopy(session.query(CueSheet).filter(CueSheet.program_name == section.program_name).filter(CueSheet.section_name == section.section_name).filter(CueSheet.streamer_type == streamer_index).all())

        if streamer_index == Role.DUO_VIDEO_HOST.value or streamer_index == Role.DUO_VIDEO_GUEST.value:
            for cue_sheet in cue_sheets:
                # ランダム配信の場合、または指定されたカウンタに基づいて適切なdelivery_sequenceを持つcue_sheetを選択
                if cue_sheet.delivery_sequence == 0 or cue_sheet.delivery_sequence == (counter // 2) + 1:
                    temp_cue_sheet = cue_sheet
                    break  # 適切なcue_sheetが見つかったのでループを終了
            else:
                # ループがアイテムを見つけずに完了した場合（temp_cue_sheetがセットされなかった場合）
                return ""
            
            if temp_cue_sheet.is_ai:
                # AIディレクターがカンペを生成
                cue_card = self._generate_ai_directed_cue(temp_cue_sheet.cue_text, section)
            else:
                # そのままのカンペを使用
                cue_card = temp_cue_sheet.cue_text
        else: # ソロの場合
            for cue_sheet in cue_sheets:
                # ランダム配信の場合、または指定されたカウンタに基づいて適切なdelivery_sequenceを持つcue_sheetを選択
                if cue_sheet.delivery_sequence == 0 or cue_sheet.delivery_sequence == counter + 1:
                    temp_cue_sheet = cue_sheet
                    break
            else:
                temp_cue_sheet = None

            # カンペの中を置き換える
            if self.video_mode == "story":
                output_num = section.end_condition_value if section.end_condition_type == 0 else None
                cue_card = self._get_story_cue(section.section_name, temp_cue_sheet, counter, output_num)
            elif self.video_mode == "game":
                cue_card = self._get_game_cue(temp_cue_sheet)
            elif self.video_mode == "talk":
                pass
            else:
                pass

        return cue_card
         
    def _get_story_cue(self, section_name, temp_cue_sheet: CueSheet, counter, output_num):
        if temp_cue_sheet == None:
            return story.get_story_cue(self.story_genre, section_name, counter, output_num)
        else:
            temp_cue_sheet.cue_text.replace("[cue]", story.get_story_cue(self.story_genre, section_name, counter, output_num))
            return temp_cue_sheet.cue_text
        
    def _get_game_cue(self, temp_cue_sheet):
        pass

    def _generate_ai_directed_cue(self, system_prompt, section:StaticSection):
        # 今までの会話をデータベースから取り出す
        user_prompt = self._create_cue_user_prompt(section)
        # AIディレクターがカンペを生成
        cue_card = self.ai_generator.generate_cue(system_prompt, user_prompt)
        return cue_card
        
    def _create_cue_user_prompt(self, section:StaticSection):
        # 直近20個のセリフをテキストで取得
        with model.session_scope() as session:
            serif_text = Serif.get_serif_text_by_video_title(session, f"{self.title}_{section.order}", 20, False)

        # 直近のストリーマーの発言：
        user_prompt = f'''
            Most recent streamer statement:
            {serif_text}
        '''

        return user_prompt

    def _check_end_condition(self, section:StaticSection, loop_counter, current_time):
        if section.end_condition_type == 0:
            if current_time > section.end_condition_value:
                return True
        elif section.end_condition_type == 1:
            if loop_counter + 1 == section.end_condition_value:
                return True
        return False
    
    # 背景画像を生成し、そのパスを返す  
    def create_background_image(self, section:StaticSection, output_path, image_title, video_data:Video):
        if section.background_image_type == 0:
            # 生成するプロンプトを取得
            background_image_prompt = self._create_background_image_prompt(section, video_data)
            log.show_message(f"background_image_prompt={background_image_prompt}", newline=True)
            # AIで背景画像を生成
            return self.ai_generator.generate_background_image(background_image_prompt, output_path, image_title)
        elif section.background_image_type == 3:
            return section.background_image_prompt
        else:
            if section.background_image_type == 1:
                order = section.order - 1
            elif section.background_image_type == 2:
                order = section.background_image_order_num
            return self._get_previous_background_image(order)

    def _create_background_image_prompt(self, section:StaticSection, video_data:Video):
        if section.background_image_prompt == "USE_SECTION_SERIF":
            # セクションのセリフを取得
            with model.session_scope() as session:
                background_image_prompt = "以下から背景画像を生成してください。\n\n"
                background_image_prompt += Serif.get_serif_text_by_section(session, self.title, section.section_name, 0, False, False)
        else:
            # システムプロンプトをデータベースから取得
            background_image_prompt = section.background_image_prompt.replace("[user_additional_data1]", video_data.user_additional_data1).replace("[user_additional_data2]", video_data.user_additional_data2)
        return background_image_prompt
    
    def _get_previous_background_image(self, order):
        with model.session_scope() as session:
            previous_video = session.query(VideoSection).filter(VideoSection.video_title == self.title).filter(VideoSection.order == order).first()
            background_image_path = previous_video.background_image_path
        return background_image_path

    def select_background_music(self, section:StaticSection):
        if section.background_music_type == 0:
            return section.background_music_path
        elif section.background_music_type == 1:
            return self._get_random_music()
        elif section.background_music_type == 2:
            order = section.order - 1
        elif section.background_music_type == 3:
            order = int(section.background_music_path)
        else:
            return None
        return self._get_previous_background_music(order)

    def _get_random_music(self):
        folder_names = [name for name in os.listdir(DATA_FOLDER + "/BGM") if os.path.isdir(os.path.join(DATA_FOLDER + "/BGM", name))]
        return random.choice(folder_names)
    
    def _get_previous_background_music(self, order):
        with model.session_scope() as session:
            previous_video = session.query(VideoSection).filter(VideoSection.video_title == self.title).filter(VideoSection.order == order).first()
            background_music_path = previous_video.background_music_path
        return background_music_path

    def create_talk_theme(self, output_path, image_title):
        # AIでトークテーマを生成
        talk_theme = self._generate_ai_talk_theme()

        # トークテーマから背景画像を生成
        talk_theme['background_image_url'] = self.ai_generator.generate_background_image(talk_theme['theme'], output_path, image_title)

        return talk_theme

    def _generate_ai_talk_theme(self):
        talk_theme = {}
        system_prompt, user_prompt = self._create_talk_theme_prompt()
        talk_theme['theme'] = self.ai_generator.generate_talk_theme(system_prompt, user_prompt)
        talk_theme['theme_jp'] = talk_theme['theme']
        return talk_theme

    def _create_talk_theme_prompt(self):
        if self.debug_mode == True:
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

        log.show_message(f"news_titles_len={len(self.news_titles)}, random_news={random_news}, random_word={random_word}", newline=True)

        # ランダムに与えられたニュースと単語を使用して、日本語で20文字程度のラジオのトークテーマを作成してください。
        system_prompt = f'''
            Please create a radio talk theme in Japanese, about 20 characters long, using randomly given news and words. Avoid names of living persons. Make it a general theme that is easy to talk about.
        '''
        user_prompt = f'''
            news: {random_news}
            word: {random_word}
        '''
        return system_prompt, user_prompt
    
    def create_summary(self, output_path, title):
        # AIでトークテーマを生成
        summary = self._generate_ai_summary(title)

        # トークテーマから背景画像を生成
        summary['background_image_url'] = self.ai_generator.generate_background_image(summary['theme'], output_path, title)

        return summary

    def _generate_ai_summary(self, title):
        # 今までのトークを取得
        serif_texts = []
        for i in range(1):
            with model.session_scope() as session:
                serif_texts.append(Serif.get_serif_text_by_video_title(session, title + f"_{i}", 0, False))
        summary = {}
        summary['theme'] = self.ai_generator.generate_radio_summary(serif_texts)
        summary['theme_jp'] = '今日のまとめ'
        return summary
    
    def create_capture_description(self, game_video_capture_path, current_time, descriptions):
        # AIでキャプチャの説明を生成
        system_prompt = self._create_capture_description_prompt(current_time, descriptions)
        capture_description = self.ai_generator.generate_capture_description(system_prompt, game_video_capture_path)
        return capture_description
    
    def _create_capture_description_prompt(self, current_time, descriptions):
        # 今までのキャプチャの説明を取得
        user_prompt = f'''
            Most recent capture description:
            {descriptions}
        '''
        system_prompt = f'''
            Please create a description of the capture, about 20 characters long, using the given time and the previous capture description. 
        '''
        return system_prompt, user_prompt