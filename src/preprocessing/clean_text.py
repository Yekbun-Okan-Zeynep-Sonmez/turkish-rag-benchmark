import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
STAGE2_DIR = BASE_DIR / "data" / "processed" / "stage2_cleaned"


def reflow_text(text: str, line_width: int = 80) -> str:
    lines = text.splitlines()
    paragraphs = []
    current = []

    for line in lines:
        stripped = line.strip()

        # ##SECTION## etiketi → paragrafı kapat, etiketi olduğu gibi bırak
        if stripped.startswith("##SECTION##"):
            if current:
                paragraphs.append(("text", ' '.join(current)))
                current = []
            paragraphs.append(("section", stripped))
            continue

        # Boş satır → paragraf sonu
        if not stripped:
            if current:
                paragraphs.append(("text", ' '.join(current)))
                current = []
            continue

        # Tire birleştirme: "kulla-" + "nılmıştır" → "kullanılmıştır"
        if current and current[-1].endswith('-'):
            current[-1] = current[-1][:-1] + stripped
        else:
            current.append(stripped)

    if current:
        paragraphs.append(("text", ' '.join(current)))

    # Her paragrafı 80 karakterde satırlara böl
    result = []
    for kind, p in paragraphs:
        if kind == "section":
            result.append(p)
            continue

        words = p.split()
        line = ""
        for word in words:
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= line_width:
                line += ' ' + word
            else:
                result.append(line)
                line = word
        if line:
            result.append(line)

        result.append("")  # paragraf arası boş satır

    final = '\n'.join(result)
    final = re.sub(r'\n{3,}', '\n\n', final)
    return final.strip()


def process_all():
    if not STAGE2_DIR.exists():
        print(f"❌ Klasör bulunamadı: {STAGE2_DIR}")
        return

    txt_files = list(STAGE2_DIR.rglob("*.txt"))

    if not txt_files:
        print(f"⚠️  Hiç .txt dosyası bulunamadı: {STAGE2_DIR}")
        return

    print(f"📁 {len(txt_files)} dosya bulundu\n")

    for txt_path in txt_files:
        try:
            original = txt_path.read_text(encoding="utf-8")
            cleaned = reflow_text(original, line_width=80)
            txt_path.write_text(cleaned, encoding="utf-8")

            original_lines = len(original.splitlines())
            cleaned_lines = len(cleaned.splitlines())

            print(f"✅ {txt_path.relative_to(BASE_DIR)}")
            print(f"   {original_lines} satır → {cleaned_lines} satır\n")

        except Exception as e:
            print(f"❌ {txt_path.name} — HATA: {e}\n")

    print("🎉 Tamamlandı.")


if __name__ == "__main__":
    process_all()