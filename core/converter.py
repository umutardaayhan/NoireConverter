import os
import subprocess
from PIL import Image
from core.utils import get_ffmpeg_path

def process_file(input_path: str, target_format: str, quality: int, output_dir: str) -> str:
    from pathlib import Path
    
    filename = Path(input_path).stem
    target_fmt = target_format.lower().strip()
    output_path = os.path.join(output_dir, f"{filename}.{target_fmt}")
    
    # Image Processing (Pillow)
    image_formats = {"webp", "png", "jpg", "jpeg", "ico"}
    if target_fmt in image_formats:
        if target_fmt == "jpg":
            target_fmt = "jpeg"
        with Image.open(input_path) as img:
            if target_fmt in ["jpeg", "jpg"] and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            save_kwargs = {}
            if target_fmt in ["jpeg", "jpg", "webp"]:
                save_kwargs['quality'] = quality
            img.save(output_path, format=target_fmt.upper(), **save_kwargs)
        return output_path
        
    # Audio/Video Processing (FFMPEG)
    media_formats = {"mp3", "wav", "mp4", "gif"}
    if target_fmt in media_formats:
        ffmpeg = get_ffmpeg_path()
        cmd = [ffmpeg, "-y", "-i", input_path]
        
        if target_fmt == "mp3":
            bitrate = max(32, min(320, int((quality / 100) * 320)))
            cmd.extend(["-b:a", f"{bitrate}k"])
            
        subprocess.run(cmd + [output_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
        
    raise ValueError(f"Unsupported target format: {target_format}")

def resize_file(input_path: str, width: int, height: int, output_dir: str) -> str:
    from pathlib import Path
    ext = Path(input_path).suffix.lower()
    filename = Path(input_path).stem
    output_path = os.path.join(output_dir, f"{filename}_resized{ext}")
    
    # Check if video
    if ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
        ffmpeg = get_ffmpeg_path()
        cmd = [ffmpeg, "-y", "-i", input_path, "-vf", f"scale={width}:{height}"]
        subprocess.run(cmd + [output_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
        
    # Treat as Image
    with Image.open(input_path) as img:
        img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
        if ext in [".jpeg", ".jpg"] and img_resized.mode in ("RGBA", "P"):
            img_resized = img_resized.convert("RGB")
        img_resized.save(output_path)
    return output_path

def optimize_file(input_path: str, quality: int, output_dir: str) -> str:
    from pathlib import Path
    ext = Path(input_path).suffix.lower()
    filename = Path(input_path).stem
    output_path = os.path.join(output_dir, f"{filename}_opt{ext}")
    
    # Check if video
    if ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
        ffmpeg = get_ffmpeg_path()
        # CRF (0-51), lower quality slider means higher CRF (more compression)
        crf = int(51 - ((quality / 100.0) * 51))
        cmd = [ffmpeg, "-y", "-i", input_path, "-vcodec", "libx264", "-crf", str(crf)]
        subprocess.run(cmd + [output_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
        
    # Treat as Image
    with Image.open(input_path) as img:
        if ext in [".jpeg", ".jpg"] and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        save_kwargs = {}
        if ext in [".jpeg", ".jpg", ".webp"]:
            save_kwargs['quality'] = quality
        elif ext == ".png":
            save_kwargs['optimize'] = True
        img.save(output_path, **save_kwargs)
    return output_path

def create_gif(input_path: str, start_time: str, end_time: str, output_dir: str) -> str:
    from pathlib import Path
    filename = Path(input_path).stem
    output_path = os.path.join(output_dir, f"{filename}_animated.gif")
    
    ffmpeg = get_ffmpeg_path()
    # Profesyonel Yüksek Kaliteli GIF dönüşümü:
    # 15 fps, 480 genişlikte ve FFMPEG palet jenarasyonu ile sıfır renk kaybı.
    vf_filter = "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    
    cmd = [
        ffmpeg, "-y",
        "-ss", start_time,
        "-to", end_time,
        "-i", input_path,
        "-vf", vf_filter,
        "-loop", "0",
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

def convert_document(input_path: str, target_format: str, output_dir: str) -> str:
    from pathlib import Path
    import traceback
    ext = Path(input_path).suffix.lower()
    filename = Path(input_path).stem
    
    target_format = target_format.lower().replace('.', '')
    output_path = os.path.join(output_dir, f"{filename}.{target_format}")
    
    try:
        if ext == '.docx' and target_format == 'pdf':
            from docx2pdf import convert as docx2pdf_convert
            docx2pdf_convert(input_path, output_path)
        elif ext == '.pdf' and target_format == 'docx':
            from pdf2docx import Converter
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
        else:
            raise ValueError(f"Unsupported document conversion: {ext} -> {target_format}")
    except ImportError as e:
        raise ImportError(f"Missing dependency for document conversion: {e}. Please 'pip install docx2pdf pdf2docx'")
        
    return output_path

def extract_text(input_path: str, language: str, output_dir: str) -> str:
    from pathlib import Path
    from PIL import Image
    import traceback
    
    filename = Path(input_path).stem
    output_path = os.path.join(output_dir, f"{filename}_ocr.txt")
    
    try:
        import pytesseract
        with Image.open(input_path) as img:
            text = pytesseract.image_to_string(img, lang=language)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
    except ImportError:
        raise ImportError("Gereksinim eksik: Lütfen 'pip install pytesseract' çalıştırın.")
    except Exception as e:
        raise Exception(f"OCR Error: {e} (Tesseract yüklü sisteminizde bulunamayabilir)")
        
    return output_path
