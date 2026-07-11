"""Video kesme ve birleştirme (ffmpeg, yeniden kodlamasız).

Kesme: -ss/-to giriş seçenekleriyle stream copy — anahtar kareye yaslanır,
saniyeler içinde biter. Birleştirme: concat demuxer ile; klipler aynı
codec/çözünürlükte olmalıdır (aynı kaynaktan kesilen parçalar idealdir).
"""

import os
import subprocess
import tempfile
import time

from core.utils import get_ffmpeg_path


def _run(cmd):
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    res = subprocess.run(cmd, capture_output=True, creationflags=flags)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.decode("utf-8", "ignore")[-400:])


def cut_video(path, start, end, output_dir):
    """Videodan [start, end] aralığını keser; süreler '00:01:05' ya da '65' biçiminde."""
    name, ext = os.path.splitext(os.path.basename(path))
    out = os.path.join(output_dir, f"{name}_kesit{ext}")
    cmd = [get_ffmpeg_path(), "-y", "-ss", str(start), "-to", str(end),
           "-i", path, "-c", "copy", out]
    _run(cmd)
    return out


def merge_videos(paths, output_dir):
    """Videoları verilen sırayla tek dosyada birleştirir."""
    if len(paths) < 2:
        raise ValueError("Birleştirme için en az 2 video gerekir.")
    first = os.path.splitext(os.path.basename(paths[0]))[0]
    out = os.path.join(output_dir, f"{first}_birlesik_{int(time.time())}.mp4")

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for p in paths:
            escaped = os.path.abspath(p).replace("'", "'\\''")
            f.write(f"file '{escaped}'\n")
        listfile = f.name
    try:
        cmd = [get_ffmpeg_path(), "-y", "-f", "concat", "-safe", "0",
               "-i", listfile, "-c", "copy", out]
        _run(cmd)
    finally:
        try:
            os.unlink(listfile)
        except OSError:
            pass
    return out
