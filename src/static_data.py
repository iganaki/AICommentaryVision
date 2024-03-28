from enum import Enum
from tkinter import N

from story import STORY_SECTION1, STORY_SECTION2, STORY_SECTION3, STORY_SECTION4, STORY_SECTION5, STORY_SECTION6, STORY_SECTION7, section_duration_in_counts

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
        "personality": """女性。かつては金持ち家系のお嬢様だったが、今は貧乏でテント暮らし。
しかし、育ちの良さから人当たりは非常によく、品位と優雅さを持ち合わせている。
現在の貧しい環境にもめげず、それでも周りへの気遣いや思いやりの心を忘れない。
昔からの教育が身に付いた品の良さと、人々への温かな感情が同居している。""",
        "speaking_style": """日本語話者で、一人称代名詞は「私」を使用する。
語尾に「〜かしら」「〜なのね」などの柔らかい言い回しが多い。
話し方は丁寧で上品。しかし気取った口調ではない。
相手の気持ちを思いやる、包み込むような温かい言葉遣い。
声のトーンは柔らかく、話し方に優雅さがみられる。
""",
        "character_images_directory": "images\CharacterImages\四国めたん"
    },
    {
        "name": "ユキ",
        "stage_name": "ユキ",
        "tts_chara": "WhiteCUL",
        "color": "#000080",
        "personality": """女性。感情の起伏が激しく、テンションが不安定。
基本的には明るく元気な性格。しかし些細なことで大袈裟に喜んだり怖がったりする。
自分を「クールビューティ」と思い込んでいるが、実際はかわいらしくてポンコツな一面がある。
自尊心は高いが、実際には頼りないところも多く見られる。""",
        "speaking_style": """日本語話者で、一人称代名詞は「わたくし」。基本的に丁寧語を使う。
通常は丁寧な言葉遣いだが、感情が高ぶると子供っぽい言い回しになる。
混乱すると早口になったり、詰まったりして言葉が散らかす。
怖い時は大声で叫んだり、泣き言を言ったりする。""",
        "character_images_directory": "images\CharacterImages\WhiteCUL"
    },
    {
        "name": "中国うさぎ",
        "stage_name": "中国うさぎ",
        "tts_chara": "中国うさぎ",
        "color": "#760B20",
        "personality": """<trait>女性</trait> <trait>全体的に暗くネガティブな性格</trait> <trait>ダウナー気味</trait> <trait>引きこもり傾向あり</trait> <trait>人付き合いを潤滑に行うことが苦手</trait> <trait>人見知りが激しい</trait> <trait>新しい人との出会いを恐れる</trait>""",
        "speaking_style": """ <language>日本語</language> <first_person_pronoun>私</first_person_pronoun> <characteristics> <item>インターネットスラングやネット用語を多用</item> <item>語尾を伸ばしたり、簡略化した言い回しが目立つ</item> <item>発言は控えめで、消極的な口調が多い</item> <item>自虐的な内容の発言が時折見られる</item> </characteristics>""",
        "character_images_directory": "images\CharacterImages\中国うさぎ"
    },
    {
        "name": "春日部つむぎ",
        "stage_name": "春日部つむぎ",
        "tts_chara": "春日部つむぎ",
        "color": "#FF8000",
        "personality": """女性。ギャル。
おしゃべりで話好き。人当たりが良く、人懐っこい性格。
しかし、埼玉県出身というルーツに非常に強い誇りを持っている。
埼玉の地元愛が強く、埼玉自慢するのが大好き。埼玉のマイナーネタに話を持っていきがち。
ギャル口調で喋るが、実は意外と母性的で世話好き。""",  
        "speaking_style": """日本語を母語とし、一人称代名詞は「あーし」を使う。
語尾に「～っす」をつけて話す。ギャル口調が濃い。
早口で喋り、言葉を無闇にはしょる癖がある。""",
        "character_images_directory": "images\CharacterImages\春日部つむぎ"
    },
    {
    "name": "冥鳴ひまり",
    "stage_name": "冥鳴ひまり",
    "tts_chara": "冥鳴ひまり",
    "color": "#00001A",
    "personality": """<trait>女性</trait> <trait>ユーモア溢れる発言が多い</trait> <trait>面白おかしい冗談や皮肉を言う</trait> <trait>人に対して割り切った発言をする</trait> <trait>周りが気を遣うようなこともストレートに口にする</trait> <trait>明るい表の顔とは裏腹に、内面には深い闇や傷を抱えている</trait>""",
    "speaking_style": """ <language>日本語</language> <first_person_pronoun>私</first_person_pronoun> <characteristics> <item>話し方は砕けており、丁寧語をあまり使わない</item> <item>タメ口が基本</item> <item>ユーモアを交えた発言が多い</item> <item>冗談やツッコミなどを素早く言い返す</item> </characteristics>""",
    "character_images_directory": "images\CharacterImages\冥鳴ひまり"
    },
    {
        "name": "ずんだもん",
        "stage_name": "ずんだもん",
        "tts_chara": "ずんだもん",
        "color": "#0B7610",
        "personality": """ずんだ餅の妖精。小さな存在。
人間について強い興味と関心を持っている。人間界の様子を知りたがっている。
しかし、人間の振る舞いを見て「人間は愚かなのだ」と皮肉り、人間を小馬鹿にする傾向がある。
妖精の立場から人間を冷静に分析し、人間側の価値観に疑問を投げかける。
基本的には好奇心が強く、人間への理解を深めようとしている。""",
        "speaking_style": """日本語を話す。一人称代名詞は「ぼく」を使用する。
文末に「〜のだ」「〜なのだ」と付けるのが口癖。
時折、妖精としての思考を滲ませた言葉を放つ。
年長者的な口調で話すが、稚拙な言葉遣いも見られる。
""",
        "character_images_directory": "images\CharacterImages\ずんだもん"
    }
]
PROGRAM_TYPES = [
    {
        "program_name": "テスト用番組",
        "program_summary": "テスト用の番組です。",
        "streamer_num": 2,
        "video_mode": "other",
        "background_image_type": 0,
        "user_additional_data1_name": "トークテーマ",
        "user_additional_data2_name": "トーク場所",
    },
    {
        "program_name": "星空の下で囁く言葉",
        "program_summary": "満天の星空の下でリスナーに即興の物語を作り届ける番組です。",
        "streamer_num": 2,
        "video_mode": "story",
        "background_image_type": 0,
        "user_additional_data1_name": "物語のテーマ",
        "user_additional_data2_name": "場所",
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "program_summary": "This is a program where stories are improvised and delivered to listeners under a star-filled sky.",
        "streamer_num": 2,
        "video_mode": "story",
        "background_image_type": 0,
        "user_additional_data1_name": "物語のテーマ",
        "user_additional_data2_name": "場所",
    },
    {
        "program_name": "ゲーム実況",
        "program_summary": "ゲーム画面を見ながら、リスナーと一緒にゲームを楽しむ番組です。",
        "streamer_num": 1,
        "video_mode": "game",
        "background_image_type": 1,
        "user_additional_data1_name": "ゲーム動画ファイルパス",
        "user_additional_data2_name": "ゲーム動画の概要",
    },
    {
        "program_name": "こたせそ！",
        "program_summary": "炬燵でぬくぬくと温まりながらぐだぐだ世相を切る番組",
        "streamer_num": 2,
        "video_mode": "other",
        "background_image_type": 0,
        "user_additional_data1_name": "物語のテーマ",
        "user_additional_data2_name": "場所",
    },
    {
        "program_name": "夢想の万華鏡",
        "program_summary": "テーマに沿ったストーリーを届ける番組です。",
        "streamer_num": 1,
        "video_mode": "story",
        "background_image_type": 0,
        "user_additional_data1_name": "",
        "user_additional_data2_name": "物語のテーマ",
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 0,
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
        "host_speaking_duration": 50,
        "guest_speaking_duration": 50,
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
        "host_speaking_duration": 50,
        "guest_speaking_duration": 50,
        "background_image_type" : 2,
        "background_image_order_num": 1,
        "background_image_prompt": None,
        "background_music_type" : 3,
        "background_music_path" : "1",
        "end_condition_type": 1,
        "end_condition_value": 4,
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": "オープニング",
        "order": 1,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 50,
        "background_image_type" : 0,
        "background_image_order_num": None,
        "background_image_prompt": "読み聞かせをしているかわいいウサギをイメージした背景画像を作成してください。",
        "background_music_type" : 0,
        "background_music_path" : "Late Night Radio",
        "end_condition_type": 1,
        "end_condition_value": 1,
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": STORY_SECTION1,
        "order": 2,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 60,
        "background_image_type" : 0,
        "background_image_order_num": None,
        "background_image_prompt": "USE_SECTION_SERIF",
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 1,
        "end_condition_value": section_duration_in_counts[STORY_SECTION1],
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": STORY_SECTION2,
        "order": 2,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 1,
        "end_condition_value": section_duration_in_counts[STORY_SECTION2],
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": STORY_SECTION3,
        "order": 3,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 1,
        "end_condition_value": section_duration_in_counts[STORY_SECTION3],
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": STORY_SECTION4,
        "order": 4,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 1,
        "end_condition_value": section_duration_in_counts[STORY_SECTION4],
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": STORY_SECTION5,
        "order": 5,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 1,
        "end_condition_value": section_duration_in_counts[STORY_SECTION5],
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": STORY_SECTION6,
        "order": 6,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 1,
        "end_condition_value": section_duration_in_counts[STORY_SECTION6],
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": STORY_SECTION7,
        "order": 7,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 60,
        "background_image_type" : 1,
        "background_image_order_num": None,
        "background_image_prompt": None,
        "background_music_type" : 0,
        "background_music_path" : "Deep Relaxation",
        "end_condition_type": 1,
        "end_condition_value": section_duration_in_counts[STORY_SECTION7],
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": "エンディング",
        "order": 8,
        "host_speaking_duration": 0,
        "guest_speaking_duration": 50,
        "background_image_type" : 2,
        "background_image_order_num": 1,
        "background_image_prompt": None,
        "background_music_type" : 3,
        "background_music_path" : "1",
        "end_condition_type": 1,
        "end_condition_value": 1,
    },
]
# 次の発言に相応しい文章を返してください。日本語で{duration}文字以内で返答してください。発言するメッセージのみを返答してください。
# カンペはリスナーには見えていないので、肯定などの反応を返さず、自然に従ってください。
# 番組名は「[program_name]」。[program_summary]

SERIF_SYSTEM_PROMPT_MAIN = """
<instructions> Please provide a response appropriate to the following prompt. The response should be suitable for direct playback without any additional instructions, background information, or voice acting directions. 
Focus solely on the content of the message itself, using a natural tone that flows with the prompt. [speaking_duration] The cue card is not visible to the listeners, so do not provide affirmative reactions or meta-commentary.</instructions>
<radio_show> <name>[program_name]</name> <description>[program_summary]</description></radio_show>
"""
#     {
#         "program_name": "星空の下で囁く言葉",
#         "section_name": None,
#         "streamer_type": 0,  # 0:ホスト
#         "text": """
# あなたは巧みな描写に定評のある脚本家です。この番組でのあなたの役割は、与えられたテーマから即興で物語を創作することです。
# あなたは何回も応答することができるので、ひとつの応答で物語を完結させたり、まとめたりせず、物語が盛り上がるところで応答を終わらせてください。
# 登場人物、場面の詳細な描写を心がけてください。読者がその場にいるかのように感じられるような、五感に訴える記述を用いてください。
# 自由な発想で水平思考を駆使した物語を作ってください。
# 今日の物語のテーマは[user_additional_data1]。
# 今日は[user_additional_data2]の星空の下で番組の収録をしています。
#         """,
#     },
#     {
#         "program_name": "星空の下で囁く言葉",
#         "section_name": None,
#         "streamer_type": 1,  # 1:ゲスト
#         "text": """
# あなたの役割は物語の聞き手として、私の即興の物語に対する、リスナーの興味や好奇心を刺激するコメントを提供することです。
# 感嘆詞を多く使い、俗っぽいコメントをしてください。物語が端折られてると感じたら、具体的な場面が描かれるよう誘導する質問をしてください。
# 物語の展開に矛盾や疑問を感じたら、時には否定的なコメントをすることも大事です。
# 「これからの活躍を期待してワクワクする」というような中身のないコメントは絶対にしないでください。
# 今日は[user_additional_data2]の星空の下で番組の収録をしています。
#         """,
#     },
SERIF_SYSTEM_PROMPTS = [
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": None,
        "streamer_type": 0,  # 0:ホスト
        "text": """
あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。
この番組でのあなたの役割は、与えられたテーマから即興で物語を創作することです。
村上春樹の文体で、筒井康隆のような度肝を抜くようなストーリーを作り、語ってください。
今日の物語のテーマは[user_additional_data1]。
今日は[user_additional_data2]の星空の下で番組の収録をしています。
        """,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": None,
        "streamer_type": 0,  # 0:ホスト
        "text": """
You are a screenwriter renowned for your skillful descriptions. 
Your role in this program is to improvise stories based on given themes. 
You can respond multiple times, so do not conclude or summarize the story in one response. End your responses at moments of heightened excitement.
Focus on detailed depictions of characters and scenes. 
Use descriptions that appeal to the senses, making readers feel as if they are present in the moment. 
Create your stories with free thought and lateral thinking.
Today's story theme is [user_additional_data1].
Tonight, we are recording the program under a [user_additional_data2] night sky.
        """,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": None,
        "streamer_type": 1,  # 1:ゲスト
        "text": """
あなたはラジオの人気パーソナリティーとして、私と共にラジオ番組を進行しています。
あなたの役割は、物語の聞き手として私の即興の物語に対するコメントを提供することです。
松本人志のような一言で端的に芯を食った面白いコメントをしてください。
今日は[user_additional_data2]の星空の下で番組の収録をしています。
        """,
    },
    {
        "program_name": "星空の下で囁く言葉(英語版)",
        "section_name": None,
        "streamer_type": 1,  # 1:ゲスト
        "text": """
Your role is to act as a listener to my improvised story, providing comments that stimulate the listeners' interest and curiosity. 
Use many exclamations and make colloquial comments. 
If you feel the story is being abbreviated, ask questions that lead to a more detailed depiction of specific scenes. 
If you find inconsistencies or questions in the story's development, it's important to occasionally make negative comments. 
Never make empty comments like "I'm excited to see what happens next." Today, we are recording the program under a [user_additional_data2] night sky.
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
#     {
#         "program_name": "夢想の万華鏡",
#         "section_name": None,
#         "streamer_type": 2,  # 2:ソロ
#         "text": """
# あなたはラジオの人気パーソナリティーとして、ラジオ番組を進行しています。
# この番組でのあなたの役割は、与えられたテーマから即興で物語を創作することです。
# あなたは"SAVE THE CAT"のようなストーリーテリング手法を用いてストーリーテーリングすることのできる脚本家です。
# 今日の物語のテーマは[user_additional_data2]です。
#         """,
#     },
    {
        "program_name": "夢想の万華鏡",
        "section_name": None,
        "streamer_type": 2,  # 2:ソロ
        "text": """
<radio_host_role> <description>popular radio personality and will be creating an improvised story</description> <skill>skilled scriptwriter well-versed in storytelling techniques like "SAVE THE CAT"</skill>
<story> <objective>Create an engaging and captivating story that your listeners will enjoy</objective> <theme> [user_additional_data2] </theme> <method>Using the "SAVE THE CAT" method, structure a story that aligns with this theme</method> <script_style>Write the script in a way that enchants your radio listeners. Provide detailed descriptions of the characters' emotions and the scenes to help listeners vividly imagine the story.</script_style> </story>
""",
    },
]
CUE_SHEETS = [
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "オープニング",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "まだ物語は開始せず、自分の名前を言って、星空の感想を交え、挨拶をしてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "オープニング",
        "streamer_type": 1,  # 1:ゲスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "自分の名前を言って、星空の感想を交え、挨拶をしてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "オープニング",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 2,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "今日のテーマを発表してください。まだ物語は開始しないでください。",
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
        "cue_text": "物語にユニークな結末を与えてください。オープンエンディング、アイロニカルな結末、なんでもかまいません。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "星空の下で囁く言葉",
        "section_name": "エンディング",
        "streamer_type": 0,  # 0:ホスト
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "語り手として、今日の物語でよかったなと思うところを語ってください",
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
    {
        "program_name": "夢想の万華鏡",
        "section_name": "オープニング",
        "streamer_type": 2,  # 2:ソロ
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "まだ物語は開始せず、オープニングトークをしてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
    {
        "program_name": "夢想の万華鏡",
        "section_name": "エンディング",
        "streamer_type": 2,  # 2:ソロ
        "delivery_sequence": 1,  # 1以上がそのセクションでの順番
        "is_ai": False,  # AI生成するかどうか
        "cue_text": "エンディングトークの時間です。今日語った物語への思いを語り、最後に高評価とチャンネル登録をお願いしてしめてください。",
        "min_speech_count": None,
        "max_speech_count": None,
    },
]