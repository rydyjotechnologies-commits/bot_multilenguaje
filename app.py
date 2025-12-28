from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def responder(mensaje):
    prompt = f"""
Detecta automáticamente el idioma del mensaje del usuario
y responde SOLO en ese mismo idioma.

Mensaje:
{mensaje}
"""
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente multilingüe profesional."},
            {"role": "user", "content": prompt}
        ]
    )
    return respuesta.choices[0].message.content


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    mensaje = data.get("mensaje")
    respuesta = responder(mensaje)
    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    app.run(debug=True)
