import json

# Archivos de entrada/salida
INPUT_JSON = "html_css_nombres.json"
OUTPUT_JSON = "html_css_nombres_combinado.json"

# Lista de temas adicionales
temas_html_css = [
    # HTML elementos básicos
    "html", "head", "body", "title", "meta", "link", "script", "style",
    "div", "span", "p", "h1", "h2", "h3", "h4", "h5", "h6",
    "a", "img", "ul", "ol", "li", "table", "tr", "td", "th",
    "form", "input", "button",
    # Atributos comunes
    "class", "id", "href", "src", "alt", "type", "value", "placeholder",
    # CSS propiedades
    "css", "style", "margin", "padding", "border", "width", "height",
    "color", "background", "font-size", "font-family", "text-align",
    "display", "position", "float", "flex", "grid", "box-sizing",
    # CSS valores y conceptos
    "absolute", "relative", "fixed", "static", "block", "inline",
    "flex-box", "grid", "responsive", "media query", "selector",
    "px", "em", "rem", "vh", "vw", "rgb", "rgba", "hexadecimal",
    # Términos generales
    "etiqueta", "propiedad", "valor", "elemento", "contenedor", "layout",
    "diseño", "maquetación", "responsive design", "framework",
    "bootstrap", "tailwind", "flexbox", "grid layout", "box model",
    "modelo de caja", "inspeccionar", "devtools", "inspector",
    "webkit", "moz", "compatibilidad", "web", "navegador", "html5",
    "css3", "pagina web", "sitio web", "webpage", "website",
    "pagina", "sitio", "página"
]

def merge_and_clean():
    # Cargar nombres originales
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        nombres = json.load(f)

    print(f"📥 Cargados {len(nombres)} nombres desde {INPUT_JSON}")

    # Unir listas
    combinado = nombres + temas_html_css

    # Normalizar y eliminar duplicados (minúsculas + orden alfabético)
    limpio = sorted(set(item.strip().lower() for item in combinado if item.strip()))

    # Guardar resultado
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(limpio, f, ensure_ascii=False, indent=2)

    print(f"✅ Guardado {OUTPUT_JSON} con {len(limpio)} términos únicos.")

if __name__ == "__main__":
    merge_and_clean()
