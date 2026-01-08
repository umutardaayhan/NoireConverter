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
        "title": "Noire Converter v1.0",
        "drop_title": "DROP MEDIA HERE",
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
        "lbl_new_dim": "New Dimensions (Pixels)",
        "lbl_quality": "Compression Quality",
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
        "btn_start": "START OPERATION",
        "status_ready": "System Ready.",
        "status_processing": "PROCESSING...",
        "status_done": "Operation Completed.",
        "msg_no_video": "Please add a video file to the queue first.",
        "msg_empty": "Queue is empty!",
        "crop_tip": "Drag corners to resize. Drag center to move.",
        "btn_apply": "APPLY CROP",
        "plh_start": "Start",
        "plh_end": "End",
        "plh_w": "W",
        "plh_h": "H",
        "plh_x": "X",
        "plh_y": "Y",
    },
    "tr": {
        "title": "Noire Converter v1.0",
        "drop_title": "MEDYA YÜKLE",
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
        "lbl_new_dim": "Yeni Boyutlar (Piksel)",
        "lbl_quality": "Sıkıştırma Kalitesi",
        "lbl_gif_time": "1. Süre (Sn):",
        "lbl_gif_crop": "2. Kırpma:",
        "btn_visual_crop": "✂️ Editör",
        "lbl_gif_out": "3. Çıktı:",
        "lbl_fps": "Kare/Sn",
        "sw_source": "Kaynak Klasörü Kullan",
        "btn_browse": "Seç...",
        "lbl_queue": "İŞLEM KUYRUĞU",
        "btn_clear": "Temizle",
        "btn_remove": "Seçileni Sil",
        "btn_start": "İŞLEMİ BAŞLAT",
        "status_ready": "Sistem Hazır.",
        "status_processing": "İŞLENİYOR...",
        "status_done": "İşlem Tamamlandı.",
        "msg_no_video": "Lütfen önce listeye bir video ekleyin.",
        "msg_empty": "Liste boş!",
        "crop_tip": "Köşeleri sürükleyerek daraltın. Ortadan tutarak taşıyın.",
        "btn_apply": "KIRPMAYI UYGULA",
        "plh_start": "Başla",
        "plh_end": "Bitir",
        "plh_w": "G",
        "plh_h": "Y",
        "plh_x": "X",
        "plh_y": "Y",
    },
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

IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".ico"]
AUDIO_EXTS = [".mp3", ".wav", ".ogg", ".flac", ".m4a"]
VIDEO_EXTS = [".mp4", ".avi", ".mkv", ".mov", ".flv", ".webm"]

# Crop editor "magic numbers" (okunurluk + ayarlanabilirlik)
CROP_CANVAS_W = 800
CROP_CANVAS_H = 550
CROP_HANDLE_SIZE = 8
CROP_HITBOX = 15
CROP_MIN_RECT = 10


def is_windows() -> bool:
    return os.name == "nt"


def creation_flags_no_window() -> int:
    # Windows'ta ffmpeg konsol penceresi açmasın
    return subprocess.CREATE_NO_WINDOW if is_windows() else 0


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# --- CROP EDITOR  ---
class CropEditor(ctk.CTkToplevel):
    def __init__(self, parent, image_path, callback, lang_code):
        super().__init__(parent)

        self.lang = lang_code
        self.callback = callback

        self.title("Crop Editor" if self.lang == "en" else "Kırpma Editörü")
        self.geometry("900x750")
        self.configure(fg_color="#000")

        # Topmost: pratik ama bazen can sıkabilir; True bırakıyorum (orijinal davranış)
        self.attributes("-topmost", True)

        self.pil_img = Image.open(image_path)
        self.orig_w, self.orig_h = self.pil_img.size

        self.cv_w, self.cv_h = CROP_CANVAS_W, CROP_CANVAS_H

        # Görseli canvas'a sığdırmak için ölçek (crop koordinatları buna göre geri çevrilecek)
        self.scale = min(self.cv_w / self.orig_w, self.cv_h / self.orig_h)
        self.disp_w = int(self.orig_w * self.scale)
        self.disp_h = int(self.orig_h * self.scale)

        self.offset_x = (self.cv_w - self.disp_w) // 2
        self.offset_y = (self.cv_h - self.disp_h) // 2

        img_resized = self.pil_img.resize((self.disp_w, self.disp_h), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_resized)

        ctk.CTkLabel(self, text=LANG[self.lang]["crop_tip"], text_color="gray").pack(pady=5)

        self.canvas = tk.Canvas(
            self,
            width=self.cv_w,
            height=self.cv_h,
            bg="#111",
            highlightthickness=0,
            cursor="arrow",
        )
        self.canvas.pack(pady=10)
        self.canvas.create_image(self.offset_x, self.offset_y, anchor="nw", image=self.tk_img)

        ctk.CTkButton(
            self,
            text=LANG[self.lang]["btn_apply"],
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="black",
            command=self.finish,
        ).pack(pady=10)

        # Başlangıçta tüm alan seçili
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
        # Overlay temizle
        for oid in self.overlay_ids:
            self.canvas.delete(oid)
        self.overlay_ids = []

        fill_color = "black"
        stipple = "gray50"

        # Seçim dışını karart
        self.overlay_ids.append(
            self.canvas.create_rectangle(0, 0, self.cv_w, self.rect_y1, fill=fill_color, stipple=stipple, outline="")
        )
        self.overlay_ids.append(
            self.canvas.create_rectangle(0, self.rect_y2, self.cv_w, self.cv_h, fill=fill_color, stipple=stipple, outline="")
        )
        self.overlay_ids.append(
            self.canvas.create_rectangle(0, self.rect_y1, self.rect_x1, self.rect_y2, fill=fill_color, stipple=stipple, outline="")
        )
        self.overlay_ids.append(
            self.canvas.create_rectangle(self.rect_x2, self.rect_y1, self.cv_w, self.rect_y2, fill=fill_color, stipple=stipple, outline="")
        )

        # Outline
        if self.rect_outline_id:
            self.canvas.delete(self.rect_outline_id)
        self.rect_outline_id = self.canvas.create_rectangle(
            self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2, outline=COLOR_ACCENT, width=2
        )

        # Handle'lar
        for hid in self.handle_ids:
            self.canvas.delete(hid)
        self.handle_ids = []

        coords = [
            (self.rect_x1, self.rect_y1),
            (self.rect_x2, self.rect_y1),
            (self.rect_x1, self.rect_y2),
            (self.rect_x2, self.rect_y2),
        ]
        for cx, cy in coords:
            self.handle_ids.append(
                self.canvas.create_rectangle(
                    cx - CROP_HANDLE_SIZE,
                    cy - CROP_HANDLE_SIZE,
                    cx + CROP_HANDLE_SIZE,
                    cy + CROP_HANDLE_SIZE,
                    fill=COLOR_ACCENT,
                    outline="black",
                )
            )

    def get_interaction_mode(self, x, y):
        th = CROP_HITBOX

        if abs(x - self.rect_x1) < th and abs(y - self.rect_y1) < th:
            return "nw"
        if abs(x - self.rect_x2) < th and abs(y - self.rect_y1) < th:
            return "ne"
        if abs(x - self.rect_x1) < th and abs(y - self.rect_y2) < th:
            return "sw"
        if abs(x - self.rect_x2) < th and abs(y - self.rect_y2) < th:
            return "se"
        if self.rect_x1 < x < self.rect_x2 and self.rect_y1 < y < self.rect_y2:
            return "move"
        return None

    def on_press(self, event):
        self.drag_mode = self.get_interaction_mode(event.x, event.y)
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def on_drag(self, event):
        if not self.drag_mode:
            return

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

            # sınırlar
            if nx1 < min_x:
                nx1 = min_x
                nx2 = min_x + w
            if nx2 > max_x:
                nx2 = max_x
                nx1 = max_x - w
            if ny1 < min_y:
                ny1 = min_y
                ny2 = min_y + h
            if ny2 > max_y:
                ny2 = max_y
                ny1 = max_y - h

            self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2 = nx1, ny1, nx2, ny2
        else:
            # resize
            if "w" in self.drag_mode:
                self.rect_x1 = min(max(self.rect_x1 + dx, min_x), self.rect_x2 - CROP_MIN_RECT)
            if "e" in self.drag_mode:
                self.rect_x2 = max(min(self.rect_x2 + dx, max_x), self.rect_x1 + CROP_MIN_RECT)
            if "n" in self.drag_mode:
                self.rect_y1 = min(max(self.rect_y1 + dy, min_y), self.rect_y2 - CROP_MIN_RECT)
            if "s" in self.drag_mode:
                self.rect_y2 = max(min(self.rect_y2 + dy, max_y), self.rect_y1 + CROP_MIN_RECT)

        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

        self.draw_selection()

    def on_hover(self, event):
        mode = self.get_interaction_mode(event.x, event.y)
        if mode == "move":
            self.canvas.config(cursor="fleur")
        elif mode in ("nw", "se"):
            self.canvas.config(cursor="sizing_nwse")
        elif mode in ("ne", "sw"):
            self.canvas.config(cursor="sizing_nesw")
        else:
            self.canvas.config(cursor="arrow")

    def finish(self):
        # Ekran koordinatını gerçek görsel koordinatına çevir
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

        # Windows AppID (taskbar icon grouping vs.)
        myappid = "com.noire.converter.v1"
        if is_windows():
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception:
                # kritik değil
                pass

        self.current_lang = "en"

        self.title(LANG[self.current_lang]["title"])
        self.geometry("1100x700")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        icon_file_path = resource_path("App.ico")
        if os.path.exists(icon_file_path):
            try:
                self.iconbitmap(icon_file_path)
                self.wm_iconbitmap(icon_file_path)
            except tk.TclError:
                # bazı ortamlar iconbitmap'i kabul etmiyor
                pass

        self.file_items = []
        self.output_folder = ""

        # Filtre değişkenleri
        self.filter_img_var = ctk.BooleanVar(value=True)
        self.filter_audio_var = ctk.BooleanVar(value=True)
        self.filter_video_var = ctk.BooleanVar(value=True)

        # Drag & drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.drop_event)

        self.create_ui()
        self.update_ui_text()

    def t(self, key: str) -> str:
        """Lang dictionary erişimi için küçük helper."""
        return LANG[self.current_lang].get(key, key)

    def create_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.left_col = ctk.CTkFrame(self.main_container, fg_color="transparent", width=420)
        self.left_col.pack(side="left", fill="y", padx=(0, 20))
        self.left_col.pack_propagate(False)

        # Header
        self.header_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        self.header_frame.pack(anchor="w", fill="x", pady=(0, 15))

        ctk.CTkLabel(self.header_frame, text="NOIRE", font=FONT_HEADER, text_color=COLOR_ACCENT).pack(side="left")
        ctk.CTkLabel(self.header_frame, text=" CONVERTER", font=FONT_HEADER, text_color="white").pack(side="left")
        ctk.CTkLabel(
            self.header_frame, text=" // v1.0", font=("Roboto", 12), text_color=COLOR_TEXT_DIM
        ).pack(side="left", padx=(5, 0), pady=(10, 0))

        self.btn_lang = ctk.CTkButton(
            self.header_frame, text="TR", width=40, height=25, fg_color="#333", command=self.toggle_language
        )
        self.btn_lang.pack(side="right")

        # Drop Zone & Filtreler
        self.drop_frame = ctk.CTkFrame(
            self.left_col,
            height=130,
            corner_radius=12,
            fg_color=COLOR_FRAME,
            border_width=2,
            border_color="#2a2a2a",
        )
        self.drop_frame.pack(fill="x", pady=(0, 15))
        self.drop_frame.pack_propagate(False)

        self.lbl_drop_title = ctk.CTkLabel(
            self.drop_frame, text="", font=("Roboto", 14, "bold"), text_color=COLOR_ACCENT
        )
        self.lbl_drop_title.place(relx=0.5, rely=0.30, anchor="center")

        self.lbl_drop_sub = ctk.CTkLabel(self.drop_frame, text="", text_color=COLOR_TEXT_DIM, font=("Roboto", 10))
        self.lbl_drop_sub.place(relx=0.5, rely=0.55, anchor="center")

        # Filtre checkboxları
        self.filter_box = ctk.CTkFrame(self.drop_frame, fg_color="transparent")
        self.filter_box.place(relx=0.5, rely=0.85, anchor="center")

        chk_style = {
            "checkbox_width": 16,
            "checkbox_height": 16,
            "font": ("Roboto", 11),
            "fg_color": COLOR_ACCENT,
            "hover_color": COLOR_ACCENT_HOVER,
        }
        self.chk_img = ctk.CTkCheckBox(self.filter_box, text="Img", variable=self.filter_img_var, **chk_style)
        self.chk_img.pack(side="left", padx=8)

        self.chk_aud = ctk.CTkCheckBox(self.filter_box, text="Aud", variable=self.filter_audio_var, **chk_style)
        self.chk_aud.pack(side="left", padx=8)

        self.chk_vid = ctk.CTkCheckBox(self.filter_box, text="Vid", variable=self.filter_video_var, **chk_style)
        self.chk_vid.pack(side="left", padx=8)

        # Sekmeler
        self.tab_view = ctk.CTkTabview(
            self.left_col,
            height=350,
            fg_color=COLOR_FRAME,
            segmented_button_fg_color="#111",
            segmented_button_selected_color=COLOR_ACCENT,
            segmented_button_selected_hover_color=COLOR_ACCENT_HOVER,
            segmented_button_unselected_color=COLOR_FRAME,
            text_color="white",
        )
        self.tab_view.pack(fill="x", pady=(0, 15))

        self.tab_convert = self.tab_view.add("Convert")
        self.tab_resize = self.tab_view.add("Resize")
        self.tab_opt = self.tab_view.add("Optimizer")
        self.tab_gif = self.tab_view.add("GIF Studio")

        seg_style = {"fg_color": "#111", "selected_color": "#333", "text_color": "#fff", "height": 30}
        entry_style = {"height": 35, "fg_color": "#111", "border_color": "#333", "justify": "center"}

        # T1 - Convert
        self.lbl_target_img = ctk.CTkLabel(self.tab_convert, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_target_img.pack(anchor="w", pady=(15, 5))

        self.img_option = ctk.CTkSegmentedButton(self.tab_convert, values=["WEBP", "JPG", "PNG", "ICO"], **seg_style)
        self.img_option.set("WEBP")
        self.img_option.pack(fill="x", pady=(0, 20))

        self.lbl_target_aud = ctk.CTkLabel(self.tab_convert, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_target_aud.pack(anchor="w", pady=(0, 5))

        self.audio_option = ctk.CTkSegmentedButton(self.tab_convert, values=["MP3", "WAV"], **seg_style)
        self.audio_option.set("MP3")
        self.audio_option.pack(fill="x")

        # T2 - Resize
        self.lbl_new_dim = ctk.CTkLabel(self.tab_resize, text="", font=FONT_SUBHEAD)
        self.lbl_new_dim.pack(pady=(40, 15))

        resize_box = ctk.CTkFrame(self.tab_resize, fg_color="transparent")
        resize_box.pack()

        self.entry_width = ctk.CTkEntry(resize_box, width=100, **entry_style)
        self.entry_width.pack(side="left", padx=5)

        ctk.CTkLabel(resize_box, text="x", font=("Roboto", 16, "bold"), text_color=COLOR_TEXT_DIM).pack(side="left", padx=5)

        self.entry_height = ctk.CTkEntry(resize_box, width=100, **entry_style)
        self.entry_height.pack(side="left", padx=5)

        # T3 - Optimizer
        self.lbl_quality_head = ctk.CTkLabel(self.tab_opt, text="", font=FONT_SUBHEAD)
        self.lbl_quality_head.pack(pady=(30, 10))

        self.quality_val = ctk.IntVar(value=80)
        self.lbl_quality_val = ctk.CTkLabel(self.tab_opt, text="", font=("Roboto", 12), text_color=COLOR_ACCENT)
        self.lbl_quality_val.pack(pady=(0, 5))

        self.slider_quality = ctk.CTkSlider(
            self.tab_opt,
            from_=10,
            to=100,
            number_of_steps=90,
            variable=self.quality_val,
            command=self.update_quality_label,
            button_color=COLOR_ACCENT,
            button_hover_color=COLOR_ACCENT_HOVER,
            progress_color=COLOR_ACCENT,
        )
        self.slider_quality.pack(fill="x", padx=50, pady=5)

        # T4 - GIF
        time_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent")
        time_frame.pack(fill="x", pady=(10, 5), padx=5)

        self.lbl_gif_time = ctk.CTkLabel(time_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT)
        self.lbl_gif_time.pack(side="left", padx=(0, 10))

        self.entry_start = ctk.CTkEntry(time_frame, width=60, **entry_style)
        self.entry_start.pack(side="left", padx=2)

        ctk.CTkLabel(time_frame, text="→", font=("Roboto", 14)).pack(side="left")

        self.entry_end = ctk.CTkEntry(time_frame, width=60, **entry_style)
        self.entry_end.pack(side="left", padx=2)

        crop_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent")
        crop_frame.pack(fill="x", pady=(5, 5), padx=5)

        self.lbl_gif_crop = ctk.CTkLabel(crop_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT)
        self.lbl_gif_crop.pack(side="left", padx=(0, 10))

        self.btn_visual_crop = ctk.CTkButton(
            crop_frame,
            text="",
            width=90,
            height=28,
            fg_color="#333",
            hover_color="#444",
            font=("Roboto", 11, "bold"),
            command=self.open_visual_cropper,
        )
        self.btn_visual_crop.pack(side="left", padx=(0, 10))

        self.entry_crop_w = ctk.CTkEntry(crop_frame, width=50, **entry_style)
        self.entry_crop_w.pack(side="left", padx=2)

        self.entry_crop_h = ctk.CTkEntry(crop_frame, width=50, **entry_style)
        self.entry_crop_h.pack(side="left", padx=2)

        self.entry_crop_x = ctk.CTkEntry(crop_frame, width=40, **entry_style)
        self.entry_crop_x.pack(side="left", padx=(10, 2))

        self.entry_crop_y = ctk.CTkEntry(crop_frame, width=40, **entry_style)
        self.entry_crop_y.pack(side="left", padx=2)

        out_frame = ctk.CTkFrame(self.tab_gif, fg_color="transparent")
        out_frame.pack(fill="x", pady=(5, 5), padx=5)

        self.lbl_gif_out = ctk.CTkLabel(out_frame, text="", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT)
        self.lbl_gif_out.pack(side="left", padx=(0, 10))

        self.entry_gif_scale = ctk.CTkEntry(out_frame, width=70, **entry_style)
        self.entry_gif_scale.insert(0, "480")
        self.entry_gif_scale.pack(side="left", padx=2)

        self.lbl_fps = ctk.CTkLabel(out_frame, text="", font=("Roboto", 11))
        self.lbl_fps.pack(side="right", padx=(5, 0))

        self.seg_fps = ctk.CTkSegmentedButton(out_frame, values=["10", "15", "24", "30"], width=120, **seg_style)
        self.seg_fps.set("15")
        self.seg_fps.pack(side="right", padx=10)

        # Output path
        self.path_frame = ctk.CTkFrame(self.left_col, fg_color=COLOR_FRAME, corner_radius=8, height=45)
        self.path_frame.pack(fill="x", side="bottom")
        self.path_frame.pack_propagate(False)

        self.use_source_var = ctk.BooleanVar(value=True)
        self.switch_source = ctk.CTkSwitch(
            self.path_frame,
            text="",
            variable=self.use_source_var,
            command=self.toggle_path_selection,
            progress_color=COLOR_ACCENT,
            font=("Roboto", 12, "bold"),
        )
        self.switch_source.pack(side="left", padx=15)

        self.btn_browse = ctk.CTkButton(
            self.path_frame,
            text="",
            width=60,
            height=24,
            fg_color="#333",
            state="disabled",
            command=self.select_output_folder,
        )
        self.btn_browse.pack(side="right", padx=10)

        self.lbl_path = ctk.CTkLabel(self.path_frame, text="", font=("Roboto", 10), text_color=COLOR_TEXT_DIM)
        self.lbl_path.pack(side="right", padx=5)

        # Right column (queue + log)
        self.right_col = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_col.pack(side="right", fill="both", expand=True)

        list_header = ctk.CTkFrame(self.right_col, fg_color="transparent")
        list_header.pack(fill="x", pady=(0, 10))

        self.lbl_queue = ctk.CTkLabel(list_header, text="", font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_queue.pack(side="left")

        self.btn_clear = ctk.CTkButton(
            list_header,
            text="",
            width=80,
            height=24,
            fg_color="transparent",
            border_width=1,
            border_color="#333",
            text_color="#888",
            hover_color="#222",
            font=("Roboto", 11),
            command=self.clear_queue,
        )
        self.btn_clear.pack(side="right")

        self.btn_remove = ctk.CTkButton(
            list_header,
            text="",
            width=110,
            height=24,
            fg_color=COLOR_DANGER,
            hover_color=COLOR_DANGER_HOVER,
            font=("Roboto", 11),
            command=self.remove_checked_files,
        )
        self.btn_remove.pack(side="right", padx=(0, 5))

        self.scroll_list = ctk.CTkScrollableFrame(self.right_col, fg_color=COLOR_FRAME, corner_radius=8)
        self.scroll_list.pack(fill="both", expand=True, pady=(0, 15))

        self.btn_start = ctk.CTkButton(
            self.right_col,
            text="",
            font=("Roboto", 16, "bold"),
            height=60,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="black",
            command=self.start_process_thread,
        )
        self.btn_start.pack(fill="x", pady=(0, 10))

        self.log_lbl = ctk.CTkLabel(self.right_col, text="", font=FONT_LOG, text_color=COLOR_TEXT_DIM, anchor="w")
        self.log_lbl.pack(fill="x")

    def toggle_language(self):
        self.current_lang = "tr" if self.current_lang == "en" else "en"
        self.btn_lang.configure(text="EN" if self.current_lang == "tr" else "TR")
        self.update_ui_text()

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

        self.lbl_quality_head.configure(text=T["lbl_quality"])
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

        # dil değişince path text de güncellensin
        self.toggle_path_selection()

    def open_visual_cropper(self):
        target_video = None
        for item in self.file_items:
            if os.path.splitext(item["path"])[1].lower() in VIDEO_EXTS:
                target_video = item["path"]
                break

        if not target_video:
            messagebox.showwarning("!", self.t("msg_no_video"))
            return

        ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
        temp_img = "temp_snap.jpg"

        cmd = [
            ffmpeg_cmd,
            "-ss",
            "00:00:02",
            "-i",
            target_video,
            "-vframes",
            "1",
            "-q:v",
            "2",
            "-y",
            temp_img,
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creation_flags_no_window(),
            )
            if os.path.exists(temp_img):
                CropEditor(self, temp_img, self.fill_crop_entries, self.current_lang)
        except subprocess.CalledProcessError as e:
            self.log(f"Snapshot Error: {e}", "error")
        except Exception as e:
            self.log(f"Snapshot Error: {e}", "error")

    def fill_crop_entries(self, coords):
        w, h, x, y = coords

        # temp dosyayı temizle
        if os.path.exists("temp_snap.jpg"):
            try:
                os.remove("temp_snap.jpg")
            except OSError:
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
        txt = self.t("lbl_quality")
        self.lbl_quality_val.configure(text=f"{txt}: {int(value)}%")

    def toggle_path_selection(self):
        if self.use_source_var.get():
            self.btn_browse.configure(state="disabled", fg_color="#333")
            self.lbl_path.configure(text="[SOURCE]" if self.current_lang == "en" else "[KAYNAK]")
            return

        self.btn_browse.configure(state="normal", fg_color="#444")
        self.lbl_path.configure(text=self.output_folder if self.output_folder else "...")

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.output_folder = folder
        self.lbl_path.configure(text=f".../{os.path.basename(folder)}")

    def log(self, message, kind="info"):
        color = COLOR_TEXT_DIM
        prefix = "•"

        if kind == "error":
            color = "#ff5252"
        elif kind == "success":
            color = "#69f0ae"

        self.log_lbl.configure(text=f"{prefix} {message}", text_color=color)
        self.update_idletasks()

    def drop_event(self, event):
        raw = event.data

        # tkdnd bazen "{a} {b}" formatında, bazen düz string döndürüyor
        if raw.startswith("{"):
            files = [f.strip("{}") for f in raw.split("} {")]
        else:
            files = raw.split()

        threading.Thread(target=self.scan_and_add_files, args=(files,), daemon=True).start()

    def scan_and_add_files(self, paths):
        added = 0

        allow_img = self.filter_img_var.get()
        allow_aud = self.filter_audio_var.get()
        allow_vid = self.filter_video_var.get()

        for p in paths:
            if os.path.isdir(p):
                for r, _, filenames in os.walk(p):
                    for fname in filenames:
                        full = os.path.join(r, fname)
                        if self.add_item_row(full, allow_img, allow_aud, allow_vid):
                            added += 1
            elif os.path.isfile(p):
                if self.add_item_row(p, allow_img, allow_aud, allow_vid):
                    added += 1

        if added > 0:
            self.log(f"+{added} file(s)", "success")

    def add_item_row(self, file_path, allow_img, allow_aud, allow_vid):
        ext = os.path.splitext(file_path)[1].lower()

        if ext in IMAGE_EXTS and allow_img:
            pass
        elif ext in AUDIO_EXTS and allow_aud:
            pass
        elif ext in VIDEO_EXTS and allow_vid:
            pass
        else:
            return False

        # Aynı dosya tekrar eklenmesin
        for item in self.file_items:
            if item["path"] == file_path:
                return False

        var = ctk.BooleanVar(value=False)
        chk = ctk.CTkCheckBox(
            self.scroll_list,
            text=f" {os.path.basename(file_path)}",
            variable=var,
            font=("Roboto", 11),
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            checkmark_color="black",
        )
        chk.pack(anchor="w", pady=3, padx=10)

        self.file_items.append({"path": file_path, "widget": chk, "var": var})
        return True

    def remove_checked_files(self):
        kept = []
        removed = 0

        for item in self.file_items:
            if item["var"].get():
                item["widget"].destroy()
                removed += 1
            else:
                kept.append(item)

        self.file_items = kept

        if removed > 0:
            self.log(f"-{removed} file(s)", "info")

    def clear_queue(self):
        for item in self.file_items:
            item["widget"].destroy()

        self.file_items = []
        self.log("Queue cleared.", "info")

    def run_ffmpeg(self, cmd_list):
        ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
        full_cmd = [ffmpeg_cmd] + cmd_list

        # Debug çıktısı kalsın (orijinalde vardı)
        print(f"DEBUG: {' '.join(full_cmd)}")

        try:
            subprocess.run(
                full_cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                creationflags=creation_flags_no_window(),
            )
            return True
        except subprocess.CalledProcessError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False

    def start_process_thread(self):
        if not self.file_items:
            messagebox.showwarning("!", self.t("msg_empty"))
            return

        self.btn_start.configure(state="disabled", text=self.t("status_processing"))

        tab = self.tab_view.get()

        if tab in ("Resize", "Boyutlandır"):
            threading.Thread(target=self.process_resize, daemon=True).start()
        elif tab in ("Optimizer", "Optimize Et"):
            threading.Thread(target=self.process_optimize, daemon=True).start()
        elif tab in ("GIF Studio", "GIF Stüdyo"):
            threading.Thread(target=self.process_gif, daemon=True).start()
        else:
            threading.Thread(target=self.process_convert, daemon=True).start()

    def process_resize(self):
        try:
            w = int(self.entry_width.get())
            h = int(self.entry_height.get())
        except ValueError:
            messagebox.showerror("!", "Error")
            self.finish_process()
            return

        for item in self.file_items:
            path = item["path"]
            ext = os.path.splitext(path)[1].lower()

            if ext not in IMAGE_EXTS:
                continue

            try:
                save_dir = os.path.dirname(path) if self.use_source_var.get() else self.output_folder
                out = os.path.join(save_dir, f"{os.path.splitext(os.path.basename(path))[0]}_{w}x{h}{ext}")

                Image.open(path).resize((w, h), Image.Resampling.LANCZOS).save(out)
                self.log(f"OK: {os.path.basename(out)}", "success")
            except Exception:
                self.log(f"Err: {os.path.basename(path)}", "error")

        self.finish_process()

    def process_optimize(self):
        q = int(self.quality_val.get())

        for item in self.file_items:
            path = item["path"]
            ext = os.path.splitext(path)[1].lower()

            if ext not in IMAGE_EXTS:
                continue

            try:
                save_dir = os.path.dirname(path) if self.use_source_var.get() else self.output_folder
                out = os.path.join(save_dir, f"{os.path.splitext(os.path.basename(path))[0]}_opt{ext}")

                with Image.open(path) as img:
                    if ext in (".jpg", ".jpeg", ".webp"):
                        img.save(out, quality=q, optimize=True)
                    else:
                        img.save(out, optimize=True)

                self.log(f"OK: {os.path.basename(out)}", "success")
            except Exception:
                self.log(f"Err: {os.path.basename(path)}", "error")

        self.finish_process()

    def process_gif(self):
        start = self.entry_start.get()
        end = self.entry_end.get()

        cw = self.entry_crop_w.get()
        ch = self.entry_crop_h.get()
        cx = self.entry_crop_x.get()
        cy = self.entry_crop_y.get()

        fps = self.seg_fps.get()

        try:
            sw = int(self.entry_gif_scale.get())
        except ValueError:
            sw = 480

        for item in self.file_items:
            path = item["path"]
            ext = os.path.splitext(path)[1].lower()

            if ext not in VIDEO_EXTS:
                continue

            save_dir = os.path.dirname(path) if self.use_source_var.get() else self.output_folder
            name = os.path.splitext(os.path.basename(path))[0]
            out = os.path.join(save_dir, f"{name}.gif")

            cmd = ["-i", path]

            if start:
                cmd.extend(["-ss", start])
            if end:
                cmd.extend(["-to", end])

            vf = []

            if cw and ch:
                xx = cx if cx else f"(in_w-{cw})/2"
                yy = cy if cy else f"(in_h-{ch})/2"
                vf.append(f"crop={cw}:{ch}:{xx}:{yy}")

            vf.append(f"fps={fps},scale={sw}:-1:flags=lanczos")

            cmd.extend(["-vf", ",".join(vf), "-y", out])

            if self.run_ffmpeg(cmd):
                self.log(f"GIF OK: {name}.gif", "success")
            else:
                self.log(f"Err: {name}", "error")

        self.finish_process()

    def process_convert(self):
        t_img = self.img_option.get().lower()
        t_aud = self.audio_option.get().lower()

        for item in self.file_items:
            path = item["path"]
            ext = os.path.splitext(path)[1].lower()

            save_dir = os.path.dirname(path) if self.use_source_var.get() else self.output_folder
            name = os.path.splitext(os.path.basename(path))[0]

            try:
                if ext in IMAGE_EXTS:
                    out = os.path.join(save_dir, f"{name}.{t_img}")

                    with Image.open(path) as img:
                        if t_img == "jpg" and img.mode in ("RGBA", "LA"):
                            img = img.convert("RGB")

                        if t_img == "ico":
                            img.save(out, format="ICO", sizes=[(256, 256)])
                        else:
                            img.save(out, "jpeg" if t_img == "jpg" else t_img)

                    self.log(f"OK: {name}.{t_img}", "success")

                elif ext in AUDIO_EXTS:
                    out = os.path.join(save_dir, f"{name}.{t_aud}")
                    if self.run_ffmpeg(["-i", path, "-y", out]):
                        self.log(f"OK: {name}.{t_aud}", "success")

            except Exception:
                self.log(f"Err: {name}", "error")

        self.finish_process()

    def finish_process(self):
        self.log(self.t("status_done"), "success")
        self.btn_start.configure(state="normal", text=self.t("btn_start"))


if __name__ == "__main__":
    app = NoireConverterApp()
    app.mainloop()
