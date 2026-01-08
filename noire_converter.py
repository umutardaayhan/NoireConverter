import os
import sys
import subprocess
import threading
import ctypes
import customtkinter as ctk
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# --- DİL PAKETİ ---
LANG = {
    "en": {
        "title": "Noire Converter v1.1",
        "drop_title": "DROP MEDIA ANYWHERE",
        "drop_sub": "Folders or Files",
        "chk_img": "Images",
        "chk_aud": "Audio",
        "chk_vid": "Video",
        "tab_convert": "Convert",
        "tab_resize": "Resize",
        "tab_opt": "Optimizer",
        "tab_gif": "GIF Studio",
        "lbl_target_img": "Target Image Format",
        "lbl_target_aud": "Target Audio Format",
        "lbl_new_dim": "Custom Dimensions (Px)",
        "lbl_presets": "Quick Presets (Multi-Select)",
        "chk_div2": "½ (Half)",
        "chk_div4": "¼ (Quarter)",
        "chk_mul2": "2x (Double)",
        "chk_mul4": "4x (Quad)",
        "lbl_quality": "Compression Quality",
        "lbl_opt_hint": "ℹ️ Best results with JPG and WebP formats.",
        "lbl_gif_time": "1. Duration (Sec):",
        "lbl_gif_crop": "2. Crop:",
        "btn_visual_crop": "✂️ Editor",
        "lbl_gif_out": "3. Output:",
        "lbl_fps": "FPS",
        "sw_source": "Use Source Folder",
        "btn_browse": "Browse",
        "lbl_queue": "FILE QUEUE",
        "btn_clear": "Clear All",
        "btn_remove": "Remove Selected",
        "chk_all": "Select All",
        "btn_start": "START OPERATION",
        "status_ready": "System Ready.",
        "status_processing": "PROCESSING...",
        "status_done": "Operation Completed.",
        "msg_no_video": "Please select a video file (checkbox) first.",
        "msg_empty": "Queue is empty!",
        "msg_no_selection": "No files selected! Please check the boxes.",
        "crop_tip": "Drag corners to resize. Drag center to move.",
        "btn_apply": "APPLY CROP",
        "plh_start": "Start",
        "plh_end": "End",
        "plh_w": "W",
        "plh_h": "H",
        "plh_x": "X",
        "plh_y": "Y",
        "guide_title": "USER MANUAL",
        "guide_text": """
1. RESIZE MODES
---------------------------
• Custom: Enter specific Width x Height.
• Presets (/2, x2...): Select multiple boxes to generate
  multiple versions of the same image at once.

2. GIF STUDIO & CROP
---------------------------
• Crop Editor: Takes a snapshot from the FIRST SELECTED video.
• Duration: Leave blank to convert the whole video.
• Output Quality: Adjusts the output resolution and bitrate.

3. FFmpeg SETUP
---------------------------
• 'ffmpeg.exe' must be in the same folder as this app."""
    },
    "tr": {
        "title": "Noire Converter v1.1",
        "drop_title": "HERHANGİ BİR YERE SÜRÜKLE",
        "drop_sub": "Klasör veya Dosya",
        "chk_img": "Resim",
        "chk_aud": "Ses",
        "chk_vid": "Video",
        "tab_convert": "Dönüştür",
        "tab_resize": "Boyutlandır",
        "tab_opt": "Optimize Et",
        "tab_gif": "GIF Stüdyo",
        "lbl_target_img": "Hedef Resim Formatı",
        "lbl_target_aud": "Hedef Ses Formatı",
        "lbl_new_dim": "Özel Boyutlar (Piksel)",
        "lbl_presets": "Hızlı Seçenekler (Çoklu Seçim)",
        "chk_div2": "½ (Yarım)",
        "chk_div4": "¼ (Çeyrek)",
        "chk_mul2": "2x (İki Kat)",
        "chk_mul4": "4x (Dört Kat)",
        "lbl_quality": "Sıkıştırma Kalitesi",
        "lbl_opt_hint": "ℹ️ JPG ve WebP formatlarında en iyi sonucu verir.",
        "lbl_gif_time": "1. Süre (Sn):",
        "lbl_gif_crop": "2. Kırpma:",
        "btn_visual_crop": "✂️ Editör",
        "lbl_gif_out": "3. Çıktı Kalitesi:",
        "lbl_fps": "Kare/Sn",
        "sw_source": "Kaynak Klasörü Kullan",
        "btn_browse": "Seç...",
        "lbl_queue": "İŞLEM KUYRUĞU",
        "btn_clear": "Temizle",
        "btn_remove": "Seçileni Sil",
        "chk_all": "Hepsini Seç",
        "btn_start": "İŞLEMİ BAŞLAT",
        "status_ready": "Sistem Hazır.",
        "status_processing": "İŞLENİYOR...",
        "status_done": "İşlem Tamamlandı.",
        "msg_no_video": "Lütfen önce bir video dosyasını seçin (tik atın).",
        "msg_empty": "Liste boş!",
        "msg_no_selection": "Hiçbir dosya seçilmedi! Lütfen kutucukları işaretleyin.",
        "crop_tip": "Köşeleri sürükleyerek daraltın. Ortadan tutarak taşıyın.",
        "btn_apply": "KIRPMAYI UYGULA",
        "plh_start": "Başla",
        "plh_end": "Bitir",
        "plh_w": "G",
        "plh_h": "Y",
        "plh_x": "X",
        "plh_y": "Y",
        "guide_title": "KULLANIM KILAVUZU",
        "guide_text": """
1. BOYUTLANDIRMA MODLARI
---------------------------
• Özel: Belirli bir Genişlik x Yükseklik girin.
• Hazır Ayarlar (/2, x2...): Birden fazla kutucuğu
  seçerek aynı resmin farklı boyutlarını tek seferde
  oluşturabilirsiniz.

2. GIF STÜDYO & KIRPMA
---------------------------
• Kırpma Editörü: SEÇİLİ olan ilk videodan örnek alır.
• Süre: Boş bırakırsanız videonun tamamı işlenir.
• Çıktı Kalitesi: Çıktı çözünürlüğünü ve bitrate oranını ayarlar.

3. FFmpeg KURULUMU
---------------------------
• 'ffmpeg.exe' dosyası bu uygulamanın hemen yanında
  (aynı klasörde) bulunmak zorundadır."""
    }
}

# --- AYARLAR ---
ctk.set_appearance_mode("Dark")
COLOR_BG = "#0F0F0F"
COLOR_FRAME = "#181818"
COLOR_ACCENT = "#D4AF37"
COLOR_ACCENT_HOVER = "#B8860B"
COLOR_TEXT_DIM = "#888888"
COLOR_DANGER = "#5D1010"
COLOR_DANGER_HOVER = "#801B1B"

FONT_HEADER = ("Roboto", 24, "bold")
FONT_SUBHEAD = ("Roboto", 14, "bold")
FONT_LOG = ("Consolas", 10)

IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.ico']
AUDIO_EXTS = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
VIDEO_EXTS = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.webm']

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- FFmpeg Yolu Bulucu (WinError Fix) ---
def get_ffmpeg_path():
    # 1. Scriptin olduğu klasöre bak
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffmpeg = os.path.join(base_dir, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    
    # 2. Çalışma dizinine bak (CWD)
    if os.path.exists("ffmpeg.exe"):
        return "ffmpeg.exe"
        
    # 3. Sistem PATH'ine bak
    return "ffmpeg"

# --- CROP EDITOR ---
class CropEditor(ctk.CTkToplevel):
    def __init__(self, parent, image_path, callback, lang_code):
        super().__init__(parent)
        self.lang = lang_code
        self.title("Crop Editor")
        self.geometry("900x750")
        self.callback = callback
        self.attributes("-topmost", True)
        self.configure(fg_color="#000")
        
        # İkonu ana pencereden al (Varsa)
        try: self.iconbitmap(resource_path("App.ico"))
        except: pass

        self.pil_img = Image.open(image_path)
        self.orig_w, self.orig_h = self.pil_img.size
        
        self.cv_w, self.cv_h = 800, 550
        self.scale = min(self.cv_w / self.orig_w, self.cv_h / self.orig_h)
        self.disp_w = int(self.orig_w * self.scale)
        self.disp_h = int(self.orig_h * self.scale)
        
        self.offset_x = (self.cv_w - self.disp_w) // 2
        self.offset_y = (self.cv_h - self.disp_h) // 2

        img_resized = self.pil_img.resize((self.disp_w, self.disp_h), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_resized)

        ctk.CTkLabel(self, text=LANG[self.lang]["crop_tip"], text_color="gray").pack(pady=5)
        
        self.canvas = tk.Canvas(self, width=self.cv_w, height=self.cv_h, bg="#111", highlightthickness=0, cursor="arrow")
        self.canvas.pack(pady=10)
        self.canvas.create_image(self.offset_x, self.offset_y, anchor="nw", image=self.tk_img)

        ctk.CTkButton(self, text=LANG[self.lang]["btn_apply"], fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", command=self.finish).pack(pady=10)

        self.rect_x1 = self.offset_x
        self.rect_y1 = self.offset_y
        self.rect_x2 = self.offset_x + self.disp_w
        self.rect_y2 = self.offset_y + self.disp_h
        
        self.drag_mode = None
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.overlay_ids = []
        self.handle_ids = []
        self.rect_outline_id = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Motion>", self.on_hover)
        
        self.draw_selection()

    def draw_selection(self):
        for oid in self.overlay_ids: self.canvas.delete(oid)
        self.overlay_ids = []
        fill_color = "black"; stipple = "gray50" 
        
        self.overlay_ids.append(self.canvas.create_rectangle(0, 0, self.cv_w, self.rect_y1, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(0, self.rect_y2, self.cv_w, self.cv_h, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(0, self.rect_y1, self.rect_x1, self.rect_y2, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(self.rect_x2, self.rect_y1, self.cv_w, self.rect_y2, fill=fill_color, stipple=stipple, outline=""))

        if self.rect_outline_id: self.canvas.delete(self.rect_outline_id)
        self.rect_outline_id = self.canvas.create_rectangle(self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2, outline=COLOR_ACCENT, width=2)
        
        for hid in self.handle_ids: self.canvas.delete(hid)
        self.handle_ids = []
        h_size = 8
        coords = [(self.rect_x1, self.rect_y1), (self.rect_x2, self.rect_y1), (self.rect_x1, self.rect_y2), (self.rect_x2, self.rect_y2)]
        for cx, cy in coords:
            self.handle_ids.append(self.canvas.create_rectangle(cx-h_size, cy-h_size, cx+h_size, cy+h_size, fill=COLOR_ACCENT, outline="black"))

    def get_interaction_mode(self, x, y):
        th = 15
        if abs(x - self.rect_x1) < th and abs(y - self.rect_y1) < th: return "nw"
        if abs(x - self.rect_x2) < th and abs(y - self.rect_y1) < th: return "ne"
        if abs(x - self.rect_x1) < th and abs(y - self.rect_y2) < th: return "sw"
        if abs(x - self.rect_x2) < th and abs(y - self.rect_y2) < th: return "se"
        if self.rect_x1 < x < self.rect_x2 and self.rect_y1 < y < self.rect_y2: return "move"
        return None

    def on_press(self, event):
        self.drag_mode = self.get_interaction_mode(event.x, event.y)
        self.last_mouse_x = event.x; self.last_mouse_y = event.y

    def on_drag(self, event):
        if not self.drag_mode: return
        dx = event.x - self.last_mouse_x; dy = event.y - self.last_mouse_y
        min_x = self.offset_x; max_x = self.offset_x + self.disp_w
        min_y = self.offset_y; max_y = self.offset_y + self.disp_h
        
        if self.drag_mode == "move":
            w = self.rect_x2 - self.rect_x1; h = self.rect_y2 - self.rect_y1
            nx1 = self.rect_x1 + dx; ny1 = self.rect_y1 + dy
            nx2 = nx1 + w; ny2 = ny1 + h
            if nx1 < min_x: nx1 = min_x; nx2 = min_x + w
            if nx2 > max_x: nx2 = max_x; nx1 = max_x - w
            if ny1 < min_y: ny1 = min_y; ny2 = min_y + h
            if ny2 > max_y: ny2 = max_y; ny1 = max_y - h
            self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2 = nx1, ny1, nx2, ny2
        else:
            if "w" in self.drag_mode: self.rect_x1 = min(max(self.rect_x1 + dx, min_x), self.rect_x2 - 10)
            if "e" in self.drag_mode: self.rect_x2 = max(min(self.rect_x2 + dx, max_x), self.rect_x1 + 10)
            if "n" in self.drag_mode: self.rect_y1 = min(max(self.rect_y1 + dy, min_y), self.rect_y2 - 10)
            if "s" in self.drag_mode: self.rect_y2 = max(min(self.rect_y2 + dy, max_y), self.rect_y1 + 10)

        self.last_mouse_x = event.x; self.last_mouse_y = event.y
        self.draw_selection()

    def on_hover(self, event):
        mode = self.get_interaction_mode(event.x, event.y)
        if mode == "move": self.canvas.config(cursor="fleur")
        elif mode in ["nw", "se"]: self.canvas.config(cursor="sizing_nwse")
        elif mode in ["ne", "sw"]: self.canvas.config(cursor="sizing_nesw")
        else: self.canvas.config(cursor="arrow")

    def finish(self):
        real_x = int((self.rect_x1 - self.offset_x) / self.scale)
        real_y = int((self.rect_y1 - self.offset_y) / self.scale)
        real_w = int((self.rect_x2 - self.rect_x1) / self.scale)
        real_h = int((self.rect_y2 - self.rect_y1) / self.scale)
        self.callback((real_w, real_h, real_x, real_y))
        self.destroy()

# --- ANA UYGULAMA ---
class NoireConverterApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        myappid = 'com.noire.converter.v1_1' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.current_lang = "en" 
        self.title("Noire Converter v1.1")
        self.geometry("1100x700") 
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)
        icon_file_path = resource_path("App.ico")
        if os.path.exists(icon_file_path):
            try: self.iconbitmap(icon_file_path); self.wm_iconbitmap(icon_file_path)
            except: pass
        self.file_items = []; self.output_folder = "" 
        
        # Filtre Değişkenleri
        self.filter_img_var = ctk.BooleanVar(value=True)
        self.filter_audio_var = ctk.BooleanVar(value=True)
        self.filter_video_var = ctk.BooleanVar(value=True)
        
        # Resize Değişkenleri
        self.res_div2 = ctk.BooleanVar(value=False)
        self.res_div4 = ctk.BooleanVar(value=False)
        self.res_mul2 = ctk.BooleanVar(value=False)
        self.res_mul4 = ctk.BooleanVar(value=False)
        
        # Select All
        self.select_all_var = ctk.BooleanVar(value=True)

        self.drop_target_register(DND_FILES); self.dnd_bind('<<Drop>>', self.drop_event)
        self.create_ui(); self.update_ui_text()

    def create_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.left_col = ctk.CTkFrame(self.main_container, fg_color="transparent", width=420)
        self.left_col.pack(side="left", fill="y", padx=(0, 20)); self.left_col.pack_propagate(False) 
        
        self.header_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        self.header_frame.pack(anchor="w", fill="x", pady=(0, 15))
        ctk.CTkLabel(self.header_frame, text="NOIRE", font=FONT_HEADER, text_color=COLOR_ACCENT).pack(side="left")
        ctk.CTkLabel(self.header_frame, text=" CONVERTER", font=FONT_HEADER, text_color="white").pack(side="left")
        ctk.CTkLabel(self.header_frame, text=" // v1.1", font=("Roboto", 12), text_color=COLOR_TEXT_DIM).pack(side="left", padx=(5,0), pady=(10,0))
        
        btn_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_box.pack(side="right")
        self.btn_lang = ctk.CTkButton(btn_box, text="TR", width=40, height=25, fg_color="#333", command=self.toggle_language)
        self.btn_lang.pack(side="left", padx=5)
        self.btn_help = ctk.CTkButton(btn_box, text="?", width=30, height=25, fg_color="#333", command=self.open_help_window)
        self.btn_help.pack(side="left")
        
        self.drop_frame = ctk.CTkFrame(self.left_col, height=130, corner_radius=12, fg_color=COLOR_FRAME, border_width=2, border_color="#2a2a2a")
        self.drop_frame.pack(fill="x", pady=(0, 15))
        self.drop_frame.pack_propagate(False)
        self.lbl_drop_title = ctk.CTkLabel(self.drop_frame, text="", font=("Roboto", 14, "bold"), text_color=COLOR_ACCENT)
        self.lbl_drop_title.place(relx=0.5, rely=0.30, anchor="center")
        self.lbl_drop_sub = ctk.CTkLabel(self.drop_frame, text="", text_color=COLOR_TEXT_DIM, font=("Roboto", 10))
        self.lbl_drop_sub.place(relx=0.5, rely=0.55, anchor="center")
        self.filter_box = ctk.CTkFrame(self.drop_frame, fg_color="transparent")
        self.filter_box.place(relx=0.5, rely=0.85, anchor="center")
        chk_style = {"checkbox_width":16, "checkbox_height":16, "font":("Roboto",11), "fg_color":COLOR_ACCENT, "hover_color":COLOR_ACCENT_HOVER}
        self.chk_img = ctk.CTkCheckBox(self.filter_box, text="Img", variable=self.filter_img_var, **chk_style)
        self.chk_img.pack(side="left", padx=8)
        self.chk_aud = ctk.CTkCheckBox(self.filter_box, text="Aud", variable=self.filter_audio_var, **chk_style)
        self.chk_aud.pack(side="left", padx=8)
        self.chk_vid = ctk.CTkCheckBox(self.filter_box, text="Vid", variable=self.filter_video_var, **chk_style)
        self.chk_vid.pack(side="left", padx=8)

        self.tab_view = ctk.CTkTabview(self.left_col, height=380, fg_color=COLOR_FRAME, segmented_button_fg_color="#111", segmented_button_selected_color=COLOR_ACCENT, segmented_button_selected_hover_color=COLOR_ACCENT_HOVER, segmented_button_unselected_color=COLOR_FRAME, text_color="white")
        self.tab_view.pack(fill="x", pady=(0, 15))
        self.tab_convert = self.tab_view.add("Convert")
        self.tab_resize = self.tab_view.add("Resize")
        self.tab_opt = self.tab_view.add("Optimizer")
        self.tab_gif = self.tab_view.add("GIF Studio")
        seg_style = {"fg_color": "#111", "selected_color": "#333", "text_color": "#fff", "height": 30}
        entry_style = {"height": 35, "fg_color": "#111", "border_color": "#333", "justify": "center"}
        
        self.lbl_target_img = ctk.CTkLabel(self.tab_convert, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_target_img.pack(anchor="w", pady=(15, 5))
        self.img_option = ctk.CTkSegmentedButton(self.tab_convert, values=["WEBP", "JPG", "PNG", "ICO"], **seg_style)
        self.img_option.set("WEBP"); self.img_option.pack(fill="x", pady=(0, 20))
        self.lbl_target_aud = ctk.CTkLabel(self.tab_convert, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_target_aud.pack(anchor="w", pady=(0, 5))
        self.audio_option = ctk.CTkSegmentedButton(self.tab_convert, values=["MP3", "WAV"], **seg_style)
        self.audio_option.set("MP3"); self.audio_option.pack(fill="x")
        
        self.lbl_new_dim = ctk.CTkLabel(self.tab_resize, text="", font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_DIM); self.lbl_new_dim.pack(pady=(15, 5))
        resize_box = ctk.CTkFrame(self.tab_resize, fg_color="transparent"); resize_box.pack()
        self.entry_width = ctk.CTkEntry(resize_box, width=100, **entry_style); self.entry_width.pack(side="left", padx=5)
        ctk.CTkLabel(resize_box, text="x", font=("Roboto", 16, "bold"), text_color=COLOR_TEXT_DIM).pack(side="left", padx=5)
        self.entry_height = ctk.CTkEntry(resize_box, width=100, **entry_style); self.entry_height.pack(side="left", padx=5)
        self.lbl_presets = ctk.CTkLabel(self.tab_resize, text="", font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_DIM); self.lbl_presets.pack(pady=(25, 5))
        preset_frame = ctk.CTkFrame(self.tab_resize, fg_color="transparent"); preset_frame.pack()
        self.chk_div2 = ctk.CTkCheckBox(preset_frame, text="", variable=self.res_div2, **chk_style); self.chk_div2.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.chk_div4 = ctk.CTkCheckBox(preset_frame, text="", variable=self.res_div4, **chk_style); self.chk_div4.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.chk_mul2 = ctk.CTkCheckBox(preset_frame, text="", variable=self.res_mul2, **chk_style); self.chk_mul2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.chk_mul4 = ctk.CTkCheckBox(preset_frame, text="", variable=self.res_mul4, **chk_style); self.chk_mul4.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.lbl_quality_head = ctk.CTkLabel(self.tab_opt, text="", font=FONT_SUBHEAD); self.lbl_quality_head.pack(pady=(30, 10))
        self.quality_val = ctk.IntVar(value=80)
        self.lbl_quality_val = ctk.CTkLabel(self.tab_opt, text="", font=("Roboto", 12), text_color=COLOR_ACCENT); self.lbl_quality_val.pack(pady=(0, 5))
        self.slider_quality = ctk.CTkSlider(self.tab_opt, from_=10, to=100, number_of_steps=90, variable=self.quality_val, command=self.update_quality_label, button_color=COLOR_ACCENT, button_hover_color=COLOR_ACCENT_HOVER, progress_color=COLOR_ACCENT); self.slider_quality.pack(fill="x", padx=50, pady=5)
        self.lbl_opt_hint = ctk.CTkLabel(self.tab_opt, text="", font=("Roboto", 11), text_color="gray"); self.lbl_opt_hint.pack(pady=(20,5))

        time_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent"); time_frame.pack(fill="x", pady=(10, 5), padx=5)
        self.lbl_gif_time = ctk.CTkLabel(time_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT); self.lbl_gif_time.pack(side="left", padx=(0,10))
        self.entry_start = ctk.CTkEntry(time_frame, width=60, **entry_style); self.entry_start.pack(side="left", padx=2)
        ctk.CTkLabel(time_frame, text="→", font=("Roboto", 14)).pack(side="left")
        self.entry_end = ctk.CTkEntry(time_frame, width=60, **entry_style); self.entry_end.pack(side="left", padx=2)
        crop_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent"); crop_frame.pack(fill="x", pady=(5, 5), padx=5)
        self.lbl_gif_crop = ctk.CTkLabel(crop_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT); self.lbl_gif_crop.pack(side="left", padx=(0,10))
        self.btn_visual_crop = ctk.CTkButton(crop_frame, text="", width=90, height=28, fg_color="#333", hover_color="#444", font=("Roboto", 11, "bold"), command=self.open_visual_cropper); self.btn_visual_crop.pack(side="left", padx=(0, 10))
        self.entry_crop_w = ctk.CTkEntry(crop_frame, width=50, **entry_style); self.entry_crop_w.pack(side="left", padx=2)
        self.entry_crop_h = ctk.CTkEntry(crop_frame, width=50, **entry_style); self.entry_crop_h.pack(side="left", padx=2)
        self.entry_crop_x = ctk.CTkEntry(crop_frame, width=40, **entry_style); self.entry_crop_x.pack(side="left", padx=(10,2))
        self.entry_crop_y = ctk.CTkEntry(crop_frame, width=40, **entry_style); self.entry_crop_y.pack(side="left", padx=2)
        out_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent"); out_frame.pack(fill="x", pady=(5, 5), padx=5)
        self.lbl_gif_out = ctk.CTkLabel(out_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT); self.lbl_gif_out.pack(side="left", padx=(0,10))
        self.entry_gif_scale = ctk.CTkEntry(out_frame, width=70, **entry_style); self.entry_gif_scale.insert(0, "480"); self.entry_gif_scale.pack(side="left", padx=2)
        self.lbl_fps = ctk.CTkLabel(out_frame, text="", font=("Roboto", 11)); self.lbl_fps.pack(side="right", padx=(5,0))
        self.seg_fps = ctk.CTkSegmentedButton(out_frame, values=["10", "15", "24", "30"], width=120, **seg_style); self.seg_fps.set("15"); self.seg_fps.pack(side="right", padx=10)

        self.path_frame = ctk.CTkFrame(self.left_col, fg_color=COLOR_FRAME, corner_radius=8, height=45); self.path_frame.pack(fill="x", side="bottom"); self.path_frame.pack_propagate(False)
        self.use_source_var = ctk.BooleanVar(value=True)
        self.switch_source = ctk.CTkSwitch(self.path_frame, text="", variable=self.use_source_var, command=self.toggle_path_selection, progress_color=COLOR_ACCENT, font=("Roboto", 12, "bold")); self.switch_source.pack(side="left", padx=15)
        self.btn_browse = ctk.CTkButton(self.path_frame, text="", width=60, height=24, fg_color="#333", state="disabled", command=self.select_output_folder); self.btn_browse.pack(side="right", padx=10)
        self.lbl_path = ctk.CTkLabel(self.path_frame, text="", font=("Roboto", 10), text_color=COLOR_TEXT_DIM); self.lbl_path.pack(side="right", padx=5)
        
        self.right_col = ctk.CTkFrame(self.main_container, fg_color="transparent"); self.right_col.pack(side="right", fill="both", expand=True)
        list_header = ctk.CTkFrame(self.right_col, fg_color="transparent"); list_header.pack(fill="x", pady=(0, 10))
        self.lbl_queue = ctk.CTkLabel(list_header, text="", font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_DIM); self.lbl_queue.pack(side="left")
        self.btn_clear = ctk.CTkButton(list_header, text="", width=80, height=24, fg_color="transparent", border_width=1, border_color="#333", text_color="#888", hover_color="#222", font=("Roboto", 11), command=self.clear_queue); self.btn_clear.pack(side="right")
        self.btn_remove = ctk.CTkButton(list_header, text="", width=110, height=24, fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, font=("Roboto", 11), command=self.remove_checked_files); self.btn_remove.pack(side="right", padx=(0,5))
        self.chk_select_all = ctk.CTkCheckBox(list_header, text="", width=80, variable=self.select_all_var, command=self.toggle_select_all, **chk_style)
        self.chk_select_all.pack(side="right", padx=(0,5))

        self.scroll_list = ctk.CTkScrollableFrame(self.right_col, fg_color=COLOR_FRAME, corner_radius=8); self.scroll_list.pack(fill="both", expand=True, pady=(0, 15))
        self.btn_start = ctk.CTkButton(self.right_col, text="", font=("Roboto", 16, "bold"), height=60, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", command=self.start_process_thread); self.btn_start.pack(fill="x", pady=(0, 10))
        self.log_lbl = ctk.CTkLabel(self.right_col, text="", font=FONT_LOG, text_color=COLOR_TEXT_DIM, anchor="w"); self.log_lbl.pack(fill="x")

    def toggle_language(self):
        self.current_lang = "tr" if self.current_lang == "en" else "en"
        self.btn_lang.configure(text="EN" if self.current_lang == "tr" else "TR")
        self.update_ui_text()

    def open_help_window(self):
        help_win = ctk.CTkToplevel(self)
        help_win.title(LANG[self.current_lang]["guide_title"])
        help_win.geometry("500x500")
        help_win.attributes("-topmost", True)
        # İkon ekle
        try: help_win.iconbitmap(resource_path("App.ico"))
        except: pass
        
        ctk.CTkLabel(help_win, text=LANG[self.current_lang]["guide_title"], font=FONT_HEADER, text_color=COLOR_ACCENT).pack(pady=20)
        tb = ctk.CTkTextbox(help_win, width=460, height=400, fg_color=COLOR_FRAME, font=("Consolas", 12))
        tb.pack(pady=10)
        tb.insert("0.0", LANG[self.current_lang]["guide_text"])
        tb.configure(state="disabled")

    def update_ui_text(self):
        T = LANG[self.current_lang]
        self.title(T["title"])
        self.lbl_drop_title.configure(text=T["drop_title"])
        self.lbl_drop_sub.configure(text=T["drop_sub"])
        self.chk_img.configure(text=T["chk_img"])
        self.chk_aud.configure(text=T["chk_aud"])
        self.chk_vid.configure(text=T["chk_vid"])
        self.lbl_target_img.configure(text=T["lbl_target_img"])
        self.lbl_target_aud.configure(text=T["lbl_target_aud"])
        self.lbl_new_dim.configure(text=T["lbl_new_dim"])
        self.lbl_presets.configure(text=T["lbl_presets"])
        self.chk_div2.configure(text=T["chk_div2"])
        self.chk_div4.configure(text=T["chk_div4"])
        self.chk_mul2.configure(text=T["chk_mul2"])
        self.chk_mul4.configure(text=T["chk_mul4"])
        self.lbl_quality_head.configure(text=T["lbl_quality"])
        self.lbl_opt_hint.configure(text=T["lbl_opt_hint"])
        self.update_quality_label(self.quality_val.get())
        self.lbl_gif_time.configure(text=T["lbl_gif_time"])
        self.lbl_gif_crop.configure(text=T["lbl_gif_crop"])
        self.btn_visual_crop.configure(text=T["btn_visual_crop"])
        self.lbl_gif_out.configure(text=T["lbl_gif_out"])
        self.lbl_fps.configure(text=T["lbl_fps"])
        self.switch_source.configure(text=T["sw_source"])
        self.btn_browse.configure(text=T["btn_browse"])
        self.lbl_queue.configure(text=T["lbl_queue"])
        self.btn_clear.configure(text=T["btn_clear"])
        self.btn_remove.configure(text=T["btn_remove"])
        self.chk_select_all.configure(text=T["chk_all"]) 
        self.btn_start.configure(text=T["btn_start"])
        self.log_lbl.configure(text=T["status_ready"])
        self.entry_start.configure(placeholder_text=T["plh_start"])
        self.entry_end.configure(placeholder_text=T["plh_end"])
        self.entry_width.configure(placeholder_text=T["plh_w"]); self.entry_height.configure(placeholder_text=T["plh_h"])
        self.entry_crop_w.configure(placeholder_text=T["plh_w"]); self.entry_crop_h.configure(placeholder_text=T["plh_h"])
        self.entry_crop_x.configure(placeholder_text=T["plh_x"]); self.entry_crop_y.configure(placeholder_text=T["plh_y"])

    def open_visual_cropper(self):
        target_video = None
        # Seçili olan ilk videoyu bul
        for item in self.file_items:
            if item['var'].get() and os.path.splitext(item['path'])[1].lower() in VIDEO_EXTS: 
                target_video = item['path']; break
        
        if not target_video: messagebox.showwarning("!", LANG[self.current_lang]["msg_no_video"]); return
        
        ffmpeg_cmd = get_ffmpeg_path()
        temp_img = "temp_snap.jpg"
        
        # WinError 2'yi önlemek için full path kullanıyoruz ve creationflags ekliyoruz
        cmd = [ffmpeg_cmd, "-ss", "00:00:02", "-i", target_video, "-vframes", "1", "-q:v", "2", "-y", temp_img]
        try:
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=creation_flags)
            if os.path.exists(temp_img): 
                CropEditor(self, temp_img, self.fill_crop_entries, self.current_lang)
            else:
                self.log(f"Snapshot Error: File not created. Check FFmpeg.", "error")
        except Exception as e: self.log(f"Snapshot Error: {str(e)}", "error")

    def fill_crop_entries(self, coords):
        w, h, x, y = coords
        if os.path.exists("temp_snap.jpg"):
            try: os.remove("temp_snap.jpg")
            except: pass
        self.entry_crop_w.delete(0, "end"); self.entry_crop_w.insert(0, str(w))
        self.entry_crop_h.delete(0, "end"); self.entry_crop_h.insert(0, str(h))
        self.entry_crop_x.delete(0, "end"); self.entry_crop_x.insert(0, str(x))
        self.entry_crop_y.delete(0, "end"); self.entry_crop_y.insert(0, str(y))

    def update_quality_label(self, value):
        txt = LANG[self.current_lang]["lbl_quality"]
        self.lbl_quality_val.configure(text=f"{txt}: {int(value)}%")

    def toggle_path_selection(self):
        if self.use_source_var.get():
            self.btn_browse.configure(state="disabled", fg_color="#333"); self.lbl_path.configure(text="[SOURCE]" if self.current_lang=="en" else "[KAYNAK]")
        else:
            self.btn_browse.configure(state="normal", fg_color="#444"); self.lbl_path.configure(text=self.output_folder if self.output_folder else "...")

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder: self.output_folder = folder; self.lbl_path.configure(text=f".../{os.path.basename(folder)}")

    def log(self, message, type="info"):
        color = COLOR_TEXT_DIM; prefix = "•"
        if type == "error": color = "#ff5252"
        if type == "success": color = "#69f0ae"
        self.log_lbl.configure(text=f"{prefix} {message}", text_color=color); self.update_idletasks()

    def drop_event(self, event):
        raw = event.data; files = [f.strip('{}') for f in raw.split('} {')] if raw.startswith('{') else raw.split()
        threading.Thread(target=self.scan_and_add_files, args=(files,)).start()

    def scan_and_add_files(self, paths):
        cnt = 0
        allow_img = self.filter_img_var.get()
        allow_aud = self.filter_audio_var.get()
        allow_vid = self.filter_video_var.get()
        for p in paths:
            if os.path.isdir(p):
                for r, d, f in os.walk(p):
                    for file in f:
                        if self.add_item_row(os.path.join(r, file), allow_img, allow_aud, allow_vid): cnt+=1
            elif os.path.isfile(p):
                if self.add_item_row(p, allow_img, allow_aud, allow_vid): cnt+=1
        if cnt>0: self.log(f"+{cnt} file(s)", "success")

    def add_item_row(self, file_path, allow_img, allow_aud, allow_vid):
        ext = os.path.splitext(file_path)[1].lower()
        is_valid = False
        if ext in IMAGE_EXTS and allow_img: is_valid = True
        elif ext in AUDIO_EXTS and allow_aud: is_valid = True
        elif ext in VIDEO_EXTS and allow_vid: is_valid = True
        if not is_valid: return False
        for item in self.file_items:
            if item['path'] == file_path: return False
        
        var = ctk.BooleanVar(value=True) 
        chk = ctk.CTkCheckBox(self.scroll_list, text=f" {os.path.basename(file_path)}", variable=var, font=("Roboto", 11), checkbox_width=20, checkbox_height=20, border_width=2, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, checkmark_color="black")
        chk.pack(anchor="w", pady=3, padx=10)
        self.file_items.append({'path': file_path, 'widget': chk, 'var': var})
        return True

    def toggle_select_all(self):
        state = self.select_all_var.get()
        for item in self.file_items:
            item['var'].set(state)

    def remove_checked_files(self):
        n_l = []; cnt = 0
        for i in self.file_items:
            if i['var'].get(): i['widget'].destroy(); cnt+=1
            else: n_l.append(i)
        self.file_items = n_l
        if cnt>0: self.log(f"-{cnt} file(s)", "info")
        # SCROLLBAR SIFIRLAMA (FIX)
        self.scroll_list._parent_canvas.yview_moveto(0.0)

    def clear_queue(self):
        for i in self.file_items: i['widget'].destroy()
        self.file_items = []; self.log("Queue cleared.", "info")
        # SCROLLBAR SIFIRLAMA (FIX)
        self.scroll_list._parent_canvas.yview_moveto(0.0)

    def run_ffmpeg(self, cmd_list):
        ffmpeg_cmd = get_ffmpeg_path() # Path Fix
        full_cmd = [ffmpeg_cmd] + cmd_list
        print(f"Running: {full_cmd}") 
        try:
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            subprocess.run(full_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, creationflags=creation_flags)
            return True
        except Exception as e: print(e); return False

    def start_process_thread(self):
        selected_count = sum([1 for i in self.file_items if i['var'].get()])
        if not self.file_items: messagebox.showwarning("!", LANG[self.current_lang]["msg_empty"]); return
        if selected_count == 0: messagebox.showwarning("!", LANG[self.current_lang]["msg_no_selection"]); return

        self.btn_start.configure(state="disabled", text=LANG[self.current_lang]["status_processing"])
        tab = self.tab_view.get()
        if tab in ["Resize", "Boyutlandır"]: threading.Thread(target=self.process_resize).start()
        elif tab in ["Optimizer", "Optimize Et"]: threading.Thread(target=self.process_optimize).start()
        elif tab in ["GIF Studio", "GIF Stüdyo"]: threading.Thread(target=self.process_gif).start()
        else: threading.Thread(target=self.process_convert).start()

    # --- PROCESSORS ---
    def process_resize(self):
        # 1. Custom
        custom_w, custom_h = None, None
        try:
            if self.entry_width.get() and self.entry_height.get():
                custom_w = int(self.entry_width.get())
                custom_h = int(self.entry_height.get())
        except: pass
        # 2. Presets
        presets = []
        if self.res_div2.get(): presets.append(0.5)
        if self.res_div4.get(): presets.append(0.25)
        if self.res_mul2.get(): presets.append(2.0)
        if self.res_mul4.get(): presets.append(4.0)

        if not custom_w and not presets:
            messagebox.showwarning("!", "Please select a resize mode."); self.finish_process(); return

        for item in self.file_items:
            if not item['var'].get(): continue
            path = item['path']; ext = os.path.splitext(path)[1].lower()
            if ext not in IMAGE_EXTS: continue
            save_dir = os.path.dirname(path) if self.use_source_var.get() else self.output_folder
            basename = os.path.splitext(os.path.basename(path))[0]
            try:
                with Image.open(path) as img:
                    if custom_w and custom_h:
                        out = os.path.join(save_dir, f"{basename}_{custom_w}x{custom_h}{ext}")
                        img.resize((custom_w, custom_h), Image.Resampling.LANCZOS).save(out)
                        self.log(f"Custom OK: {os.path.basename(out)}", "success")
                    for scale in presets:
                        nw = int(img.width * scale); nh = int(img.height * scale)
                        suffix = f"x{int(scale)}" if scale >= 1 else f"div{int(1/scale)}"
                        out = os.path.join(save_dir, f"{basename}_{suffix}{ext}")
                        img.resize((nw, nh), Image.Resampling.LANCZOS).save(out)
                        self.log(f"Preset OK: {os.path.basename(out)}", "success")
            except: self.log(f"Err: {basename}", "error")
        self.finish_process()

    def process_optimize(self):
        q = int(self.quality_val.get())
        for item in self.file_items:
            if not item['var'].get(): continue
            path = item['path']; ext = os.path.splitext(path)[1].lower()
            if ext not in IMAGE_EXTS: continue
            try:
                save = os.path.dirname(path) if self.use_source_var.get() else self.output_folder
                out = os.path.join(save, f"{os.path.splitext(os.path.basename(path))[0]}_opt{ext}")
                with Image.open(path) as img:
                    if ext in ['.jpg','.jpeg','.webp']: img.save(out, quality=q, optimize=True)
                    else: img.save(out, optimize=True)
                self.log(f"OK: {os.path.basename(out)}", "success")
            except: self.log(f"Err: {os.path.basename(path)}", "error")
        self.finish_process()

    def process_gif(self):
        start=self.entry_start.get(); end=self.entry_end.get()
        cw=self.entry_crop_w.get(); ch=self.entry_crop_h.get()
        cx=self.entry_crop_x.get(); cy=self.entry_crop_y.get()
        fps=self.seg_fps.get()
        try: sw=int(self.entry_gif_scale.get())
        except: sw=480
        
        for item in self.file_items:
            if not item['var'].get(): continue
            path=item['path']; ext=os.path.splitext(path)[1].lower()
            if ext not in VIDEO_EXTS: continue
            save = os.path.dirname(path) if self.use_source_var.get() else self.output_folder
            name = os.path.splitext(os.path.basename(path))[0]
            out = os.path.join(save, f"{name}.gif")
            cmd = ["-i", path]
            if start: cmd.extend(["-ss", start])
            if end: cmd.extend(["-to", end])
            vf = []
            if cw and ch:
                xx = cx if cx else f"(in_w-{cw})/2"
                yy = cy if cy else f"(in_h-{ch})/2"
                vf.append(f"crop={cw}:{ch}:{xx}:{yy}")
            vf.append(f"fps={fps},scale={sw}:-1:flags=lanczos")
            cmd.extend(["-vf", ",".join(vf), "-y", out])
            if self.run_ffmpeg(cmd): self.log(f"GIF OK: {name}.gif", "success")
            else: self.log(f"Err: {name}", "error")
        self.finish_process()

    def process_convert(self):
        t_img = self.img_option.get().lower(); t_aud = self.audio_option.get().lower()
        for item in self.file_items:
            if not item['var'].get(): continue
            path=item['path']; ext=os.path.splitext(path)[1].lower()
            save = os.path.dirname(path) if self.use_source_var.get() else self.output_folder
            name = os.path.splitext(os.path.basename(path))[0]
            try:
                if ext in IMAGE_EXTS:
                    out = os.path.join(save, f"{name}.{t_img}")
                    with Image.open(path) as img:
                        if t_img=='jpg' and img.mode in ('RGBA','LA'): img=img.convert('RGB')
                        if t_img=='ico': img.save(out, format='ICO', sizes=[(256,256)])
                        else: img.save(out, 'jpeg' if t_img=='jpg' else t_img)
                    self.log(f"OK: {name}.{t_img}", "success")
                elif ext in AUDIO_EXTS:
                    out = os.path.join(save, f"{name}.{t_aud}")
                    if self.run_ffmpeg(["-i", path, "-y", out]): self.log(f"OK: {name}.{t_aud}", "success")
            except: self.log(f"Err: {name}", "error")
        self.finish_process()

    def finish_process(self):
        self.log(LANG[self.current_lang]["status_done"], "success")
        self.btn_start.configure(state="normal", text=LANG[self.current_lang]["btn_start"])

if __name__ == "__main__":
    app = NoireConverterApp()
    app.mainloop()