"""Gizlilik araçları.

- EXIF: resimlerdeki metadata'yı (konum, cihaz, tarih...) görüntüler ve
  temiz kopya üreterek kaldırır (Pillow).
- ID3/etiket: ses dosyalarının başlık/sanatçı/albüm etiketlerini düzenler
  veya tamamen siler (mutagen — yt-dlp ile birlikte zaten kurulu).
"""

import os

import mutagen
from PIL import Image
from PIL.ExifTags import TAGS


def read_exif(path):
    """Resmin EXIF verisini {etiket: değer} olarak döner (boşsa {})."""
    with Image.open(path) as img:
        exif = img.getexif()
        if not exif:
            return {}
        return {str(TAGS.get(tag_id, tag_id)): str(value)[:80] for tag_id, value in exif.items()}


def strip_exif(path, output_dir):
    """Resmi tüm metadata'dan arındırılmış _clean kopyası olarak kaydeder."""
    name, ext = os.path.splitext(os.path.basename(path))
    out = os.path.join(output_dir, f"{name}_clean{ext}")
    with Image.open(path) as img:
        clean = img.copy()  # pixel verisi kalır, info/exif kopyalanmaz
    save_kwargs = {"quality": 95} if ext.lower() in (".jpg", ".jpeg", ".webp") else {}
    clean.save(out, **save_kwargs)
    return out


def edit_audio_tags(path, title=None, artist=None, album=None):
    """Ses dosyasının etiketlerini yerinde günceller (boş geçilen alan dokunulmaz)."""
    tags = mutagen.File(path, easy=True)
    if tags is None:
        raise ValueError("Desteklenmeyen ses formatı.")
    if tags.tags is None:
        tags.add_tags()
    if title:
        tags["title"] = title
    if artist:
        tags["artist"] = artist
    if album:
        tags["album"] = album
    tags.save()


def clear_audio_tags(path):
    """Ses dosyasındaki tüm etiketleri (kapak dahil) siler."""
    f = mutagen.File(path)
    if f is None:
        raise ValueError("Desteklenmeyen ses formatı.")
    f.delete()
    f.save()
