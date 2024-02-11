import datetime
import json
import time
import uuid
import wave
import contextlib
import requests
import pandas as pd
from config import VOICEVOX_VVID_DATA_CSV

class VoiceGenerator:
    def __init__(self):
        self.api_url = 'http://127.0.0.1:50021'  # APIのURL

    def generate_voice_from_text(self, save_falder, file_number, text: str, voicevox_chara, voice_paramater) -> str:
        # CSVファイルから使用するvvidを取得
        vvid = VoiceVOXDataSingleton.get_instance().get_vvid(voicevox_chara, voice_paramater["voice_style"])
        # テキストから音声ファイルを生成
        audio_query_response = self._create_audio_query (text, vvid)
        content = self._synthesize_voice(audio_query_response, vvid, voice_paramater)
        return self._save_voice(content, text, voicevox_chara, vvid, save_falder, file_number)

    def _create_audio_query(self, text: str, vvid) -> dict:
        # テキストからオーディオクエリを生成し、APIにポスト
        params = {'text': text, 'speaker': vvid}
        response = requests.post(f'{self.api_url}/audio_query', params=params)
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
            f'{self.api_url}/synthesis',
            json=audio_query_response,
            params=params,
            headers=headers
        )
        response.raise_for_status()  # ネットワークエラーをチェック
        return response.content

    def _save_voice(self, content, text, voicevox_chara, vvid, save_falder, file_number):
        # 入力テキストの先頭10文字を取得（10文字未満の場合はそのまま使用）
        text_preview = text[:10]
        # ファイル名を生成
        filename = f'{save_falder}/temp/{file_number}_{voicevox_chara}_{vvid}_{text_preview}_{uuid.uuid4()}.wav'
        with open(filename, 'wb') as f:
            f.write(content)  # ファイルに音声データを書き込み
        return filename
        
    def get_style_list(self, voicevox_chara):
        return VoiceVOXDataSingleton.get_instance().get_style_list(voicevox_chara)

    # wavファイルの再生時間（秒）を返す。
    def get_audio_duration(wav_filename: str) -> float:
        # waveファイルを開いて、フレーム数とフレームレートを取得
        with contextlib.closing(wave.open(wav_filename, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return frames / rate  # 再生時間を秒単位で計算

class VoiceVOXDataSingleton:
    _instance = None
    vvid_data = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.vvid_data = cls._load_csv()
        return cls._instance

    @staticmethod
    def _load_csv():
        # CSVファイルを読み込むロジック
        return pd.read_csv(VOICEVOX_VVID_DATA_CSV)

    def get_vvid(self, speaker_name, style_name):
        # 指定された話者名とスタイル名に基づいてデータをフィルタリング
        filtered_data = self.vvid_data[(self.vvid_data['speaker_name'] == speaker_name) & (self.vvid_data['style_name'] == style_name)]

        # 指定された条件に一致するデータが見つかった場合
        if not filtered_data.empty:
            return filtered_data.iloc[0]['style_id']
        else:
            # 指定された話者名に基づいて再フィルタリング
            speaker_filtered_data = self.vvid_data[self.vvid_data['speaker_name'] == speaker_name]
            # 話者名に一致するデータが存在する場合、その最初のスタイルIDを返す
            if not speaker_filtered_data.empty:
                return speaker_filtered_data.iloc[0]['style_id']
            else:
                # 一致する話者がいない場合はNoneを返す
                return None

        
    def get_style_list(self, speaker_name):
        # 指定されたスピーカーのスタイル名を抽出
        filtered_data = self.vvid_data[self.vvid_data['speaker_name'] == speaker_name]
        # スタイル名のリストを返す
        return filtered_data['style_name'].tolist()





