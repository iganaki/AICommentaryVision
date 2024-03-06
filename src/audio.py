import csv
import os
import model
import utils
import uuid
import wave
import contextlib
import requests
from config import DATA_FOLDER, Session
from model import VoiceVoxSpeaker, StyleBertVITS2Speaker

class VoiceGenerator:
    def __init__(self):
        self.voicevox_client = VOICEVOX_client()
        self.stylebertvits2_client = StyleBertVITS2_client()

    @staticmethod
    def reset_tts():
        return (("VoiceVox", VOICEVOX_client().reset_data()), ("Style-Bert-VITS2", StyleBertVITS2_client().reset_data()))

    @staticmethod
    def is_tts_set():
        with model.session_scope() as session:
            return session.query(VoiceVoxSpeaker).count() > 0 or session.query(StyleBertVITS2Speaker).count() > 0

    def generate_voice_from_text(self, save_falder, file_number, text: str, tts_chara, voice_paramater) -> str:
        # キャラ名からTTSクライアントを選択
        tts_cliant = self.voicevox_client if tts_chara in self.voicevox_client.get_speaker_list() else self.stylebertvits2_client
        # テキストから音声を生成
        content, ttsid = tts_cliant.generate_voice_from_text(text, tts_chara, voice_paramater)
        return self._save_voice(content, text, tts_chara, ttsid, save_falder, file_number)

    def _save_voice(self, content, text, tts_chara, vvid, save_falder, file_number):
        # 入力テキストの先頭10文字を取得（10文字未満の場合はそのまま使用）
        text_preview = text[:10]
        # ファイル名を生成
        filename = f'{save_falder}/temp/{file_number}_{tts_chara}_{vvid}_{text_preview}_{uuid.uuid4()}.wav'
        filename = utils.sanitize_filename(filename)

        with open(filename, 'wb') as f:
            f.write(content)  # ファイルに音声データを書き込み
        return filename
        
    def get_style_list(self, tts_chara):
        return VOICEVOX_client.get_style_list(tts_chara)

    # wavファイルの再生時間（秒）を返す。
    def get_audio_duration(wav_filename: str) -> float:
        # waveファイルを開いて、フレーム数とフレームレートを取得
        with contextlib.closing(wave.open(wav_filename, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return frames / rate  # 再生時間を秒単位で計算

VOICEVOX_api_url = 'http://127.0.0.1:50021'  # VOICEVOX Engineのエンドポイント
class VOICEVOX_client:
    @staticmethod
    def reset_data():
        #  データベースを削除する
        with model.session_scope() as session:
            VoiceVoxSpeaker.delete_voicevox_speakers_table(session)

        # 話者情報を取得する
        try:
            response = requests.get(f"{VOICEVOX_api_url}/speakers")
            # ステータスコードが200以外の場合、エラーを発生させる
            response.raise_for_status()
            speakers = response.json()
        except requests.exceptions.HTTPError as http_err:
            # HTTPエラーが発生した場合、エラーメッセージを表示
            print(f"HTTP error occurred: {http_err}")
            return False
        except requests.exceptions.ConnectionError as conn_err:
            # 接続エラーが発生した場合、エラーメッセージを表示
            print(f"VOICEVOXが起動していません")
            return False
        except requests.exceptions.Timeout as timeout_err:
            # タイムアウトエラーが発生した場合、エラーメッセージを表示
            print(f"Timeout error occurred: {timeout_err}")
            return False
        except requests.exceptions.RequestException as req_err:
            # その他のリクエストエラーが発生した場合、エラーメッセージを表示
            print(f"An error occurred: {req_err}")
            return False

        # データベースに保存する
        with model.session_scope() as session:
            VoiceVoxSpeaker.set_voicevox_speakers_table(session, speakers)
        return True
    
    def get_speaker_list(self):
        with model.session_scope() as session:
            speakers = session.query(VoiceVoxSpeaker).all()
            return [s.speaker_name for s in speakers]

    def generate_voice_from_text(self, text: str, voicevox_chara, voice_paramater) -> str:
        vvid = self._get_vvid(voicevox_chara, voice_paramater["voice_style"])
        audio_query_response = self._create_audio_query(text, vvid)
        content = self._synthesize_voice(audio_query_response, vvid, voice_paramater)
        return content, vvid

    def _get_vvid(self, speaker_name, style_name):
        session = Session()
        # 指定された話者名とスタイル名に基づいてデータをフィルタリング
        filtered_data = session.query(VoiceVoxSpeaker).filter_by(speaker_name=speaker_name, style_name=style_name).first()

        # 指定された条件に一致するデータが見つかった場合
        if filtered_data is not None:
            return filtered_data.style_id
        else:
            # 指定された話者名に基づいて再フィルタリング
            speaker_filtered_data = session.query(VoiceVoxSpeaker).filter_by(speaker_name=speaker_name).first()
            # 話者名に一致するデータが存在する場合、その最初のスタイルIDを返す
            if speaker_filtered_data is not None:
                return speaker_filtered_data.style_id
            else:
                # 一致する話者がいない場合はNoneを返す
                print(f"話者名{speaker_name}に一致するデータが見つかりませんでした")
                return None

    def _create_audio_query(self, text: str, vvid) -> dict:
        # テキストからオーディオクエリを生成し、APIにポスト
        params = {'text': text, 'speaker': vvid}
        response = requests.post(f'{VOICEVOX_api_url}/audio_query', params=params)
        if response.status_code == 422:
            json_data = response.json()
            print(json_data)
            print(f"text: {text}, speaker: {vvid}")
        response.raise_for_status()  # ネットワークエラーをチェック
        return response.json()  # レスポンスをJSON形式で返す

    def _synthesize_voice(self, audio_query_response: dict, vvid, voice_paramater) -> str:
        # オーディオクエリに速度スケールを追加
        audio_query_response['speedScale'] = voice_paramater["voice_speed"] + 0.1
        audio_query_response['pitchScale'] = (float(voice_paramater["voice_pitch"]) - 1.0) / 2.0

        params = {'speaker': vvid}
        headers = {'content-type': 'application/json'}
        response = requests.post(
            f'{VOICEVOX_api_url}/synthesis',
            json=audio_query_response,
            params=params,
            headers=headers
        )
        response.raise_for_status()  # ネットワークエラーをチェック
        return response.content

    @staticmethod    
    def get_style_list(speaker_name):
        # 指定されたスピーカーのスタイル名をデータベースから抽出
        with model.session_scope() as session:
            filtered_data = session.query(VoiceVoxSpeaker).filter(VoiceVoxSpeaker.speaker_name == speaker_name).all()
            style_list = [speaker.style_name for speaker in filtered_data]
        # スタイル名のリストを返す
        return style_list
    
    @staticmethod
    def make_csv_voicevox_speaker_list():
        # 話者情報を取得する
        response = requests.get(f"{VOICEVOX_api_url}/speakers")
        speakers = response.json()

        # CSVファイルに保存する
        csv_file = os.path.join(DATA_FOLDER, 'voicevox_speakers.csv')

        with open(csv_file, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["話者名", "スタイル名", "スタイルID"])  # ヘッダー行を書き込む

            for speaker in speakers:
                speaker_name = speaker["name"]
                for style in speaker["styles"]:
                    style_name = style["name"]
                    style_id = style["id"]
                    writer.writerow([speaker_name, style_name, style_id])

StyleBertVITS2_api_url = 'http://127.0.0.1:5000'
class StyleBertVITS2_client:
    @staticmethod
    def reset_data():
        # データベースを削除する
        with model.session_scope() as session:
            StyleBertVITS2Speaker.delete_stylebertvits2_speakers_table(session)
            
        # 話者情報を取得する
        try:
            response = requests.get(f"{StyleBertVITS2_api_url}/models/info")
            speakers = response.json()
        except requests.exceptions.HTTPError as http_err:
            # HTTPエラーが発生した場合、エラーメッセージを表示
            print(f"HTTP error occurred: {http_err}")
            return False
        except requests.exceptions.ConnectionError as conn_err:
            # 接続エラーが発生した場合、エラーメッセージを表示
            print(f"Style-Bert-VITS2が起動していません")
            return False
        except requests.exceptions.Timeout as timeout_err:
            # タイムアウトエラーが発生した場合、エラーメッセージを表示
            print(f"Timeout error occurred: {timeout_err}")
            return False
        except requests.exceptions.RequestException as req_err:
            # その他のリクエストエラーが発生した場合、エラーメッセージを表示
            print(f"An error occurred: {req_err}")
            return False
        
        # データベースに保存する
        with model.session_scope() as session:
            StyleBertVITS2Speaker.set_stylebertvits2_speakers_table(session, speakers)

    def generate_voice_from_text(self, text: str, speaker_name: str, voice_parameter: dict) -> bytes:
        # スピーカー名とスタイルに基づいてパラメータを設定
        params = self._prepare_parameters(text, speaker_name, voice_parameter)
        
        # 音声を合成
        content = self._synthesize_voice(params)
        return content

    def _prepare_parameters(self, text, speaker_name, voice_parameter):
        # Style-Bert-VITS2に合わせたパラメータ設定
        params = {
            'text': text,
            'speaker_name': speaker_name,
            'style': voice_parameter.get('style', 'Neutral'),  # スタイル（感情）を設定
            'style_weight': voice_parameter.get('style_weight', 5.0),  # スタイルの強さ
            'length': voice_parameter.get('length', 1.0),  # 話速
            # その他パラメータも同様に設定可能
        }
        return params

    def _synthesize_voice(self, params):
        # Style-Bert-VITS2の音声合成APIエンドポイントへリクエスト
        response = requests.get(f'{StyleBertVITS2_api_url}/voice', params=params)
        if response.status_code == 200:
            return response.content
        else:
            # エラー処理
            response.raise_for_status()