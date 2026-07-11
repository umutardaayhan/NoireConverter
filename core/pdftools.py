"""PDF araçları (pypdf): birleştirme, sayfalara bölme, aralık çıkarma."""

import os

from pypdf import PdfReader, PdfWriter


def merge_pdfs(paths, output_dir):
    """PDF'leri verilen sırayla tek dosyada birleştirir."""
    if len(paths) < 2:
        raise ValueError("Birleştirme için en az 2 PDF gerekir.")
    name = os.path.splitext(os.path.basename(paths[0]))[0]
    out = os.path.join(output_dir, f"{name}_birlesik.pdf")
    writer = PdfWriter()
    for p in paths:
        writer.append(p)
    with open(out, "wb") as f:
        writer.write(f)
    writer.close()
    return out


def split_pdf(path, output_dir):
    """Her sayfayı ayrı PDF olarak kaydeder; dosya yolu listesi döner."""
    reader = PdfReader(path)
    name = os.path.splitext(os.path.basename(path))[0]
    outs = []
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out = os.path.join(output_dir, f"{name}_s{i}.pdf")
        with open(out, "wb") as f:
            writer.write(f)
        outs.append(out)
    return outs


def extract_range(path, first, last, output_dir):
    """[first, last] sayfa aralığını (1 tabanlı, uçlar dahil) yeni PDF'e çıkarır."""
    reader = PdfReader(path)
    total = len(reader.pages)
    first, last = max(1, int(first)), min(int(last), total)
    if first > last:
        raise ValueError(f"Geçersiz sayfa aralığı (belge {total} sayfa).")
    name = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(output_dir, f"{name}_s{first}-{last}.pdf")
    writer = PdfWriter()
    for i in range(first - 1, last):
        writer.add_page(reader.pages[i])
    with open(out, "wb") as f:
        writer.write(f)
    return out
