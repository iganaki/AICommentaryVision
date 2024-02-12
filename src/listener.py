import openai

from openai_client import OpenAIClient

class Listener:
    LETTER_PROMPTS = {
        # あなたはこのラジオ番組の熱狂的なリスナーです。
        # 
        '': '''
            
        ''',
    }
    LETTER_FORMATS = """
    以下のフォーマットに従って返答してください。

    ラジオネーム：{name}
    〇〇さん、△△さん、こんにちは！
    (以下、メール本文が続く)
"""
    def __init__(self, personality):
        # リスナーの性格を設定
        self.personality = personality
        self.commentary_generator = OpenAIClient()

    def create_letter(self):
        # システムプロンプトを設定
        system_prompt = self.LETTER_PROMPTS[self.personality]

        user_prompt = 

        # GPTによるおたより生成
        self.commentary_generator.generate_lerrer_from_listener(system_prompt, user_prompt)
