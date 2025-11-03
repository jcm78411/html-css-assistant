import math
import flet as ft
import asyncio
import requests
import json
import os
import re
import random
from dotenv import load_dotenv
import nltk
from nltk.tokenize import word_tokenize

# Descargar recursos de NLTK (necesario para tokenización)
nltk.download("punkt_tab")
nltk.download("punkt")

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY")
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# -------------------------------------------
# Función para consultar el modelo en OpenRouter
# -------------------------------------------

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

    except Exception as e:
        print("❌ Error en la API:", e)
        return "Hubo un problema al conectar con el modelo. Intenta nuevamente."


# -------------------------------------------
# Función principal de lógica del chat
# -------------------------------------------
def responder(pregunta):
    texto = pregunta.lower()
    tokens = word_tokenize(texto)

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
    if any(p in texto for p in saludos):
        return "👋 ¡Hola! Soy un asistente especializado en HTML y CSS. ¿En qué puedo ayudarte?"
    elif any(p in tokens for p in temas_html_css):
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

# -------------------------------------------
# Interfaz Flet
# -------------------------------------------
def main(page: ft.Page):
    page.title = "Asistente HTML & CSS"
    # page.window.width = 620
    # page.window.height = 700
    page.window.center()
    page.update()

    chat_display = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=True)

    user_input = ft.TextField(label="Mensaje", expand=True, autofocus=True, width=350)
    send_btn = ft.ElevatedButton("Enviar", icon=ft.Icons.SEND)
    clear_btn = ft.ElevatedButton("Limpiar", icon=ft.Icons.DELETE)

    # 🌀 Overlay con spinner mientras se genera respuesta
    overlay = ft.Container(
        visible=False,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK87),
        alignment=ft.alignment.center,
        content=ft.Column(
            [
                ft.ProgressRing(width=50, height=50, stroke_width=5),
                ft.Text("Pensando...", color=ft.Colors.WHITE, size=18, weight="bold"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
    )

    def add_message(text, is_user=True):
        """Agrega un mensaje con estilo tipo WhatsApp (burbujas asimétricas y soporte Markdown)."""
        if is_user:
            bubble_color = ft.Colors.LIGHT_BLUE_100
            alignment = ft.MainAxisAlignment.END
            border = ft.border_radius.only(
                top_left=15, top_right=15, bottom_left=15, bottom_right=0
            )
            content = ft.Text(
                text,
                color=ft.Colors.BLACK,
                selectable=True,
                size=14,
            )
        else:
            bubble_color = ft.Colors.BLACK12
            alignment = ft.MainAxisAlignment.START
            border = ft.border_radius.only(
                top_left=15, top_right=15, bottom_left=0, bottom_right=15
            )
            # 🧠 Mostrar respuesta de la IA con formato Markdown
            content = ft.Markdown(
                text,
                selectable=True,
                extension_set="gitHubWeb",  # admite tablas, listas, código, etc.
                code_theme="atom-one-dark",  # bonito estilo para bloques de código
                auto_follow_links=True,
                on_tap_link=lambda e: page.launch_url(e.data),
            )

        chat_display.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=content,
                        bgcolor=bubble_color,
                        padding=10,
                        border_radius=border,
                        margin=ft.margin.only(left=5, right=5),
                        width=400,
                        shadow=ft.BoxShadow(blur_radius=2, spread_radius=0.5),
                        expand=True
                    )
                ],
                alignment=alignment,
            )
        )
        chat_display.update()


    async def send_message(e):
        text = user_input.value.strip()
        if not text:
            return

        # Mensaje del usuario
        add_message(text, is_user=True)
        user_input.value = ""
        overlay.visible = True
        page.update()

        # Llamada a la IA en segundo plano
        respuesta_ia = await asyncio.to_thread(responder, text)

        add_message(respuesta_ia, is_user=False)
        overlay.visible = False
        page.update()

    def clear_chat(e):
        chat_display.controls.clear()
        page.update()

    # Eventos
    send_btn.on_click = send_message
    clear_btn.on_click = clear_chat
    user_input.on_submit = send_message

    # Estructura visual
    main_content = ft.Column(
        [
            ft.Text("🤖 Asistente HTML & CSS", size=22, weight="bold", text_align="center"),
            ft.Container(
                chat_display,
                height=450,
                # width=500,
                bgcolor=ft.Colors.GREY_100,
                border_radius=10,
                padding=10,
            ),
            ft.Row([user_input, ft.Column([send_btn, clear_btn])], alignment=ft.MainAxisAlignment.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(ft.Stack([main_content, overlay]))

# 🔹 Iniciar app
if __name__ == "__main__":
    port = int(os.environ.get("FLET_PORT", ""))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
    # ft.app(target=main)

