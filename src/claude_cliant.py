import base64
from gc import DEBUG_UNCOLLECTABLE
from math import e
from multiprocessing import dummy
import os
import random
import re
import time
import anthropic
import cv2
from config import MESSAGE_HISTORY_LIMIT
import log

claude_api_key = os.getenv("CLAUDE_API_KEY", "")
client = anthropic.Anthropic(
    api_key=claude_api_key,
)
class ClaudeClient:
    def __init__(self, debug_mode):
        self.debug_mode = debug_mode
        self.cnt = 0
        
    # 実況文を生成する。
    def generate_commentary(self, system_prompts, previous_messages, partner_message, cue_card, serif_duration, llm_model="claude-3-opus-20240229"):
        dummy_texts = ['これはデバッグ用のダミー応答です。いい。改行のテストのため、意図的に長い文章にしています。ご協力感謝します。',
                      'I\'m sorry, his is a dummy response for debugging. Good. It is intentionally long for testing line breaks. Thank you for your cooperation.',
                      'これは短いデバッグダミー応答です。',
                      """宇宙太郎、実は昔、さいたま市の星空があまりにも美しいのに心奪われて、自分だけのものにしたいって思っちゃったんすよ。だから、ある夜、星を観測するための大きな望遠鏡を持ち出して、公園で独り占めしてたんす。でも、そこに来たのが小学生の真希ちゃん。真希ちゃんは星が大好きで、毎晩星を見るのが日課だったんすけど、宇宙太郎がいるせいで見れなくなっちゃったんすよね。

真希ちゃんの「星はみんなのものだよ」という一言で、宇宙太郎は自分の間違いに気づいたんす。罪悪感と反省から、宇宙太郎は星空保護活動を始めたんす。さいたま市の星空をより美しく、そして""",
"""
真希ちゃんの一言が全てを変えたんだね。でも、「星はみんなのもの」というシンプルな真実に気づくまで、宇宙太郎はなぜそんなに星を独り占めしたかったんだろう？""",
""" 宇宙太郎が星を独り占めしたかったのは、実は幼い頃からの夢があったからなんすよ。宇宙太郎は子供の頃に父親と一緒に星空を見るのが大好きだったんすけど、父親が急にいなくなっちゃって、その思い出だけが宇宙太郎にとっての宝物だったんす。だから、その思い出を守るために、「星は自分だけのもの」と思い込んでしまったんすよね。

でも、真希ちゃんの一言で、宇宙太郎は気づいたんす。「星はみんなのもの」というシンプルな真実を。そして、星空を共有する喜びが、実は父親との思い出をより美しく、より大切なものに変えるんだってことに。だからこそ、彼は星空保護の活動に情""",
""" あーしもそれ、気になるっすね。星空観察会でのルール違反に対しては、埼玉太郎が考えた対処法があって、それがこの物語のクライマックスにもつながるんですよ。埼玉太郎は、星空の下でのお楽しみを最大限に味わってもらうために、万が一ルールを破った参加者がいた場合は、その人にさいたま市の美しい夜空をもっと深く知ってもらうための特別プログラムを用意していました。
そのプログラムとは、星空ガイドの専門家と一緒に、夜空の星々を詳しく学ぶセッション。ルール違反をした人には、なんと星空の美しさと大切さをもっと深く理解してもらうチャンスを与えるんです。しかし、物語のクライマックスで、ルールを破ったの"""]
        # dummy_texts = ['１', '２', '３', '４', '５']
        dummy_text = random.choice(dummy_texts)

        commentary = self._generate_text(system_prompts, llm_model, previous_messages=previous_messages, 
                                         partner_message=partner_message, cue_card=cue_card,
                                         dummy_text=dummy_text, text_duration=serif_duration)
        return commentary
        
    def _generate_text(self, system_prompts, claude_model, text_duration=300, temperature=0.7, 
                      previous_messages=[], partner_message="", cue_card="", dummy_text="これはデバッグ用のダミー応答です。"):
        system_prompt = "\n".join(reversed(system_prompts))
        messages = self._build_messages(previous_messages=previous_messages, 
                                        partner_message=partner_message, cue_card=cue_card)
        if self.debug_mode:
            text = dummy_text
            expected_role = "user"
            for message in messages:
                if message["role"] != expected_role:
                    raise ValueError(f"roleが交互になっていません。{message['role']}が連続しています。{messages}")
                expected_role = "assistant" if expected_role == "user" else "user"
        else:
            max_retries = 100  # 最大再試行回数
            retry_delay = 60  # 再試行までの遅延時間（秒）

            for attempt in range(max_retries):
                try:
                    response = client.messages.create(
                        model=claude_model,
                        system=system_prompt,
                        max_tokens=text_duration+100 if text_duration != 0 else 1024,
                        messages=messages
                    )
                    text = response.content[0].text if response.content else None
                    break  # 成功したらループを抜ける
                except Exception as e:
                    # 特定のエラーを捕捉して処理
                    if "Internal server error" in str(e) or "Overloaded" in str(e):
                        print(f"エラー発生、再試行します ({attempt+1}/{max_retries})")
                        time.sleep(retry_delay)  # 設定した時間だけ待機
                    else:
                        log.handle_api_error(e, "CLAUDE呼び出し中にエラーが発生しました", system_prompt=system_prompt, gpt_model=claude_model, partner_message=partner_message, cue_card=cue_card)
                        raise  # 未知のエラーは再試行しない
            else:
                print("最大再試行回数に達しました。処理を中断します。")
                raise

        return text

    # Claude3 APIに渡すメッセージを組み立てる
    def _build_messages(self, previous_messages=[], partner_message="", cue_card=""):
        # 過去のプロンプトリストがあれば付加
        messages=[]
        messages.extend(previous_messages)

        # パートナーメッセージがあれば追加
        if partner_message != "":
            content = [{"type": "text", "text": partner_message}]
            messages.append({
                "role": "user",
                "content": content
            })

        # パートナーメッセージとカンペがあれば間にダミーアシスタントプロンプトを追加
        if cue_card != "" and partner_message != "":
            content = [{"type": "text", "text": "(スタッフのカンペ待ち)"}]
            messages.append({
                "role": "assistant",
                "content": content
            })
        
        # カンペがあれば追加
        if cue_card != "":
            content = [{"type": "text", "text": cue_card}]
            messages.append({
                "role": "user",
                "content": content
            })

        return messages

    def analyze_video(self, video_path, max_images=20):
        dummy_text = "これはデバッグ用のダミー応答です。"
        current_sec = 0
        analysis_text = None
        analysis_texts = []
        DUE = 5
        for i in range(5):
            print(f"動画解析中... {i+1}/5")
            base64_frames = self._get_frames_from_video(video_path, current_sec, current_sec+DUE)
#             直前の20秒間でのあなたの解析結果：
# {analysis_text if analysis_text else "これは初回の解析です。"}

# --------------------------------------------
#             prompt = f"""
# デジタルカードゲーム「シャドウバース」の対戦リプレイ動画から抽出された、ゲーム開始時点からの2秒間隔のフレーム画像です。
# {current_sec}秒~{current_sec+20}秒の区間のフレームを解析します。
# これらの画像から、盤面の状況変化を詳細に分析してください。盤面には使用したカードしか並びません。そのため、ゲーム開始直後には何もないことに注意してください。
# <rule>このゲームでは、プレイヤーはリーダーとなり、40枚のデッキを使用して対戦相手と戦います。フォロワーを盤面に出したり、スペルを使用したりしてダメージを与え、相手リーダーの体力を0にすることで勝利します。
# 試合開始時には先攻後攻がランダムに決定され、その後マリガン（手札交換）を行います。
# 半分より上側が相手プレイヤー、下側が自プレイヤーの領域です。各リーダーの体力はリーダースキンの左上に表示されます。画面の最下部には、自プレイヤーの手札が表示されています。
# カードのコストは左上の数字で示され、毎ターンプレイヤーが得るPPを消費してプレイします。
# フォロワーは攻撃力と体力を持ち、それぞれ左下と右下の数字で表されます。</rule>

# ゲーム実況での解説に使用できるよう、対戦の状況と自プレイヤー、他プレイヤーの動きを正確に記述してください。
# 分析には具体的なカード名称や数字を必ず使用してください。盤面のカードは名前が表示されていません。発動時に名称が読み取れなかった場合、絵からの推測で名前を創作し、使用してください。
# 手札のカードを、盤面にあると誤認しないように注意してください。
# """
            prompt = f"""<game> <name>POPULATION: ONE</name> <description>VRFPSゲーム「POPULATION: ONE」の視点録画から抽出された、0.5秒間隔のフレーム画像です。</description> <frame_interval> <start>{current_sec}秒</start> <end>{current_sec+DUE}秒</end> </frame_interval> </game>

<game_features>
<feature>3人1チームで、最大6チーム（18人）が最後の1チームになるまで戦います。</feature>
<feature>マップ内のすべての建造物は、プレイヤーが手で登ることができます。</feature>
<feature>両手を広げることで、空中を滑空して移動することができます。</feature>
<feature>武器には、アサルトライフル、ショットガン、スナイパーライフル、ナイフ、ソードなどがあります。</feature>
<feature>プレイヤーは好きな場所に壁を建造でき、遮蔽物や登るための足場として利用できます。</feature>
</game_features>

<ui_description>
<status_bars>
<location>画面中央下部</location>
<red_bar>
<description>次のエリア縮小までの残り時間を示しています。</description>
</red_bar>
<blue_bar>
<description>シールド値を表しています。</description>
</blue_bar>
<green_bar>
<description>体力を表しています。</description>
</green_bar>
<values>
<location>バーの左端</location>
<color>白字</color>
</values>
<visibility>ただし、マップまたはインベントリを開いている間は表示されません。</visibility>
</status_bars>

<death_respawn_log>
  <location>エリア縮小までの残り時間の上</location>
  <visibility>プレイヤーの死亡・復活時に表示されることがあります。ただし、マップまたはインベントリを開いている間は表示されません。</visibility>
</death_respawn_log>

<map>
  <player_markers>
    <color>青色</color>
    <description>自分と味方の位置が表示されます。</description>
  </player_markers>
  <player_count>
    <location>上部</location>
    <description>味方と敵の生存人数が表示されています。</description>
  </player_count>
</map>

<inventory>
  <shape>ピザのように扇形に分割された円形</shape>
  <description>所持しているアイテム（武器、グレネード、回復アイテムなど）が表示されます。</description>
</inventory>

<player_info>
  <friendly_player>
    <name_color>青字</name_color>
    <health>体力が表示されます。</health>
  </friendly_player>
  <enemy_player>
    <description>味方以外のプレイヤーは敵です。</description>
  </enemy_player>
</player_info>

<screen_effects>
  <damage>
    <description>画面が全体的に赤みがかっているときはダメージを受けています。</description>
  </damage>
  <death>
    <description>画面が白黒でステータスが表示されていないときは、自身が死亡し、復活待ち状態になっています。</description>
  </death>
</screen_effects>

</ui_description>

<output_instructions>
<format>1秒（2枚）ごとに現在の秒数と、以下の内容を数字の優先順で、その変化を出力してください。前の秒から変化がないものは出力に含めないで下さい。：</format>
<priority_1>敵が視界に入った場合、そのことと見た目の距離</priority_1>
<priority_2>戦闘中の場合、敵味方の使用武器や行動を詳細に</priority_2>
<priority_3>死亡・復活のログが新たに出た場合、その内容</priority_3>
<priority_4>体力、シールドの数値</priority_4>
<priority_5>現在見える風景、状況、進行方向などの動画から読み取れる情報</priority_5>
</output_instructions>
"""
            model = "claude-3-haiku-20240307"
            analysis_text = self._analyze_video(base64_frames, prompt, model, max_images, dummy_text)
            analysis_texts.append(analysis_text)
            print(f"解析結果：{analysis_text}")
            current_sec += DUE
            
        return analysis_texts


    def _analyze_video(self, base64_frames, prompt, model, max_images=20, dummy_text="これはデバッグ用のダミー応答です。"):
        if self.debug_mode:
            return dummy_text
        else:
            max_retries = 100  # 最大再試行回数
            retry_delay = 60  # 再試行までの遅延時間（秒）

            for attempt in range(max_retries):
                try:
                    response = client.messages.create(
                        model=model,
                        max_tokens=1024,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    *map(lambda x: {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": x}}, base64_frames),
                                    {
                                        "type": "text",
                                        "text": prompt
                                    }
                                ],
                            }
                        ],
                    )
                    
                    analysis_text = response.content[0].text if response.content else ""
                    return analysis_text
                except Exception as e:
                    # 特定のエラーを捕捉して処理
                    if "Internal server error" in str(e) or "Overloaded" in str(e):
                        print(f"エラー発生、再試行します ({attempt+1}/{max_retries})")
                        time.sleep(retry_delay)  # 設定した時間だけ待機
                    else:
                        log.handle_api_error(e, "CLAUDE呼び出し中にエラーが発生しました", prompt=prompt, model=model)
                        raise  # 未知のエラーは再試行しない
            else:
                print("最大再試行回数に達しました。処理を中断します。")
                raise
                
    def _get_frames_from_video(self, file_path, start_sec, end_sec, max_images=10):
        video = cv2.VideoCapture(file_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        start_frame = int(start_sec * fps)
        end_frame = int(end_sec * fps)
        frame_interval = (end_frame - start_frame) // max_images

        base64_frames = []
        frame_count = 0

        output_dir = "D:\\pj\\AICommentaryVision\\output\\test3"
        os.makedirs(output_dir, exist_ok=True)

        for frame_number in range(start_frame, end_frame + 1, frame_interval):
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, frame = video.read()
            if not success:
                break

            frame_count += 1
            frame_path = os.path.join(output_dir, f"frame_{start_sec}_{end_sec}_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)

            _, encoded_frame = cv2.imencode(".jpg", frame)
            base64_frame = base64.b64encode(encoded_frame).decode("utf-8")
            base64_frames.append(base64_frame)

        video.release()

        return base64_frames[:max_images]
    
if __name__ == "__main__":
    cc = ClaudeClient(False)
    video_path = "D:/pj/AICommentaryVision/output/test/test2.mp4"
    test = cc.analyze_video(video_path)
    print_log_path = "D:/pj/AICommentaryVision/output/test3/test4.log"
    with open(print_log_path, "w") as f:
        for t in test:
            f.write("----\n")
            f.write(t)
            f.write("\n")
    print("ログを出力しました。")
