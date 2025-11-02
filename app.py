import random
import gradio as gr
import requests
import json
import os
import re
from dotenv import load_dotenv
import nltk

nltk.download("punkt_tab")
nltk.download("punkt")
from nltk.tokenize import word_tokenize
import math


# Load environment variables
load_dotenv()
# --- Configuración inicial ---

API_KEY = os.getenv("API_KEY")
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"


def formato_prettier(contenido):
    """
    Envuelve el texto en un contenedor HTML con estilos visuales tipo Prettier.
    """
    contenido = contenido.replace("\n", "<br>")
    contenido = re.sub(
        r"```(.*?)```", r"<pre><code>\1</code></pre>", contenido, flags=re.S
    )
    html = f"""
    <div style="background-color:#1e1e2e;color:#e5e5e5;
                padding:1rem;border-radius:10px;
                font-family:'JetBrains Mono', monospace;
                font-size:15px;line-height:1.6;">
        {contenido}
    </div>
    """
    return html


# --- Función para consultar el modelo en OpenRouter ---


def estimate_tokens(text):
    """
    Estima el número de tokens de un texto.
    Aproximadamente: 1 token ≈ 4 caracteres en inglés/español.
    """
    return math.ceil(len(text) / 4)


def consultar_openrouter(prompt):
    """
    Envía la pregunta al modelo alojado en OpenRouter y devuelve la respuesta.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openrouter.ai",
        "X-Title": "Asistente HTML & CSS",
    }

    # --- cálculo dinámico de tokens ---
    prompt_tokens = estimate_tokens(prompt)
    max_model_tokens = 4096  # límite estimado del modelo (depende del modelo exacto)
    safety_margin = 500  # margen para evitar pasarse del límite
    max_tokens = max(256, min(max_model_tokens - prompt_tokens - safety_margin, 1500))

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente experto en HTML y CSS."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        message = data["choices"][0]["message"]["content"]

        # Detectar posibles cortes (opcional)
        if data.get("choices")[0].get("finish_reason") == "length":
            message += "\n\n⚠️ *La respuesta fue truncada por límite de tokens.*"

        return message
        # return formato_prettier(message)

    except Exception as e:
        print("❌ Error en la API:", e)
        return "Hubo un problema al conectar con el modelo. Intenta nuevamente."


# --- Lógica principal ---
def responder(pregunta):
    texto = pregunta.lower()

    # --- Detectar saludos ---
    saludos = [
        "hola",
        "buenas",
        "hey",
        "qué tal",
        "saludos",
        "buenos días",
        "buenas tardes",
        "buenas noches",
        "¿cómo estás?",
        "¿qué pasa?",
        "¿qué hay?",
        "saludos cordiales",
        "¿cómo va?",
        "¿qué tal estás?",
        "hola, ¿cómo te va?",
    ]

    # --- Palabras clave HTML/CSS ---
    temas_html_css = [
        # HTML elementos básicos
        "html",
        "head",
        "body",
        "title",
        "meta",
        "link",
        "script",
        "style",
        "div",
        "span",
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "a",
        "img",
        "ul",
        "ol",
        "li",
        "table",
        "tr",
        "td",
        "th",
        "form",
        "input",
        "button",
        # Atributos comunes
        "class",
        "id",
        "href",
        "src",
        "alt",
        "type",
        "value",
        "placeholder",
        # CSS propiedades
        "css",
        "style",
        "margin",
        "padding",
        "border",
        "width",
        "height",
        "color",
        "background",
        "font-size",
        "font-family",
        "text-align",
        "display",
        "position",
        "float",
        "flex",
        "grid",
        "box-sizing",
        # CSS valores y conceptos
        "absolute",
        "relative",
        "fixed",
        "static",
        "block",
        "inline",
        "flex-box",
        "grid",
        "responsive",
        "media query",
        "selector",
        "px",
        "em",
        "rem",
        "vh",
        "vw",
        "rgb",
        "rgba",
        "hexadecimal",
        # Términos generales
        "etiqueta",
        "propiedad",
        "valor",
        "elemento",
        "contenedor",
        "layout",
        "diseño",
        "maquetación",
        "responsive design",
        "framework",
        "bootstrap",
        "tailwind",
        "flexbox",
        "grid layout",
        "box model",
        "modelo de caja",
        "inspeccionar",
        "devtools",
        "inspector",
        "webkit",
        "moz",
        "compatibilidad",
        "web",
        "navegador",
        "html5",
        "css3",
        "pagina web",
        "sitio web",
        "webpage",
        "website",
        "pagina",
        "sitio",
        "página",
    ]

    tokens = word_tokenize(texto)
    # --- Lógica de filtrado ---
    if any(palabra in texto for palabra in saludos):
        return "👋 ¡Hola! Soy un asistente especializado en HTML y CSS. ¿En qué puedo ayudarte?"
    # elif any(re.search(rf"\b{re.escape(palabra)}\b", texto) for palabra in temas_html_css):
    elif any(palabra in tokens for palabra in temas_html_css):
        return consultar_openrouter(pregunta)
    else:
        respuestas = [
            "Lo siento, estoy capacitado solo para responder preguntas sobre HTML y CSS.",
            "No puedo ayudar con eso, solo respondo preguntas sobre HTML y CSS.",
            "Mis conocimientos se limitan a HTML y CSS, ¿puedes preguntar algo relacionado?",
            "Lo siento, pero solo puedo responder preguntas sobre HTML y CSS.",
            "No tengo información sobre eso, pero puedo ayudarte con HTML y CSS.",
            "Por favor, pregúntame algo sobre HTML o CSS.",
            "Mis respuestas están enfocadas en HTML y CSS, ¿tienes alguna pregunta sobre eso?",
            "No puedo ayudar con temas fuera de HTML y CSS.",
            "Estoy aquí para ayudarte con HTML y CSS, ¿qué necesitas saber?",
            "Lo siento, pero mi especialidad es HTML y CSS.",
            "No tengo conocimientos en ese tema, pero puedo responder preguntas sobre HTML y CSS.",
            "Por favor, formula una pregunta relacionada con HTML o CSS.",
            "Mis capacidades están limitadas a HTML y CSS, ¿puedes preguntar algo en esa área?",
            "No puedo proporcionar información sobre eso, pero puedo ayudarte con HTML y CSS.",
            "Estoy diseñado para responder preguntas sobre HTML y CSS, ¿qué necesitas?",
            "Lo siento, pero solo puedo ofrecer asistencia en HTML y CSS.",
        ]
        return random.choice(respuestas)


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", ""))  # Render asigna el puerto automáticamente
    gr.Interface(
        fn=responder,
        inputs=gr.Textbox(
            label="💬 Escribe tu pregunta sobre HTML o CSS",
            placeholder="Ejemplo: ¿Cómo centro un div horizontalmente?",
            lines=10,  # altura del cuadro
            max_lines=10,  # máximo si el texto crece
        ),
        outputs=gr.Markdown(
            label="🧠 Respuesta del asistente",
            min_height=267,
            max_height=415,
            elem_id="output-markdown",
        ),
        title="Asistente HTML & CSS — OpenRouter",
        description="Un chatbot especializado en HTML y CSS, potenciado por LLaMA 3.3.",
    ).launch(server_name="0.0.0.0", server_port=port, share=True)
