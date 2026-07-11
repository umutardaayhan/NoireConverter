# Noire Converter v2.2 🌑

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat&logo=windows)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<div align="center">
  <h3>
    <a href="#-english">🇬🇧 English</a> | 
    <a href="#-türkçe">🇹🇷 Türkçe</a>
  </h3>
</div>

---

<a name="-english"></a>
## 🇬🇧 English

**Noire Converter** is a modern, all-in-one media processing tool built with Python and FFmpeg. Designed for computer engineering students, game developers, and content creators to handle media assets efficiently with a professional dark UI.

### 🌟 Features

* **Privacy (v2.2 - NEW!):** Strip ALL metadata (GPS, device, date) from images as _clean copies; edit or wipe ID3 tags of audio files.
* **Video Studio (v2.2 - NEW!):** Cut videos without re-encoding and merge clips in queue order.
* **PDF Tools (v2.2 - NEW!):** Merge PDFs, split into pages, or extract a page range.
* **Settings (v2.2 - NEW!):** Startup language, default audio quality, default output folder, clipboard watcher — all persistent.
* **Media DL Comfort (v2.2 - NEW!):** Clipboard watcher auto-catches copied media links, multi-link paste queues them all, and download history warns about repeats.
* **Refreshed UI (v2.0):** Layered noir-gold palette, icon tabs, a live progress bar, and a fully centralized style system under the hood.
* **Converter:** Convert between Image (.webp, .png, .jpg, .ico) and Audio (.mp3, .wav) formats instantly.
* **Doc Station:** Convert Word/PowerPoint to PDF, or PDF/PowerPoint to Word documents. *(Requires MS Office)*.
* **Renamer (v1.3):** Batch rename files by finding and replacing text. Perfect for cleaning asset tags (e.g., removing `_1500x1500` suffixes).
* **Tree View (v1.7):** Export folder structure as a beautiful tree-view text file. Great for documentation and project overviews.
* **Text Extract (v1.7):** Extract content from ANY file type (.py, .js, .java, .c, .cpp, etc.) and save as .txt. Perfect for code documentation and text extraction.
* **Media DL (v2.1 - NEW: Instagram · TikTok · X!):** Download from **YouTube, Instagram, TikTok, and X (Twitter)** as **MP3** (128/192/320 kbps), **M4A**, or **MP4** (480p/720p/1080p/Best). Paste a link from any supported platform or search by song name (YouTube search) — results appear in the Queue with a platform badge, then hit START. Cover art and metadata are embedded automatically for audio.
* **Resizer:** High-quality image resizing using the Lanczos algorithm.
* **Optimizer:** Compress assets by up to 80% without visible quality loss (Ideal for Unity/Godot/Web).
* **GIF Studio:** Create optimized GIFs from videos. Includes a **Visual Crop Editor** to trim and crop specific areas easily.
* **Drag & Drop:** Support for dragging files and folders directly into the UI.
* **Dual Language:** Switch between English and Turkish interface instantly.

### 🛠️ Installation

> [!TIP]
> **Quick Start:** If you don't want to deal with installation, you can directly run the precompiled executable **`NoireConverter.exe`** under the `dist` directory!

1. **Clone the repository:**
```
    git clone https://github.com/umutardaayhan/NoireConverter.git
    cd NoireConverter
```
2. **Install Python dependencies:**
```
    pip install -r requirements.txt
```

### 📖 How to Use

#### 1. Converter Tab
* Select files by dragging and dropping or using **Browse Folder**.
* Choose target format (WEBP, JPG, PNG, ICO for images / MP3, WAV for audio).
* Click **START**.

#### 2. Resizer Tab
* Select images.
* Choose preset sizes (½, ¼, 2x, 4x) or enter custom dimensions.
* Click **START**.

#### 3. Optimizer Tab
* Select images.
* Adjust quality slider (10-100%).
* Click **START**.

#### 4. GIF Studio Tab
* Select a video.
* Set duration (or leave blank for full video).
* Use **Crop Editor** to select the area.
* Set FPS and output settings.
* Click **START**.

#### 5. Doc Station Tab
* Select Word/PowerPoint/PDF files.
* Choose conversion mode.
* Click **START**.
* *Requires MS Office installed.*

#### 6. Renamer Tab
* Select files.
* Enter text to find and replace.
* Click **START**.

#### 7. Tree View Tab
* Select a folder.
* Click **Export Tree**.

#### 8. Translate Tab
* Click "**Add From Folder**" to select text files.
* Choose Target Language (e.g., TR, EN, DE).
* Click **START**.
* Translated files are saved as `filename_lang.ext`.

#### 9. Text Extract Tab (v1.7 - NEW!)
* **Drag & Drop** files or use **Browse Folder** in Drop Media panel.
* Toggle **Source Folder** switch to choose save location.
* Switch to **Text Extract** tab.
* Click **START**.
* All selected files will be extracted as `.txt` files.
* Supports: .py, .js, .ts, .cs, .java, .c, .cpp, .h, .hpp, and any text-based file!

#### 10. Media DL Tab (YouTube · Instagram · TikTok · X)
* Paste a **link** from YouTube, Instagram, TikTok, or X (Twitter) — or type a **song name** (searches YouTube) — and click **Fetch**.
* Instagram and some X content requires login — see the cookies.txt section below.
* Search results appear in a dropdown; each selection is added to the **Queue** on the right.
* Choose **Audio** or **Video** format. Audio: **128 / 192 / 320 kbps MP3** or **M4A** (original audio, no re-encoding). Video: **480p / 720p / 1080p / Best** MP4.
* Click **DOWNLOAD** (or **START**) — all checked YouTube items in the queue are downloaded in order.
* Files are saved to the output folder (or `~/Downloads` if none is selected), with embedded cover art and metadata.
* Playlists are limited to 50 tracks for safety (Mix/radio lists can be endless).

> [!NOTE]
> YouTube protects its stream URLs with a JavaScript challenge. yt-dlp solves it automatically,
> but it needs a JS runtime installed on your system: **Node.js** or **Deno**. If downloads fail with
> *"Requested format is not available"*, install [Node.js](https://nodejs.org) and update yt-dlp:
> `pip install -U "yt-dlp[default]"`.

#### 🔞 Age-Restricted Videos ("Sign in to confirm your age")
YouTube requires cookies from a signed-in account for age-restricted videos:

1. Install the **"Get cookies.txt LOCALLY"** browser extension (free, open source).
2. Go to youtube.com while signed in, click the extension → **Export**.
3. Save the file as **`cookies.txt`** in the NoireConverter root folder and restart the app.

> [!CAUTION]
> `cookies.txt` contains your personal YouTube session. **Never commit or share it.**
> It is already listed in `.gitignore`, so it will not be pushed to the repository.

### ⚠️ IMPORTANT: FFmpeg Setup
This application requires the **FFmpeg engine** to process video and audio files. Since it is a large binary file, it is not included in this repository.

1.  **Download:** Go to [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) and download the `.7z` or `.zip` file.
2.  **Extract:** Open the downloaded file. Go into the `bin` folder.
3.  **Copy:** Find the `ffmpeg.exe` file (application).
4.  **Paste:** Copy `ffmpeg.exe` and paste it directly into the **NoireConverter** folder (next to `noire_converter.py`).

**Your folder structure must look like this:**

    NoireConverter/
    ├── noire_converter.py
    ├── ffmpeg.exe        <-- IMPORTANT! Place it here.
    ├── ffprobe.exe       <-- Recommended (used by the YouTube tab).
    ├── cookies.txt       <-- Optional (age-restricted YouTube videos). NEVER commit!
    ├── App.ico
    ├── requirements.txt
    └── README.md

### 🚀 Usage

Run the application via terminal:

    python noire_converter.py

---

<a name="-türkçe"></a>
## 🇹🇷 Türkçe

**Noire Converter**, Python ve FFmpeg tabanlı, modern ve karanlık arayüze sahip hepsi bir arada bir medya işleme aracıdır. Bilgisayar mühendisliği öğrencileri, oyun geliştiriciler ve içerik üreticileri için performans odaklı tasarlanmıştır.

### 🌟 Özellikler

* **Gizlilik (v2.2 - YENİ!):** Resimlerdeki TÜM metadata'yı (GPS, cihaz, tarih) _clean kopyalar olarak temizleyin; ses dosyalarının ID3 etiketlerini düzenleyin ya da silin.
* **Video Stüdyo (v2.2 - YENİ!):** Videoları yeniden kodlamadan kesin, klipleri kuyruk sırasıyla birleştirin.
* **PDF Araçları (v2.2 - YENİ!):** PDF birleştirin, sayfalara bölün ya da sayfa aralığı çıkarın.
* **Ayarlar (v2.2 - YENİ!):** Açılış dili, varsayılan ses kalitesi, varsayılan çıktı klasörü, pano izleyici — hepsi kalıcı.
* **Media DL Konforu (v2.2 - YENİ!):** Pano izleyici kopyalanan medya linklerini otomatik yakalar, çoklu link yapıştırma hepsini kuyruğa dizer, indirme geçmişi tekrarlarda uyarır.
* **Yenilenen Arayüz (v2.0):** Katmanlı noir-altın palet, ikonlu sekmeler, canlı ilerleme çubuğu ve arka planda tamamen merkezileştirilmiş stil sistemi.
* **Dönüştürücü (Converter):** Resim (.webp, .png, .jpg, .ico) ve Ses (.mp3, .wav) formatları arasında hızlı dönüşüm.
* **Doc İstasyonu:** Word/PPT dosyalarını PDF'e, PDF/PPT dosyalarını Word'e çevirin. *(MS Office gerektirir)*.
* **Adlandırıcı (Renamer - v1.3):** Dosya isimlerindeki belirli metinleri topluca bulun ve değiştirin. Asset temizliği (örn: `_kopya` yazılarını silmek) için idealdir.
* **Ağaç Görünümü (Tree View - v1.7):** Klasör yapısını estetik ağaç görünümünde text dosyasına aktarın. Dokümantasyon ve proje özetleri için idealdir.
* **Metin Çıkar (Text Extract - v1.7):** HERHANGİ bir dosya türünün (.py, .js, .java, .c, .cpp, vb.) içeriğini çıkarır ve .txt olarak kaydeder. Kod dokümantasyonu ve metin çıkarma için mükemmel.
* **Media DL (v2.1 - YENİ: Instagram · TikTok · X!):** **YouTube, Instagram, TikTok ve X (Twitter)** içeriklerini **MP3** (128/192/320 kbps), **M4A** ya da **MP4** (480p/720p/1080p/Best) olarak indirin. Desteklenen platformlardan link yapıştırın veya şarkı adıyla arayın (YouTube araması) — sonuçlar platform rozetiyle Kuyruğa düşer, BAŞLAT'a basın. Kapak resmi ve metadata sesli indirmelerde otomatik gömülür.
* **Boyutlandırıcı (Resizer):** Resimleri kalite kaybını minimize ederek (Lanczos algoritması) yeniden boyutlandırın.
* **Optimizer:** Web ve Oyun projeleri (Unity/Godot assetleri) için dosya boyutunu %80'e kadar sıkıştırır.
* **GIF Studio:** Videoları kırpın (Crop), süresini ayarlayın (Trim) ve optimize edilmiş GIF'lere dönüştürün. **Görsel Kırpma Editörü** dahildir.
* **Drag & Drop:** Dosyaları veya klasörleri sürükleyip bırakarak listeye ekleyin.
* **Çoklu Dil Desteği:** Tek tuşla Türkçe ve İngilizce arasında geçiş yapın.

### 🛠️ Kurulum

> [!TIP]
> **Hızlı Başlangıç:** Kurulumla uğraşmak istemeyenler direkt `dist` klasörü içerisindeki **`NoireConverter.exe`** dosyamızı indirip uygulamamızı çalıştırabilir!

1. **Projeyi bilgisayarınıza klonlayın:**
```
    git clone https://github.com/umutardaayhan/NoireConverter.git
    cd NoireConverter
```
2. **Gerekli kütüphaneleri yükleyin:**
```
    pip install -r requirements.txt
```

### 📖 Nasıl Kullanılır

#### 1. Dönüştürücü Sekmesi
* Dosyaları sürükleyip bırakarak veya **Klasör Seç** ile ekleyin.
* Hedef formatı seçin (WEBP, JPG, PNG, ICO / MP3, WAV).
* **BAŞLAT**'a basın.

#### 2. Boyutlandırıcı Sekmesi
* Resimleri seçin.
* Hazır ayarları (½, ¼, 2x, 4x) seçin veya özel boyut girin.
* **BAŞLAT**'a basın.

#### 3. Optimize Sekmesi
* Resimleri seçin.
* Kalite kaydırıcısını ayarlayın (10-100%).
* **BAŞLAT**'a basın.

#### 4. GIF Stüdyo Sekmesi
* Video seçin.
* Süreyi ayarlayın (boş bırakırsanız tamamını işler).
* **Kırpma Editörü** ile alan seçin.
* FPS ve çıktı ayarlarını yapın.
* **BAŞLAT**'a basın.

#### 5. Doc İstasyonu Sekmesi
* Word/PowerPoint/PDF dosyaları seçin.
* Dönüştürme modunu seçin.
* **BAŞLAT**'a basın.
* *Bilgisayarda MS Office yüklü olmalıdır.*

#### 6. Adlandırıcı Sekmesi
* Dosyaları seçin.
* Bulunacak metin ve yeni metini girin.
* **BAŞLAT**'a basın.

#### 7. Ağaç Görünümü Sekmesi
* Klasör seçin.
* **Ağacı Dışa Aktar**'a basın.

#### 8. Çeviri Sekmesi
* **"Klasörden Ekle"** butonuna basarak metin dosyalarınızın olduğu klasörü seçin.
* Hedef Dili (TR, EN vb.) seçin.
* **BAŞLAT**'a basın.
* Çevrilen dosyalar `dosyaadi_dil.uzanti` şeklinde kaydedilir.

#### 9. Metin Çıkar Sekmesi (Text Extract - v1.7 - YENİ!)
* **Sürükle ve bırak** veya **Drop Media** panelindeki **Klasör Seç** butonunu kullanarak dosya ekleyin.
* **Kaynak Klasör** anahtarını kullanarak kaydetme konumunu belirleyin.
* **Metin Çıkar** sekmesine geçin.
* **BAŞLAT**'a basın.
* Tüm seçili dosyalar `.txt` dosyası olarak kaydedilir.
* Desteklenen: .py, .js, .ts, .cs, .java, .c, .cpp, .h, .hpp ve herhangi bir metin tabanlı dosya!

#### 10. Media DL Sekmesi (YouTube · Instagram · TikTok · X)
* YouTube, Instagram, TikTok veya X (Twitter) **linki** yapıştırın — ya da **şarkı adı** yazıp (YouTube'da arar) **Bul**'a basın.
* Instagram ve bazı X içerikleri oturum ister — aşağıdaki cookies.txt bölümüne bakın.
* Arama sonuçları açılır menüde listelenir; her seçim sağdaki **Kuyruğa** eklenir.
* **Ses** veya **Video** formatını seçin. Ses: **128 / 192 / 320 kbps MP3** veya **M4A** (orijinal ses, yeniden kodlamasız). Video: **480p / 720p / 1080p / Best** MP4.
* **İNDİR**'e (veya **BAŞLAT**'a) basın — kuyruktaki işaretli tüm YouTube öğeleri sırayla indirilir.
* Dosyalar çıktı klasörüne (seçilmemişse `~/Downloads`'a) kapak resmi ve metadata gömülü olarak kaydedilir.
* Oynatma listeleri güvenlik için 50 parçayla sınırlıdır (Mix/radyo listeleri sonsuz olabilir).

> [!NOTE]
> YouTube, yayın adreslerini bir JavaScript bulmacasıyla korur. yt-dlp bunu otomatik çözer ancak
> sistemde bir JS çalıştırıcısı gerekir: **Node.js** veya **Deno**. İndirmeler
> *"Requested format is not available"* hatası verirse [Node.js](https://nodejs.org) kurun ve
> yt-dlp'yi güncelleyin: `pip install -U "yt-dlp[default]"`.

#### 🔞 Yaş Kısıtlamalı Videolar ("Sign in to confirm your age")
YouTube, yaş kısıtlamalı videolar için oturum açmış bir hesabın çerezlerini ister:

1. Tarayıcınıza **"Get cookies.txt LOCALLY"** uzantısını kurun (ücretsiz, açık kaynak).
2. youtube.com'da oturum açıkken uzantıya tıklayın → **Export**.
3. Dosyayı NoireConverter kök klasörüne **`cookies.txt`** adıyla kaydedin ve uygulamayı yeniden başlatın.

> [!CAUTION]
> `cookies.txt` kişisel YouTube oturumunuzu içerir. **Asla commit'lemeyin, kimseyle paylaşmayın.**
> `.gitignore`'da zaten listelidir; depoya push edilmez.

### ⚠️ Önemli: FFmpeg Kurulumu
Bu uygulama video ve ses işlemleri için **FFmpeg** motorunu kullanır.

1.  **İndir:** [FFmpeg İndir (Gyan.dev)](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) adresinden zip dosyasını indirin.
2.  **Ayıkla:** İndirdiğiniz arşivin içine girin ve `bin` klasörünü bulun.
3.  **Kopyala:** İçindeki `ffmpeg.exe` dosyasını kopyalayın.
4.  **Yapıştır:** Bu dosyayı `noire_converter.py` dosyasının olduğu ana klasöre yapıştırın.

**Klasör yapınız tam olarak şöyle görünmelidir:**

    NoireConverter/
    ├── noire_converter.py
    ├── ffmpeg.exe        <-- BURADA OLMALI
    ├── ffprobe.exe       <-- Önerilir (YouTube sekmesi kullanır)
    ├── cookies.txt       <-- İsteğe bağlı (yaş kısıtlamalı videolar). ASLA commit'lemeyin!
    ├── App.ico
    ├── requirements.txt
    └── README.md

### 🚀 Kullanım

Uygulamayı başlatmak için terminalde şu komutu çalıştırın:

    python noire_converter.py

---

## 📄 License / Lisans
This project is licensed under the MIT License.
