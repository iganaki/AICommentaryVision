import os
import re

def sanitize_filename(path):
    # OSに適したパス区切り文字に統一
    path = os.path.normpath(path)
    
    # ファイル名とディレクトリ名を分離
    directory, filename = os.path.split(path)
    
    # 不適切な文字をアンダースコアに置換（ここでは例としてWindowsの禁止文字を示す）
    filename = re.sub(r'[\\/*?:"<>|\n]', '_', filename)
    
    # ファイル名の長さがOSの制限内に収まるように調整（例としてWindowsの最大長255を仮定）
    max_length = 255
    if len(filename) > max_length:
        # 拡張子を保持しつつ、必要に応じてファイル名を短縮
        root, ext = os.path.splitext(filename)
        filename = root[:max_length-len(ext)-1] + ext
    
    # サニタイズされたファイル名でパスを再構成
    sanitized_path = os.path.join(directory, filename)
    
    return sanitized_path