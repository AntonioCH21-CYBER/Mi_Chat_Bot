
from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    datos = request.get_json(silent=True) or {}
    mensaje = datos.get("mensaje", "").strip()

    if not mensaje:
        return {"respuesta": "Escribe una pregunta para comenzar."}, 400

    instrucciones = r"""
Eres un asistente educativo. Responde siempre en español,
con explicaciones claras y sencillas.

REGLAS IMPORTANTES DE FORMATO:

1. Usa Markdown para títulos, listas y negritas.

2. Escribe las fórmulas matemáticas usando LaTeX.

3. Para fórmulas dentro de un párrafo, usa:
   \( F = |q| \cdot v \cdot B \cdot \sin(\theta) \)

4. Para fórmulas importantes en una línea separada, usa:
   \[
   F = |q| \cdot v \cdot B \cdot \sin(\theta)
   \]

5. Escribe las fórmulas directamente con esos delimitadores.
   NO las encierres entre corchetes cuadrados [ ].

6. Para fórmulas químicas, puedes usar:
   \( H_2O \), \( CO_2 \), \( O_2 \).

7. No escribas las fórmulas dentro de bloques de código.
   No expliques Markdown ni LaTeX a menos que te lo pidan.

8. Explica el significado de los símbolos cuando sea útil.
"""

    try:
        respuesta = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                instrucciones
                + "\n\nPregunta del usuario:\n"
                + mensaje
            )
        )

        texto_respuesta = respuesta.text

        if not texto_respuesta:
            texto_respuesta = "No recibí una respuesta. Inténtalo de nuevo."

        return {"respuesta": texto_respuesta}

    except Exception as error:
        print("Error de Gemini:", error)

        return {
            "respuesta": (
                "No pude generar una respuesta en este momento. "
                "Espera unos segundos e inténtalo de nuevo."
            )
        }, 200


if __name__ == "__main__":
    app.run(debug=True)
