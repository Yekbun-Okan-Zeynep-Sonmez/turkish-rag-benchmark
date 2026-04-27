import fitz  # PyMuPDF
import os
from pathlib import Path

def extract_all_pdfs_to_text(raw_dir, output_dir):
    # Hedef klasör yoksa oluştur
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(raw_dir):
        print(f"Hata: {raw_dir} klasörü bulunamadı!")
        return

    print(f"--- İşlem Başlatıldı: {raw_dir} içindeki PDF'ler dönüştürülüyor ---")
    
    count = 0
    for file_name in os.listdir(raw_dir):
        if file_name.lower().endswith(".pdf"):
            pdf_path = os.path.join(raw_dir, file_name)
            txt_file_name = Path(file_name).stem + ".txt"
            txt_output_path = os.path.join(output_dir, txt_file_name)
            
            try:
                doc = fitz.open(pdf_path)
                full_text = ""
                
                for page in doc:
                    full_text += page.get_text("text")
                
                with open(txt_output_path, "w", encoding="utf-8") as f:
                    f.write(full_text)
                
                print(f"Başarılı: {file_name} -> {txt_file_name}")
                doc.close()
                count += 1
                
            except Exception as e:
                print(f"Hata oluştu ({file_name}): {e}")
    
    print(f"--- İşlem Tamamlandı. Toplam {count} dosya aktarıldı. ---")

if __name__ == "__main__":
    # Proje kök dizinini baz alarak yolları belirle
    # Bu scriptin 'src/preprocessing' altında olduğunu varsayar
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
    
    RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
    STAGE1_DIR = os.path.join(BASE_DIR, "data", "processed", "stage1_extracted")
    
    extract_all_pdfs_to_text(RAW_DATA_DIR, STAGE1_DIR)