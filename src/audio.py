import model
import uuid
import wave
import contextlib
import requests
from config import Session
from model import VoiceVoxSpeaker

class VoiceGenerator:
    def __init__(self):
        self.voicevox_client = VOICEVOX_client()

    @staticmethod
    def set_tts():
        VOICEVOX_client().set_data()
    
    @staticmethod
    def is_tts_set():
        with model.session_scope() as session:
            return session.query(VoiceVoxSpeaker).count() > 0

    def generate_voice_from_text(self, save_falder, file_number, text: str, voicevox_chara, voice_paramater) -> str:
        content, ttsid = self.voicevox_client.generate_voice_from_text(text, voicevox_chara, voice_paramater)
        return self._save_voice(content, text, voicevox_chara, ttsid, save_falder, file_number)

    def _save_voice(self, content, text, voicevox_chara, vvid, save_falder, file_number):
        # 入力テキストの先頭10文字を取得（10文字未満の場合はそのまま使用）
        text_preview = text[:10]
        # ファイル名を生成
        filename = f'{save_falder}/temp/{file_number}_{voicevox_chara}_{vvid}_{text_preview}_{uuid.uuid4()}.wav'
        with open(filename, 'wb') as f:
            f.write(content)  # ファイルに音声データを書き込み
        return filename
        
    def get_style_list(self, voicevox_chara):
        return VOICEVOX_client.get_style_list(voicevox_chara)

    # wavファイルの再生時間（秒）を返す。
    def get_audio_duration(wav_filename: str) -> float:
        # waveファイルを開いて、フレーム数とフレームレートを取得
        with contextlib.closing(wave.open(wav_filename, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return frames / rate  # 再生時間を秒単位で計算

vv_api_url = 'http://127.0.0.1:50021'  # VOICEVOX Engineのエンドポイント
class VOICEVOX_client:
    @staticmethod
    def set_data():

        # 話者情報を取得する
        response = requests.get(f"{vv_api_url}/speakers")
        speakers = response.json()

        # データベースに保存する
        for speaker in speakers:
            speaker_name = speaker["name"]
            for style in speaker["styles"]:
                style_name = style["name"]
                style_id = style["id"]
                voicevox_speaker = VoiceVoxSpeaker(speaker_name=speaker_name, style_name=style_name, style_id=style_id)
                with model.session_scope() as session:
                    session.add(voicevox_speaker)

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
            if filtered_data is not None:
                return speaker_filtered_data.style_id
            else:
                # 一致する話者がいない場合はNoneを返す
                return None

    def _create_audio_query(self, text: str, vvid) -> dict:
        # テキストからオーディオクエリを生成し、APIにポスト
        params = {'text': text, 'speaker': vvid}
        response = requests.post(f'{vv_api_url}/audio_query', params=params)
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
            f'{vv_api_url}/synthesis',
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



