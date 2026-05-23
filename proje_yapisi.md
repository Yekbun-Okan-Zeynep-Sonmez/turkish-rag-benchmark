Turkish-RAG-Benchmark/
├── data/
│   ├── raw/                    # Orijinal PDF'ler 
│   │   ├── tip
│   │   ├── ml-ai
│   │   ├── sosyal_toplum_bilimleri
│   │   ├── sosyal_bilimler
│   │   └──fizik_matematik
│   ├── processed/              # Metin dönüşüm aşamaları
│   │   ├── stage1_extracted/   # Temizlenmemiş ham md dosyaları
│   │   └── stage2_cleaned/     # Regex ve temizlikten geçmiş md'ler
│   └── benchmark/              # Test seti (Soru-Cevap İkilileri)
├── notebooks/                  # Notebooklar
├── results/                    # Çıktılar ve Analizler
│   ├── figures/                # Grafikler
│   └── tables/                 # Performans karşılaştırma tabloları (CSV)
└── README.md                   # Proje açıklaması