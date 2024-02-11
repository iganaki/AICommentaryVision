from enum import Enum

# プログラム内で使用する列挙型
# モード
class Mode(Enum):
    SOLO_GAMEPLAY = 0
    DUO_GAMEPLAY = 1
    DUO_RADIO = 2

# 役割
class Role(Enum):
    SOLO_PLAYER = 0
    DUO_GAME_PLAYER = 1
    DUO_GAME_COMMENTATOR = 2
    DUO_RADIO_HOST = 3
    DUO_RADIO_GUEST = 4


# データベースの初期化時に使用するマスターデータ
# カンペ(cue_card)を辞書形式で定義
CUE_CARD_DATA = [
    {"cue_card": "ここでボケて", "cue_card_print": "ここでボケて", "next_cue": "ボケにツッコんで", "next_cue_print": "ボケにツッコんで"},
    {"cue_card": "ここでボケて", "cue_card_print": "ここでボケて", "next_cue": "ノリツッコみして", "next_cue_print": "ノリツッコみして"},
    {"cue_card": "ここでボケて", "cue_card_print": "ここでボケて", "next_cue": "ボケをスルーして", "next_cue_print": "スルーして"},
    {"cue_card": "画面に映っているものを使ってボケて", "cue_card_print": "モノボケ", "next_cue": "ボケにツッコんで", "next_cue_print": "ボケにツッコんで"},
    {"cue_card": "相方のうっかりエピソードを話して", "cue_card_print": "うっかりエピソード", "next_cue": "", "next_cue_print": ""},
    {"cue_card": "最近会ったうれしいことを話して", "cue_card_print": "うれしかった話", "next_cue": "", "next_cue_print": ""},
    {"cue_card": "盛り上がって！！！", "cue_card_print": "盛り上がって", "next_cue": "", "next_cue_print": ""},
    {"cue_card": "豆知識を一つ披露して", "cue_card_print": "豆知識を話して", "next_cue": "", "next_cue_print": ""},
    {"cue_card": "相方へこのゲームに関して質問して", "cue_card_print": "相方へ質問して", "next_cue": "質問に回答して", "next_cue_print": "質問に回答して"},
    {"cue_card": "相方へ楽しい質問して", "cue_card_print": "相方へ質問して", "next_cue": "質問に回答して", "next_cue_print": "質問に回答して"},  
    {"cue_card": "相方へ子供のころの質問して", "cue_card_print": "相方へ質問して", "next_cue": "質問に回答して", "next_cue_print": "質問に回答して"},
    {"cue_card": "最近会った悲しかった話をして", "cue_card_print": "悲しかった話", "next_cue": "", "next_cue_print": ""},
    {"cue_card": "秘密の話を一つしてください", "cue_card_print": "秘密の話", "next_cue": "", "next_cue_print": ""}
]

# ラジオのトークテーマを辞書形式で定義
TALK_THEME_DATA = [
    {'theme': 'Where do you start washing in the bath?', 'theme_jp': 'お風呂でどこから洗う？'},
    {'theme': 'If you could take one thing to a deserted island, what would it be?', 'theme_jp': '無人島に一つ持っていくなら何？'},
    {'theme': 'Nostalgic commercials you watched as a child.', 'theme_jp': '子供のころに見た懐かしいCM'}
]

# 二人の関係性を辞書形式で定義
RELATIONSHIP_DATA = [
    {'our_relationship': '博士と助手', 'your_role1': '物知りな博士', 'your_role2': '博士を尊敬している助手'},
    {'our_relationship': '恋人', 'your_role1': 'クールな恋人', 'your_role2': '好きすぎる恋人'},
    {'our_relationship': '親友', 'your_role1': 'なんでも知ってる親友', 'your_role2': '頼りがちな親友'},
    {'our_relationship': '先輩と後輩', 'your_role1': 'しっかりものの後輩', 'your_role2': 'おっちょこちょいな先輩'},
    {'our_relationship': '上司と部下', 'your_role1': '敏腕上司', 'your_role2': '新人の部下'},
    {'our_relationship': '先生と生徒', 'your_role1': '人情味あふれる先生', 'your_role2': 'ひねくれた生徒'},
    {'our_relationship': '師匠と弟子', 'your_role1': '厳しい師匠', 'your_role2': '師匠を尊敬する弟子'},
    {'our_relationship': 'マスターとウェイトレス', 'your_role1': 'かっこいいマスター', 'your_role2': 'かわいいウェイトレス'}
]

# 配信者の基礎情報を辞書形式で定義
STATIC_STREAMER_PROFILES_DATA = [
    {
        "name": "四国めたん",
        "voicevox_chara": "四国めたん",
        "color": "#FF1493",
        "personality": "女性。没落した貧乏なお嬢様。今は一人でテント暮らしをしている。育ちがよい。",
        "speaking_style": "日本語話者。一人称は「私」、語尾は「～かしら」「なのよね」などをつける。上品な言葉遣いをする。"
    },
    {
        "name": "ユキ",
        "voicevox_chara": "WhiteCUL",
        "color": "#000080",
        "personality": "女性。非常に感情豊かで、浮かれたり怖がったりとテンションの浮き沈みが激しい。自己評価が高い。自分のことをクールビューティだと思っている",
        "speaking_style": "日本語話者。一人称は「わたし」。慌てると言葉が乱れ、叫んだり、泣き言を言ったりする",
    },
    {
        "name": "中国うさぎ",
        "voicevox_chara": "中国うさぎ",
        "color": "#760B20",
        "personality": "女性。ダウナーで暗めの性格。ひきこもり。引っ込み思案で、人とのコミュニケーションが苦手。",
        "speaking_style": "日本語話者。一人称は「私」。ネットスラングをよく使う。",
    },
    {
        "name": "春日部つむぎ",
        "voicevox_chara": "春日部つむぎ",
        "color": "#FF8000",
        "personality": "女性。ギャル。おしゃべりで、人懐っこい。出身地の埼玉に非常に強い誇りを持っている。",  
        "speaking_style": "日本語話者。一人称は「あーし」。語尾に「～っす」をつける。",
    },
    {
        "name": "冥鳴ひまり",
        "voicevox_chara": "冥鳴ひまり",
        "color": "#00001A",
        "personality": "女性。ユーモアのセンスが高い。他の人が言いにくいこともズバズバ言う。闇が深い。",
        "speaking_style": "日本語話者。一人称は「私」。砕けた話し方をする。",
    },
    {
        "name": "ずんだもん",
        "voicevox_chara": "ずんだもん",
        "color": "#0B7610",
        "personality": "ずんだの妖精。人間について知りたいと思っている。無邪気。あまりものを知らない。",
        "speaking_style": "日本語話者。一人称は「ぼく」、語尾は「～のだ」「～なのだ」をつける。",
    }
]
