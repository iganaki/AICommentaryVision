import datetime
import wave
import contextlib
import requests
import json
import wave
from config import TEMP_FOLDER

def get_audio_duration(wav_filename):
    """
    指定されたwavファイルの再生時間（秒）を返します。

    :param wav_filename: 再生時間を計算する.wavファイルのパス
    :return: 音声ファイルの再生時間（ミリ秒）
    """
    with contextlib.closing(wave.open(wav_filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration_sec = frames / float(rate)
        return duration_sec

def post_audio_query(text: str, vvid = 1) -> dict:
    params = {'text': text, 'speaker': vvid}
    res = requests.post('http://127.0.0.1:50021/audio_query', params=params)
    return res.json()

def post_synthesis(audio_query_response: dict, vvid = 1) -> bytes:
    params = {'speaker': vvid, "speedScale": 1.3}
    headers = {'content-type': 'application/json'}
    audio_query_response_json = json.dumps(audio_query_response)
    res = requests.post(
        'http://127.0.0.1:50021/synthesis',
        data=audio_query_response_json,
        params=params,
        headers=headers
    )
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f'{TEMP_FOLDER}/audio_vvid{vvid}_{timestamp}.wav'
    with open(filename, mode='wb') as f:
        f.write(res.content)

    return filename

def generate_audio_from_text(text: str, vvid = 1):
    res = post_audio_query(text, vvid)
    wav_file = post_synthesis(res, vvid)
    return wav_file