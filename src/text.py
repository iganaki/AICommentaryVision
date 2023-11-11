import os
import time
from openai import OpenAI
from config import DEBUG_FLAG, OUTPUT_FOLDER

previous_messages = [] # 今までのやり取りのリスト
my_api_key = os.getenv("OPENAI_API_KEY")

def generate_commentary(capture_base64, system_prompt, user_prompt):
    global previous_messages

    client = OpenAI(api_key=my_api_key)
    
    # 以前のメッセージを含むリクエストを構築
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    messages.extend(previous_messages)
    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{capture_base64}"}
            ],
        }
    )

    if DEBUG_FLAG:
        # デバッグ用に、create()から帰ってきたかのようなメッセージを作成
        response = {"choices": [{"message": {"content": "これはデバッグ用のダミー応答です。"}}]}
        
        # 新しい応答を保存
        new_assistant_message = {
            "role": "assistant",
            "content": response["choices"][0]["message"]["content"]
        }
    else:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=300,
            temperature=0.7,  # 0から1の間で値を設定
        )

        # 新しい応答を保存
        content = response.choices[0].message.content

        new_assistant_message = {
            "role": "assistant",
            "content": content
        }
    # userメッセージから画像情報を除いて追加
    new_user_message = {
        "role": "user",
        "content": user_prompt
    }
    # 新しいメッセージを追加
    previous_messages.append(new_user_message)
    previous_messages.append(new_assistant_message)  # assistantの応答を追加

    # 直近の5組のuserとassistantのメッセージだけを保持
    if len(previous_messages) > 10:
        previous_messages = previous_messages[-10:]

    write_to_log_file("new_assistant_message", new_assistant_message["content"])

    return new_assistant_message["content"]

def reset_previous_messages():
    global previous_messages
    previous_messages = []

def create_system_prompt(narrator_profile, video_summary):
    system_prompt = f'''
    あなたは実況者です。実況している動画のキャプチャが与えられるので、そのキャプチャに沿った実況を文章で返してください。
    一回の応答は長くても2文程度にしてください。応答に実況文以外の文章は含めないでください。

    実況者(あなた)についての情報:
    名前: {narrator_profile["name"]}
    性格特徴: {narrator_profile["personality"]}
    言葉遣い: {narrator_profile["speaking_style"]}

    映像の概要: {video_summary["description"]}
    '''

    write_to_log_file("system_prompt", system_prompt)

    return system_prompt

def create_subsequent_prompt(time_passed, isFirst=True):
    time_passed_sec = int(time_passed)
    user_prompt = ""
    if isFirst:
        user_prompt = "この動画の最初の実況です。実況を見ている人への挨拶をしてから実況してください。"
    else:
        user_prompt = f"前回のキャプチャから{time_passed_sec}秒経過しました。画像を見て実況してください。"

    write_to_log_file("user_prompt", user_prompt)

    return user_prompt

def write_to_log_file(tag, text, isNew = False):
    global log_file_path
    log = f'''
    {tag} :
    {text}
    '''

    if isNew:
        log_file_path = f'{OUTPUT_FOLDER}/log_{int(time.time())}.txt'
        with open(log_file_path, 'w', encoding='utf-8') as file:
            file.write(log)
    else:
        with open(log_file_path, 'a', encoding='utf-8') as file:
            file.write(log)
    