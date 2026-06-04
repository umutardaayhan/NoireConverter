# 🧬 NoireConverter Proje Anatomisi

## 🎭 Nedir?
**NoireConverter**, adeta dijital bir matbaa gibidir. Sizin verdiğiniz yazıları, resimleri, sesleri veya videoları alır; içerisindeki dönüştürücü motorlar (fonksiyonlar) sayesinde bunları bambaşka formatlara çevirip size geri sunan, son derece yetenekli ve tek bir pencereden yönetilen bir "hepsi bir arada" dönüştürücü asistanıdır.

---

## 🗺️ Klasör Haritası (Projenin Organları)

Projemizin içindeki dosyalar rastgele değil, tıpkı insan vücudundaki organlar gibi her birinin ayrı bir görevi olacak şekilde tasarlanmıştır:

*   **`/core` (Projenin Beyni):** Burası uygulamanın kararlar aldığı, kuralları belirlediği ve dış sistemlere (örneğin internete) bağlandığı yerdir. Arayüz (`ui`) bir iş yapılmasını istediğinde, o işin "nasıl" yapılacağını bu klasördeki dosyalar anlatır.
*   **`/ui` (Yüz ve Duyu Organları):** Kullanıcının gördüğü pencere, tıkladığı butonlar, sürükleyip bıraktığı alanlar tamamen buradadır. Projenin tenidir; kullanıcı ile sistemin iletişim kurmasını sağlar. Altındaki `/components` klasörü ise bu yüzün içindeki göz, kulak gibi spesifik parçaları (örneğin resim kırpma ekranını) barındırır.
*   **`/docs` (Projenin Hafızası):** Burası bizim pusulamızdır. Projenin mimarisinin, kural ve standartlarının yazılı olduğu yerdir. Geliştiriciler yeni bir şey eklemeden önce mutlaka bu hafızaya danışırlar.
*   **`/build` (Şantiye Alanı):** Kodların, son kullanıcı için bir "uygulamaya" dönüşürken geçici olarak kullanıldığı, inşaatın yapıldığı şantiye alanıdır. Müşteriler buraları görmez, bittikten sonra çıkan molozlar burada kalır.
*   **`/dist` (Vitrin):** Paketleme işlemi bittikten sonra, son kullanıcının çift tıklayıp çalıştıracağı hazır, paketlenmiş programın (exe vs.) konulduğu yerdir. Yani şantiyede yapılan binanın açılışa hazır halidir.

---

## ⚙️ Sistem Nasıl Çalışıyor? (Tiyatro Metaforu)

Bir dönüştürme işlemi başlattığınızda arka planda şu oyun sergilenir:

1.  **Seyirci Talebi:** İlk olarak seyirci (kullanıcı) `/ui` sahnesine gelir ve elindeki dosyayı sahneye bırakır (Sürükle-Bırak/Seçme).
2.  **Yönetmenin Harekete Geçmesi:** Sahnede duran buton, sahne arkasındaki yönetmene (`noire_converter.py` - Ana Şalter) haber verir.
3.  **Senaristin Devreye Girmesi:** Yönetmen, görevin nasıl yapılacağını bilen uzmanlara yani `/core` içerisindeki araçlara dosyayı iletir.
4.  **Oyunun Sergilenmesi:** `/core`, dışarıdan destek aldığı `ffmpeg` (bir nevi özel efekt ustası) veya diğer çeviri/işlem araçlarını görevlendirir. İşlem asenkron (arkaplanda, izleyiciyi sıkmadan) gerçekleştirilir.
5.  **Perdenin Kapanışı:** Dönüştürülen yepyeni dosya hazırlandığında, yönetmen sahneye (`/ui`) işlemin bittiğini fısıldar ve seyirciye "İşlem Tamam!" yazısı gösterilir.

---

## 🧱 Yapı Taşları (Kritik Dosyalar)

Sistemi ayakta tutan ana kolonlar şunlardır:

*   **`noire_converter.py`**: Motorun kontağıdır. Projeyi başlatan, ayarlamaları (Dark mode vs.) yapan ve arayüzü ekrana çizen ana şalterimizdir.
*   **`core/config.py` & `core/utils.py`**: Uygulamanın ezberlediği sabit ayarlar (renkler, fontlar vs.) ve işlemleri yaparken kullandığı pratik tornavida takımlarıdır.
*   **`ui/app.py`**: Uygulamanın ana ekranının çizildiği büyük tuvaldir. Tüm görsel bileşenler bu dosya üzerinde birleştirilir.
*   **`noire_converter.spec`**: Şantiye yönergesi! Kodların ve simgelerin (App.ico) nasıl paketlenip tek bir exe haline getirileceğini belirten talimatlar bütünüdür.
*   **`requirements.txt`**: Projemizin dışarıdan ihtiyaç duyduğu (yemek tarifi için gereken malzemeler gibi) Python kütüphanelerinin listelendiği malzeme faturasıdır.

---

## 💡 Geliştirici Notu (Önemli Uyarılar)

Bu projeye katkıda bulunacak bir geliştiricinin kulağına küpe olması gereken altın kurallar:
- 🚫 **Bütün sorumluluğu tek bir dosyaya yığma!** Projemiz modülerdir. Kullanıcı arayüzü ile işlem yapan kodları birbirine karıştırma. Görsel şeyler `/ui` içine, mantıksal işler `/core` veya uygun modüllere yazılmalıdır.
- 🚫 **Ana ipliği (Main Thread) tıkama!** Video dönüştürme, çeviri yapma gibi ağır işlemler kullanıcının ekranını dondurmasın diye mutlaka asenkron (arkaplan görevleri ile) yapılmalıdır.
- 💡 **Önce Okuyun!** `docs` klasörünü ve `Yapilan_Islemler.txt` günlüğünü okumadan kod değişikliklerine başlamayın. Mimariyi anlamak, kod yazmaktan daha değerlidir.
