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
import comtypes.client

# --- DİL PAKETİ (v1.3) ---
LANG = {
    "en": {
        "title": "Noire Converter v1.3",
        "drop_title": "DROP MEDIA",
        "drop_sub": "Files/Folders",
        "chk_img": "Img", "chk_aud": "Aud", "chk_vid": "Vid", "chk_doc": "Doc",
        "tab_convert": "Convert", "tab_resize": "Resize", "tab_opt": "Optimizer",
        "tab_gif": "GIF Studio", "tab_doc": "Doc Station", "tab_tools": "Renamer",
        "lbl_target_img": "Target Image Format",
        "lbl_target_aud": "Target Audio Format",
        "lbl_target_doc": "Conversion Mode",
        "lbl_new_dim": "Dimensions (Px)",
        "lbl_presets": "Quick Presets",
        "chk_div2": "½", "chk_div4": "¼", "chk_mul2": "2x", "chk_mul4": "4x",
        "lbl_quality": "Quality",
        "lbl_opt_hint": "ℹ️ Best for JPG/WebP.",
        "lbl_gif_time": "1. Time (Sec):",
        "lbl_gif_crop": "2. Crop:",
        "btn_visual_crop": "✂️ Editor",
        "lbl_gif_out": "3. Out:",
        "lbl_fps": "FPS",
        "lbl_doc_info": "ℹ️ Word/PPT -> PDF | PDF/PPT -> Word\nRequires Microsoft Office.",
        "lbl_tools_find": "Find Text:",
        "lbl_tools_rep": "Replace With:",
        "lbl_tools_info": "ℹ️ Replaces text in filenames. Leave 'Replace With' empty to delete text.",
        "sw_source": "Source Folder",
        "btn_browse": "Browse",
        "lbl_queue": "QUEUE",
        "btn_clear": "Clear", "btn_remove": "Remove", "chk_all": "All",
        "btn_start": "START",
        "status_ready": "Ready.", "status_processing": "Working...", "status_done": "Done.",
        "msg_no_video": "Select a video first.", "msg_empty": "Empty!", "msg_no_selection": "No selection!",
        "crop_tip": "Drag corners. Center to move.", "btn_apply": "APPLY",
        "plh_start": "Start", "plh_end": "End", "plh_w": "W", "plh_h": "H", "plh_x": "X", "plh_y": "Y",
        "guide_title": "USER MANUAL",
        "guide_text": """
1. RESIZE MODES
---------------------------
• Custom: Enter specific Width x Height.
• Presets (/2, x2...): Select multiple boxes.

2. GIF STUDIO
---------------------------
• Crop Editor: Takes a snapshot from video.
• Duration: Leave blank for full video.

3. DOC STATION
---------------------------
• Word (DOCX) -> PDF
• PowerPoint (PPTX) -> JUST PDF
• PDF -> Word (DOCX)
• Requires MS Office installed on PC.

4. RENAMER
---------------------------
• Find Text: Text to remove (e.g. _1500x1500).
• Replace With: Leave empty to delete.

5. SETUP
---------------------------
• 'ffmpeg.exe' must be in the same folder."""
    },
    "tr": {
        "title": "Noire Converter v1.3",
        "drop_title": "MEDYA SÜRÜKLE",
        "drop_sub": "Dosya/Klasör",
        "chk_img": "Img", "chk_aud": "Aud", "chk_vid": "Vid", "chk_doc": "Doc",
        "tab_convert": "Dönüştür", "tab_resize": "Boyutlandır", "tab_opt": "Optimize",
        "tab_gif": "GIF Stüdyo", "tab_doc": "Doc İstasyonu", "tab_tools": "Adlandır",
        "lbl_target_img": "Hedef Resim Formatı",
        "lbl_target_aud": "Hedef Ses Formatı",
        "lbl_target_doc": "Dönüştürme Modu",
        "lbl_new_dim": "Boyutlar (Px)",
        "lbl_presets": "Hızlı Ayarlar",
        "chk_div2": "½", "chk_div4": "¼", "chk_mul2": "2x", "chk_mul4": "4x",
        "lbl_quality": "Kalite",
        "lbl_opt_hint": "ℹ️ JPG/WebP için ideal.",
        "lbl_gif_time": "1. Süre (Sn):",
        "lbl_gif_crop": "2. Kırpma:",
        "btn_visual_crop": "✂️ Editör",
        "lbl_gif_out": "3. Çıktı:",
        "lbl_fps": "Kare/Sn",
        "lbl_doc_info": "ℹ️ Word/PPT -> PDF | PDF/PPT -> Word\nBilgisayarda MS Office yüklü olmalıdır.",
        "lbl_tools_find": "Bulunacak Metin:",
        "lbl_tools_rep": "Yeni Metin:",
        "lbl_tools_info": "ℹ️ Dosya adındaki metni değiştirir. Silmek için 'Yeni Metin'i boş bırakın.",
        "sw_source": "Kaynak Klasör",
        "btn_browse": "Seç...",
        "lbl_queue": "KUYRUK",
        "btn_clear": "Temizle", "btn_remove": "Sil", "chk_all": "Tümü",
        "btn_start": "BAŞLAT",
        "status_ready": "Hazır.", "status_processing": "İşleniyor...", "status_done": "Tamamlandı.",
        "msg_no_video": "Önce video seçin.", "msg_empty": "Liste boş!", "msg_no_selection": "Seçim yok!",
        "crop_tip": "Köşelerden boyutlandır. Ortadan taşı.", "btn_apply": "UYGULA",
        "plh_start": "Başla", "plh_end": "Bitir", "plh_w": "G", "plh_h": "Y", "plh_x": "X", "plh_y": "Y",
        "guide_title": "KULLANIM KILAVUZU",
        "guide_text": """
1. BOYUTLANDIRMA MODLARI
---------------------------
• Özel: Belirli bir Genişlik x Yükseklik girin.
• Hazır Ayarlar (/2, x2...): Çoklu seçim yapılabilir.

2. GIF STÜDYO
---------------------------
• Kırpma Editörü: Videodan örnek resim alır.
• Süre: Boş bırakılırsa tamamını işler.

3. DOC İSTASYONU
---------------------------
• Word (DOCX) -> PDF
• PowerPoint (PPTX) -> SADECE PDF
• PDF -> Word (DOCX)
• MS Office yüklü olmalıdır.

4. ADLANDIRICI
---------------------------
• Bulunacak Metin: Silinecek ek (örn: _1500x1500).
• Yeni Metin: Silmek için boş bırakın.

5. KURULUM
---------------------------
• 'ffmpeg.exe' aynı klasörde olmalıdır."""
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
DOC_EXTS   = ['.docx', '.doc', '.pptx', '.ppt', '.pdf']

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffmpeg = os.path.join(base_dir, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    if os.path.exists("ffmpeg.exe"):
        return "ffmpeg.exe"
    return "ffmpeg"

# --- CROP EDITOR ---
class CropEditor(ctk.CTkToplevel):
    def __init__(self, parent, image_path, callback, lang_code):
        super().__init__(parent)
        self.lang = lang_code
        self.callback = callback
        self.title("Crop Editor")
        self.geometry("900x750")
        self.attributes("-topmost", True)
        self.configure(fg_color="#000")
        
        try:
            self.iconbitmap(resource_path("App.ico"))
        except:
            pass

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
        for oid in self.overlay_ids:
            self.canvas.delete(oid)
        self.overlay_ids = []
        fill_color = "black"
        stipple = "gray50" 
        
        self.overlay_ids.append(self.canvas.create_rectangle(0, 0, self.cv_w, self.rect_y1, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(0, self.rect_y2, self.cv_w, self.cv_h, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(0, self.rect_y1, self.rect_x1, self.rect_y2, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(self.rect_x2, self.rect_y1, self.cv_w, self.rect_y2, fill=fill_color, stipple=stipple, outline=""))

        if self.rect_outline_id:
            self.canvas.delete(self.rect_outline_id)
        self.rect_outline_id = self.canvas.create_rectangle(self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2, outline=COLOR_ACCENT, width=2)
        
        for hid in self.handle_ids:
            self.canvas.delete(hid)
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
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def on_drag(self, event):
        if not self.drag_mode: return
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y
        min_x = self.offset_x
        max_x = self.offset_x + self.disp_w
        min_y = self.offset_y
        max_y = self.offset_y + self.disp_h
        
        if self.drag_mode == "move":
            w = self.rect_x2 - self.rect_x1
            h = self.rect_y2 - self.rect_y1
            nx1 = self.rect_x1 + dx
            ny1 = self.rect_y1 + dy
            nx2 = nx1 + w
            ny2 = ny1 + h
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

        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
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
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('com.noire.converter.v1_3')
        self.current_lang = "en"
        self.title("Noire Converter v1.3")
        self.geometry("1100x700") 
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)
        icon_file_path = resource_path("App.ico")
        if os.path.exists(icon_file_path):
            try:
                self.iconbitmap(icon_file_path)
                self.wm_iconbitmap(icon_file_path)
            except: pass
        self.file_items = []
        self.output_folder = "" 
        
        self.filter_img_var = ctk.BooleanVar(value=True)
        self.filter_audio_var = ctk.BooleanVar(value=True)
        self.filter_video_var = ctk.BooleanVar(value=True)
        self.filter_doc_var = ctk.BooleanVar(value=True)
        
        self.res_div2 = ctk.BooleanVar(value=False)
        self.res_div4 = ctk.BooleanVar(value=False)
        self.res_mul2 = ctk.BooleanVar(value=False)
        self.res_mul4 = ctk.BooleanVar(value=False)
        self.select_all_var = ctk.BooleanVar(value=True)

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_event)
        self.create_ui()
        self.update_ui_text()

    def create_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.left_col = ctk.CTkFrame(self.main_container, fg_color="transparent", width=420)
        self.left_col.pack(side="left", fill="y", padx=(0, 20))
        self.left_col.pack_propagate(False) 
        
        self.header_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        self.header_frame.pack(anchor="w", fill="x", pady=(0, 15))
        ctk.CTkLabel(self.header_frame, text="NOIRE", font=FONT_HEADER, text_color=COLOR_ACCENT).pack(side="left")
        ctk.CTkLabel(self.header_frame, text=" CONVERTER", font=FONT_HEADER, text_color="white").pack(side="left")
        ctk.CTkLabel(self.header_frame, text=" // v1.3", font=("Roboto", 12), text_color=COLOR_TEXT_DIM).pack(side="left", padx=(5,0), pady=(10,0))
        
        btn_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_box.pack(side="right")
        self.btn_lang = ctk.CTkButton(btn_box, text="TR", width=40, height=25, fg_color="#333", command=self.toggle_language)
        self.btn_lang.pack(side="left", padx=5)
        self.btn_help = ctk.CTkButton(btn_box, text="?", width=30, height=25, fg_color="#333", command=self.open_help_window)
        self.btn_help.pack(side="left")
        
        self.drop_frame = ctk.CTkFrame(self.left_col, height=200, corner_radius=12, fg_color=COLOR_FRAME, border_width=2, border_color="#2a2a2a")
        self.drop_frame.pack(fill="x", pady=(0, 15))
        self.drop_frame.pack_propagate(False)
        
        self.lbl_drop_title = ctk.CTkLabel(self.drop_frame, text="", font=("Roboto", 14, "bold"), text_color=COLOR_ACCENT)
        self.lbl_drop_title.place(relx=0.5, rely=0.20, anchor="center")
        self.lbl_drop_sub = ctk.CTkLabel(self.drop_frame, text="", text_color=COLOR_TEXT_DIM, font=("Roboto", 10))
        self.lbl_drop_sub.place(relx=0.5, rely=0.40, anchor="center")
        
        self.filter_box = ctk.CTkFrame(self.drop_frame, fg_color="transparent")
        self.filter_box.place(relx=0.55, rely=0.65, anchor="center")
        chk_style = {"checkbox_width":16, "checkbox_height":16, "font":("Roboto",11,"bold"), "fg_color":COLOR_ACCENT, "hover_color":COLOR_ACCENT_HOVER}
        
        self.chk_img = ctk.CTkCheckBox(self.filter_box, text="Img", variable=self.filter_img_var, **chk_style)
        self.chk_img.grid(row=0, column=0, padx=15, pady=3, sticky="w")
        self.chk_aud = ctk.CTkCheckBox(self.filter_box, text="Aud", variable=self.filter_audio_var, **chk_style)
        self.chk_aud.grid(row=0, column=1, padx=15, pady=3, sticky="w")
        self.chk_vid = ctk.CTkCheckBox(self.filter_box, text="Vid", variable=self.filter_video_var, **chk_style)
        self.chk_vid.grid(row=1, column=0, padx=15, pady=3, sticky="w")
        self.chk_doc = ctk.CTkCheckBox(self.filter_box, text="Doc", variable=self.filter_doc_var, **chk_style)
        self.chk_doc.grid(row=1, column=1, padx=15, pady=3, sticky="w")

        self.tab_view = ctk.CTkTabview(self.left_col, height=270, fg_color=COLOR_FRAME, segmented_button_fg_color="#111", segmented_button_selected_color=COLOR_ACCENT, segmented_button_selected_hover_color=COLOR_ACCENT_HOVER, segmented_button_unselected_color=COLOR_FRAME, text_color="white")
        self.tab_view.pack(fill="x", pady=(0, 15))
        self.tab_convert = self.tab_view.add("Convert")
        self.tab_resize = self.tab_view.add("Resize")
        self.tab_opt = self.tab_view.add("Optimizer")
        self.tab_gif = self.tab_view.add("GIF Studio")
        self.tab_docs = self.tab_view.add("Doc Station")
        self.tab_tools = self.tab_view.add("Renamer") # YENİ SEKME

        seg_style = {"fg_color": "#111", "selected_color": "#333", "text_color": "#fff", "height": 30}
        entry_style = {"height": 35, "fg_color": "#111", "border_color": "#333", "justify": "center"}
        
        # --- TAB İÇERİKLERİ ---
        self.lbl_target_img = ctk.CTkLabel(self.tab_convert, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_target_img.pack(anchor="w", pady=(10, 5))
        self.img_option = ctk.CTkSegmentedButton(self.tab_convert, values=["WEBP", "JPG", "PNG", "ICO"], **seg_style)
        self.img_option.set("WEBP")
        self.img_option.pack(fill="x", pady=(0, 15))
        self.lbl_target_aud = ctk.CTkLabel(self.tab_convert, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_target_aud.pack(anchor="w", pady=(0, 5))
        self.audio_option = ctk.CTkSegmentedButton(self.tab_convert, values=["MP3", "WAV"], **seg_style)
        self.audio_option.set("MP3")
        self.audio_option.pack(fill="x")
        
        self.lbl_new_dim = ctk.CTkLabel(self.tab_resize, text="", font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_new_dim.pack(pady=(10, 5))
        resize_box = ctk.CTkFrame(self.tab_resize, fg_color="transparent")
        resize_box.pack()
        self.entry_width = ctk.CTkEntry(resize_box, width=100, **entry_style)
        self.entry_width.pack(side="left", padx=5)
        ctk.CTkLabel(resize_box, text="x", font=("Roboto", 16, "bold"), text_color=COLOR_TEXT_DIM).pack(side="left", padx=5)
        self.entry_height = ctk.CTkEntry(resize_box, width=100, **entry_style)
        self.entry_height.pack(side="left", padx=5)
        self.lbl_presets = ctk.CTkLabel(self.tab_resize, text="", font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_presets.pack(pady=(15, 5))
        preset_frame = ctk.CTkFrame(self.tab_resize, fg_color="transparent")
        preset_frame.pack()
        self.chk_div2 = ctk.CTkCheckBox(preset_frame, text="", variable=self.res_div2, **chk_style)
        self.chk_div2.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.chk_div4 = ctk.CTkCheckBox(preset_frame, text="", variable=self.res_div4, **chk_style)
        self.chk_div4.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.chk_mul2 = ctk.CTkCheckBox(preset_frame, text="", variable=self.res_mul2, **chk_style)
        self.chk_mul2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.chk_mul4 = ctk.CTkCheckBox(preset_frame, text="", variable=self.res_mul4, **chk_style)
        self.chk_mul4.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.lbl_quality_head = ctk.CTkLabel(self.tab_opt, text="", font=FONT_SUBHEAD)
        self.lbl_quality_head.pack(pady=(20, 10))
        self.quality_val = ctk.IntVar(value=80)
        self.lbl_quality_val = ctk.CTkLabel(self.tab_opt, text="", font=("Roboto", 12), text_color=COLOR_ACCENT)
        self.lbl_quality_val.pack(pady=(0, 5))
        self.slider_quality = ctk.CTkSlider(self.tab_opt, from_=10, to=100, number_of_steps=90, variable=self.quality_val, command=self.update_quality_label, button_color=COLOR_ACCENT, button_hover_color=COLOR_ACCENT_HOVER, progress_color=COLOR_ACCENT)
        self.slider_quality.pack(fill="x", padx=50, pady=5)
        self.lbl_opt_hint = ctk.CTkLabel(self.tab_opt, text="", font=("Roboto", 11), text_color="gray")
        self.lbl_opt_hint.pack(pady=(20,5))

        time_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent")
        time_frame.pack(fill="x", pady=(10, 5), padx=5)
        self.lbl_gif_time = ctk.CTkLabel(time_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT)
        self.lbl_gif_time.pack(side="left", padx=(0,10))
        self.entry_start = ctk.CTkEntry(time_frame, width=60, **entry_style)
        self.entry_start.pack(side="left", padx=2)
        ctk.CTkLabel(time_frame, text="→", font=("Roboto", 14)).pack(side="left")
        self.entry_end = ctk.CTkEntry(time_frame, width=60, **entry_style)
        self.entry_end.pack(side="left", padx=2)
        crop_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent")
        crop_frame.pack(fill="x", pady=(5, 5), padx=5)
        self.lbl_gif_crop = ctk.CTkLabel(crop_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT)
        self.lbl_gif_crop.pack(side="left", padx=(0,10))
        self.btn_visual_crop = ctk.CTkButton(crop_frame, text="", width=90, height=28, fg_color="#333", hover_color="#444", font=("Roboto", 11, "bold"), command=self.open_visual_cropper)
        self.btn_visual_crop.pack(side="left", padx=(0, 10))
        self.entry_crop_w = ctk.CTkEntry(crop_frame, width=50, **entry_style)
        self.entry_crop_w.pack(side="left", padx=2)
        self.entry_crop_h = ctk.CTkEntry(crop_frame, width=50, **entry_style)
        self.entry_crop_h.pack(side="left", padx=2)
        self.entry_crop_x = ctk.CTkEntry(crop_frame, width=40, **entry_style)
        self.entry_crop_x.pack(side="left", padx=(10,2))
        self.entry_crop_y = ctk.CTkEntry(crop_frame, width=40, **entry_style)
        self.entry_crop_y.pack(side="left", padx=2)
        out_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent")
        out_frame.pack(fill="x", pady=(5, 5), padx=5)
        self.lbl_gif_out = ctk.CTkLabel(out_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT)
        self.lbl_gif_out.pack(side="left", padx=(0,10))
        self.entry_gif_scale = ctk.CTkEntry(out_frame, width=70, **entry_style)
        self.entry_gif_scale.insert(0, "480")
        self.entry_gif_scale.pack(side="left", padx=2)
        self.lbl_fps = ctk.CTkLabel(out_frame, text="", font=("Roboto", 11))
        self.lbl_fps.pack(side="right", padx=(5,0))
        self.seg_fps = ctk.CTkSegmentedButton(out_frame, values=["10", "15", "24", "30"], width=120, **seg_style)
        self.seg_fps.set("15")
        self.seg_fps.pack(side="right", padx=10)

        # --- DOC STATION ---
        self.lbl_target_doc = ctk.CTkLabel(self.tab_docs, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_target_doc.pack(anchor="w", pady=(15, 5))
        self.doc_option = ctk.CTkSegmentedButton(self.tab_docs, values=["TO PDF", "TO WORD"], **seg_style)
        self.doc_option.set("TO PDF")
        self.doc_option.pack(fill="x", pady=(0, 20))
        self.lbl_doc_info = ctk.CTkLabel(self.tab_docs, text="", font=("Roboto", 12), text_color="gray", justify="left")
        self.lbl_doc_info.pack(pady=20, padx=20)

        # --- RENAMER TAB  ---
        self.lbl_tools_find = ctk.CTkLabel(self.tab_tools, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_tools_find.pack(anchor="w", pady=(15, 5))
        
        self.entry_ren_find = ctk.CTkEntry(self.tab_tools, placeholder_text="_1500x1500", **entry_style)
        self.entry_ren_find.pack(fill="x", pady=(0, 10))
        
        self.lbl_tools_rep = ctk.CTkLabel(self.tab_tools, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_tools_rep.pack(anchor="w", pady=(5, 5))
        
        self.entry_ren_rep = ctk.CTkEntry(self.tab_tools, placeholder_text="", **entry_style)
        self.entry_ren_rep.pack(fill="x", pady=(0, 20))
        
        self.lbl_tools_info = ctk.CTkLabel(self.tab_tools, text="", font=("Roboto", 12), text_color="gray", justify="left")
        self.lbl_tools_info.pack(pady=20, padx=20)

        # --- ALT PANEL ---
        self.path_frame = ctk.CTkFrame(self.left_col, fg_color=COLOR_FRAME, corner_radius=8, height=45)
        self.path_frame.pack(fill="x", side="bottom")
        self.path_frame.pack_propagate(False)
        self.use_source_var = ctk.BooleanVar(value=True)
        self.switch_source = ctk.CTkSwitch(self.path_frame, text="", variable=self.use_source_var, command=self.toggle_path_selection, progress_color=COLOR_ACCENT, font=("Roboto", 12, "bold"))
        self.switch_source.pack(side="left", padx=15)
        self.btn_browse = ctk.CTkButton(self.path_frame, text="", width=60, height=24, fg_color="#333", state="disabled", command=self.select_output_folder)
        self.btn_browse.pack(side="right", padx=10)
        self.lbl_path = ctk.CTkLabel(self.path_frame, text="", font=("Roboto", 10), text_color=COLOR_TEXT_DIM)
        self.lbl_path.pack(side="right", padx=5)
        
        self.right_col = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_col.pack(side="right", fill="both", expand=True)
        list_header = ctk.CTkFrame(self.right_col, fg_color="transparent")
        list_header.pack(fill="x", pady=(0, 10))
        self.lbl_queue = ctk.CTkLabel(list_header, text="", font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_queue.pack(side="left")
        self.btn_clear = ctk.CTkButton(list_header, text="", width=80, height=24, fg_color="transparent", border_width=1, border_color="#333", text_color="#888", hover_color="#222", font=("Roboto", 11), command=self.clear_queue)
        self.btn_clear.pack(side="right")
        self.btn_remove = ctk.CTkButton(list_header, text="", width=110, height=24, fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, font=("Roboto", 11), command=self.remove_checked_files)
        self.btn_remove.pack(side="right", padx=(0,5))
        self.chk_select_all = ctk.CTkCheckBox(list_header, text="", width=80, variable=self.select_all_var, command=self.toggle_select_all, **chk_style)
        self.chk_select_all.pack(side="right", padx=(0,5))

        self.scroll_list = ctk.CTkScrollableFrame(self.right_col, fg_color=COLOR_FRAME, corner_radius=8)
        self.scroll_list.pack(fill="both", expand=True, pady=(0, 15))
        self.btn_start = ctk.CTkButton(self.right_col, text="", font=("Roboto", 16, "bold"), height=60, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", command=self.start_process_thread)
        self.btn_start.pack(fill="x", pady=(0, 10))
        self.log_lbl = ctk.CTkLabel(self.right_col, text="", font=FONT_LOG, text_color=COLOR_TEXT_DIM, anchor="w")
        self.log_lbl.pack(fill="x")

    def toggle_language(self):
        self.current_lang = "tr" if self.current_lang == "en" else "en"
        self.btn_lang.configure(text="EN" if self.current_lang == "tr" else "TR")
        self.update_ui_text()

    def open_help_window(self):
        help_win = ctk.CTkToplevel(self)
        help_win.title(LANG[self.current_lang]["guide_title"])
        help_win.geometry("500x500")
        help_win.attributes("-topmost", True)
        try:
            help_win.iconbitmap(resource_path("App.ico"))
        except:
            pass
        
        ctk.CTkLabel(help_win, text=LANG[self.current_lang]["guide_title"], font=FONT_HEADER, text_color=COLOR_ACCENT).pack(pady=20)
        tb = ctk.CTkTextbox(help_win, width=460, height=400, fg_color=COLOR_FRAME, font=("Consolas", 12))
        tb.pack(pady=10)
        tb.insert("1.0", LANG[self.current_lang]["guide_text"])
        tb.configure(state="disabled")

    def update_ui_text(self):
        T = LANG[self.current_lang]
        self.title(T["title"])
        self.lbl_drop_title.configure(text=T["drop_title"])
        self.lbl_drop_sub.configure(text=T["drop_sub"])
        self.chk_img.configure(text=T["chk_img"])
        self.chk_aud.configure(text=T["chk_aud"])
        self.chk_vid.configure(text=T["chk_vid"])
        self.chk_doc.configure(text=T["chk_doc"])
        self.lbl_target_img.configure(text=T["lbl_target_img"])
        self.lbl_target_aud.configure(text=T["lbl_target_aud"])
        self.lbl_target_doc.configure(text=T["lbl_target_doc"])
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
        self.lbl_doc_info.configure(text=T["lbl_doc_info"])
        self.lbl_tools_find.configure(text=T["lbl_tools_find"])
        self.lbl_tools_rep.configure(text=T["lbl_tools_rep"])
        self.lbl_tools_info.configure(text=T["lbl_tools_info"])
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
        self.entry_width.configure(placeholder_text=T["plh_w"])
        self.entry_height.configure(placeholder_text=T["plh_h"])
        self.entry_crop_w.configure(placeholder_text=T["plh_w"])
        self.entry_crop_h.configure(placeholder_text=T["plh_h"])
        self.entry_crop_x.configure(placeholder_text=T["plh_x"])
        self.entry_crop_y.configure(placeholder_text=T["plh_y"])

    def open_visual_cropper(self):
        target_video = None
        for item in self.file_items:
            if item['var'].get() and os.path.splitext(item['path'])[1].lower() in VIDEO_EXTS: 
                target_video = item['path']
                break
        if not target_video:
            messagebox.showwarning("!", LANG[self.current_lang]["msg_no_video"])
            return
        
        ffmpeg_cmd = get_ffmpeg_path()
        temp_img = "temp_snap.jpg"
        cmd = [ffmpeg_cmd, "-ss", "00:00:02", "-i", target_video, "-vframes", "1", "-q:v", "2", "-y", temp_img]
        try:
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=creation_flags)
            if os.path.exists(temp_img):
                CropEditor(self, temp_img, self.fill_crop_entries, self.current_lang)
            else:
                self.log(f"Snapshot Error: File not created.", "error")
        except Exception as e:
            self.log(f"Snapshot Error: {str(e)}", "error")

    def fill_crop_entries(self, coords):
        w, h, x, y = coords
        if os.path.exists("temp_snap.jpg"):
            try:
                os.remove("temp_snap.jpg")
            except:
                pass
        self.entry_crop_w.delete(0, "end")
        self.entry_crop_w.insert(0, str(w))
        self.entry_crop_h.delete(0, "end")
        self.entry_crop_h.insert(0, str(h))
        self.entry_crop_x.delete(0, "end")
        self.entry_crop_x.insert(0, str(x))
        self.entry_crop_y.delete(0, "end")
        self.entry_crop_y.insert(0, str(y))

    def update_quality_label(self, value):
        txt = LANG[self.current_lang]["lbl_quality"]
        self.lbl_quality_val.configure(text=f"{txt}: {int(value)}%")

    def toggle_path_selection(self):
        if self.use_source_var.get():
            self.btn_browse.configure(state="disabled", fg_color="#333")
            self.lbl_path.configure(text="[SOURCE]" if self.current_lang=="en" else "[KAYNAK]")
        else:
            self.btn_browse.configure(state="normal", fg_color="#444")
            self.lbl_path.configure(text=self.output_folder if self.output_folder else "...")

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.lbl_path.configure(text=f".../{os.path.basename(folder)}")

    def log(self, message, type="info"):
        color = COLOR_TEXT_DIM
        prefix = "•"
        if type == "error": color = "#ff5252"
        if type == "success": color = "#69f0ae"
        self.log_lbl.configure(text=f"{prefix} {message}", text_color=color)
        self.update_idletasks()

    def drop_event(self, event):
        raw = event.data
        files = [f.strip('{}') for f in raw.split('} {')] if raw.startswith('{') else raw.split()
        threading.Thread(target=self.scan_and_add_files, args=(files,)).start()

    def scan_and_add_files(self, paths):
        cnt = 0
        allow_img = self.filter_img_var.get()
        allow_aud = self.filter_audio_var.get()
        allow_vid = self.filter_video_var.get()
        allow_doc = self.filter_doc_var.get()
        
        for p in paths:
            if os.path.isdir(p):
                for r, d, f in os.walk(p):
                    for file in f:
                        if self.add_item_row(os.path.join(r, file), allow_img, allow_aud, allow_vid, allow_doc):
                            cnt+=1
            elif os.path.isfile(p):
                if self.add_item_row(p, allow_img, allow_aud, allow_vid, allow_doc):
                    cnt+=1
        if cnt>0: self.log(f"+{cnt} file(s)", "success")

    def add_item_row(self, file_path, allow_img, allow_aud, allow_vid, allow_doc):
        ext = os.path.splitext(file_path)[1].lower()
        is_valid = False
        if ext in IMAGE_EXTS and allow_img: is_valid = True
        elif ext in AUDIO_EXTS and allow_aud: is_valid = True
        elif ext in VIDEO_EXTS and allow_vid: is_valid = True
        elif ext in DOC_EXTS and allow_doc: is_valid = True
        
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
        n_l = []
        cnt = 0
        for i in self.file_items:
            if i['var'].get():
                i['widget'].destroy()
                cnt+=1
            else:
                n_l.append(i)
        self.file_items = n_l
        if cnt>0: self.log(f"-{cnt} file(s)", "info")
        self.scroll_list._parent_canvas.yview_moveto(0.0)

    def clear_queue(self):
        for i in self.file_items:
            i['widget'].destroy()
        self.file_items = []
        self.log("Queue cleared.", "info")
        self.scroll_list._parent_canvas.yview_moveto(0.0)

    def run_ffmpeg(self, cmd_list):
        ffmpeg_cmd = get_ffmpeg_path()
        full_cmd = [ffmpeg_cmd] + cmd_list
        try:
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            subprocess.run(full_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, creationflags=creation_flags)
            return True
        except Exception as e:
            print(e)
            return False

    def start_process_thread(self):
        selected_count = sum([1 for i in self.file_items if i['var'].get()])
        if not self.file_items:
            messagebox.showwarning("!", LANG[self.current_lang]["msg_empty"])
            return
        if selected_count == 0:
            messagebox.showwarning("!", LANG[self.current_lang]["msg_no_selection"])
            return

        self.btn_start.configure(state="disabled", text=LANG[self.current_lang]["status_processing"])
        tab = self.tab_view.get()
        
        if tab in ["Resize", "Boyutlandır"]: threading.Thread(target=self.process_resize).start()
        elif tab in ["Optimizer", "Optimize Et"]: threading.Thread(target=self.process_optimize).start()
        elif tab in ["GIF Studio", "GIF Stüdyo"]: threading.Thread(target=self.process_gif).start()
        elif tab in ["Doc Station", "Doc İstasyonu"]: threading.Thread(target=self.process_documents).start()
        elif tab in ["Renamer", "Adlandır"]: threading.Thread(target=self.process_rename).start()
        else: threading.Thread(target=self.process_convert).start()

    # --- PROCESSORS ---
    def process_resize(self):
        custom_w, custom_h = None, None
        try:
            if self.entry_width.get() and self.entry_height.get():
                custom_w = int(self.entry_width.get())
                custom_h = int(self.entry_height.get())
        except: pass
        presets = []
        if self.res_div2.get(): presets.append(0.5)
        if self.res_div4.get(): presets.append(0.25)
        if self.res_mul2.get(): presets.append(2.0)
        if self.res_mul4.get(): presets.append(4.0)

        if not custom_w and not presets:
            messagebox.showwarning("!", "Please select a resize mode.")
            self.finish_process()
            return

        for item in self.file_items:
            if not item['var'].get(): continue
            path = item['path']
            ext = os.path.splitext(path)[1].lower()
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
                        nw = int(img.width * scale)
                        nh = int(img.height * scale)
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
            path = item['path']
            ext = os.path.splitext(path)[1].lower()
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
        start=self.entry_start.get()
        end=self.entry_end.get()
        cw=self.entry_crop_w.get()
        ch=self.entry_crop_h.get()
        cx=self.entry_crop_x.get()
        cy=self.entry_crop_y.get()
        fps=self.seg_fps.get()
        try: sw=int(self.entry_gif_scale.get())
        except: sw=480
        
        for item in self.file_items:
            if not item['var'].get(): continue
            path=item['path']
            ext=os.path.splitext(path)[1].lower()
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
        t_img = self.img_option.get().lower()
        t_aud = self.audio_option.get().lower()
        for item in self.file_items:
            if not item['var'].get(): continue
            path=item['path']
            ext=os.path.splitext(path)[1].lower()
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

    # --- DOC STATION ---
    def process_documents(self):
        try:
            comtypes.CoInitialize()
        except:
            pass
        
        mode = self.doc_option.get() # "TO PDF" or "TO WORD"
        word_app = None
        ppt_app = None
        
        # Word Sabitleri
        wdFormatPDF = 17
        wdFormatDocumentDefault = 16
        # PPT Sabitleri
        ppSaveAsPDF = 32
        ppSaveAsRTF = 6

        def get_word():
            nonlocal word_app
            if not word_app: 
                word_app = comtypes.client.CreateObject("Word.Application")
                word_app.Visible = False
                word_app.DisplayAlerts = 0 
            return word_app
        
        def get_ppt():
            nonlocal ppt_app
            if not ppt_app:
                ppt_app = comtypes.client.CreateObject("Powerpoint.Application")
            return ppt_app

        for item in self.file_items:
            if not item['var'].get(): continue
            
            raw_path = item['path']
            abs_path = os.path.abspath(raw_path)
            ext = os.path.splitext(raw_path)[1].lower()
            if ext not in DOC_EXTS: continue
            
            base_folder = os.path.dirname(raw_path) if self.use_source_var.get() else self.output_folder
            save_dir = os.path.abspath(base_folder)
            name = os.path.splitext(os.path.basename(raw_path))[0]
            
            try:
                # --- PDF DÖNÜŞÜMLERİ ---
                if mode == "TO PDF":
                    if ext in ['.docx', '.doc']:
                        w = get_word()
                        doc = w.Documents.Open(abs_path)
                        out = os.path.join(save_dir, f"{name}.pdf")
                        doc.SaveAs(out, FileFormat=wdFormatPDF)
                        doc.Close()
                        self.log(f"DOC->PDF: {name}", "success")
                        
                    elif ext in ['.pptx', '.ppt']:
                        p = get_ppt()
                        deck = p.Presentations.Open(abs_path, WithWindow=False)
                        out = os.path.join(save_dir, f"{name}.pdf")
                        deck.SaveAs(out, ppSaveAsPDF)
                        deck.Close()
                        self.log(f"PPT->PDF: {name}", "success")
                
                # --- WORD DÖNÜŞÜMLERİ ---
                elif mode == "TO WORD":
                    if ext == '.pdf':
                        w = get_word()
                        doc = w.Documents.Open(abs_path) 
                        out = os.path.join(save_dir, f"{name}.docx")
                        doc.SaveAs(out, FileFormat=wdFormatDocumentDefault)
                        doc.Close()
                        self.log(f"PDF->DOC: {name}", "success")
                    
                    elif ext in ['.pptx', '.ppt']:
                        # PPT -> RTF -> WORD (Outline Method)
                        p = get_ppt()
                        w = get_word()
                        
                        # 1. PPT aç ve RTF olarak kaydet
                        deck = p.Presentations.Open(abs_path, WithWindow=False)
                        temp_rtf = os.path.join(save_dir, f"{name}_temp_outline.rtf")
                        deck.SaveAs(temp_rtf, ppSaveAsRTF)
                        deck.Close()
                        
                        # 2. Word ile RTF'i aç ve DOCX yap
                        if os.path.exists(temp_rtf):
                            doc = w.Documents.Open(temp_rtf)
                            out = os.path.join(save_dir, f"{name}.docx")
                            doc.SaveAs(out, FileFormat=wdFormatDocumentDefault)
                            doc.Close()
                            os.remove(temp_rtf)
                            self.log(f"PPT->DOC: {name}", "success")
                        else:
                            self.log(f"Err: PPT Export Fail", "error")

            except Exception as e:
                err_msg = str(e)
                self.log(f"Err: {err_msg[:30]}...", "error")
                print(f"FULL ERROR: {e}")
        
        if word_app: 
            try: word_app.Quit()
            except: pass
        if ppt_app: 
            try: ppt_app.Quit()
            except: pass
            
        self.finish_process()

    # --- RENAMER PROCESSOR ---
    def process_rename(self):
        find_text = self.entry_ren_find.get()
        rep_text = self.entry_ren_rep.get()
        
        if not find_text:
            messagebox.showwarning("!", "Please enter text to find.")
            self.finish_process()
            return

        cnt = 0
        for item in self.file_items:
            if not item['var'].get(): continue
            
            old_path = item['path']
            folder = os.path.dirname(old_path)
            old_name = os.path.basename(old_path)
            
            if find_text in old_name:
                new_name = old_name.replace(find_text, rep_text)
                new_path = os.path.join(folder, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    # UI güncellemesi
                    item['path'] = new_path 
                    item['widget'].configure(text=f" {new_name}")
                    self.log(f"Renamed: {new_name}", "success")
                    cnt += 1
                except Exception as e:
                    self.log(f"Err Rename: {old_name}", "error")
        
        if cnt == 0:
            self.log("No files matched the text.", "info")
            
        self.finish_process()

    def finish_process(self):
        self.log(LANG[self.current_lang]["status_done"], "success")
        self.btn_start.configure(state="normal", text=LANG[self.current_lang]["btn_start"])

if __name__ == "__main__":
    app = NoireConverterApp()
    app.mainloop()