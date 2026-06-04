import os
from pathlib import Path
import shutil

def collect_files(source_dir: str, target_dir: str, extensions: list | None = None, recursive: bool = True, callback=None) -> tuple:
    """
    Kaynak klasördeki belirli uzantılardaki dosyaları hedef klasöre kopyalar.
    
    Args:
        source_dir: Aranacak ana klasör yolu
        target_dir: Dosyaların kopyalanacağı klasör yolu
        extensions: Aranacak uzantılar listesi, örn: ['.txt', '.jpg']. None ise tüm dosyalar (.txt default değil, UI'dan gelir)
        recursive: True ise alt klasörlere de bakar
        callback: Her kopyalama işleminden sonra çağrılır. fn(dosya_adi, basarili_mi)
        
    Returns:
        tuple(basarili_islem_sayisi, hata_listesi)
    """
    if not source_dir or not target_dir:
        return 0, ["Kaynak veya hedef klasör belirtilmedi."]
        
    kaynak_yol = Path(source_dir)
    hedef_yol = Path(target_dir)
    
    if not kaynak_yol.exists():
        return 0, [f"Kaynak klasör bulunamadı: {source_dir}"]
        
    # Hedef klasör yoksa oluştur
    if not hedef_yol.exists():
        try:
            hedef_yol.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return 0, [f"Hedef klasör oluşturulamadı: {e}"]

    # Arama patternini belirle
    search_pattern = "*" 
    
    dosya_listesi = []
    if recursive:
        # Önce tüm dosyaları al, sonra filtrele
        all_files = kaynak_yol.rglob(search_pattern)
    else:
        all_files = kaynak_yol.glob(search_pattern)
        
    for f in all_files:
        if f.is_file():
            # Uzantı filtresi varsa uygula
            if extensions:
                if f.suffix.lower() in extensions:
                    dosya_listesi.append(f)
            else:
                dosya_listesi.append(f)

    if not dosya_listesi:
        return 0, [] # Dosya bulunamadı ama hata değil

    basarili_islem = 0
    hatalar = []
    
    for dosya in dosya_listesi:
        hedef_dosya = hedef_yol / dosya.name
        
        # Eğer hedefte aynı isimde dosya varsa ismini değiştir (çakışmayı önle)
        sayac = 1
        orj_isim = hedef_dosya.stem
        uzanti = hedef_dosya.suffix
        while hedef_dosya.exists():
            hedef_dosya = hedef_yol / f"{orj_isim}_{sayac}{uzanti}"
            sayac += 1
            
        try:
            shutil.copy2(dosya, hedef_dosya)
            basarili_islem += 1
            if callback:
                callback(dosya.name, True)
        except Exception as e:
            hatalar.append(f"{dosya.name}: {e}")
            if callback:
                callback(dosya.name, False)

    return basarili_islem, hatalar


def prefix_rename(parent_dir: str, separator: str = "_", callback=None) -> tuple:
    """
    Ana klasörün altındaki alt klasörlerdeki dosyaların adına,
    içinde bulundukları alt klasörün adını prefix olarak ekler.
    
    Örn: parent_dir/AlbumA/sarki.mp3 -> parent_dir/AlbumA/AlbumA_sarki.mp3
    
    Args:
        parent_dir: İçinde alt klasörlerin bulunduğu ana klasör
        separator: Klasör adı ile dosya adı arasındaki ayırıcı
        callback: Her işlemde çağrılır. fn(eski_isim, yeni_isim, basarili_mi, is_skipped)
        
    Returns:
        tuple(basarili_sayi, atlanan_sayi, hata_listesi)
    """
    if not parent_dir:
        return 0, 0, ["Ana klasör belirtilmedi."]
        
    ana_klasor = Path(parent_dir)
    
    if not ana_klasor.exists() or not ana_klasor.is_dir():
        return 0, 0, [f"Geçerli bir ana klasör bulunamadı: {parent_dir}"]
        
    basarili = 0
    atlanan = 0
    hatalar = []
    
    # 1. Ana klasörün içindeki tüm alt klasörleri tek tek gez
    for alt_klasor in ana_klasor.iterdir():
        if alt_klasor.is_dir():
            
            # 2. Alt klasörün içindeki dosyaları bul
            for dosya in alt_klasor.iterdir():
                if dosya.is_file():
                    dosya_adi = dosya.name
                    klasor_adi = alt_klasor.name
                    beklenen_prefix = f"{klasor_adi}{separator}"
                    
                    # 3. Zaten adlandırılmışsa atla (idempotent)
                    if dosya_adi.startswith(beklenen_prefix):
                        atlanan += 1
                        if callback:
                            callback(dosya_adi, dosya_adi, True, True)
                        continue
                        
                    # 4. Başına klasör adını ekle
                    yeni_isim = f"{beklenen_prefix}{dosya_adi}"
                    yeni_yol = dosya.with_name(yeni_isim)
                    
                    # 5. Dosyanın adını olduğu yerde değiştir
                    try:
                        dosya.rename(yeni_yol)
                        basarili += 1
                        if callback:
                            callback(dosya_adi, yeni_isim, True, False)
                    except Exception as e:
                        hatalar.append(f"{dosya_adi}: {e}")
                        if callback:
                            callback(dosya_adi, yeni_isim, False, False)
                            
    return basarili, atlanan, hatalar
