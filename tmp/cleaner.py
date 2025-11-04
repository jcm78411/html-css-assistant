import json
import re

INPUT_JSON = "tags_and_themes.json"   # o el que tengas
OUTPUT_JSON = "tags_and_themes_limpio.json"

def clean_angle_brackets():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"📥 Cargados {len(data)} nombres desde {INPUT_JSON}")

    cleaned = []
    for item in data:
        if not isinstance(item, str):
            continue
        # Eliminar los signos < > y espacios sobrantes
        limpio = re.sub(r"[<>]", "", item).strip()
        if limpio:
            cleaned.append(limpio.lower())

    # Eliminar duplicados y ordenar
    cleaned = sorted(set(cleaned))

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"✅ Guardado {OUTPUT_JSON} con {len(cleaned)} términos limpios.")

if __name__ == "__main__":
    clean_angle_brackets()
