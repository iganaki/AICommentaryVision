class OBSController:
    def __init__(self):
        # Initialize OBS connection here
        load_dotenv()
        password = os.environ.get('OBS_WS_PASSWORD')
        host = os.environ.get('OBS_WS_HOST')
        port = os.environ.get('OBS_WS_PORT')
        # 設定されていない場合はエラー
        if(password == None or host == None or port ==None):
            raise Exception("OBSの設定がされていません")
        self.ws = obs.ReqClient(host=host, port=port, password=password)

    def start_streaming(self):
        # Code to start streaming in OBS
        pass

    def stop_streaming(self):
        # Code to stop streaming in OBS
        pass

    def set_scene(self, scene_name):
        # Code to set the active scene in OBS
        pass

    def set_source_visibility(self, source_name, visibility):
        # Code to set the visibility of a source in OBS
        pass

# Usage example:
obs = OBSController()
obs.start_streaming()
obs.set_scene("Main Scene")
obs.set_source_visibility("Webcam", True)


import obsws_python as obs
import os
from dotenv import load_dotenv
class OBSAdapter:
    def __init__(self) -> None:
        load_dotenv()
        password = os.environ.get('OBS_WS_PASSWORD')
        host = os.environ.get('OBS_WS_HOST')
        port = os.environ.get('OBS_WS_PORT')
        # 設定されていない場合はエラー
        if(password == None or host == None or port ==None):
            raise Exception("OBSの設定がされていません")
        self.ws = obs.ReqClient(host=host, port=port,password=password)
    def set_question(self, text: str):
        self.ws.set_input_settings(name="Question",settings={"text": text},overlay=True)
    def set_answer(self, text: str):
        self.ws.set_input_settings(name="Answer",settings={"text": text},overlay=True)
    # fileを直接指定したとき
if __name__ == '__main__':
    obsAdapter = OBSAdapter()
    import random
    question_text = "Qustionの番号は" + str(random.randint(0,100)) + "になりました"
    obsAdapter.set_question(question_text)
    answer_text = "Answerの番号は" + str(random.    randint(0,100)) + "になりました"
    obsAdapter.set_answer(answer_text)