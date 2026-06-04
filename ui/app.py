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
from deep_translator import GoogleTranslator
import json

from core.config import *
from core.utils import resource_path, get_ffmpeg_path
from core.file_ops import collect_files, prefix_rename
from ui.components.crop_editor import CropEditor

class NoireConverterApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('com.noire.converter.v1_3')
        self.current_lang = "en"
        self.title("Noire Converter v1.7")
        self.geometry("1180x800") 
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
        
        # --- Translation Variables ---
        self.translate_target_lang = ctk.StringVar(value="TR")
        self.translate_source_lang = ctk.StringVar(value="auto")
        self.translate_mode = ctk.StringVar(value="separate")  # "separate" veya "same"
        self.translated_content = {}  # Dosya yolu -> çeviri içeriği
        
        # Persistence
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.settings = self.load_config()
        
        self.filter_img_var = ctk.BooleanVar(value=True)
        self.filter_audio_var = ctk.BooleanVar(value=True)
        self.filter_video_var = ctk.BooleanVar(value=True)
        self.filter_doc_var = ctk.BooleanVar(value=True)
        
        self.res_div2 = ctk.BooleanVar(value=False)
        self.res_div4 = ctk.BooleanVar(value=False)
        self.res_mul2 = ctk.BooleanVar(value=False)
        self.res_mul4 = ctk.BooleanVar(value=False)
        self.select_all_var = ctk.BooleanVar(value=True)
        self._thumb_cache = {}
        self.queue_limit_var = ctk.StringVar(value="100")

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_event)
        self.create_ui()
        self.update_ui_text()

    def create_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sol paneli scrollable frame ile sarma
        self.left_col = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", width=500, scrollbar_button_color="#222", scrollbar_button_hover_color=COLOR_ACCENT)
        self.left_col.pack(side="left", fill="y", padx=(0, 20)) 
        
        self.header_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        self.header_frame.pack(anchor="w", fill="x", pady=(0, 15))
        ctk.CTkLabel(self.header_frame, text="NOIRE", font=FONT_HEADER, text_color=COLOR_ACCENT).pack(side="left")
        ctk.CTkLabel(self.header_frame, text=" CONVERTER", font=FONT_HEADER, text_color="white").pack(side="left")
        ctk.CTkLabel(self.header_frame, text=" // v1.7", font=("Roboto", 12), text_color=COLOR_TEXT_DIM).pack(side="left", padx=(5,0), pady=(10,0))
        
        btn_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_box.pack(side="right")
        self.btn_lang = ctk.CTkButton(btn_box, text="TR", width=42, height=28, fg_color="#222", hover_color=COLOR_ACCENT, text_color="#fff", corner_radius=6, font=("Roboto", 12, "bold"), command=self.toggle_language)
        self.btn_lang.pack(side="left", padx=5)
        self.btn_help = ctk.CTkButton(btn_box, text="?", width=32, height=28, fg_color="#222", hover_color=COLOR_ACCENT, text_color="#fff", corner_radius=6, font=("Roboto", 13, "bold"), command=self.open_help_window)
        self.btn_help.pack(side="left")
        
        # Source Folder switch değişkeni
        self.use_source_var = ctk.BooleanVar(value=True)
        
        self.drop_frame = ctk.CTkFrame(self.left_col, height=200, corner_radius=12, fg_color=COLOR_FRAME, border_width=2, border_color="#2a2a2a")
        self.drop_frame.pack(fill="x", pady=(0, 15))
        self.drop_frame.pack_propagate(False)
        
        self.lbl_drop_title = ctk.CTkLabel(self.drop_frame, text="", font=("Roboto", 14, "bold"), text_color=COLOR_ACCENT)
        self.lbl_drop_title.place(relx=0.5, rely=0.20, anchor="center")
        self.lbl_drop_sub = ctk.CTkLabel(self.drop_frame, text="", text_color=COLOR_TEXT_DIM, font=("Roboto", 10))
        self.lbl_drop_sub.place(relx=0.5, rely=0.40, anchor="center")
        
        self.filter_box = ctk.CTkFrame(self.drop_frame, fg_color="transparent")
        self.filter_box.place(relx=0.55, rely=0.65, anchor="center")
        chk_style = {"checkbox_width": 20, "checkbox_height": 20, "corner_radius": 4, "border_width": 2, "font": ("Roboto", 12), "fg_color": COLOR_ACCENT, "hover_color": COLOR_ACCENT_HOVER, "checkmark_color": "black"}
        
        self.chk_img = ctk.CTkCheckBox(self.filter_box, text="Img", variable=self.filter_img_var, **chk_style)
        self.chk_img.grid(row=0, column=0, padx=15, pady=3, sticky="w")
        self.chk_aud = ctk.CTkCheckBox(self.filter_box, text="Aud", variable=self.filter_audio_var, **chk_style)
        self.chk_aud.grid(row=0, column=1, padx=15, pady=3, sticky="w")
        self.chk_vid = ctk.CTkCheckBox(self.filter_box, text="Vid", variable=self.filter_video_var, **chk_style)
        self.chk_vid.grid(row=1, column=0, padx=15, pady=3, sticky="w")
        self.chk_doc = ctk.CTkCheckBox(self.filter_box, text="Doc", variable=self.filter_doc_var, **chk_style)
        self.chk_doc.grid(row=1, column=1, padx=15, pady=3, sticky="w")
        
        # Browse Folder Button for Drop Media
        self.btn_drop_browse = ctk.CTkButton(self.drop_frame, text="Browse Folder", width=140, height=32, fg_color="#222", hover_color=COLOR_ACCENT, text_color="white", corner_radius=8, font=("Roboto", 12, "bold"), command=self.browse_folder_for_queue)
        self.btn_drop_browse.place(relx=0.5, rely=0.88, anchor="center")

        # Custom Tab Container
        self.tab_container = ctk.CTkFrame(self.left_col, height=280, fg_color=COLOR_FRAME, corner_radius=12)
        self.tab_container.pack(fill="x", pady=(0, 15))
        self.tab_container.pack_propagate(False)

        # Tab Content Frames (Hidden by default)
        self.frames = {}
        for name in ["Convert", "Resize", "Optimizer", "GIF Studio", "Doc Station", "Renamer", "Tree View", "Translate", "Text Extract", "Collector"]:
            f = ctk.CTkFrame(self.tab_container, fg_color="transparent")
            f.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = f
        
        self.tab_container.grid_rowconfigure(0, weight=1)
        self.tab_container.grid_columnconfigure(0, weight=1)
        
        # Shortcuts for cleaner code
        self.tab_convert = self.frames["Convert"]
        self.tab_resize = self.frames["Resize"]
        self.tab_opt = self.frames["Optimizer"]
        self.tab_gif = self.frames["GIF Studio"]
        self.tab_docs = self.frames["Doc Station"]
        self.tab_tools = self.frames["Renamer"]
        self.tab_tree = self.frames["Tree View"]
        self.tab_translate = self.frames["Translate"]
        self.tab_text = self.frames["Text Extract"]
        self.tab_collector = self.frames["Collector"]

        # Navigation Buttons
        self.setup_custom_tabs()

        seg_style = {"fg_color": "#151515", "selected_color": "#2a2a2a", "selected_hover_color": "#333", "unselected_color": "#111", "unselected_hover_color": "#1a1a1a", "text_color": "#fff", "height": 32, "corner_radius": 8, "font": ("Roboto", 12, "bold")}
        entry_style = {"height": 35, "fg_color": "#111", "border_color": "#222", "justify": "center", "corner_radius": 8, "font": ("Roboto", 13)}
        
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
        self.btn_visual_crop = ctk.CTkButton(crop_frame, text="", width=90, height=32, corner_radius=8, fg_color="#222", hover_color=COLOR_ACCENT, font=("Roboto", 12, "bold"), command=self.open_visual_cropper)
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
        self.lbl_rename_mode = ctk.CTkLabel(self.tab_tools, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_rename_mode.pack(anchor="w", pady=(10, 5))
        
        self.ren_mode_var = ctk.StringVar(value="Find & Replace")
        self.seg_rename_mode = ctk.CTkSegmentedButton(self.tab_tools, values=["Find & Replace", "Prefix by Folder"], variable=self.ren_mode_var, command=self.toggle_renamer_mode, **seg_style)
        self.seg_rename_mode.pack(fill="x", pady=(0, 15))
        
        # Find & Replace Frame
        self.frame_ren_find = ctk.CTkFrame(self.tab_tools, fg_color="transparent")
        self.frame_ren_find.pack(fill="both", expand=True)
        
        self.lbl_tools_find = ctk.CTkLabel(self.frame_ren_find, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_tools_find.pack(anchor="w", pady=(5, 5))
        self.entry_ren_find = ctk.CTkEntry(self.frame_ren_find, placeholder_text="_1500x1500", **entry_style)
        self.entry_ren_find.pack(fill="x", pady=(0, 10))
        
        self.lbl_tools_rep = ctk.CTkLabel(self.frame_ren_find, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_tools_rep.pack(anchor="w", pady=(5, 5))
        self.entry_ren_rep = ctk.CTkEntry(self.frame_ren_find, placeholder_text="", **entry_style)
        self.entry_ren_rep.pack(fill="x", pady=(0, 10))
        
        self.lbl_tools_info = ctk.CTkLabel(self.frame_ren_find, text="", font=("Roboto", 11), text_color="gray", justify="left")
        self.lbl_tools_info.pack(pady=5, padx=10)

        # Prefix by Folder Frame
        self.frame_ren_prefix = ctk.CTkFrame(self.tab_tools, fg_color="transparent")
        
        self.lbl_prefix_info = ctk.CTkLabel(self.frame_ren_prefix, text="", font=("Roboto", 11), text_color="gray", justify="left")
        self.lbl_prefix_info.pack(pady=(5, 10), padx=10)
        
        self.btn_prefix_folder = ctk.CTkButton(self.frame_ren_prefix, text="Select Parent Folder", width=200, height=36, corner_radius=8, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", font=("Roboto", 12, "bold"), command=self.select_prefix_folder)
        self.btn_prefix_folder.pack(pady=(0, 10))
        self.lbl_prefix_path = ctk.CTkLabel(self.frame_ren_prefix, text="...", font=("Roboto", 10), text_color=COLOR_TEXT_DIM)
        self.lbl_prefix_path.pack(pady=(0, 10))
        
        self.lbl_prefix_sep = ctk.CTkLabel(self.frame_ren_prefix, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_prefix_sep.pack(anchor="w", pady=(5, 5))
        self.entry_prefix_sep = ctk.CTkEntry(self.frame_ren_prefix, placeholder_text="_", **entry_style)
        self.entry_prefix_sep.insert(0, "_")
        self.entry_prefix_sep.pack(fill="x", pady=(0, 10))
        
        self.prefix_folder_path = ""
        
        # --- COLLECTOR TAB ---
        # Title and description are handled by update_ui_text
        self.lbl_collector_title = ctk.CTkLabel(self.tab_collector, text="File Collector", font=("Roboto", 14, "bold"), text_color=COLOR_ACCENT)
        self.lbl_collector_title.pack(anchor="w", pady=(15, 10), padx=10)
        
        self.lbl_collector_info = ctk.CTkLabel(self.tab_collector, text="", font=("Roboto", 11), text_color="gray", justify="left", anchor="w")
        self.lbl_collector_info.pack(anchor="w", pady=(0, 15), padx=10)
        
        # Source Selection
        src_frame = ctk.CTkFrame(self.tab_collector, fg_color="transparent")
        src_frame.pack(fill="x", pady=5)
        self.btn_collector_source = ctk.CTkButton(src_frame, text="", width=120, height=32, corner_radius=8, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", font=("Roboto", 12, "bold"), command=self.select_collector_source)
        self.btn_collector_source.pack(side="left", padx=(10, 10))
        self.lbl_collector_source_path = ctk.CTkLabel(src_frame, text="...", font=("Roboto", 10), text_color=COLOR_TEXT_DIM)
        self.lbl_collector_source_path.pack(side="left")
        
        # Target Selection 
        tgt_frame = ctk.CTkFrame(self.tab_collector, fg_color="transparent")
        tgt_frame.pack(fill="x", pady=5)
        self.btn_collector_target = ctk.CTkButton(tgt_frame, text="", width=120, height=32, corner_radius=8, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", font=("Roboto", 12, "bold"), command=self.select_collector_target)
        self.btn_collector_target.pack(side="left", padx=(10, 10))
        self.lbl_collector_target_path = ctk.CTkLabel(tgt_frame, text="...", font=("Roboto", 10), text_color=COLOR_TEXT_DIM)
        self.lbl_collector_target_path.pack(side="left")
        
        # Options
        opt_frame = ctk.CTkFrame(self.tab_collector, fg_color="transparent")
        opt_frame.pack(fill="x", pady=15, padx=10)
        self.collector_recursive_var = ctk.BooleanVar(value=True)
        self.chk_collector_recursive = ctk.CTkCheckBox(opt_frame, text="", variable=self.collector_recursive_var, **chk_style)
        self.chk_collector_recursive.pack(side="left", padx=(0, 15))
        
        self.chk_col_img_var = ctk.BooleanVar(value=True)
        self.chk_col_vid_var = ctk.BooleanVar(value=True)
        self.chk_col_aud_var = ctk.BooleanVar(value=True)
        self.chk_col_doc_var = ctk.BooleanVar(value=True)
        
        self.chk_col_img = ctk.CTkCheckBox(opt_frame, text="", variable=self.chk_col_img_var, command=self.preview_collector_files, **chk_style)
        self.chk_col_img.pack(side="left", padx=(5,5))
        self.chk_col_vid = ctk.CTkCheckBox(opt_frame, text="", variable=self.chk_col_vid_var, command=self.preview_collector_files, **chk_style)
        self.chk_col_vid.pack(side="left", padx=(5,5))
        self.chk_col_aud = ctk.CTkCheckBox(opt_frame, text="", variable=self.chk_col_aud_var, command=self.preview_collector_files, **chk_style)
        self.chk_col_aud.pack(side="left", padx=(5,5))
        self.chk_col_doc = ctk.CTkCheckBox(opt_frame, text="", variable=self.chk_col_doc_var, command=self.preview_collector_files, **chk_style)
        self.chk_col_doc.pack(side="left", padx=(5,5))
        
        self.collector_source_path = ""
        self.collector_target_path = ""

        # --- TREE VIEW TAB ---
        self.lbl_tree_select = ctk.CTkLabel(self.tab_tree, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_tree_select.pack(anchor="w", pady=(10, 5))
        
        tree_btn_frame = ctk.CTkFrame(self.tab_tree, fg_color="transparent")
        tree_btn_frame.pack(fill="x", pady=(0, 10))
        
        self.btn_tree_browse = ctk.CTkButton(tree_btn_frame, text="", width=120, height=32, corner_radius=8, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", font=("Roboto", 12, "bold"), command=self.select_tree_folder)
        self.btn_tree_browse.pack(side="left", padx=(0, 10))
        
        self.lbl_tree_path = ctk.CTkLabel(tree_btn_frame, text="", font=("Roboto", 10), text_color=COLOR_TEXT_DIM)
        self.lbl_tree_path.pack(side="left")
        
        self.lbl_tree_preview = ctk.CTkLabel(self.tab_tree, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_tree_preview.pack(anchor="w", pady=(5, 5))
        
        # Reduced height for Tree View preview
        self.tree_preview_box = ctk.CTkTextbox(self.tab_tree, width=460, height=80, fg_color="#111", border_color="#333", border_width=1, font=("Consolas", 9))
        self.tree_preview_box.pack(fill="both", expand=True, pady=(0, 10))
        self.tree_preview_box.configure(state="disabled")
        
        copy_tree_frame = ctk.CTkFrame(self.tab_tree, fg_color="transparent")
        copy_tree_frame.pack(fill="x", pady=5)
        self.btn_tree_copy = ctk.CTkButton(copy_tree_frame, text="Copy", width=120, height=36, corner_radius=8, fg_color="#444", hover_color="#555", font=("Roboto", 12, "bold"), command=self.copy_tree_to_clipboard)
        self.btn_tree_copy.pack(side="right", padx=(5,10))
        
        self.lbl_tree_info = ctk.CTkLabel(self.tab_tree, text="", font=("Roboto", 11), text_color="gray", justify="left")
        self.lbl_tree_info.pack(pady=5)
        
        self.tree_folder_path = ""

        # --- TEXT EXTRACT TAB ---
        # Bu sekme sağ paneldeki kuyruk ve Start butonu ile çalışır
        self.lbl_text_title = ctk.CTkLabel(self.tab_text, text="Text Extract", font=("Roboto", 14, "bold"), text_color=COLOR_ACCENT)
        self.lbl_text_title.pack(anchor="w", pady=(15, 10), padx=10)
        
        self.lbl_text_desc = ctk.CTkLabel(self.tab_text, text="", font=("Roboto", 11), text_color="gray", justify="left", anchor="w")
        self.lbl_text_desc.pack(anchor="w", pady=(5, 10), padx=10, fill="x")
        
        # Info box
        text_info_frame = ctk.CTkFrame(self.tab_text, fg_color=COLOR_FRAME, corner_radius=8)
        text_info_frame.pack(fill="x", padx=10, pady=(10, 10))
        
        self.lbl_text_info = ctk.CTkLabel(text_info_frame, text="", font=("Roboto", 10), text_color="gray", justify="left")
        self.lbl_text_info.pack(anchor="w", padx=10, pady=10)
        
        self.text_folder_path = ""
        
        # --- SOURCE FOLDER PANEL (Sol panelde) ---
        self.path_frame = ctk.CTkFrame(self.left_col, fg_color=COLOR_FRAME, corner_radius=12, height=50)
        self.path_frame.pack(fill="x", side="bottom", pady=(10, 0))
        self.path_frame.pack_propagate(False)
        self.switch_source = ctk.CTkSwitch(self.path_frame, text="", variable=self.use_source_var, command=self.toggle_path_selection, progress_color=COLOR_ACCENT, font=("Roboto", 12, "bold"))
        self.switch_source.pack(side="left", padx=15)
        self.btn_browse = ctk.CTkButton(self.path_frame, text="", width=70, height=30, corner_radius=6, fg_color="#222", hover_color=COLOR_ACCENT, font=("Roboto", 12, "bold"), state="disabled", command=self.select_output_folder)
        self.btn_browse.pack(side="right", padx=10)
        self.lbl_path = ctk.CTkLabel(self.path_frame, text="", font=("Roboto", 10), text_color=COLOR_TEXT_DIM)
        self.lbl_path.pack(side="right", padx=5)

        # Reduced padding to raise UI
        # Google Translate Mode (No API Key needed)
        self.lbl_google_hint = ctk.CTkLabel(self.tab_translate, text="Google Translate Mode (Free/No Key)", font=("Roboto", 11, "bold"), text_color=COLOR_ACCENT)
        self.lbl_google_hint.pack(anchor="w", pady=(5, 5))
        
        lang_frame = ctk.CTkFrame(self.tab_translate, fg_color="transparent")
        lang_frame.pack(fill="x", pady=(0, 5))
        
        self.lbl_target_lang = ctk.CTkLabel(lang_frame, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_target_lang.pack(side="left", padx=(0, 10))
        
        # DeepL target language codes
        deepl_langs = ["TR", "EN", "DE", "FR", "ES", "IT", "PT", "RU", "JA", "KO", "ZH", "NL", "PL", "CS", "EL", "HU", "RO", "SV", "DA", "FI"]
        combo_style = {"fg_color": "#111", "text_color": "#fff", "height": 30, "dropdown_fg_color": "#222", "button_color": COLOR_ACCENT, "button_hover_color": COLOR_ACCENT_HOVER}
        self.combo_target_lang = ctk.CTkComboBox(lang_frame, values=deepl_langs, variable=self.translate_target_lang, **combo_style)
        self.combo_target_lang.pack(side="left", padx=(0, 20))
        
        self.combo_target_lang.pack(side="left", padx=(0, 20))
        
        # Source Folder Button
        self.lbl_translate_preview = ctk.CTkLabel(self.tab_translate, text="", font=("Roboto", 11, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_translate_preview.pack(anchor="w", pady=(5, 0))
        
        self.btn_trans_add_folder = ctk.CTkButton(self.tab_translate, text="", width=200, height=36, corner_radius=8, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", font=("Roboto", 12, "bold"), command=self.select_translate_source_folder)
        self.btn_trans_add_folder.pack(pady=(0, 5))
        
        self.lbl_translate_hint = ctk.CTkLabel(self.tab_translate, text="", font=("Roboto", 11), text_color="gray", justify="left")
        self.lbl_translate_hint.pack(pady=5)

        # --- ALT PANEL (Kaldırıldı - Sağ panele taşındı) ---
        # (Eski path_frame buradaydı)
        
        self.right_col = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_col.pack(side="right", fill="both", expand=True)
        list_header = ctk.CTkFrame(self.right_col, fg_color="transparent")
        list_header.pack(fill="x", pady=(0, 10))
        
        self.lbl_queue = ctk.CTkLabel(list_header, text="", font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_DIM)
        self.lbl_queue.pack(side="left", padx=(0, 10))
        
        self.view_mode_var = ctk.StringVar(value="List")
        self.seg_view_mode = ctk.CTkSegmentedButton(list_header, values=["List", "Preview"], variable=self.view_mode_var, command=self.refresh_queue_view, height=28, selected_color="#2a2a2a", unselected_color="#1a1a1a", selected_hover_color="#333", font=("Roboto", 11))
        self.seg_view_mode.pack(side="left", padx=5)
        
        self.opt_queue_limit = ctk.CTkOptionMenu(list_header, values=["50", "100", "150", "250"], variable=self.queue_limit_var, width=65, height=28, fg_color="#1a1a1a", button_color="#2a2a2a", button_hover_color="#333", font=("Roboto", 11))
        self.opt_queue_limit.pack(side="left", padx=(3, 0))
        
        self.btn_clear = ctk.CTkButton(list_header, text="", width=60, height=28, corner_radius=6, fg_color="transparent", border_width=1, border_color="#333", text_color="#888", hover_color="#222", font=("Roboto", 12, "bold"), command=self.clear_queue)
        self.btn_clear.pack(side="right")
        self.btn_remove = ctk.CTkButton(list_header, text="", width=90, height=28, corner_radius=6, fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, font=("Roboto", 12, "bold"), command=self.remove_checked_files)
        self.btn_remove.pack(side="right", padx=(0,5))
        self.chk_select_all = ctk.CTkCheckBox(list_header, text="", width=60, variable=self.select_all_var, command=self.toggle_select_all, **chk_style)
        self.chk_select_all.pack(side="right", padx=(0,5))

        self.scroll_list = ctk.CTkScrollableFrame(self.right_col, fg_color=COLOR_FRAME, corner_radius=12, scrollbar_button_color="#222", scrollbar_button_hover_color=COLOR_ACCENT)
        self.scroll_list.pack(fill="both", expand=True, pady=(0, 15))
        self.btn_start = ctk.CTkButton(self.right_col, text="", font=("Roboto", 18, "bold"), height=60, corner_radius=12, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", command=self.start_process_thread)
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
        self.lbl_tree_select.configure(text=T["lbl_tree_select"])
        self.lbl_tree_preview.configure(text=T["lbl_tree_preview"])
        self.lbl_tree_info.configure(text=T["lbl_tree_info"])
        self.btn_tree_browse.configure(text=T["btn_tree_browse"])
        self.lbl_text_title.configure(text=T["lbl_text_title"])
        self.lbl_text_desc.configure(text=T["lbl_text_desc"])
        self.lbl_text_info.configure(text=T["lbl_text_info_box"])
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
        self.entry_crop_h.configure(placeholder_text=T["plh_h"])
        self.entry_crop_x.configure(placeholder_text=T["plh_x"])
        self.entry_crop_y.configure(placeholder_text=T["plh_y"])
        
        # Additional UI components for Renamer & Collector
        if "lbl_rename_mode" in T:
            self.lbl_rename_mode.configure(text=T["lbl_rename_mode"])
            self.lbl_prefix_info.configure(text=T["lbl_prefix_info"])
            self.lbl_prefix_sep.configure(text=T["lbl_prefix_sep"])
            self.seg_rename_mode.configure(values=[T.get("seg_rename_find", "Find & Replace"), T.get("seg_rename_prefix", "Prefix by Folder")])
            current_mode = self.ren_mode_var.get()
            if current_mode == "Find & Replace" or current_mode == "Bul ve Değiştir":
                self.ren_mode_var.set(T.get("seg_rename_find", "Find & Replace"))
            else:
                self.ren_mode_var.set(T.get("seg_rename_prefix", "Prefix by Folder"))
            
            self.lbl_collector_title.configure(text=T["tab_collector"])
            self.lbl_collector_info.configure(text=T["lbl_collector_info"])
            self.btn_collector_source.configure(text=T["btn_collector_source"])
            self.btn_collector_target.configure(text=T["btn_collector_target"])
            self.chk_collector_recursive.configure(text=T["lbl_collector_recursive"])
            
            if "lbl_collect_img" in T:
                self.chk_col_img.configure(text=T["lbl_collect_img"])
                self.chk_col_vid.configure(text=T["lbl_collect_vid"])
                self.chk_col_aud.configure(text=T["lbl_collect_aud"])
                self.chk_col_doc.configure(text=T["lbl_collect_doc"])
                self.btn_tree_copy.configure(text=T["btn_tree_copy"])
            
            current_view = self.view_mode_var.get()
            v_list = T.get("view_list", "List")
            v_preview = T.get("view_preview", "Preview")
            self.seg_view_mode.configure(values=[v_list, v_preview])
            if current_view in ["List", "Liste"]: self.view_mode_var.set(v_list)
            else: self.view_mode_var.set(v_preview)
        
        # Translation tab UI
        self.lbl_target_lang.configure(text=T["lbl_target_lang"])

        # Source Folder Button UI Text Update
        self.lbl_translate_preview.configure(text="Add From Folder:" if self.current_lang == "en" else "Klasörden Ekle:")
        self.btn_trans_add_folder.configure(text="Select Folder" if self.current_lang == "en" else "Klasör Seç")
        
        self.lbl_translate_hint.configure(text=T["lbl_translate_hint"])

    def setup_custom_tabs(self):
        nav_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 10), before=self.tab_container)
        
        # Row 1
        row1 = ctk.CTkFrame(nav_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 2))
        # Row 2
        row2 = ctk.CTkFrame(nav_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 2))
        # Row 3
        row3 = ctk.CTkFrame(nav_frame, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 2))
        # Row 4
        row4 = ctk.CTkFrame(nav_frame, fg_color="transparent")
        row4.pack(fill="x")
        
        self.tab_btns = {}
        
        # Tabs Struct: Name, Display, Row_Frame
        tabs_def = [
            ("Convert", "Convert", row1),
            ("Resize", "Resize", row1),
            ("Optimizer", "Optimizer", row1),
            ("GIF Studio", "GIF Studio", row2),
            ("Doc Station", "Doc Station", row2),
            ("Renamer", "Renamer", row2),
            ("Tree View", "Tree View", row3),
            ("Translate", "Translate", row3),
            ("Text Extract", "Text Extract", row3),
            ("Collector", "Collector", row4)
        ]
        
        for name, label, parent in tabs_def:
            btn = ctk.CTkButton(parent, text=label, width=110, height=32, corner_radius=8, fg_color="#1a1a1a", hover_color="#2a2a2a", border_width=1, border_color="#333", font=("Roboto", 12, "bold"), text_color="#aaa", command=lambda n=name: self.select_tab(n))
            btn.pack(side="left", padx=2, fill="x", expand=True)
            self.tab_btns[name] = btn
            
        self.current_tab_name = "Convert"
        self.select_tab("Convert")

    def select_tab(self, name):
        self.current_tab_name = name
        
        # Reset styles
        for n, btn in self.tab_btns.items():
            btn.configure(fg_color="#1a1a1a", text_color="#888", border_color="#333")
            
        # Set active style
        self.tab_btns[name].configure(fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", border_color=COLOR_ACCENT)
        self.frames[name].tkraise()
        
        # Collector is independent from queue items, so don't alter much, but 
        if name == "Collector" or name == "Toplayıcı":
            pass

    def toggle_renamer_mode(self, value):
        if value in ["Find & Replace", "Bul ve Değiştir"]:
            self.frame_ren_prefix.pack_forget()
            self.frame_ren_find.pack(fill="both", expand=True)
        else:
            self.frame_ren_find.pack_forget()
            self.frame_ren_prefix.pack(fill="both", expand=True)

    def select_prefix_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.prefix_folder_path = folder
            self.lbl_prefix_path.configure(text=f".../{os.path.basename(folder)}")
            self.generate_prefix_tree(folder)

    def generate_prefix_tree(self, folder):
        self.file_items = []
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        self.view_mode_var.set("List")
        limit = int(self.queue_limit_var.get())
        count = 0
        
        for root, dirs, files in os.walk(folder):
            if root != folder:
                rel = os.path.relpath(root, folder)
                lbl = ctk.CTkLabel(self.scroll_list, text=f"📁 {rel}", font=("Roboto", 12, "bold"), text_color=COLOR_ACCENT, anchor="w")
                lbl.pack(fill="x", pady=(8, 2), padx=8)
            
            for f in sorted(files):
                if count >= limit:
                    self.log(f"Limit ({limit}) reached", "info")
                    return
                fpath = os.path.join(root, f)
                var = ctk.BooleanVar(value=True)
                indent = 25 if root != folder else 10
                chk = ctk.CTkCheckBox(self.scroll_list, text=f"📄 {f}", variable=var, font=("Roboto", 11), checkbox_width=18, checkbox_height=18, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, checkmark_color="black")
                chk.pack(fill="x", pady=1, padx=(indent, 8), anchor="w")
                self.file_items.append({'path': fpath, 'widget': chk, 'var': var})
                count += 1
        
        self.log(f"Tree: {len(self.file_items)} files", "info")

    def select_collector_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.collector_source_path = folder
            self.lbl_collector_source_path.configure(text=f".../{os.path.basename(folder)}")
            self.preview_collector_files()

    def preview_collector_files(self, *args):
        if not hasattr(self, 'collector_source_path') or not self.collector_source_path: return
        
        allowed_exts = set()
        if self.chk_col_img_var.get(): allowed_exts.update(IMAGE_EXTS)
        if self.chk_col_vid_var.get(): allowed_exts.update(VIDEO_EXTS)
        if self.chk_col_aud_var.get(): allowed_exts.update(AUDIO_EXTS)
        if self.chk_col_doc_var.get(): allowed_exts.update(DOC_EXTS)
            
        recursive = self.collector_recursive_var.get()
        folder = self.collector_source_path
        
        self.file_items = []
        
        if recursive:
            for root, dirs, files in os.walk(folder):
                for f in files:
                    path = os.path.join(root, f)
                    if os.path.splitext(f)[1].lower() in allowed_exts:
                        self.file_items.append({'path': path, 'widget': None, 'var': ctk.BooleanVar(value=True)})
        else:
            try:
                for f in os.listdir(folder):
                    path = os.path.join(folder, f)
                    if os.path.isfile(path):
                        if os.path.splitext(f)[1].lower() in allowed_exts:
                            self.file_items.append({'path': path, 'widget': None, 'var': ctk.BooleanVar(value=True)})
            except: pass
            
        self.refresh_queue_view()
        self.log(f"Collector preview: {len(self.file_items)} files added", "info")

    def select_collector_target(self):
        folder = filedialog.askdirectory()
        if folder:
            self.collector_target_path = folder
            self.lbl_collector_target_path.configure(text=f".../{os.path.basename(folder)}")

    def select_translate_source_folder(self):
        folder = filedialog.askdirectory()
        if not folder: return
        
        self.log(f"Scanning: {os.path.basename(folder)}", "info")
        threading.Thread(target=self.scan_and_add_files_translate, args=(folder,)).start()

    def scan_and_add_files_translate(self, folder):
        files = []
        try:
            for f in os.listdir(folder):
                full_path = os.path.join(folder, f)
                if os.path.isfile(full_path):
                     files.append(full_path)
        except: pass
        
        if files:
            self.scan_and_add_files(files)

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

    def browse_folder_for_queue(self):
        """Drop Media panelinden klasör seçip kuyruğa ekle"""
        folder = filedialog.askdirectory()
        if not folder:
            return
        
        self.log(f"Scanning folder: {os.path.basename(folder)}", "info")
        
        # Klasördeki tüm dosyaları al (Recursive)
        files = []
        try:
            for root, _, fil in os.walk(folder):
                for f in fil:
                    full_path = os.path.join(root, f)
                    if os.path.isfile(full_path):
                        files.append(full_path)
        except Exception as e:
            self.log(f"Error scanning folder: {str(e)}", "error")
            return
        
        if files:
            self.scan_and_add_files(files)
            self.log(f"Added {len(files)} files to queue", "success")
        else:
            self.log("No files found in folder", "info")

    def select_tree_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.tree_folder_path = folder
            folder_name = os.path.basename(folder)
            self.lbl_tree_path.configure(text=folder_name)
            self.generate_tree_preview(folder)

    def select_text_folder(self):
        """Text Extract için klasör seçimi"""
        folder = filedialog.askdirectory()
        if folder:
            self.text_folder_path = folder
            folder_name = os.path.basename(folder)
            self.lbl_text_path.configure(text=folder_name)
            self.generate_text_preview(folder)

    def generate_text_preview(self, folder_path, max_items=50):
        """Klasördeki dosyaları listele ve önizleme kutusuna yaz"""
        file_lines = []
        file_lines.append(os.path.basename(folder_path) + "/")
        
        try:
            items = sorted(os.listdir(folder_path))
            # Gizli dosyaları filtrele
            items = [item for item in items if not item.startswith('.')]
        except (PermissionError, OSError):
            file_lines.append("Error: Cannot access folder")
            self.text_preview_box.configure(state="normal")
            self.text_preview_box.delete("1.0", "end")
            self.text_preview_box.insert("1.0", "\n".join(file_lines))
            self.text_preview_box.configure(state="disabled")
            return
        
        count = 0
        for item in items:
            if count >= max_items:
                file_lines.append("...")
                break
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                file_lines.append(f"📄 {item}")
                count += 1
            elif os.path.isdir(item_path):
                file_lines.append(f"📁 {item}/")
        
        file_text = "\n".join(file_lines)
        
        self.text_preview_box.configure(state="normal")
        self.text_preview_box.delete("1.0", "end")
        self.text_preview_box.insert("1.0", file_text)
        self.text_preview_box.configure(state="disabled")

    def extract_text_to_txt(self):
        """Klasördeki tüm dosyaların içeriğini oku ve .txt olarak kaydet"""
        if not self.text_folder_path:
            messagebox.showwarning("!", "Please select a folder first." if self.current_lang == "en" else "Lütfen önce bir klasör seçin.")
            return
        
        self.log(self.current_lang["status_processing"] if self.current_lang["status_processing"] else "Processing...", "info")
        threading.Thread(target=self._extract_text_worker, args=(self.text_folder_path,)).start()

    def _extract_text_from_queue(self):
        """Kuyruktaki seçili dosyaları .txt olarak kaydet"""
        count = 0
        errors = []
        
        # Seçili dosyaları al
        selected_files = [item['path'] for item in self.file_items if item['var'].get()]
        
        if not selected_files:
            self.after(0, lambda: messagebox.showwarning("!", "No files selected" if self.current_lang == "en" else "Dosya seçilmedi"))
            self.after(0, lambda: self.btn_start.configure(state="normal", text=LANG[self.current_lang]["btn_start"]))
            return
        
        for file_path in selected_files:
            if not os.path.isfile(file_path):
                continue
            
            # Zaten txt ise atla
            if file_path.lower().endswith('.txt'):
                continue
            
            # Kaydetme konumunu belirle
            if self.use_source_var.get():
                save_dir = os.path.dirname(file_path)
            else:
                save_dir = self.output_folder if self.output_folder else os.path.dirname(file_path)
            
            if not save_dir:
                save_dir = os.path.dirname(file_path)
            
            basename = os.path.splitext(os.path.basename(file_path))[0]
            output_file = os.path.join(save_dir, f"{basename}.txt")
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                count += 1
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
        
        # Sonucu raporla
        self.after(0, lambda: self.btn_start.configure(state="normal", text=LANG[self.current_lang]["btn_start"]))
        
        if errors:
            error_msg = "\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\n...and {len(errors) - 5} more errors"
            self.after(0, lambda: self.log(f"Completed with errors: {count} files", "error"))
            self.after(0, lambda: messagebox.showwarning("Errors", f"Processed {count} files.\nErrors:\n{error_msg}"))
        else:
            self.after(0, lambda: self.log(f"Completed: {count} files saved as .txt", "success"))
            self.after(0, lambda: messagebox.showinfo("Success", f"{count} files extracted successfully!" if self.current_lang == "en" else f"{count} dosya başarıyla çıkarıldı!"))

    def _extract_text_worker(self, folder_path):
        """Arka planda çalışan dosya işleme fonksiyonu"""
        count = 0
        errors = []
        
        try:
            items = os.listdir(folder_path)
            items = [item for item in items if not item.startswith('.')]
        except (PermissionError, OSError) as e:
            errors.append(str(e))
            self.after(0, lambda: self.log(f"Error: {str(e)}", "error"))
            return
        
        for item in items:
            item_path = os.path.join(folder_path, item)
            
            if not os.path.isfile(item_path):
                continue
            
            # Zaten txt ise atla
            if item.lower().endswith('.txt'):
                continue
            
            # Kaydetme konumunu belirle
            if self.use_source_var.get():
                save_dir = os.path.dirname(item_path)
            else:
                save_dir = self.output_folder if self.output_folder else folder_path
            
            if not save_dir:
                save_dir = folder_path
            
            basename = os.path.splitext(item)[0]
            output_file = os.path.join(save_dir, f"{basename}.txt")
            
            try:
                # Dosya içeriğini oku
                with open(item_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # .txt olarak kaydet
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                count += 1
            except Exception as e:
                errors.append(f"{item}: {str(e)}")
        
        # Sonucu raporla
        if errors:
            error_msg = "\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\n...and {len(errors) - 5} more errors"
            self.after(0, lambda: self.log(f"Completed with errors: {count} files", "error"))
            messagebox.showwarning("Errors", f"Processed {count} files.\nErrors:\n{error_msg}")
        else:
            self.after(0, lambda: self.log(f"Completed: {count} files saved as .txt", "success"))
            self.after(0, lambda: messagebox.showinfo("Success", f"{count} files extracted successfully!" if self.current_lang == "en" else f"{count} dosya başarıyla çıkarıldı!"))

    def generate_tree_preview(self, folder_path, max_items=50):
        """Klasör ağacını oluştur ve önizleme kutusuna yaz"""
        tree_lines = []
        tree_lines.append(os.path.basename(folder_path) + "/")
        
        def add_tree_items(path, prefix="", is_last=True, count=[0]):
            if count[0] >= max_items:
                return
            try:
                items = sorted(os.listdir(path))
                # Gizli dosyaları filtrele
                items = [item for item in items if not item.startswith('.')]
            except (PermissionError, OSError):
                return
            
            for i, item in enumerate(items):
                if count[0] >= max_items:
                    return
                is_last_item = (i == len(items) - 1)
                item_path = os.path.join(path, item)
                
                # Ağaç karakterleri
                connector = "└── " if is_last_item else "├── "
                tree_lines.append(prefix + connector + item)
                count[0] += 1
                
                if os.path.isdir(item_path):
                    extension = "    " if is_last_item else "│   "
                    add_tree_items(item_path, prefix + extension, is_last_item, count)
        
        add_tree_items(folder_path)
        
        if len(tree_lines) > max_items:
            tree_lines.append("...")
        
        tree_text = "\n".join(tree_lines)
        
        self.tree_preview_box.configure(state="normal")
        self.tree_preview_box.delete("1.0", "end")
        self.tree_preview_box.insert("1.0", tree_text)
        self.tree_preview_box.configure(state="disabled")

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
                        if self.add_item_data(os.path.join(r, file), allow_img, allow_aud, allow_vid, allow_doc):
                            cnt+=1
            elif os.path.isfile(p):
                if self.add_item_data(p, allow_img, allow_aud, allow_vid, allow_doc):
                    cnt+=1
        if cnt>0: 
            self.log(f"+{cnt} file(s)", "success")
            self.refresh_queue_view()

    def add_item_data(self, file_path, allow_img, allow_aud, allow_vid, allow_doc):
        limit = int(self.queue_limit_var.get())
        if len(self.file_items) >= limit:
            return False
        
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
        self.file_items.append({'path': file_path, 'widget': None, 'var': var})
        return True

    def get_file_icon(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in IMAGE_EXTS: return "🖼️"
        if ext in AUDIO_EXTS: return "🎵"
        if ext in VIDEO_EXTS: return "🎬"
        if ext in DOC_EXTS: return "📄"
        return "📋"

    def _get_thumbnail(self, file_path, size=(80, 80)):
        """Generate a CTkImage thumbnail for image/video files. Returns None for non-previewable."""
        if file_path in self._thumb_cache:
            return self._thumb_cache[file_path]
        
        ext = os.path.splitext(file_path)[1].lower()
        pil_img = None
        
        try:
            if ext in IMAGE_EXTS:
                pil_img = Image.open(file_path)
                pil_img.thumbnail(size, Image.LANCZOS)
            elif ext in VIDEO_EXTS:
                ffmpeg = get_ffmpeg_path()
                if ffmpeg:
                    import tempfile
                    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                    tmp_path = tmp.name
                    tmp.close()
                    try:
                        subprocess.run(
                            [ffmpeg, "-i", file_path, "-ss", "00:00:01", "-vframes", "1", "-y", tmp_path],
                            capture_output=True, timeout=5,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                        )
                        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
                            pil_img = Image.open(tmp_path)
                            pil_img.thumbnail(size, Image.LANCZOS)
                            pil_img = pil_img.copy()
                    finally:
                        try: os.unlink(tmp_path)
                        except: pass
        except:
            pil_img = None
        
        if pil_img:
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
            self._thumb_cache[file_path] = ctk_img
            return ctk_img
        
        self._thumb_cache[file_path] = None
        return None

    def refresh_queue_view(self, *args):
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
            
        mode = self.view_mode_var.get()
        
        if mode in ["Preview", "Önizleme"]:
            cols = 3
            row_frame = None
            for idx, item in enumerate(self.file_items):
                if idx % cols == 0:
                    row_frame = ctk.CTkFrame(self.scroll_list, fg_color="transparent")
                    row_frame.pack(fill="x", pady=2, padx=2)
                
                card = ctk.CTkFrame(row_frame, fg_color="#1a1a1a", corner_radius=8, width=160, height=160)
                card.pack(side="left", padx=3, pady=3, expand=True, fill="both")
                card.pack_propagate(False)
                
                chk = ctk.CTkCheckBox(card, text="", variable=item['var'], width=20, height=20, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, checkmark_color="black")
                chk.pack(anchor="ne", padx=4, pady=4)
                
                thumb = self._get_thumbnail(item['path'], size=(90, 90))
                if thumb:
                    ctk.CTkLabel(card, text="", image=thumb).pack(pady=(0, 4))
                else:
                    icon = self.get_file_icon(item['path'])
                    ctk.CTkLabel(card, text=icon, font=("Segoe UI Emoji", 42)).pack(pady=(0, 4))
                
                name = os.path.basename(item['path'])
                if len(name) > 23: name = name[:20] + "..."
                ctk.CTkLabel(card, text=name, font=("Roboto", 10), wraplength=140).pack(pady=(0, 4))
                item['widget'] = card
                
        else:  # List mode (default)
            for item in self.file_items:
                icon = self.get_file_icon(item['path'])
                chk = ctk.CTkCheckBox(self.scroll_list, text=f" {icon} {os.path.basename(item['path'])}", variable=item['var'], font=("Roboto", 11), checkbox_width=20, checkbox_height=20, border_width=2, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, checkmark_color="black")
                chk.pack(fill="x", pady=2, padx=8, anchor="w")
                item['widget'] = chk

    def toggle_select_all(self):
        state = self.select_all_var.get()
        for item in self.file_items:
            item['var'].set(state)

    def remove_checked_files(self):
        n_l = []
        for i in self.file_items:
            if not i['var'].get():
                n_l.append(i)
        
        cnt = len(self.file_items) - len(n_l)
        self.file_items = n_l
        
        if cnt>0: 
            self.log(f"-{cnt} file(s)", "info")
            self.refresh_queue_view()
        self.scroll_list._parent_canvas.yview_moveto(0.0)

    def clear_queue(self):
        self.file_items = []
        self.refresh_queue_view()
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
        tab = self.current_tab_name
        
        if tab in ["Resize", "Boyutlandır"]: threading.Thread(target=self.process_resize).start()
        elif tab in ["Optimizer", "Optimize Et"]: threading.Thread(target=self.process_optimize).start()
        elif tab in ["GIF Studio", "GIF Stüdyo"]: threading.Thread(target=self.process_gif).start()
        elif tab in ["Doc Station", "Doc İstasyonu"]: threading.Thread(target=self.process_documents).start()
        elif tab in ["Renamer", "Adlandır"]: threading.Thread(target=self.process_rename).start()
        elif tab in ["Tree View", "Ağaç Görünümü"]: threading.Thread(target=self.process_tree_export).start()
        elif tab == "Translate": threading.Thread(target=self.process_translation).start()
        elif tab == "Text Extract": threading.Thread(target=self._extract_text_from_queue).start()
        elif tab in ["Collector", "Toplayıcı"]: threading.Thread(target=self.process_collect).start()
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
        mode = self.ren_mode_var.get()
        
        if mode in ["Find & Replace", "Bul ve Değiştir"]:
            find_text = self.entry_ren_find.get()
            rep_text = self.entry_ren_rep.get()
            
            if not find_text:
                self.after(0, lambda: messagebox.showwarning("!", "Please enter text to find." if self.current_lang == "en" else "Lütfen bulunacak metni girin."))
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
                        item['path'] = new_path 
                        self.log(f"Renamed: {new_name}", "success")
                        cnt += 1
                    except Exception as e:
                        self.log(f"Err Rename: {old_name}", "error")
            
            if cnt > 0:
                self.after(0, self.refresh_queue_view)
            else:
                self.log("No files matched the text." if self.current_lang == "en" else "Metin ile eşleşen dosya bulunamadı.", "info")
                
        else:
            # Prefix Mode
            parent_dir = self.prefix_folder_path
            if not parent_dir:
                self.after(0, lambda: messagebox.showwarning("!", "Please select a parent folder first." if self.current_lang == "en" else "Lütfen önce ana klasörü seçin."))
                self.finish_process()
                return
                
            separator = self.entry_prefix_sep.get() or "_"
            
            cnt = 0
            for item in self.file_items:
                if not item['var'].get(): continue
                
                old_path = item['path']
                folder = os.path.dirname(old_path)
                old_name = os.path.basename(old_path)
                parent_name = os.path.basename(folder)
                
                expected_prefix = f"{parent_name}{separator}"
                if old_name.startswith(expected_prefix):
                    continue
                    
                new_name = f"{expected_prefix}{old_name}"
                new_path = os.path.join(folder, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    item['path'] = new_path
                    self.log(f"Prefixed: {new_name}", "success")
                    cnt += 1
                except Exception as e:
                    self.log(f"Err Prefix: {old_name}", "error")
            
            if cnt > 0:
                self.after(0, self.refresh_queue_view)
            else:
                self.log("No new files prefixed." if self.current_lang == "en" else "Yeni isimlendirilen dosya yok.", "info")
                
        self.finish_process()

    # --- COLLECTOR PROCESSOR ---
    def process_collect(self):
        src = self.collector_source_path
        tgt = self.collector_target_path
        
        if not src or not tgt:
            self.after(0, lambda: messagebox.showwarning("!", "Please select both source and target folders." if self.current_lang == "en" else "Lütfen kaynak ve hedef klasörleri seçin."))
            self.finish_process()
            return
            
        allowed_exts = set()
        if self.chk_col_img_var.get(): allowed_exts.update(IMAGE_EXTS)
        if self.chk_col_vid_var.get(): allowed_exts.update(VIDEO_EXTS)
        if self.chk_col_aud_var.get(): allowed_exts.update(AUDIO_EXTS)
        if self.chk_col_doc_var.get(): allowed_exts.update(DOC_EXTS)
        extensions = list(allowed_exts)
            
        recursive = self.collector_recursive_var.get()
        
        def cb(filename, success):
            if success:
                self.after(0, lambda: self.log(f"Copied: {filename}", "success"))
            else:
                self.after(0, lambda: self.log(f"Err Copy: {filename}", "error"))
                
        self.after(0, lambda: self.log("Collecting files...", "info"))
        
        success_count, errors = collect_files(src, tgt, extensions, recursive, callback=cb)
        
        msg = f"Collected {success_count} files successfully." if self.current_lang == "en" else f"{success_count} dosya başarıyla toplandı."
        self.after(0, lambda: self.log(msg, "success"))
        
        if errors:
            err_text = "\n".join(errors[:5])
            if len(errors) > 5: err_text += f"\n...and {len(errors)-5} more."
            self.after(0, lambda: messagebox.showwarning("Errors", err_text))
            
        self.finish_process()

    def finish_process(self):
        self.log(LANG[self.current_lang]["status_done"], "success")
        self.btn_start.configure(state="normal", text=LANG[self.current_lang]["btn_start"])

    def generate_full_tree(self, folder_path):
        """Tam klasör ağacını text olarak döndür"""
        tree_lines = []
        folder_name = os.path.basename(folder_path)
        tree_lines.append(folder_name + "/")
        tree_lines.append("")
        
        def add_tree_items(path, prefix=""):
            try:
                items = sorted(os.listdir(path))
                # Gizli dosyaları filtrele
                items = [item for item in items if not item.startswith('.')]
            except (PermissionError, OSError):
                return
            
            for i, item in enumerate(items):
                is_last = (i == len(items) - 1)
                item_path = os.path.join(path, item)
                
                # Ağaç karakterleri
                connector = "└── " if is_last else "├── "
                tree_lines.append(prefix + connector + item)
                
                if os.path.isdir(item_path):
                    extension = "    " if is_last else "│   "
                    add_tree_items(item_path, prefix + extension)
        
        add_tree_items(folder_path)
        return "\n".join(tree_lines)

    def process_tree_export(self):
        """Tree View'i text dosyasına kaydet"""
        if not self.tree_folder_path:
            messagebox.showwarning("!", "Please select a folder first." if self.current_lang == "en" else "Lütfen önce bir klasör seçin.")
            self.finish_process()
            return
        
        try:
            # Tam ağacı oluştur
            tree_content = self.generate_full_tree(self.tree_folder_path)
            
            # Kaydetme konumunu belirle
            if self.use_source_var.get():
                save_dir = os.path.dirname(self.tree_folder_path)
            else:
                save_dir = self.output_folder if self.output_folder else os.path.dirname(self.tree_folder_path)
            
            folder_name = os.path.basename(self.tree_folder_path)
            output_file = os.path.join(save_dir, f"{folder_name}_tree.txt")
            
            # Text dosyasına kaydet
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"📁 {folder_name}\n")
                f.write("=" * 50 + "\n\n")
                f.write(tree_content)
                f.write("\n\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated by Noire Converter v1.7\n")
            
            self.log(f"Tree exported: {folder_name}_tree.txt", "success")
            
        except Exception as e:
            self.log(f"Tree export error: {str(e)[:30]}", "error")
        
        self.finish_process()

    def copy_tree_to_clipboard(self):
        text = self.tree_preview_box.get("1.0", "end-1c")
        if text.strip():
            self.clipboard_clear()
            self.clipboard_append(text)
            self.log("Tree copied to clipboard.", "success")

    # --- TRANSLATION METHODS ---
    def translate_large_text(self, text, target_lang):
        """Splits text into chunks and translates them to avoid 5000 char limit."""
        translator = GoogleTranslator(source='auto', target=target_lang)
        MAX_CHUNK = 4500
        
        if len(text) < MAX_CHUNK:
            return translator.translate(text)
            
        chunks = []
        current_chunk = ""
        
        # Simple splitting by lines to preserve structure
        lines = text.split('\n')
        
        for line in lines:
            if len(line) > MAX_CHUNK:
                # Line itself is too long, split by characters
                while len(line) > 0:
                    part = line[:MAX_CHUNK]
                    line = line[MAX_CHUNK:]
                    if len(current_chunk) + len(part) < MAX_CHUNK:
                        current_chunk += part
                    else:
                        if current_chunk: chunks.append(translator.translate(current_chunk))
                        current_chunk = part
            elif len(current_chunk) + len(line) < MAX_CHUNK:
                current_chunk += line + "\n"
            else:
                if current_chunk:
                    chunks.append(translator.translate(current_chunk))
                current_chunk = line + "\n"
                
        if current_chunk:
             chunks.append(translator.translate(current_chunk))
             
        return "\n".join(chunks)

    def process_translation(self):
        """Main translation processing method using file_items from queue"""
        # No API Key needed for Google Translate
        
        target_lang = self.translate_target_lang.get()
        print(f"[DEBUG] User Selected Language: '{target_lang}'")
        
        # DeepL language code mapping
        lang_map = {
            "TR": "tr", "EN": "en", "DE": "de", "FR": "fr", "ES": "es",
            "IT": "it", "PT": "pt", "RU": "ru", "JA": "ja", "KO": "ko",
            "ZH": "zh", "NL": "nl", "PL": "pl", "CS": "cs", "EL": "el",
            "HU": "hu", "RO": "ro", "SV": "sv", "DA": "da", "FI": "fi"
        }
        target_code = lang_map.get(target_lang, "tr")
        
        # Get selected files from queue
        translate_files = [item['path'] for item in self.file_items if item['var'].get()]
        
        # Filtrele: Sadece text dosyaları
        valid_files = []
        for f in translate_files:
            ext = os.path.splitext(f)[1].lower()
            if ext in TEXT_EXTS:
                valid_files.append(f)
        
        if not valid_files:
            self.log("No text files to translate.", "info")
            self.finish_process()
            return

        total = len(valid_files)
        success_count = 0
        
        for i, file_path in enumerate(valid_files):
            try:
                file_name = os.path.basename(file_path)
                ext = os.path.splitext(file_path)[1].lower()
                
                # UI Update
                self.log(f"[{i+1}/{total}] Translating: {file_name}...", "info")
                
                # Read file content
                content = ""
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            content = f.read()
                    except:
                        self.log(f"Read Error: {file_name}", "error")
                        continue
                
                if not content.strip():
                    continue
                
                # Translate using Google Translate (with chunking)
                try:
                    print(f"[DEBUG] Translating {file_name} to {target_code} via Google...")
                    translated = self.translate_large_text(content, target_code)
                    if not translated:
                         raise Exception("Empty translation result")
                    print(f"[DEBUG] Translation success. Length: {len(translated)}")
                except Exception as e:
                    self.log(f"Google Error: {str(e)[:40]}...", "error")
                    print(f"[DEBUG] Google Exception: {str(e)[:200]}") # Truncate log
                    continue
                
                # Save translated file (Always Separate)
                # Separate file: original_tr.txt, original_de.json, etc.
                suffix = f"_{target_lang.lower()}"
                new_name = os.path.splitext(file_name)[0] + suffix + ext
                save_path = os.path.join(os.path.dirname(file_path), new_name)
                    
                # Write output
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(translated)
                self.log(f"[{i+1}/{total}] ✓ {file_name} -> {new_name}", "success")
                
                success_count += 1
                
                # Show preview of first file
                if i == 0:
                    self.text_translate_preview.configure(state="normal")
                    self.text_translate_preview.delete("1.0", "end")
                    preview_text = translated[:2000] + ("..." if len(translated) > 2000 else "")
                    self.text_translate_preview.insert("1.0", f"[{file_name}]\n\n{preview_text}")
                    self.text_translate_preview.configure(state="disabled")
                    
            except Exception as e:
                self.log(f"[{i+1}/{total}] ✗ {os.path.basename(file_path)}: {str(e)[:20]}", "error")
        
        self.log(LANG[self.current_lang]["msg_trans_done"] + f" ({success_count}/{total})", "success")
        self.finish_process()

    def refresh_translate_source_list(self):
        pass # Removed

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except: pass
        return {}

    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f)
        except: pass

