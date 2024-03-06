from audio import VoiceGenerator
from config import Session, engine
from model import Base, CueSheet, ProgramType, StaticSection, StaticStreamerProfile, SerifSystemPrompt
from static_data import CUE_SHEETS, PROGRAM_TYPES, SERIF_SYSTEM_PROMPTS, STATIC_SECTIONS, STATIC_STREAMER_PROFILES_DATA

def initialize_database():
    # データベースの初期化
    Base.metadata.create_all(engine)
    session = Session()
    tts_status = None
    
    # 静的データとモデルクラスのマッピング
    static_data_mappings = {
        StaticStreamerProfile: STATIC_STREAMER_PROFILES_DATA,
        ProgramType: PROGRAM_TYPES,
        StaticSection: STATIC_SECTIONS,
        SerifSystemPrompt: SERIF_SYSTEM_PROMPTS,
        CueSheet: CUE_SHEETS
    }
    # 共通メソッドを使用して静的データを挿入
    for model_class, data_list in static_data_mappings.items():
        _insert_static_data(session, model_class, data_list)
    
    # TTSの初期化
    tts_status = VoiceGenerator.reset_tts()
    
    session.close()
    return tts_status

def _insert_static_data(session, model_class, data_list):
    if session.query(model_class).count() == 0:
        for data in data_list:
            model_instance = model_class(**data)
            session.add(model_instance)
        session.commit()
