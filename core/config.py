import customtkinter as ctk

LANG = {
    "en": {
        "title": "Noire Converter v1.8",
        "drop_title": "DROP MEDIA",
        "drop_sub": "Files/Folders",
        "chk_img": "Img", "chk_aud": "Aud", "chk_vid": "Vid", "chk_doc": "Doc",
        "tab_convert": "Convert", "tab_resize": "Resize", "tab_opt": "Optimizer",
        "tab_gif": "GIF Studio", "tab_doc": "Doc Station", "tab_tools": "Renamer",
        "tab_tree": "Tree View",
        "tab_text": "Text Extract",
        "tab_youtube": "YouTube",
        "yt_lbl_input": "Link or Search",
        "yt_btn_fetch": "Fetch",
        "yt_btn_fetching": "Searching...",
        "yt_lbl_results": "Result",
        "yt_lbl_quality": "Quality",
        "yt_btn_download": "DOWNLOAD",
        "yt_lbl_info": "ℹ️ Paste a YouTube link (video/playlist) or type a song name.",
        "yt_status_fetching": "Fetching info...",
        "yt_status_no_results": "No results found.",
        "yt_status_done": "Download complete",
        "yt_err_empty": "Enter a link or search term first.",
        "yt_err_select": "Fetch a video first.",
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
        "lbl_tree_select": "Select Folder:",
        "lbl_text_select": "Select Folder:",
        "lbl_tree_preview": "Preview:",
        "lbl_tree_info": "ℹ️ Exports the folder structure as a text file with tree view.",
        "lbl_text_preview": "Preview:",
        "lbl_text_info": "ℹ️ Extracts content from any file and saves as .txt.",
        "lbl_text_title": "Text Extract",
        "lbl_text_desc": "Save selected files content as .txt.",
        "lbl_text_info_box": "Extract text from Word/PDF/PowerPoint documents, or transcribe spoken text from Audio/Video media.\nSaves standard TXT file side-by-side with original media.",
        
        # --- VIEW MODES ---
        "view_list": "List",
        "view_preview": "Preview",
        "queue_limit": "Limit",
        "lbl_collect_img": "Images",
        "lbl_collect_vid": "Videos",
        "lbl_collect_aud": "Audio",
        "lbl_collect_doc": "Docs",
        "btn_tree_copy": "Copy",
        
        # --- SAVE AREA ---
        "btn_tree_browse": "Browse Folder",
        "btn_tree_export": "Export Tree",
        "btn_text_browse": "Browse Folder",
        "btn_text_export": "Extract & Save",
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
        # --- TRANSLATION TAB ---
        "tab_translate": "Translate",
        "lbl_target_lang": "Target Language",
        "lbl_source_lang": "Source Language",
        "lbl_translate_mode": "Save Mode",
        "opt_separate": "Separate File",
        "opt_same": "Append to Same File",
        "btn_translate": "TRANSLATE",
        "lbl_translate_preview": "Preview:",
        "lbl_translate_hint": "ℹ️ Supported: .txt, .srt, .json, .xml, .csv, .html",
        "status_translating": "Translating...",
        "msg_api_key_missing": "DeepL API Key is required!",
        "msg_no_translatable": "No translatable files selected!",
        "msg_trans_done": "Translation completed!",
        "msg_trans_error": "Translation error: ",
        "msg_select_trans_folder": "Select folder containing files to translate",
        "btn_trans_folder": "Select Files",
        "lbl_trans_folder": "Selected Folder:",
        "lbl_trans_files": "Files to Translate:",
        "msg_save_separate": "Save to separate file",
        "msg_save_append": "Append to existing file",
        "lbl_auto": "Auto",
        # --- FILE COLLECTOR TAB ---
        "tab_collector": "Collector",
        "lbl_collector_source": "Source Folder (Root):",
        "lbl_collector_target": "Target Folder:",
        "lbl_collector_ext": "File Types:",
        "lbl_collector_recursive": "Include Subfolders",
        "btn_collector_source": "Select Source",
        "btn_collector_target": "Select Target",
        "lbl_collector_info": "ℹ️ Collects files from nested folders to a single target folder.",
        # --- RENAMER TAB (Prefix mode ekleri) ---
        "lbl_rename_mode": "Rename Mode:",
        "seg_rename_find": "Find & Replace",
        "seg_rename_prefix": "Prefix by Folder",
        "lbl_prefix_info": "ℹ️ Select parent folder. Adds subfolder name to files inside them.",
        "lbl_prefix_sep": "Separator:",
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
• Find & Replace: Replaces text in filenames.
• Prefix by Folder: Adds parent folder name to filename.

5. TRANSLATE (New)
---------------------------
• Free Google Translate integration.
• Auto-splits large files (>5000 chars).
• Saves as separate files (e.g. file_tr.txt).

6. COLLECTOR (New)
---------------------------
• Collect files from nested subfolders into one folder.

7. SETUP
---------------------------
• 'ffmpeg.exe' must be in the same folder."""
    },
    "tr": {
        "title": "Noire Converter v1.8",
        "drop_title": "MEDYA SÜRÜKLE",
        "drop_sub": "Dosya/Klasör",
        "chk_img": "Img", "chk_aud": "Aud", "chk_vid": "Vid", "chk_doc": "Doc",
        "tab_convert": "Dönüştür", "tab_resize": "Boyutlandır", "tab_opt": "Optimize",
        "tab_gif": "GIF Stüdyo", "tab_doc": "Doc İstasyonu", "tab_tools": "Adlandır",
        "tab_tree": "Ağaç Görünümü",
        "tab_text": "Metin Çıkar",
        "tab_youtube": "YouTube",
        "yt_lbl_input": "Link ya da Arama",
        "yt_btn_fetch": "Bul",
        "yt_btn_fetching": "Aranıyor...",
        "yt_lbl_results": "Sonuç",
        "yt_lbl_quality": "Kalite",
        "yt_btn_download": "İNDİR",
        "yt_lbl_info": "ℹ️ YouTube linki (video/playlist) yapıştır ya da şarkı adı yaz.",
        "yt_status_fetching": "Bilgi alınıyor...",
        "yt_status_no_results": "Sonuç bulunamadı.",
        "yt_status_done": "İndirme tamamlandı",
        "yt_err_empty": "Önce bir link ya da arama terimi gir.",
        "yt_err_select": "Önce bir video getir.",
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
        "lbl_tree_select": "Klasör Seç:",
        "lbl_text_select": "Klasör Seç:",
        "lbl_tree_preview": "Önizleme:",
        "lbl_tree_info": "ℹ️ Klasör yapısını ağaç görünümünde text dosyasına aktarır.",
        "lbl_text_preview": "Önizleme:",
        "lbl_text_info": "ℹ️ Herhangi bir dosyanın içeriğini .txt olarak kaydeder.",
        "lbl_text_title": "Text Extract",
        "lbl_text_desc": "Seçili dosyaların içeriğini .txt olarak kaydet.",
        "lbl_text_info_box": "Word/PDF/PowerPoint belgelerinden metin çıkarır veya Ses/Video dosyalarındaki konuşmaları metne döker.\nOrijinal dosyanın yanına standart TXT dosyası olarak kaydeder.",
        
        # --- VIEW MODES ---
        "view_list": "Liste",
        "view_preview": "Önizleme",
        "queue_limit": "Limit",
        "lbl_collect_img": "Resim",
        "lbl_collect_vid": "Video",
        "lbl_collect_aud": "Ses",
        "lbl_collect_doc": "Belge",
        "btn_tree_copy": "Kopyala",
        
        # --- SAVE AREA ---
        "btn_tree_browse": "Klasör Seç",
        "btn_tree_export": "Ağacı Dışa Aktar",
        "btn_text_browse": "Klasör Seç",
        "btn_text_export": "Çıkar ve Kaydet",
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
        # --- TRANSLATION TAB ---
        "tab_translate": "Çeviri",
        "lbl_target_lang": "Hedef Dil",
        "lbl_source_lang": "Kaynak Dil",
        "lbl_translate_mode": "Kaydetme Modu",
        "opt_separate": "Ayrı Dosya",
        "opt_same": "Aynı Dosyaya Ekle",
        "btn_translate": "ÇEVİR",
        "lbl_translate_preview": "Önizleme:",
        "lbl_translate_hint": "ℹ️ Desteklenen: .txt, .srt, .json, .xml, .csv, .html",
        "status_translating": "Çeviriliyor...",
        "msg_api_key_missing": "DeepL API Anahtarı gerekli!",
        "msg_no_translatable": "Çevrilebilir dosya seçilmedi!",
        "msg_trans_done": "Çeviri tamamlandı!",
        "msg_trans_error": "Çeviri hatası: ",
        "msg_select_trans_folder": "Çevrilecek dosyaları içeren klasörü seçin",
        "btn_trans_folder": "Dosya Seç",
        "lbl_trans_folder": "Seçilen Klasör:",
        "lbl_trans_files": "Çevrilecek Dosyalar:",
        "msg_save_separate": "Ayrı dosya olarak kaydet",
        "msg_save_append": "Mevcut dosyaya ekle",
        "lbl_auto": "Otomatik",
        # --- FILE COLLECTOR TAB ---
        "tab_collector": "Toplayıcı",
        "lbl_collector_source": "Kaynak Klasör (Kök):",
        "lbl_collector_target": "Hedef Klasör:",
        "lbl_collector_ext": "Dosya Türleri:",
        "lbl_collector_recursive": "Alt Klasörleri Dahil Et",
        "btn_collector_source": "Kaynak Seç",
        "btn_collector_target": "Hedef Seç",
        "lbl_collector_info": "ℹ️ İç içe geçmiş klasörlerdeki dosyaları tek yere toplar.",
        # --- RENAMER TAB (Prefix mode ekleri) ---
        "lbl_rename_mode": "Yeniden Adlandırma Modu:",
        "seg_rename_find": "Bul ve Değiştir",
        "seg_rename_prefix": "Klasör Adı Ekle",
        "lbl_prefix_info": "ℹ️ Ana klasörü seçin. Alt klasörlerdeki dosyaların başına klasör adını ekler.",
        "lbl_prefix_sep": "Ayırıcı:",
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
• Bul ve Değiştir: Dosyadaki metni değiştirir.
• Klasör Adı Ekle: Dosya adına bulunduğu alt klasörün adını ekler.

5. ÇEVİRİ (Yeni)
---------------------------
• Ücretsiz Google Translate entegrasyonu.
• Uzun metinleri otomatik böler.
• Ayrı dosya olarak kaydeder (örn: dosya_tr.txt).

6. TOPLAYICI (Yeni)
---------------------------
• Alt klasörlere dağılmış dosyaları tek bir hedefe toplar.

7. KURULUM
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
DOC_EXTS   = ['.docx', '.doc', '.pptx', '.ppt', '.pdf', '.txt', '.srt', '.json', '.xml', '.csv', '.html', '.htm', '.md', '.yaml', '.yml', '.py', '.js', '.ts', '.cs', '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rs', '.swift', '.kt', '.rb', '.php', '.pl', '.sh', '.bat', '.ps1', '.log', '.ini', '.cfg', '.conf', '.properties']
TEXT_EXTS  = ['.txt', '.srt', '.json', '.xml', '.csv', '.html', '.htm', '.md', '.yaml', '.yml', '.py', '.js', '.ts', '.cs', '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rs', '.swift', '.kt', '.rb', '.php', '.pl', '.sh', '.bat', '.ps1', '.log', '.ini', '.cfg', '.conf', '.properties']

