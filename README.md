# 💬 TinyLlama HTML & CSS Assistant

Un asistente conversacional inteligente 🧠 especializado **única y exclusivamente en HTML y CSS**.  
Desarrollado con **Gradio** y potenciado por el modelo **TinyLlama-1.1B-Chat-v1.0**, este bot responde preguntas técnicas sobre maquetación, estilos, diseño web y conceptos fundamentales de frontend.  
Cuando recibe una pregunta fuera de ese ámbito, responde amablemente indicando que solo maneja temas de HTML y CSS. 🎯

---

## ✨ Características principales

✅ **Especialización en HTML y CSS**  
Responde con precisión sobre etiquetas, propiedades, estructuras, selectores y buenas prácticas.

🚫 **Filtro temático inteligente**  
Ignora preguntas fuera del tema y responde con mensajes predefinidos y naturales.

🧩 **Interfaz amigable con Gradio**  
Ofrece un entorno visual limpio y funcional, perfecto para probar el modelo desde el navegador.

⚙️ **Basado en Hugging Face Hub**  
Se conecta al modelo remoto de TinyLlama mediante la API de `huggingface_hub`.

---

## 🧠 Funcionamiento general

1. El usuario escribe una pregunta.  
2. El sistema analiza si contiene palabras clave de HTML o CSS.  
3. Si está relacionada ➜ se envía al modelo **TinyLlama-1.1B-Chat-v1.0**.  
4. Si no lo está ➜ responde con una frase predefinida como:  
   > “Lo siento, solo puedo responder preguntas sobre HTML y CSS.”  

---

## 🚀 Guía operativa

### 🪜 1. Clonar el proyecto
```bash
git clone [https://github.com/tuusuario/html-css-assistant.git](https://github.com/jcm78411/html-css-assistant.git)
cd html-css-assistant
```

### 📦 2. Instalar dependencias
Asegúrate de tener Python 3.9+ instalado, luego ejecuta:

```bash
pip install -r requirements.txt
```

### 🔑 3. Configurar tu token de Hugging Face

Crea un Access Token en https://huggingface.co/settings/tokens

Luego inicia sesión desde terminal:

```bash
huggingface-cli login
```

### 💻 4. Ejecutar la aplicación

```bash
python app.py
```

Se cargarán los tensores y otras bases. Despues aparecerá una URL local (ejemplo: http://127.0.0.1:7860) donde podrás usar tu asistente desde el navegador. 🌐

### 🧾 Estructura del proyecto
📂 html-css-assistant/
 ┣ 📜 app.py               # Código principal de la aplicación
 ┣ 📜 requirements.txt     # Librerías necesarias
 ┣ 📜 README.md            # Este archivo de documentación

### 🧑‍💻 Tecnologías utilizadas

- 🧱 Python 3.9+

- ⚡ Gradio

- 🤗 Hugging Face Hub

- 💬 TinyLlama-1.1B-Chat-v1.0

- 💡 Ejemplo de interacción

# Usuario:

- ¿Cómo centrar un div horizontalmente en CSS?

- Asistente:

- # Puedes centrar un div horizontalmente usando margin: 0 auto; siempre que tenga un ancho definido.
  # Ejemplo:

```bash
div {
  width: 300px;
  margin: 0 auto;
}
```

- # Usuario:

- ¿Cuál es la capital de Francia?

- Asistente:

- # Lo siento, estoy capacitado solo para responder preguntas sobre HTML y CSS.

🌟 Autor

Desarrollado por: [jcm78411]
📧 Contacto: [jcm78411@ejemplo.com]

🌍 Proyecto alojado en: [Hugging Face Space / GitHub]

### 🪄 Licencia

# Este proyecto se distribuye bajo la licencia MIT, por lo que puedes usarlo, modificarlo o adaptarlo libremente, citando la fuente.

# 💬 “El código es el lenguaje universal del diseño. Aprende a hablarlo con estilo.”