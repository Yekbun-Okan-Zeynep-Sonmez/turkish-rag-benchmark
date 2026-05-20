import json, os, time
from google import genai

API_KEY = "AIzaSyAJz3ZhNQgTCnf6jCmD7T5Vsku-37u6CJE"
client = genai.Client(api_key=API_KEY)

with open("_texts_clean.json", encoding="utf-8") as f:
    texts = json.load(f)

output_file = "dataset_matematik_fen.json"
if os.path.exists(output_file):
    with open(output_file, encoding="utf-8") as f:
        try:
            dataset = json.load(f)
        except Exception:
            dataset = []
else:
    dataset = []

done_articles = {entry["makale_adi"] for entry in dataset}
print(f"Zaten tamamlanan: {sorted(done_articles)}")

articles = sorted(texts.keys())

for article_name in articles:
    if article_name in done_articles:
        print(f"[ATLANDI] {article_name}")
        continue

    text = texts[article_name][:40000]
    print(f"[ISLENIYOR] {article_name} ...", flush=True)

    prompt = f"""Asagidaki akademik makale metnini oku ve tam olarak 10 adet TURKCE soru-cevap cifti uret.

ZORUNLU FORMAT - Sadece JSON dizisi dondur, baska hicbir sey yazma:
[
  {{"soru": "Soru metni burada", "cevap": "Cevap metni burada", "zorluk": "kolay"}},
  ...
]

ZORLUK DAGILIMU (kesinlikle uy):
- 3 adet "kolay" (tanimlar, temel kavramlar)
- 4 adet "orta" (cikarim, yontem karsilastirma)
- 3 adet "zor" (derin analiz, elestiri, sentez)

KURALLAR:
- Tum soru ve cevaplar TURKCE olmali
- Her cevap en az 2-3 cumle olmali
- Sadece JSON, baska hicbir sey yazma

MAKALE ADI: {article_name}
MAKALE METNI:
{text}"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt
        )
        raw = response.text.strip()

        # JSON temizle
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        qa_list = json.loads(raw)

        entry = {
            "makale_adi": article_name,
            "soru_cevap_ciftleri": []
        }
        for i, qa in enumerate(qa_list[:10]):
            entry["soru_cevap_ciftleri"].append({
                "id": i + 1,
                "soru": qa.get("soru", ""),
                "cevap": qa.get("cevap", ""),
                "zorluk": qa.get("zorluk", "orta")
            })

        dataset.append(entry)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)

        print(f"  [OK] {len(entry['soru_cevap_ciftleri'])} soru kaydedildi. Toplam: {len(dataset)}/50", flush=True)
        print(f"  65 saniye bekleniyor...", flush=True)
        time.sleep(65)

    except Exception as e:
        print(f"  [HATA] {article_name}: {e}", flush=True)
        time.sleep(30)
        continue

total_qa = sum(len(e["soru_cevap_ciftleri"]) for e in dataset)
print(f"\n=== TAMAMLANDI === {len(dataset)} makale, {total_qa} soru-cevap cifti.")
