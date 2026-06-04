# NoireConverter Mimari Dokümantasyonu

## 🎭 Nedir?
NoireConverter, kullanıcıların görsel, işitsel, video ve metin dosyalarını kolayca ve hızlıca çeşitli formatlar arasında dönüştürmesini, boyutlandırmasını ve optimize etmesini sağlayan hepsi bir arada bir medya modifikasyon aracıdır.

## ⚙️ Nasıl Çalışır?
Python tabanlı bir "orkestra şefi" gibi çalışır. `customtkinter` üzerinden sağlanan görsel kullanıcı arayüzü sayesinde kullanıcı komutlarını alır. Arka planda ise `ffmpeg` gibi endüstri standardı araçları veya çeviri/okuma API'lerini nesne tabanlı yapılarla asenkron veya thread'ler üzerinden çalıştırır. Yeni modüler yapısıyla sistem şu parçalara ayrılır:
- **`core/`**: Uygulamanın beyni. Sabitler (`config.py`), dış sisteme erişim araçları (`utils.py`) ve toplu dosya operasyonları (`file_ops.py`).
- **`ui/`**: Uygulamanın yüzü. Ana pencere (`app.py`) ve görsel bileşenler (`crop_editor.py` vb.).
- **Dış Araçlar & İş Mantığı**: Format dönüşüm işlemleri (DND arayüzü ile) dış bağımlılıklara (ffmpeg vb.) dağıtılır.

## 💎 Neden Gereklidir?
Gündelik, tekrar eden teknik işler (video kırpma, resim boyutlandırma, Word'den PDF yapma, belge içi metin değiştirme, çeviri, dosya toplama vb.) için farklı programlar kullanma ihtiyacını ortadan kaldırır. Geliştirici bağlamında; 1000+ satırlık, tüm sorumlulukları üstlenen monolitik bir dosya yerine modüler bir yapı kullanmak, projenin büyümesini, hata takibini ve takım çalışmasını mümkün kılar.

## 🔥 Olmazsa Ne Olur?
Eğer bu modüler mimari olmazsa geliştirici ekibi 1700+ satırlık kod yığını içinde yeni bir özellik eklemeye çalışırken kırılmalara yol açabilir. Proje büyüdükçe sürdürülebilirliği kaybolur ve hata ayıklama imkansız hale gelir. Son kullanıcı perspektifinde ise her özellik için dağınık farklı yazılımlar kullanma eziyeti devam eder.
