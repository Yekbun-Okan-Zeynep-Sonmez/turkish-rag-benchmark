Turkish-RAG-Benchmark/
├── data/
│   ├── raw/                    # Orijinal PDF'ler 
│   │   ├── tip
│   │   ├── ml-ai
│   │   ├── sosyal_toplum_bilimleri
│   │   ├── sosyal_bilimler
│   │   └──fizik_matematik
│   ├── processed/              # Metin dönüşüm aşamaları
│   │   ├── stage1_extracted/   # Temizlenmemiş ham txt dosyaları
│   │   └── stage2_cleaned/     # Regex ve temizlikten geçmiş md'ler
│   └── benchmark/              # Test seti (Altın veri)
│       └── ground_truth.json   # Soru-Cevap-Context üçlüleri
├── notebooks/                  # 
├── results/                    # Çıktılar ve Analizler
│   ├── figures/                # Makale için grafikler
│   └── tables/                 # Performans karşılaştırma tabloları (CSV)
└── README.md                   # Proje açıklaması ve çalıştırma rehberi