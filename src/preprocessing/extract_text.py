import os
import fitz  # PyMuPDF
import pandas as pd

def extract_text():

    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    
    # Tam yolları tanımlıyoruz
    raw_dir = os.path.join(project_root, "data", "raw")
    output_dir = os.path.join(project_root, "data", "processed", "stage1_extracted")
    
    categories = ["egitim", "hukuk", "matematik-fizik", "ml-ai", "sosyal_bilimler", "tip"]
    metadata = []

    print(f"Proje Kök Dizini: {project_root}")
    print("Metin çıkarım süreci başlatılıyor...")

    for category in categories:
        input_path = os.path.join(raw_dir, category)
        category_output_path = os.path.join(output_dir, category)
        
        os.makedirs(category_output_path, exist_ok=True)
        
        if not os.path.exists(input_path):
            print(f"Uyarı: {input_path} dizini bulunamadı, atlanıyor.")
            continue
            
        print(f"İşleniyor -> {category}")
        
        for filename in os.listdir(input_path):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(input_path, filename)
                
                # Uzantıyı .pdf'den .txt'ye çevir
                txt_filename = filename[:-4] + ".txt"
                txt_path = os.path.join(category_output_path, txt_filename)
                
                try:
                    doc = fitz.open(pdf_path)
                    full_text = ""
                    for page in doc:
                        full_text += page.get_text()
                    
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(full_text)
                        
                    # Metadata için proje içi bağıl yolları (relative path) kaydet
                    metadata.append({
                        "kategori": category,
                        "orijinal_pdf_yolu": os.path.relpath(pdf_path, project_root),
                        "hedef_txt_yolu": os.path.relpath(txt_path, project_root),
                        "sayfa_sayisi": len(doc),
                        "karakter_sayisi": len(full_text)
                    })
                    doc.close()
                except Exception as e:
                    print(f"Hata oluştu ({filename}): {str(e)}")
    
    # Metadata dosyasını data/raw/metadata.csv olarak kaydet
    if metadata:
        df = pd.DataFrame(metadata)
        metadata_file = os.path.join(raw_dir, "metadata.csv")
        df.to_csv(metadata_file, index=False, encoding="utf-8-sig", sep=";")
        print(f"\nİşlem başarıyla tamamlandı. Metadata şuraya kaydedildi: {metadata_file}")

if __name__ == "__main__":
    extract_text()