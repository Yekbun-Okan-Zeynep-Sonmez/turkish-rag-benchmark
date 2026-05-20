import os
import glob
import time
import json
import logging
import fitz  # PyMuPDF
import google.generativeai as genai
from pydantic import BaseModel
from typing import List

# Loglama ayarları
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# API Anahtarı kontrolü
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("UYARI: 'GEMINI_API_KEY' ortam değişkeni bulunamadı. Lütfen ayarlayın.")
    logging.warning("GEMINI_API_KEY bulunamadı.")
    
genai.configure(api_key=API_KEY)

# Pydantic şemaları (Yapılandırılmış çıktı için)
class QAPair(BaseModel):
    soru: str
    cevap: str
    zorluk_seviyesi: str

class ArticleQA(BaseModel):
    qa_listesi: list[QAPair]

def extract_text_from_pdf(pdf_path, max_chars=40000):
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            # Sayfadaki blokları okuyup koordinatlara göre sıralıyoruz
            blocks = page.get_text("blocks")
            # Blokları y koordinatına göre (yukarıdan aşağıya), ardından x koordinatına göre (soldan sağa) sıralayalım
            blocks.sort(key=lambda b: (b[1], b[0]))
            for block in blocks:
                if block[6] == 0:  # Sadece metin bloklarını (tip 0) alıyoruz
                    full_text += block[4] + "\n"
        
        # Uzunluk sınırlaması (Token limitini aşmamak için)
        return full_text[:max_chars]
    except Exception as e:
        logging.error(f"PDF okuma hatasi ({pdf_path}): {e}")
        return None

def generate_qa_pairs(text):
    try:
        # Seçili modele göre ayar (Gemini Flash)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = (
            "Aşağıdaki akademik metni okuyarak, metnin içeriğine dayalı tam olarak 10 adet "
            "Türkçe soru-cevap çifti üret.\n\n"
            "Soruların zorluk seviyesi dağılımı şu şekilde olmalıdır:\n"
            "- 3 adet Kolay (Temel tanımlar ve doğrudan metinde geçen bilgiler)\n"
            "- 4 adet Orta (Çıkarım yapmayı gerektiren, bağlantı kurmaya yönelik sorular)\n"
            "- 3 adet Zor (Derin analiz gerektiren, metnin ana fikrini veya karmaşık bir bulguyu irdeleyen sorular)\n\n"
            "Çıktıyı 'zorluk_seviyesi' (Kolay, Orta, Zor), 'soru' ve 'cevap' alanlarına sahip "
            "bir JSON nesnesi olarak ver.\n\n"
            f"Metin:\n{text}"
        )

        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=ArticleQA
            )
        )
        
        # API'nin döndürdüğü JSON'u parse edelim
        result = json.loads(response.text)
        return result.get('qa_listesi', [])
    except Exception as e:
        logging.error(f"API hatasi: {e}")
        return None

def main():
    folder_path = "."
    # PDF dosyalarını isme göre sıralı alıp ilk 50'sini seçiyoruz
    pdf_files = sorted(glob.glob(os.path.join(folder_path, "*.pdf")))[:50]
    
    if not pdf_files:
        print("Klasörde PDF dosyası bulunamadı.")
        return

    dataset = []

    for i, pdf_path in enumerate(pdf_files):
        filename_with_ext = os.path.basename(pdf_path)
        # Uzantısız dosya adı (ör. MF01)
        makale_adi = os.path.splitext(filename_with_ext)[0]
        
        print(f"[{i+1}/{len(pdf_files)}] İşleniyor: {makale_adi}")
        logging.info(f"İşleniyor: {makale_adi}")

        context = extract_text_from_pdf(pdf_path)
        
        if not context:
            print(f"  -> {makale_adi} atlandı (Metin okunamadı).")
            continue
            
        qa_list = generate_qa_pairs(context)
        
        if qa_list:
            dataset.append({
                "makale_adi": makale_adi,
                "qa_listesi": qa_list
            })
            print(f"  -> Başarılı: 10 soru-cevap üretildi.")
            logging.info(f"Başarılı: {makale_adi} için sorular üretildi.")
        else:
            print(f"  -> {makale_adi} atlandı (API sorunu).")
            
        # İstek sınırlarına takılmamak için bekleme süresi
        time.sleep(12)

    # Verisetini kaydetme
    output_file = "dataset_matematik_fen.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
        print(f"\nİşlem tamamlandı! Toplam {len(dataset)} makale için veri üretildi ve '{output_file}' dosyasına kaydedildi.")
        logging.info("Tüm işlem tamamlandı ve kaydedildi.")
    except Exception as e:
        print(f"Dosya kaydetme hatası: {e}")
        logging.error(f"Dosya kaydetme hatasi: {e}")

if __name__ == "__main__":
    main()
