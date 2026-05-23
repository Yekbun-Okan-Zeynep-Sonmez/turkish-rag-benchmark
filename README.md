# 🇹🇷 Turkish RAG Benchmark
> **Türkçe Akademik Metinler İçin RAG Benchmark Veri Seti ve Performans Değerlendirmesi**

[![LlamaIndex](https://img.shields.io/badge/Framework-LlamaIndex-red.svg?style=flat-square&logo=diagrams&logoColor=white)](https://www.llamaindex.ai/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![GPU Acceleration](https://img.shields.io/badge/GPU%20Acceleration-CUDA-green.svg?style=flat-square&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-zone)
[![IBM Docling](https://img.shields.io/badge/Parser-Docling-orange.svg?style=flat-square)](https://github.com/DS4SD/docling)

Bu proje, Türkçe akademik ve teknik dokümanlar üzerinde en doğru ve kararlı **RAG (Retrieval-Augmented Generation)** mimarisini bulmak amacıyla tasarlanmış uçtan uca bir benchmark çalışmasıdır. Proje kapsamında, ham akademik PDF dosyalarının yüksek doğrulukla metne dönüştürülmesinden,  LLM'ler ile sentetik test seti (Soru-Cevap) üretimine ve LlamaIndex kullanılarak farklı yerleştirme (embedding), bölümleme (chunking) ve geri getirme (retrieval) stratejilerinin GPU tabanlı performans testlerine kadar tüm süreçler analiz edilmiştir. Çalışmada kullanılan değerlendirme veri seti, **235 akademik makale** ve bu makalelerden üretilmiş **2132 doğrulanmış soru-cevap çiftinden** oluşmaktadır.


---

## 🎯 Projenin Amacı 


Bu projeyle, heterojen akademik disiplinlerden veriler derlenerek, **Türkçe RAG sistemleri için en ideal tasarım şablonunu (best practices) belirlemek** ve geliştiricilere somut metriklerle rehberlik etmek hedeflenmiştir.

---

## 🚀 İş Akışı 

Proje, birbirini takip eden **4 temel aşamadan** oluşmaktadır:


### 1. Veri Toplama (Raw Data Collection)
Farklı disiplinlerin terminolojik ve yapısal dinamiklerini yansıtmak amacıyla **5 ana akademik alandan** toplam **235 akademik makale** (PDF formatında) derlenmiştir:
*   🩺 **Tıp (Medicine):** Yoğun latince terimler ve karmaşık vaka analizleri.
*   💻 **ML-AI (Machine Learning):** İngilizce-Türkçe karışık teknik terimler, matematiksel formüller ve kod blokları.
*   ⚖️ **Sosyal Bilimler (Social Sciences):** Uzun paragraflar ve betimsel anlatım.
*   👥 **Sosyal Toplum Bilimleri (Social & Policy Sciences):** Mevzuatlar, anket verileri ve kurumsal dil.
*   📐 **Fizik-Matematik (Physics & Mathematics):** Formüller, semboller ve yoğun sayısal veri tabloları.

### 2. Doküman Dönüştürme (IBM Docling)
Ham PDF'lerin metne dönüştürülmesinde geleneksel araçlar yerine IBM Research tarafından geliştirilen **Docling (DocumentConverter)** kullanılmıştır. 
*   Docling, çok sütunlu sayfa tasarımlarını, görseller altındaki yazıları ve tabloları yapısal bütünlüğünü bozmadan **Markdown (MD)** formatına dönüştürmüştür.
*   Bu aşamada üretilen ham markdown dosyaları `data/processed/stage1_extracted/` dizininde saklanmıştır.

### 3. Metin Ön İşleme ve Temizleme (Text Cleaning)
Ham dönüştürme çıktısı üzerinde özel Regex filtreleri uygulanarak:
*   Tekrarlanan sayfa numaraları, başlık/dipnot bilgileri kaldırılmıştır.
*   Tablo formatları standardize edilmiş ve gereksiz boşluklar temizlenmiştir.
*   RAG sisteminin anlamsal arama başarımını doğrudan baltalayan "gürültü" veriler izole edilmiştir.
*   Temizlenmiş nihai MD dosyaları `data/processed/stage2_cleaned/` klasörüne aktarılmıştır.

### 4. Gelişmiş LLM'ler ile Sentetik Soru-Cevap Üretimi (QA Generation)
RAG değerlendirmesi için gereken yüksek kaliteli test kümesini oluşturmak amacıyla, temizlenen MD dosyaları kaynak gösterilerek gelişmiş LLM'ler kullanılmıştır:
*   **Kullanılan Modeller:** `Gemini 3.5 Flash (High)`, `Gemini 3.1 Pro (High)` ve `Claude Opus 4.6 (Thinking)`.
*   Her model, ilgili metin bölümlerinden (Özet, Giriş, Deneyler, Sonuç vb.) yola çıkarak **Soru-Cevap (QA) ve Kaynak Eşleşmesi (Ground Truth)** ikililerini türetmiştir.
*   Oluşturulan 5 farklı konu bazlı veri seti `data/benchmark/` altında toplanmış olup, toplamda **2132 soru-cevap çiftinden** oluşan zengin bir Türkçe benchmark veri seti elde edilmiştir.

---


## 📁 Proje Klasör Yapısı

```
turkish-rag-benchmark/
├── data/
│   ├── raw/                    # Orijinal ham PDF dosyaları (Tıp, ML-AI, Sosyal Bilimler vb.)
│   ├── processed/              # Metin dönüşüm aşamaları
│   │   ├── stage1_extracted/   # Docling çıktısı ham Markdown (.md) dosyaları
│   │   └── stage2_cleaned/     # Temizleme ve gürültüden arındırma sonrası Markdown (.md) dosyaları
│   └── benchmark/              # Sentetik Soru-Cevap test seti (JSON)
├── notebooks/                  # Deneysel Jupyter Notebook dosyaları
│   ├── extract_text.ipynb      # Docling ile PDF-to-MD dönüşüm betiği
│   └── rag-benchmarks.ipynb    # LlamaIndex ile RAG testleri ve analizleri
├── results/                    # Değerlendirme Çıktıları
│   ├── figures/                # Performans ve gelişim grafikleri (.png)
│   └── tables/                 # Sistem bazlı metrik sonuçları (.csv)
└── README.md                   # Proje ana tanıtım dökümanı (Bu dosya)
```

---

## ⚙️ RAG Konfigürasyonları ve Test Mimarisi

Değerlendirmeler **LlamaIndex** framework'ü üzerinde, GPU (CUDA) hızlandırmasıyla yapılmıştır. Test edilen **8 RAG konfigürasyonu** 3 bağımsız grupta karşılaştırılmıştır:

### 📊 Karşılaştırma Grupları

#### **Grup 1: Yerleştirme (Embedding) Modelleri**
*Sabit Koşul: Bölüm boyutu (Chunk Size) = 512, Örtüşme (Overlap) = 128.*
*   **RAG-1 (bge-m3):** `BAAI/bge-m3` (Çok dilli ve hibrit destekli güçlü yerleştirme modeli)
*   **RAG-2 (multilingual-e5-large):** `intfloat/multilingual-e5-large` (Arama görevlerinde lider çok dilli model)
*   **RAG-3 (paraphrase-multilingual-mpnet-base-v2):** `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (Hafif ve hızlı anlamsal benzerlik modeli)

#### **Grup 2: Bölümleme (Chunk) Stratejileri**
*Sabit Koşul: En iyi performansı veren Grup 1 modeli kullanılır.*
*   **RAG-4 (256/50):** Küçük parçalar halinde sabit boyutlu bölümleme (`SentenceSplitter`)
*   **RAG-5 (1024/200):** Geniş bağlamlı sabit boyutlu bölümleme (`SentenceSplitter`)
*   **RAG-6 (Header Based):** Markdown başlık yapılarını (`#`, `##`, `###`) temel alan anlamsal bölümleme (`MarkdownNodeParser`)

#### **Grup 3: Geri Getirme (Retrieval) Stratejileri**
*Sabit Koşul: En iyi performansı veren Grup 1 ve Grup 2 kombinasyonu temel alınır.*
*   **RAG-7 (BM25 Only):** Geleneksel kelime eşleştirmeli arama (`BM25Retriever`)
*   **RAG-8 (Hybrid: Vector + BM25):** Vektörel arama ile BM25'i birleştiren melez arama yapısı (`QueryFusionRetriever`)

---

## 🏆 Deneysel Sonuçlar ve Performans Metrikleri

Tüm modeller sorgu seviyesinde iki kritik metrik üzerinden test edilmiştir:
1.  **Hit Rate @ 5:** İlgili dökümanın, getirilen ilk 5 parça arasında yer alma olasılığı.
2.  **MRR @ 5 (Mean Reciprocal Rank):** İlgili dökümanın getirilme sırasının tersinin ortalaması.

### 📊 Performans Tablosu

| Grup | Konfigürasyon Kimliği (Sistem) | Yerleştirme Modeli / Strateji | MRR @ 5 | Hit Rate @ 5 |
| :--- | :--- | :--- | :---: | :---: |
| **Grup 1** | RAG-1 | BAAI/bge-m3 | 0.9155 | 0.9658 |
| **Grup 1** | **RAG-2 (Grup 1 Kazananı)** | **intfloat/multilingual-e5-large** | **0.9236** | **0.9733** |
| **Grup 1** | RAG-3 | paraphrase-multilingual-mpnet-base-v2 | 0.7319 | 0.8677 |
| **Grup 2** | **RAG-4 (Genel Şampiyon)** | **Chunk: 256 / Overlap: 50** | **0.9343** | **0.9756** |
| **Grup 2** | RAG-5 | Chunk: 1024 / Overlap: 200 | 0.9037 | 0.9639 |
| **Grup 2** | RAG-6 | Header Based (Markdown Node) | 0.8294 | 0.9264 |
| **Grup 3** | RAG-7 | BM25 Only | 0.9305 | 0.9719 |
| **Grup 3** | RAG-8 | Hybrid (Vector + BM25) | 0.9300 | 0.9719 |

### 📈 Grafiklerle Analiz

#### Modellerin Genel Performansı (Overall Performance)
![Modellerin Genel Performansı](results/figures/overall_performance.png)

#### Gruplar Arası Başarım Gelişimi (Progression by Groups)
![Grup Bazlı Gelişim Grafikleri](results/figures/progression_by_groups.png)

---

## 🧠 Temel Bulgular ve Mimari Tavsiyeler 

Bu benchmark çalışmasından elde edilen somut çıkarımlar ve Türkçe RAG projeleri için tasarım önerileri şunlardır:

1.  **Türkçe İçin En İyi Vektör Temsili:**
    *   `multilingual-e5-large` modeli, Türkçe akademik terimler ve anlamsal ilişkilerde en yüksek doğruluğu sunmuştur (**MRR: 0.9236**).
    *   `bge-m3` modeli de oldukça güçlü ve yakın bir performans göstermiştir. Ancak `paraphrase-multilingual` modeli Türkçe'nin karmaşık dil yapısında zayıf kalmış ve ciddi bir performans düşüşü yaşamıştır.

2.  **Bölümleme (Chunk Size) Altın Oranı:**
    *   **Küçük chunk boyutları (256/50)**, büyük chunk boyutlarına (1024/200) göre daha üstün performans sağlamıştır (**MRR: 0.9343** vs **0.9037**). Türkçe sondan eklemeli olduğu için daha dar ve odaklanmış anlamsal pencereler gürültüyü azaltmakta ve geri getirme doğruluğunu artırmaktadır.
    *   Başlık tabanlı anlamsal bölümleme (`MarkdownNodeParser`), hiyerarşiyi korumasına rağmen küçük sabit pencereli yaklaşıma göre daha düşük sonuç vermiştir. Bunun temel nedeni akademik makalelerdeki başlık altı metinlerin çok uzun olması ve tek bir node içine sığdırılırken anlamsal yoğunluğun seyrelmesidir.

3.  **Leksikal Arama (BM25) Algoritmasının Etkinliği:**
    *   Türkçe teknik ve akademik metin arama süreçlerinde geleneksel leksikal arama yöntemi olan **BM25**, salt semantik (vektörel) arama modelleriyle rekabet edebilir düzeyde son derece yüksek bir performans sergilemiştir (**MRR: 0.9305**). Türkçe dil yapısının sondan eklemeli doğası ve akademik terminolojinin morfolojik özellikleri, anahtar kelime eşleştirme tabanlı leksikal algoritmaların bilgi geri getirme süreçlerinde ayırt edici ve etkin kalmasını sağlamaktadır.
    *   Bu bulgu, Türkçe RAG sistem tasarımlarında leksikal ve semantik yaklaşımları entegre eden melez (Hybrid) geri getirme mimarilerinin tercih edilmesinin, sistemin kararlılığı ve erişim başarımı açısından en rasyonel yaklaşım olduğunu ortaya koymaktadır.

4.  **GPU Optimizasyonu:**
    *   Değerlendirme notebook'unda (`rag-benchmarks.ipynb`), sorguların GPU üzerinde **toplu olarak vektörleştirilmesini (Batch embedding)** sağlayan özel bir asenkron değerlendirici kurgulanmıştır. Bu yaklaşım, GPU bellek taşmalarını (OOM) önlemiş ve değerlendirme sürelerini
    hızlandırmıştır.
