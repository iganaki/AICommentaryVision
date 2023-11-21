import datetime
import uuid
import wave
import contextlib
import requests
from config import TEMP_FOLDER

class VoiceGenerator:
    def __init__(self, vvid: int = 1, speedScale: float = 1.2):
        self._counter = 0  # ファイル名に使用する連番
        self.vvid = vvid  # 音声のバリエーションを管理するID
        self.speedScale = speedScale  # 音声の速度
        self.api_url = 'http://127.0.0.1:50021'  # APIのURL

    def generate_voice_from_text(self, text: str) -> str:
        self._counter += 1  # 連番をインクリメント
        # テキストから音声ファイルを生成
        audio_query_response = self._create_audio_query (text)
        return self._synthesize_voice(audio_query_response, text)

    def _create_audio_query (self, text: str) -> dict:
        # テキストからオーディオクエリを生成し、APIにポスト
        params = {'text': text, 'speaker': self.vvid}
        response = requests.post(f'{self.api_url}/audio_query', params=params)
        response.raise_for_status()  # ネットワークエラーをチェック
        return response.json()  # レスポンスをJSON形式で返す

    def _synthesize_voice(self, audio_query_response: dict, text) -> str:
        # オーディオクエリに速度スケールを追加
        audio_query_response['speedScale'] = self.speedScale

        params = {'speaker': self.vvid}
        headers = {'content-type': 'application/json'}
        response = requests.post(
            f'{self.api_url}/synthesis',
            json=audio_query_response,
            params=params,
            headers=headers
        )
        response.raise_for_status()  # ネットワークエラーをチェック
        # 入力テキストの先頭10文字を取得（10文字未満の場合はそのまま使用）
        text_preview = text[:10]
        # ファイル名を生成
        filename = f'{TEMP_FOLDER}/{self._counter}_{self.vvid}_{text_preview}_{uuid.uuid4()}.wav'
        with open(filename, 'wb') as f:
            f.write(response.content)  # ファイルに音声データを書き込み
        return filename

def get_audio_duration(wav_filename: str) -> float:
    """
    指定されたwavファイルの再生時間（秒）を返します。

    :param wav_filename: 再生時間を計算する.wavファイルのパス
    :return: 音声ファイルの再生時間（秒）
    """
    # waveファイルを開いて、フレーム数とフレームレートを取得
    with contextlib.closing(wave.open(wav_filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / rate  # 再生時間を秒単位で計算
