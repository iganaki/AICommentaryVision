from pathlib import Path
import time
import gradio as gr
from audio import VoiceGenerator
from config import DATA_FOLDER
import model, settings
from static_data import Role
from studio import Studio

class WebUI:
    def __init__(self):
        tts_status = settings.initialize_database()
        self.tts_speakers = self._get_tts_speakers()
        self.studio = Studio()

        self.interface = gr.Blocks()

        with self.interface:
            # TTS接続セクション
            with gr.Tab("TTS接続") as tts_section:
                gr.Markdown("## TTS接続")
                with gr.Row():
                    status_text = gr.Textbox(label="TTS接続状況", lines=4, value=self._make_tts_connection_text(tts_status))
                    tts_check_button = gr.Button("接続確認")

            # ストリーマー編集セクション
            with gr.Tab("ストリーマー編集") as streamer_section:
                with gr.Row():
                    gr.Markdown("## ストリーマー編集")
                with gr.Row():
                    streamer_selector = gr.Dropdown(choices=self._get_streamers_list(), label="編集するストリーマーを選択", allow_custom_value=True)
                    streamer_edit_button = gr.Button("呼び出し")
                with gr.Row():
                    name = gr.Textbox(label="ストリーマーID")
                    stage_name = gr.Textbox(label="動画中での名前")
                    tts_chara = gr.Dropdown(choices=self.tts_speakers, label="TTS")
                    color = gr.ColorPicker(label="色（字幕などで使用）")
                    update_profile_button = gr.Button("更新")
                    insert_profile_button = gr.Button("追加")
                with gr.Row():
                    personality = gr.TextArea(label="性格")
                    speaking_style = gr.TextArea(label="話し方")
                    character_images_directory = gr.Textbox(label=f"{Path(DATA_FOLDER).resolve().as_posix()}以下の立ち絵保存フォルダパス")
                    character_image = gr.Image(label="立ち絵", width=100, height=300)
                profile_edit_result = gr.Text()

            # 番組編集セクション
            with gr.Tab("番組編集") as program_section:
                with gr.Row():
                    gr.Markdown("## 番組編集")
                with gr.Row():
                    program_selector = gr.Dropdown(choices=self._get_program_names_list(), label="編集する番組を選択", allow_custom_value=True)
                    program_edit_button = gr.Button("呼び出し")
                with gr.Row():
                    program_name_ = gr.Textbox(label="番組名")
                    user_additional_data1_name = gr.Textbox(label="追加データ1の名前")
                    user_additional_data2_name = gr.Textbox(label="追加データ2の名前")

            # 動画作成セクション
            with gr.Tab("動画作成") as video_section:
                with gr.Row():
                    gr.Markdown("## 動画作成")
                with gr.Row():
                    debug_mode = gr.Checkbox(label="デバッグモード", value=True)
                    program_name = gr.Dropdown(choices=self._get_program_names_list(), label="番組名")
                    streamer_num = gr.Radio(label="実況人数", choices=[1, 2], value=2)
                with gr.Row():
                    title = gr.Textbox(label="動画タイトル(全角文字やファイルパスに使えない文字は使用不可)")
                with gr.Accordion("番組追加情報", visible=True):
                    user_additional_data1 = gr.Textbox()
                    user_additional_data2 = gr.Textbox()
                with gr.Row():
                    streamer1_dropdown = gr.Dropdown(choices=self._get_streamers_list(), label="ストリーマー1")
                    streamer1_profile = gr.TextArea(label="プロフィール")
                    streamer2_dropdown = gr.Dropdown(choices=self._get_streamers_list(), label="ストリーマー2")
                    streamer2_profile = gr.TextArea(label="プロフィール")
                with gr.Accordion("詳細設定", open=False):
                    open_ai_api_key = gr.Textbox(label="OpenAI APIキー")
                with gr.Row():
                    create_video_button = gr.Button("動画作成開始")
                    video_output = gr.Video(label="生成された動画")
                    video_output_path = gr.Text(label="動画URL")
            
            # TTS接続確認ボタンのアクション
            tts_check_button.click(fn=self._check_and_reset_tts_connection, inputs=[], outputs=[status_text, tts_chara])

            # ストリーマー選択時の編集ボタンアクション
            streamer_edit_button.click(fn=self._set_streamer_info, inputs=streamer_selector, outputs=[name, stage_name, tts_chara, color, personality, speaking_style, character_images_directory, character_image])

            # プロフィール更新ボタンのアクション
            update_profile_button.click(
                fn=self._update_streamer_profile,
                inputs=[name, tts_chara, stage_name, color, personality, speaking_style, character_images_directory],
                outputs=profile_edit_result,
            )
            # プロフィール保存ボタンのアクション
            insert_profile_button.click(
                fn=self._insert_streamer_profile,
                inputs=[name, tts_chara, stage_name, color, personality, speaking_style, character_images_directory],
                outputs=[profile_edit_result, streamer_selector, streamer1_dropdown, streamer2_dropdown]
            )

            # 番組選択時の編集ボタンアクション
            program_edit_button.click(fn=self._set_program_info, inputs=program_selector, outputs=[program_name_, user_additional_data1_name, user_additional_data2_name])

            # 番組名選択時のプログラム情報表示アクション
            program_name.change(self._change_program, inputs=program_name, outputs=[user_additional_data1, user_additional_data2])

            # ストリーマー選択時のプロフィール表示アクション
            streamer1_dropdown.input(self._get_streamer_profile, inputs=streamer1_dropdown, outputs=streamer1_profile)
            streamer2_dropdown.input(self._get_streamer_profile, inputs=streamer2_dropdown, outputs=streamer2_profile)

            # 動画作成ボタンのアクション
            create_video_button.click(
                fn=self._create_video,
                inputs=[debug_mode, streamer1_dropdown, streamer2_dropdown, streamer_num, program_name, title, user_additional_data1, user_additional_data2],
                outputs=[video_output, video_output_path]
            )

    # 接続状況を確認する関数
    def _check_and_reset_tts_connection(self):
        tts_status = VoiceGenerator.reset_tts()

        return self._make_tts_connection_text(tts_status), gr.update(choices=self._get_tts_speakers())
    
    # TTS接続状況をテキストに変換する
    def _make_tts_connection_text(self, tts_status):
        statuses = []
        for app_name, is_connected in tts_status:
            status = "接続済み" if is_connected else "未接続"
            statuses.append(f"{app_name}: {status}")
        return "\n".join(statuses)

    # データベースからストリーマーの一覧を取得する
    def _get_streamers_list(self):
        with model.session_scope() as session:
            streamers = session.query(model.StaticStreamerProfile).all()
            return [s.name for s in streamers]

    # ストリーマー情報をUIにセットする
    def _set_streamer_info(self, streamer_selector):
        streamer_info = self._get_streamer_info(streamer_selector)
        name = streamer_info["name"]
        stage_name = streamer_info["stage_name"]
        tts_chara = streamer_info["tts_chara"]
        color = streamer_info["color"]
        personality = streamer_info["personality"]
        speaking_style = streamer_info["speaking_style"]
        character_images_directory = streamer_info["character_images_directory"]
        output_image_path = f"{DATA_FOLDER}/{character_images_directory}/normal.png"
        return name, stage_name, tts_chara, color, personality, speaking_style, character_images_directory, output_image_path

    # データベースから特定のストリーマー情報を取得する
    def _get_streamer_info(self, name):
        with model.session_scope() as session:
            streamer = session.query(model.StaticStreamerProfile).filter(model.StaticStreamerProfile.name == name).first()
            return {
                "name": streamer.name,
                "stage_name": streamer.stage_name,
                "tts_chara": streamer.tts_chara,
                "color": streamer.color,
                "personality": streamer.personality,
                "speaking_style": streamer.speaking_style,
                "character_images_directory": streamer.character_images_directory
            }

    # データベースから番組情報をUIにセットする
    def _set_program_info(self, program_selector):
        with model.session_scope() as session:
            program = session.query(model.ProgramType).filter(model.ProgramType.program_name == program_selector).first()
            program_name = program.program_name
            user_additional_data1_name = program.user_additional_data1_name
            user_additional_data2_name = program.user_additional_data2_name
            return program_name, user_additional_data1_name, user_additional_data2_name

    def _get_streamer_profile(self, streamer_name):
        info = self._get_streamer_info(streamer_name)
        profile = ""
        for key, value in info.items():
            profile += f"{key}: {value}\n"
        return profile

    # データベースからTTS話者の名前を取得する
    def _get_tts_speakers(self):
        with model.session_scope() as session:
            # VoiceVoxの話者を取得
            voicevox_speakers = session.query(model.VoiceVoxSpeaker).all()
            tts_speakers = [s.speaker_name for s in voicevox_speakers]

            # StyleBertVITS2の話者を取得
            stylebertvits2_speakers = session.query(model.StyleBertVITS2Speaker).all()
            tts_speakers += [s.speaker_name for s in stylebertvits2_speakers]

            # 重複を除去しつつ順序を保持
            unique_tts_speakers = []
            seen = set()
            for speaker in tts_speakers:
                if speaker not in seen:
                    unique_tts_speakers.append(speaker)
                    seen.add(speaker)

            return unique_tts_speakers

    # データベースのストリーマープロフィールを更新する
    def _update_streamer_profile(self, name, stage_name, tts_chara, color, personality, speaking_style, character_images_directory):
        with model.session_scope() as session:
            streamer = session.query(model.StaticStreamerProfile).filter(model.StaticStreamerProfile.name == name).first()
            if streamer is None:
                return f"{name}のプロフィールは存在しません"
            else:
                streamer.stage_name = stage_name
                streamer.tts_chara = tts_chara
                streamer.color = color
                streamer.personality = personality
                streamer.speaking_style = speaking_style
                streamer.character_images_directory = character_images_directory
                session.commit()
                return f"{name}のプロフィールを更新しました"
            
    # データベースにストリーマープロフィールを保存する
    def _insert_streamer_profile(self, name, stage_name, tts_chara, color, personality, speaking_style, character_images_directory):
        with model.session_scope() as session:
            streamer = session.query(model.StaticStreamerProfile).filter(model.StaticStreamerProfile.name == name).first()
            if streamer is not None:
                return f"{name}のプロフィールは既に存在します"
            else:
                streamer = model.StaticStreamerProfile(
                    name=name,
                    stage_name=stage_name,
                    tts_chara=tts_chara,
                    color=color,
                    personality=personality,
                    speaking_style=speaking_style,
                    character_images_directory=character_images_directory
                )
                session.add(streamer)
                session.commit()
                return f"{name}のプロフィールを保存しました", gr.update(choices=self._get_streamers_list()), gr.update(choices=self._get_streamers_list()), gr.update(choices=self._get_streamers_list())

    # 
    def _change_program(self, program_name):
        with model.session_scope() as session:
            program = session.query(model.ProgramType).filter(model.ProgramType.program_name == program_name).first()
            return gr.update(label=program.user_additional_data1_name), gr.update(label=program.user_additional_data2_name)
        
    def _get_program_names_list(self):
        with model.session_scope() as session:
            programs = session.query(model.ProgramType).all()
            return [p.program_name for p in programs]
        
    # 動画を作成する
    def _create_video(self, debug_mode, streamer1_name, streamer2_name, streamer_num, program_name, title, user_additional_data1, user_additional_data2):
        # 動画情報をデータベースに登録
        title = self._set_video_info(title, program_name, user_additional_data1, user_additional_data2)
        if title == "":
            return "すでにそのタイトルの動画が存在します"

        # ストリーマーをデータベースに登録
        self._set_streamers_info(streamer1_name, streamer2_name, streamer_num, title)

        # 動画を作成
        self.studio.initialize_project(title, debug_mode)
        video_path = self.studio.create_video()
        formatted_path = Path(video_path).resolve().as_posix()
        return formatted_path, formatted_path
    
    def _set_video_info(self, title, program_name, user_additional_data1, user_additional_data2):
        # タイトルに時間を追加して重複を防ぐ
        title += time.strftime('_%Y%m%d_%H%M%S', time.localtime())
        with model.session_scope() as session:
            # すでにそのタイトルの動画が存在する場合はエラー
            if session.query(model.Video).filter(model.Video.video_title == title).first() is not None:
                return ""
            
            # 動画情報をデータベースに登録
            video = model.Video(
                program_name=program_name,
                video_title=title,
                user_additional_data1=user_additional_data1,
                user_additional_data2=user_additional_data2
            )
            session.add(video)
       
        return title
    
    def _set_streamers_info(self, streamer1_name, streamer2_name, streamer_num, title):
        streamer2_name = "" if streamer_num == 1 else streamer2_name
        partner_names = [streamer2_name, streamer1_name]
        for index, streamer in enumerate([streamer1_name, streamer2_name]):
            if streamer == "":
                continue
            with model.session_scope() as session:
                streamer_profile = session.query(model.StaticStreamerProfile).filter(model.StaticStreamerProfile.name == streamer).first()
                if streamer_profile is None:
                    return f"{streamer}のプロフィールが存在しません"
                else:
                    streamer_profile = model.StreamerProfile(
                        video_title=title,
                        name=streamer_profile.name,
                        stage_name=streamer_profile.stage_name,
                        tts_chara=streamer_profile.tts_chara,
                        color=streamer_profile.color,
                        role = self._get_role(index, streamer_num),
                        personality=streamer_profile.personality,
                        speaking_style=streamer_profile.speaking_style,
                        partner_name=partner_names[index],
                        character_images_directory=streamer_profile.character_images_directory
                    )
                    session.add(streamer_profile)
                    session.commit()

    def _get_role(self, index, streamer_num):
        if streamer_num == 1:
            return Role.SOLO_VIDEO_HOST.value
        else:
            return Role.DUO_VIDEO_HOST.value if index == 0 else Role.DUO_VIDEO_GUEST.value

    def launch(self):
        self.interface.launch(inbrowser=True)

# Gradioのインターフェースを作成し、起動する
if __name__ == "__main__":
    app = WebUI()
    app.launch()

def webui():
    app = WebUI()
    app.launch()
    return app.interface