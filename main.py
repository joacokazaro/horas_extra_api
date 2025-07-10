import os
from flask import Flask, request, jsonify
from logica import calcular_horas_extra
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "API Calculadora de Horas Extra - Kazaró"

@app.route("/calcular", methods=["POST"])
def calcular():
    try:
        data = request.get_json()

        horas_trabajadas = float(data["horas_trabajadas"])
        jornada = int(data["jornada"])
        mes = int(data["mes"])
        servicio = data["servicio"]
        ausencias_str = data.get("ausencias", [])
        ausencias = [datetime.strptime(f, "%Y-%m-%d").date() for f in ausencias_str]

        resultado = calcular_horas_extra(
            horas_trabajadas, jornada, mes, servicio, ausencias
        )

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
