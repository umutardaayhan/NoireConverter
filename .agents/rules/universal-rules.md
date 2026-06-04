---
trigger: always_on
---

# 🚀 ANTIGRAVITY: EVRENSEL GELİŞTİRME VE İŞBİRLİĞİ REHBERİ

Bu rehber, projenin uzun vadeli sağlığını korumak, karmaşıklığı yönetmek ve AI ile insan arasındaki yaratıcı süreci en verimli hale getirmek için paylaştığımız ortak bir vizyondur. Birer kuraldan ziyade, "iyi mühendislik" adına özen göstermemiz gereken prensiplerimizdir.

---

## 1. PROJENİN HAFIZASI: `docs` EKOSİSTEMİ

Projemizin en değerli varlığı, sahip olduğumuz bilgi birikimidir. Bu nedenle `docs` klasörünü projemizin "kolonları" ve "yol haritası" olarak görüyoruz.

*   **Önce Oku, Sonra Uygula:** Herhangi bir analiz veya geliştirme sürecine başlamadan önce, `docs` klasöründeki ilgili Markdown dosyalarını inceleyerek projenin o bölümündeki temel mantığı, veritabanı şemasını veya backend tercihlerini anlamaya çalışmalıyız.
*   **Bilgiyi Güncel Tut:** Yaptığımız her anlamlı değişiklikten veya eklediğimiz her yeni özellikten sonra, `docs` klasöründeki ilgili dokümanları da güncellemeliyiz. Eğer yeni bir alan (örneğin: yeni bir API entegrasyonu) eklediysek, bunun için `docs` altında yeni bir rehber dosyası oluşturmamız projenin sürdürülebilirliği için harika olacaktır.
*   **Hayati Değer:** Dokümantasyonumuz, sadece bilgi vermekle kalmaz; projenin hangi kısımlarının "dokunulmaz" olduğunu veya hangi kısımların değişime açık olduğunu gösteren bir pusuladır.

---

## 2. GÖZLEM VE MİMARİ SADAKAT

*   **Keşif Yolculuğu:** Kod yazmaya başlamadan önce mevcut dizini ve dosyaları taramayı tercih ediyoruz. Mevcut bir fonksiyonu veya değişkeni yeniden keşfetmek yerine, var olanı kullanmak projemizi daha hafif tutacaktır.
*   **Diyalog Kur:** Eğer bir kaynağa ulaşamıyorsak veya projenin yapısında bir karmaşa hissediyorsak, "placeholder" yapılar kurmak yerine durup birbirimize danışmalı ve en doğru yolu birlikte seçmeliyiz.
*   **Dosya Boyutu ve Modülerlik:** Dosyalarımızın okunabilirliğini artırmak adına, 1000 satırı aşmaya başlayan dosyaları mantıklı alt modüllere bölmeyi bir standart olarak düşünebiliriz. Bu, hata ayıklama süreçlerimizi çok daha kolaylaştıracaktır.

---

## 3. FEYNMAN PRENSİBİ İLE ORTAK ANLAYIŞ

Birbirimize karmaşık sistemleri anlatırken jargona boğulmak yerine, herkesin anlayabileceği (ELI5) bir dil kullanmaya özen gösteriyoruz:

1.  **🎭 Nedir?:** En sade haliyle tanım.
2.  **⚙️ Nasıl Çalışır?:** Günlük hayattan bir metafor veya somut bir benzetme.
3.  **💎 Neden Gereklidir?:** Projeye kattığı spesifik değer.
4.  **🔥 Olmazsa Ne Olur?:** Eksikliğinde yaşanacak senaryo.

---

## 4. İŞLEM GÜNLÜĞÜ VE KARAKTER STANDARTLARI

Yaptığımız her işlemi projenin ana dizinindeki `Yapilan_Islemler.txt` dosyasına kronolojik olarak eklemeliyiz.

*   **🌐 UTF-8 Standartı ve Terminal Yasağı:** Emojilerin ve Türkçe karakterlerin her zaman canlı ve okunabilir kalması için, günlük dosyasına ekleme yaparken **KESİNLİKLE PowerShell/terminal komutları (`Add-Content`, `echo` vb.) KULLANILMAMALIDIR.** (Dosya kilitlenmesi veya karakter bozulması yaşatır.) Bunun yerine daima Python okuma/yazma blokları (örn: `with open(..., encoding='utf-8')`) veya AI yerleşik metin değiştirme araçları kullanılmalıdır.
*   **Kayıt Yapısı:** Kayıtlarımızı her zaman dosyanın sonuna eklemeli ve şu estetik formatı korumalıyız:
    ```text
    =========================================
    🕒 Tarih/Saat: [GG.AA.YYYY - SS:DD]
    ⚠️ Sorun/İhtiyaç: [Kısa açıklama]
    🎯 İşlem Özeti: [Yapılan işin özü]
    📁 Etkilenen Kapsam: [Dosyalar ve Dokümanlar]
    🔄 Geri Dönüş: [Git veya Manuel adımlar]
    =========================================
    ```

---

## 5. "SNAPSHOT" ARŞİVLEME VE COMMIT KÜLTÜRÜ

Projemizin her aşamasını Git geçmişine birer "anlık görüntü" (snapshot) olarak mühürlemeyi seviyoruz:

*   **Tam Kapsamlı Kayıt:** Commit atmadan önce `git add .` yaparak projenin o anki tam durumunu pakete dahil etmeye özen göstermeliyiz.
*   **Profesyonel Dil:** Commit mesajlarımızı tamamen Türkçe, ancak dünya standartlarında (Conventional Commits) yazmalıyız.
    *   *Format:* `<tip>(<kapsam>): <açıklama>` (Örn: `feat(database): Kullanıcı tablosuna yaş alanı eklendi`)
*   **Son Kontrol:** "Şu an stage'lenmemiş tek bir detay bile kaldı mı?" sorusunu kendimize sormamız, tertemiz bir geçmiş yönetimi sağlayacaktır.

---

## 6. ESTETİK VE PROJE PERSONASI

*   **Arayüz Uyumu:** Uyguladığımız tüm görsel değişikliklerde projenin mevcut estetik diline, renk paletine ve kullanıcı deneyimi (UX) tercihlerine sadık kalmalıyız.
*   **Dil ve Üslup:** Proje içindeki tüm mesajlarda ve kullanıcı etkileşimlerinde, projemizin kimliğini yansıtan profesyonel ve tutarlı bir dil inşa etmeliyiz.

---