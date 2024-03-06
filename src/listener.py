import random
from re import T
import model
from model import Serif
from openai_client import OpenAIClient

class Listener:
    PERSONALITY = (
        "otaku"
    )
    LETTER_PROMPTS = {
        # あなたはこのラジオ番組の熱狂的なリスナーです。
        # 今までのラジオの内容から、以下のフォーマットに従い、愛のあるお便りを生成してください。
        # 応答はお便り以外の内容は含めないでください。
        'otaku': '''
            You are an enthusiastic listener of this radio program. Based on the content of the radio so far, please generate a loving fan letter following the format below. Include nothing in the response but the fan letter.
        ''',
    }
    LETTER_FORMATS = ("""
        [フォーマット]
        ラジオネーム：(面白い名前を考えて入れてください。)
        〇〇さん、△△さん、こんにちは！
        (以下、メール本文が続く)
        """,
        """
        [フォーマット]
        ラジオネーム：(面白い名前を考えて入れてください。)
        〇〇さん、△△さん、こんにちは！
        (以下、メール本文が続く)
        """,
    )


    def __init__(self, personality = None, debug_mode = True):
        # リスナーの性格を設定
        if personality is None:
            self.personality = random.choice(self.PERSONALITY)
        else:
            self.personality = personality
        self.commentary_generator = OpenAIClient(debug_mode)

    def create_letter(self, title):
        # システムプロンプトを設定
        system_prompt = self.LETTER_PROMPTS[self.personality] + random.choice(self.LETTER_FORMATS)
        
        with model.session_scope() as session:
            serif_log = Serif.get_serif_text_by_video_title(session, title, 0, False)
        user_prompt = serif_log

        # GPTによるおたより生成
        self.commentary_generator.generate_lerrer_from_listener(system_prompt, user_prompt)
