# Noire Converter v1.1 🌑

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

* **Converter:** Convert between Image (.webp, .png, .jpg, .ico) and Audio (.mp3, .wav) formats instantly.
* **Resizer:** High-quality image resizing using the Lanczos algorithm.
* **Optimizer:** Compress assets by up to 80% without visible quality loss (Ideal for Unity/Godot/Web).
* **GIF Studio:** Create optimized GIFs from videos. Includes a **Visual Crop Editor** to trim and crop specific areas easily.
* **UX Improvements (v1.1):** Renamed "Output Setting" to **"Render Quality"** with added tooltips to clearly explain resolution options.
* **Drag & Drop:** Support for dragging files and folders directly into the UI.
* **Dual Language:** Switch between English and Turkish interface instantly.

### 🛠️ Installation

1. **Clone the repository:**

    git clone https://github.com/umutardaayhan/NoireConverter.git
   
    cd NoireConverter

3. **Install Python dependencies:**

    pip install -r requirements.txt

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

* **Dönüştürücü (Converter):** Resim (.webp, .png, .jpg, .ico) ve Ses (.mp3, .wav) formatları arasında hızlı dönüşüm.
* **Boyutlandırıcı (Resizer):** Resimleri kalite kaybını minimize ederek (Lanczos algoritması) yeniden boyutlandırın.
* **Optimizer:** Web ve Oyun projeleri (Unity/Godot assetleri) için dosya boyutunu %80'e kadar sıkıştırır.
* **GIF Studio:** Videoları kırpın (Crop), süresini ayarlayın (Trim) ve optimize edilmiş GIF'lere dönüştürün. **Görsel Kırpma Editörü** dahildir.
* **Arayüz Güncellemesi (v1.1):** "Çıktı Ayarı" etiketi **"Render Kalitesi"** olarak güncellendi ve seçenekler için açıklayıcı ipuçları (tooltip) eklendi.
* **Drag & Drop:** Dosyaları veya klasörleri sürükleyip bırakarak listeye ekleyin.
* **Çoklu Dil Desteği:** Tek tuşla Türkçe ve İngilizce arasında geçiş yapın.

### 🛠️ Kurulum

1. **Projeyi bilgisayarınıza klonlayın:**

    git clone https://github.com/umutardaayhan/NoireConverter.git
   
    cd NoireConverter

3. **Gerekli kütüphaneleri yükleyin:**

    pip install -r requirements.txt

### ⚠️ Önemli: FFmpeg Kurulumu
Bu uygulama video ve ses işlemleri için **FFmpeg** motorunu kullanır. Dosya boyutu büyük olduğu için bu depoya dahil edilmemiştir, manuel eklenmelidir.

1.  **İndir:** [FFmpeg İndir (Gyan.dev)](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) adresinden zip dosyasını indirin.
2.  **Ayıkla:** İndirdiğiniz arşivin içine girin ve `bin` klasörünü bulun.
3.  **Kopyala:** İçindeki `ffmpeg.exe` dosyasını kopyalayın.
4.  **Yapıştır:** Bu dosyayı `noire_converter.py` dosyasının olduğu ana klasöre yapıştırın.

**Klasör yapınız tam olarak şöyle görünmelidir:**

    NoireConverter/
    ├── noire_converter.py
    ├── ffmpeg.exe        <-- BURADA OLMALI
    ├── App.ico
    ├── requirements.txt
    └── README.md

### 🚀 Kullanım

Uygulamayı başlatmak için terminalde şu komutu çalıştırın:

    python noire_converter.py

---

## 📄 License / Lisans
This project is licensed under the MIT License.
