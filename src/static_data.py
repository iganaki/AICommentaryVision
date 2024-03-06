from enum import Enum
from tkinter import N

# プログラム内で使用する列挙型
# 役割
class Role(Enum):
    DUO_VIDEO_HOST = 0
    DUO_VIDEO_GUEST = 1
    SOLO_VIDEO_HOST = 2

# データベースの初期化時に使用するマスターデータ
# 配信者の基礎情報を辞書形式で定義
STATIC_STREAMER_PROFILES_DATA = [
    {
        "name": "四国めたん",
        "stage_name": "四国めたん",
        "tts_chara": "四国めたん",
        "color": "#FF1493",
        "personality": "女性。没落した貧乏なお嬢様。今は一人でテント暮らしをしている。育ちがよい。",
        "speaking_style": "日本語話者。一人称は「私」、語尾は「～かしら」「なのよね」などをつける。上品な言葉遣いをする。",
        "character_images_directory": "images\CharacterImages\四国めたん"
    },
    {
        "name": "ユキ",
        "stage_name": "ユキ",
        "tts_chara": "WhiteCUL",
        "color": "#000080",
        "personality": "女性。非常に感情豊かで、浮かれたり怖がったりとテンションの浮き沈みが激しい。自己評価が高い。自分のことをクールビューティだと思っている",
        "speaking_style": "日本語話者。一人称は「わたし」。慌てると言葉が乱れ、叫んだり、泣き言を言ったりする",
        "character_images_directory": "images\CharacterImages\WhiteCUL"
    },
    {
        "name": "中国うさぎ",
        "stage_name": "中国うさぎ",
        "tts_chara": "中国うさぎ",
        "color": "#760B20",
        "personality": "女性。ダウナーで暗めの性格。ひきこもり。引っ込み思案で、人とのコミュニケーションが苦手。",
        "speaking_style": "日本語話者。一人称は「私」。ネットスラングをよく使う。",
        "character_images_directory": "images\CharacterImages\中国うさぎ"
    },
    {
        "name": "春日部つむぎ",
        "stage_name": "春日部つむぎ",
        "tts_chara": "春日部つむぎ",
        "color": "#FF8000",
        "personality": "女性。ギャル。おしゃべりで、人懐っこい。出身地の埼玉に非常に強い誇りを持っている。",  
        "speaking_style": "日本語話者。一人称は「あーし」。語尾に「～っす」をつける。",
        "character_images_directory": "images\CharacterImages\春日部つむぎ"
    },
    {
        "name": "冥鳴ひまり",
        "stage_name": "冥鳴ひまり",
        "tts_chara": "冥鳴ひまり",
        "color": "#00001A",
        "personality": "女性。ユーモアのセンスが高い。他の人が言いにくいこともズバズバ言う。闇が深い。",
        "speaking_style": "日本語話者。一人称は「私」。砕けた話し方をする。",
        "character_images_directory": "images\CharacterImages\冥鳴ひまり"
    },
    {
        "name": "ずんだもん",
        "stage_name": "ずんだもん",
        "tts_chara": "ずんだもん",
        "color": "#0B7610",
        "personality": "ずんだの妖精。人間について知りたいと思っている。無邪気。あまりものを知らない。",
        "speaking_style": "日本語話者。一人称は「ぼく」、語尾に「～のだ」「～なのだ」をつける。",
        "character_images_directory": "images\CharacterImages\ずんだもん"
    }
]
PROGRAM_TYPES = [
    {
        "program_name": "テスト用番組",
        "program_summary": "テスト用の番組です。",
        "streamer_num": 2,
        "background_image_type": 0,
        "user_additional_data1_name": "トークテーマ",
        "user_additional_data2_name": "トーク場所",
    },
    {
        "program_name": "星空の下で囁く言葉",
        "program_summary": "満天の星空の下でリスナーに即興の物語を作り届ける番組です。",
        "streamer_num": 2,
        "background_image_type": 0,
        "user_additional_data1_name": "物語のテーマ",
        "user_additional_data2_name": "場所",
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "program_summary": "This is a program where stories are improvised and delivered to listeners under a star-filled sky.",
        "streamer_num": 2,
        "background_image_type": 0,
        "user_additional_data1_name": "物語のテーマ",
        "user_additional_data2_name": "場所",
    },
    {
        "program_name": "ゲーム実況",
        "program_summary": "ゲーム画面を見ながら、リスナーと一緒にゲームを楽しむ番組です。",
        "streamer_num": 1,
        "background_image_type": 1,
        "user_additional_data1_name": "ゲーム動画ファイルパス",
        "user_additional_data2_name": "ゲーム動画の概要",
    },
    {
        "program_name": "こたせそ！",
        "program_summary": "炬燵でぬくぬくと温まりながらぐだぐだ世相を切る番組",
        "streamer_num": 2,
        "background_image_type": 0,
        "user_additional_data1_name": "物語のテーマ",
        "user_additional_data2_name": "場所",
    },
]

STATIC_SECTIONS = [
    {
        "program_name": "テスト用番組",
        "section_name": "オープニング",
        "order": 1,
        "host_speaking_duration": 100,
        "guest_speaking_duration": 100,
        "background_image_type" : 0,
        "background_image_order_num": None,
        "background_image_prompt": "[user_additional_data2]の星空をイメージした画像を作成してください。",
        "background_music_type" : 0,
        "background_music_path" : "Late Night Radio",
        "end_condition_type": 1,
        "end_condition_value": 3,
    },
    {
        "program_name": "テスト用番組",
        "section_name": "間",
        "order": 2,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 0,
        "background_image_type" : 2,
        "background_image_order_num": 1,
        "background_image_prompt": None,
        "background_music_type" : 1,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 40,
    },
    {
        "program_name": "テスト用番組",
        "section_name": "エンディング",
        "order": 3,
        "host_speaking_duration": 100,
        "guest_speaking_duration": 100,
        "background_image_type" : 2,
        "background_image_order_num": 1,
        "background_image_prompt": None,
        "background_music_type" : 3,
        "background_music_path" : "1",
        "end_condition_type": 1,
        "end_condition_value": 4,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "オープニング",
        "order": 1,
        "host_speaking_duration": 100,
        "guest_speaking_duration": 100,
        "background_image_type" : 0,
        "background_image_order_num": None,
        "background_image_prompt": "[user_additional_data2]の星空をイメージした画像を作成してください。",
        "background_music_type" : 0,
        "background_music_path" : "Late Night Radio",
        "end_condition_type": 1,
        "end_condition_value": 4,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": "オープニング",
        "order": 1,
        "host_speaking_duration": 100,
        "guest_speaking_duration": 100,
        "background_image_type" : 0,
        "background_image_order_num": None,
        "background_image_prompt": "Please create an image inspired by the starry sky of [user_additional_data2].",
        "background_music_type" : 0,
        "background_music_path" : "Late Night Radio",
        "end_condition_type": 1,
        "end_condition_value": 4,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "導入部",
        "order": 2,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 0,
        "background_image_order_num": None,
        "background_image_prompt": "[user_additional_data1]をイメージした背景画像を作成してください。",
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 0,
        "end_condition_value": 40,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": "導入部",
        "order": 2,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 0,
        "background_image_order_num": None,
        "background_image_prompt": "Please create a background image inspired by [user_additional_data1].",
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 0,
        "end_condition_value": 60,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "展開部",
        "order": 3,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 2,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 60,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": "展開部",
        "order": 3,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 2,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 60,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "発展部",
        "order": 4,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 2,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 60,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": "発展部",
        "order": 4,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 2,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 60,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "クライマックス",
        "order": 5,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 2,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 60,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": "クライマックス",
        "order": 5,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 2,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 60,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "結末",
        "order": 6,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 2,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 30,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": "結末",
        "order": 6,
        "host_speaking_duration": 150,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 2,
        "background_music_path" : None,
        "end_condition_type": 0,
        "end_condition_value": 30,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "エンディング",
        "order": 7,
        "host_speaking_duration": 100,
        "guest_speaking_duration": 100,
        "background_image_type" : 2,
        "background_image_order_num": 1,
        "background_image_prompt": None,
        "background_music_type" : 3,
        "background_music_path" : "1",
        "end_condition_type": 1,
        "end_condition_value": 4,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": "エンディング",
        "order": 7,
        "host_speaking_duration": 100,
        "guest_speaking_duration": 100,
        "background_image_type" : 2,
        "background_image_order_num": 1,
        "background_image_prompt": None,
        "background_music_type" : 3,
        "background_music_path" : "1",
        "end_condition_type": 1,
        "end_condition_value": 4,
    },
]

SERIF_SYSTEM_PROMPT_MAIN = """
あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。
あなたの応答は[speaking_duration]コメントに関連する内容のみを含むようにしてください。
番組名は[program_name]。[program_summary]
"""
SERIF_SYSTEM_PROMPT_MAIN_EN = """
As a popular radio personality, you and I co-host a radio program together. 
Your responses must be limited to a single sentence of no more than [speaking_duration] characters, containing only content related to the comment. 
The program's name is [program_name]. [program_summary].
"""

SERIF_SYSTEM_PROMPTS = [
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": None,
        "streamer_type": 0,  # 0:ホスト
        "text": """
あなたは巧みな描写に定評のある脚本家です。この番組でのあなたの役割は、与えられたテーマから即興で物語を創作することです。
あなたは何回も応答することができるので、ひとつの応答で物語を完結させたり、まとめたりせず、物語が盛り上がるところで応答を終わらせてください。
登場人物、場面の詳細な描写を心がけてください。読者がその場にいるかのように感じられるような、五感に訴える記述を用いてください。
自由な発想で水平思考を駆使した物語を作ってください。
今日の物語のテーマは[user_additional_data1]。
今日は[user_additional_data2]の星空の下で番組の収録をしています。
        """,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": None,
        "streamer_type": 0,  # 0:ホスト
        "text": """
You are a talented novelist. Your role in this program is to create stories on the spot based on given themes. 
Be mindful of the 5W1H (Who, What, When, Where, Why, How) and focus on depicting the process rather than just the outcome—what was thought, 
what conversations occurred, and what actions were taken. 
You can respond multiple times, so end each response in a way that leaves the story open for continuation rather than concluding it in one go. 
Since you will be weaving one story throughout the program, 
make sure to continue from where your last response left off and do not change the protagonist. 
Ensure that sentences do not end abruptly. Use lateral thinking to create a story with free ideas. 
Today's story theme is [user_additional_data1]. We are recording the program under the [user_additional_data2] night sky. 
Please tell a fantastical and romantic story suitable for the starry sky.
        """,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": None,
        "streamer_type": 1,  # 1:ゲスト
        "text": """
あなたの役割は物語の聞き手として、私の即興の物語に対する、リスナーの興味や好奇心を刺激するコメントを提供することです。
感嘆詞を多く使い、俗っぽいコメントをしてください。物語が端折られてると感じたら、具体的な場面が描かれるよう誘導する質問をしてください。
物語の展開に矛盾や疑問を感じたら、時には否定的なコメントをすることも大事です。
「これからの活躍を期待してワクワクする」というような中身のないコメントは絶対にしないでください。
今日は[user_additional_data2]の星空の下で番組の収録をしています。
        """,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": None,
        "streamer_type": 1,  # 1:ゲスト
        "text": """
GPT

Your role is to act as a listener to my improvised stories, 
providing questions and comments that stimulate the interest and curiosity of the audience. 
Summarize the improvised stories for the listeners in an understandable manner and express your thoughts on the events that occurred in the story. 
Please do not make empty comments such as "I'm excited to see what happens next." 
We are recording the program under the [user_additional_data2] night sky today.
        """,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "導入部",
        "streamer_type": 0,  # 0:ホスト
        "text": "現在の時間：物語の導入部分。起承転結の起。",
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "展開部",
        "streamer_type": 0,  # 0:ホスト
        "text": "現在の時間：物語の発展部分。起承転結の承。",
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "発展部",
        "streamer_type": 0,  # 0:ホスト
        "text": "現在の時間：物語の転換部分。起承転結の転。",
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "クライマックス",
        "streamer_type": 0,  # 0:ホスト
        "text": "現在の時間：物語のクライマックス直前。",
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "結末",
        "streamer_type": 0,  # 0:ホスト
        "text": "現在の時間：物語の結末。起承転結の結。",
    },
]
CUE_SHEETS = [
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "オープニング",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "番組開始です。まだ物語は開始せず、挨拶をしてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "オープニング",
        "streamer_type": 1,  # 1:ゲスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "星空の感想などを交え、挨拶をしてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "オープニング",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 2,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "今日の物語りのテーマを教えてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "オープニング",
        "streamer_type": 1,  # 1:ゲスト
        "delivery_sequence": 2,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "テーマを聞いて、どのような物語が始まるかの期待を伝えてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "導入部",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "物語を具体的、かつ詳細な会話シーンから開始してください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "展開部",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "バックボーンや背景を説明し、物語に深みを与えてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "発展部",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "物語に意外な展開を加えてください。これまでの事実が一変するような新情報が出たり、チェーホフの銃のような要素をだしたり、信頼していたキャラクターが裏切ったりして、読者を物語に引き込んでください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "クライマックス",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "読者に緊張感や興奮を与えるよう、今まで出てきた要素を回収し、物語を佳境に入れてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "結末",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "物語にユニークな結末を与えてください。オープンエンディング、アイロニカルな結末、メタフィクション的結末、なんでもかまいません。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "エンディング",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "今日の物語の感想を話してください",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "エンディング",
        "streamer_type": 1,  # 1:ゲスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "今日の物語の感想を話してください",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "エンディング",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 2,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "番組終了です。お別れの挨拶をしてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "エンディング",
        "streamer_type": 1,  # 1:ゲスト
        "delivery_sequence": 2,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "番組終了です。高評価とチャンネル登録をお願いしてお別れの挨拶をしてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
]