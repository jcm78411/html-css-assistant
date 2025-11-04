import json

INPUT_JSON = "html_css_dataset.json"
OUTPUT_JSON_NAMES = "html_css_nombres.json"

def extract_names():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    nombres = [item["nombre"] for item in data if "nombre" in item]

    with open(OUTPUT_JSON_NAMES, "w", encoding="utf-8") as f:
        json.dump(nombres, f, ensure_ascii=False, indent=2)

    print(f"✅ Guardado {OUTPUT_JSON_NAMES} con {len(nombres)} nombres extraídos.")

if __name__ == "__main__":
    extract_names()
