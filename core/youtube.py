"""Sosyal medya -> MP3/M4A/MP4 indirme motoru (yt-dlp).

YouTube, Instagram, TikTok ve X (Twitter) linklerini destekler; metin
girilirse YouTube'da arama yapılır. Noire_Mp3 projesinden uyarlanmıştır.
UI bu modülü arka plan thread'i içinden çağırır; ilerleme bilgisi
progress_cb geri çağrısıyla iletilir.
"""

import os
import re
from pathlib import Path

from yt_dlp import YoutubeDL

from core.utils import get_ffmpeg_path

BASE_DIR = Path(__file__).resolve().parent.parent
# Yaş kısıtlamalı videolar için: tarayıcıdan dışa aktarılan cookies.txt proje köküne konur
COOKIE_FILE = BASE_DIR / "cookies.txt"

AUDIO_QUALITIES = {"128", "192", "320", "m4a"}
VIDEO_QUALITIES = {"480p", "720p", "1080p", "best"}
_VIDEO_HEIGHTS = {"480p": 480, "720p": 720, "1080p": 1080}

MAX_PLAYLIST = 50  # Mix/radyo listeleri sonsuz olabilir; güvenli üst sınır
PLAYLIST_RE = re.compile(r"[?&]list=|/playlist\b", re.IGNORECASE)

# Desteklenen platformlar ve URL kalıpları (yt-dlp extractor'ları hepsini tanır)
PLATFORMS = {
    "YouTube": re.compile(r"^https?://(www\.|m\.|music\.)?(youtube\.com|youtu\.be)/", re.IGNORECASE),
    "Instagram": re.compile(r"^https?://(www\.)?instagram\.com/", re.IGNORECASE),
    "TikTok": re.compile(r"^https?://((www|vm|vt)\.)?tiktok\.com/", re.IGNORECASE),
    "X": re.compile(r"^https?://(www\.|mobile\.)?(x\.com|twitter\.com)/", re.IGNORECASE),
}

AGE_HINT = (
    "Yaş kısıtlamalı video: cookies.txt gerekli (bkz. yt-dlp wiki). / "
    "Age-restricted video: cookies.txt required (see yt-dlp wiki)."
)
LOGIN_HINT = (
    "Bu içerik oturum istiyor: tarayıcından cookies.txt dışa aktarıp uygulama "
    "klasörüne koy. / This content requires login: export cookies.txt from "
    "your browser into the app folder."
)


def detect_platform(url):
    """URL desteklenen bir platforma aitse adını, değilse None döner."""
    url = url.strip()
    for name, rx in PLATFORMS.items():
        if rx.match(url):
            return name
    return None


def is_supported_url(text):
    return detect_platform(text) is not None


def is_playlist(url):
    # Liste mantığı yalnızca YouTube'da var; diğer platformlar tek gönderi indirir
    return detect_platform(url) == "YouTube" and bool(PLAYLIST_RE.search(url))


def friendly_error(exc):
    msg = str(exc)
    if "confirm your age" in msg:
        return AGE_HINT
    lowered = msg.lower()
    if any(k in lowered for k in ("login required", "log in", "authentication", "rate-limit", "nsfw")):
        return f"{msg[:120]} — {LOGIN_HINT}"
    return msg


def _base_opts():
    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        # YouTube'un "n challenge" koruması için JS çalıştırıcısı gerekir.
        # Varsayılan yalnızca deno'dur; Node kuruluysa onu da kullanabilsin.
        "js_runtimes": {"deno": {}, "node": {}},
    }
    if COOKIE_FILE.exists():
        opts["cookiefile"] = str(COOKIE_FILE)
    return opts


def _audio_opts(quality, output_dir, hook):
    opts = _base_opts() | {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "writethumbnail": True,
    }
    if hook:
        opts["progress_hooks"] = [hook]
    ffmpeg = get_ffmpeg_path()
    if os.path.isfile(ffmpeg):
        opts["ffmpeg_location"] = ffmpeg
    if quality == "m4a":
        # AAC kaynağı varsa yeniden kodlamadan kopyalanır (orijinal kalite)
        opts["format"] = "bestaudio[ext=m4a]/bestaudio/best"
        extract = {"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}
    else:
        opts["format"] = "bestaudio/best"
        extract = {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality,
        }
    opts["postprocessors"] = [extract, {"key": "FFmpegMetadata"}, {"key": "EmbedThumbnail"}]
    return opts


def _video_opts(quality, output_dir, hook):
    opts = _base_opts() | {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "postprocessors": [{"key": "FFmpegMetadata"}],
    }
    if hook:
        opts["progress_hooks"] = [hook]
    ffmpeg = get_ffmpeg_path()
    if os.path.isfile(ffmpeg):
        opts["ffmpeg_location"] = ffmpeg
    # Son çare her zaman "best": TikTok/Instagram/X gibi platformlar ayrı
    # video+ses akışı sunmayabilir ya da dikey videolarda yükseklik filtresi
    # tüm formatları eleyebilir — indirme asla bu yüzden başarısız olmamalı.
    if quality == "best":
        opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
    else:
        h = _VIDEO_HEIGHTS[quality]
        opts["format"] = (
            f"bestvideo[ext=mp4][height<={h}]+bestaudio[ext=m4a]"
            f"/bestvideo[height<={h}]+bestaudio"
            f"/best[height<={h}]"
            f"/best"
        )
    return opts


def search(query, limit=10):
    """YouTube'da arar; başlık/kanal/süre/url listesi döner."""
    opts = _base_opts() | {"extract_flat": True}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
    return [
        {
            "type": "video",
            "platform": "YouTube",
            "url": e.get("url") or f"https://www.youtube.com/watch?v={e['id']}",
            "title": e.get("title") or "(başlıksız)",
            "channel": e.get("channel") or e.get("uploader") or "",
            "duration": e.get("duration"),
        }
        for e in (info.get("entries") or [])
        if e.get("id")
    ]


def get_info(url):
    """Video veya oynatma listesi bilgisi döner (indirme yapmaz)."""
    platform = detect_platform(url) or "YouTube"
    if is_playlist(url):
        with YoutubeDL(_base_opts() | {"extract_flat": True, "noplaylist": False}) as ydl:
            info = ydl.extract_info(url, download=False)
        entries = [e for e in (info.get("entries") or []) if e.get("id")]
        if not entries:
            raise ValueError("Oynatma listesinde video bulunamadı.")
        return {
            "type": "playlist",
            "platform": platform,
            "url": url,
            "title": info.get("title") or "Oynatma listesi",
            "channel": info.get("channel") or info.get("uploader") or "",
            "count": min(len(entries), MAX_PLAYLIST),
        }
    with YoutubeDL(_base_opts()) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "type": "video",
        "platform": platform,
        "url": url,
        "title": info.get("title") or (info.get("description") or "")[:60] or "(başlıksız)",
        "channel": info.get("channel") or info.get("uploader") or "",
        "duration": info.get("duration"),
    }


def _download_one(url, quality, output_dir, progress_cb, index=1, total=1, title=""):
    def hook(d):
        if not progress_cb:
            return
        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total_bytes:
                pct = d.get("downloaded_bytes", 0) / total_bytes * 100
                progress_cb({"stage": "downloading", "percent": round(pct, 1),
                             "index": index, "total": total, "title": title})
        elif d["status"] == "finished":
            progress_cb({"stage": "converting", "index": index, "total": total, "title": title})

    is_video = quality in VIDEO_QUALITIES
    opts = _video_opts(quality, output_dir, hook) if is_video else _audio_opts(quality, output_dir, hook)
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        base = Path(ydl.prepare_filename(info))
    if is_video:
        ext = ".mp4"
    else:
        ext = ".m4a" if quality == "m4a" else ".mp3"
    return str(base.with_suffix(ext)), info.get("title", base.stem)


def download(url, quality, output_dir, progress_cb=None):
    """Tek video ya da oynatma listesi indirir.

    quality: "128" | "192" | "320" | "m4a" (ses) ya da "480p" | "720p" | "1080p" | "best" (video)
    Dönüş: [{"file": yol, "title": başlık} | {"title": ..., "error": ...}]
    """
    os.makedirs(output_dir, exist_ok=True)

    if not is_playlist(url):
        path, title = _download_one(url, quality, output_dir, progress_cb)
        return [{"file": path, "title": title}]

    with YoutubeDL(_base_opts() | {"extract_flat": True, "noplaylist": False}) as ydl:
        info = ydl.extract_info(url, download=False)
    entries = [e for e in (info.get("entries") or []) if e.get("id")][:MAX_PLAYLIST]
    if not entries:
        raise ValueError("Oynatma listesinde video bulunamadı.")

    results = []
    for i, entry in enumerate(entries, start=1):
        video_url = f"https://www.youtube.com/watch?v={entry['id']}"
        title = entry.get("title") or entry["id"]
        try:
            path, real_title = _download_one(
                video_url, quality, output_dir, progress_cb, index=i, total=len(entries), title=title
            )
            results.append({"file": path, "title": real_title})
        except Exception as exc:
            results.append({"title": title, "error": friendly_error(exc)})
    return results
