Turkish-RAG-Benchmark/
├── data/
│   ├── raw/                    # Orijinal PDF'ler 
│   │   ├── hukuk/
│   │   ├── tip/
│   │   ├── ml_ai/
│   │   ├── felsefe/
│   │   └── tarih/
│   ├── processed/              # Metin dönüşüm aşamaları
│   │   ├── stage1_extracted/   # Temizlenmemiş ham txt dosyaları
│   │   ├── stage2_cleaned/     # Regex ve temizlikten geçmiş txt'ler
│   │   └── stage3_chunks/      # RAG için parçalanmış (chunked) json/csv
│   └── benchmark/              # Test seti (Altın veri)
│       └── ground_truth.json   # Soru-Cevap-Context üçlüleri
├── configs/                    # Deney parametreleri
│   ├── model_config.yaml       # Embedding ve LLM model isimleri
│   └── rag_params.json         # Chunk size, overlap, k-değeri
├── src/                        # Modüler kaynak kodlar
│   ├── preprocessing/          # PDF to Text ve Temizlik scriptleri
│   ├── indexing/               # Vektör veritabanı (Chroma/FAISS) işlemleri
│   ├── retrieval/              # Geri çağırma mantığı (BM25, Hybrid, Semantic)
│   ├── generation/             # LLM (Llama, Trendyol vb.) entegrasyonu
│   └── evaluation/             # Metriklerin (RAGAS, MRR, Hit Rate) hesabı
├── notebooks/                  # EDA ve hızlı denemeler (Jupyter)
├── results/                    # Çıktılar ve Analizler
│   ├── figures/                # Makale için grafikler
│   └── tables/                 # Performans karşılaştırma tabloları (CSV)
├── docs/                       # Literatür notları ve makale taslakları
├── requirements.txt            # Kütüphane listesi
└── README.md                   # Proje açıklaması ve çalıştırma rehberi