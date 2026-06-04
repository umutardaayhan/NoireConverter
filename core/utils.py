import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
    # 1. PyInstaller bundle içinde ara (exe olarak paketlendiğinde)
    try:
        meipass_ffmpeg = os.path.join(sys._MEIPASS, "ffmpeg.exe")
        if os.path.exists(meipass_ffmpeg):
            return meipass_ffmpeg
    except AttributeError:
        pass
    # 2. Proje kök dizininde ara
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_ffmpeg = os.path.join(base_dir, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    # 3. Çalışma dizininde ara
    if os.path.exists("ffmpeg.exe"):
        return "ffmpeg.exe"
    # 4. Sistem PATH'inde ffmpeg
    return "ffmpeg"

