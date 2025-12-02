import os
from flask import Flask, request, jsonify
from logica import calcular_horas_extra
from datetime import datetime, date

app = Flask(__name__)

def parse_fecha(f):
    """
    Acepta fechas tipo:
    - 2025-10-02
    - 2025-10-2
    - 2025-9-30
    - 2025-09-30
    - Espacios o strings raros

    Devuelve un date() válido o lanza error claro.
    """
    if isinstance(f, date):   # si ya es nativo date
        return f

    s = str(f).strip()

    # Normalizar formato YYYY-M-D → YYYY-MM-DD
    partes = s.split("-")
    if len(partes) == 3:
        y, m, d = partes
        y = y.zfill(4)
        m = m.zfill(2)
        d = d.zfill(2)
        s = f"{y}-{m}-{d}"

    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except:
        raise ValueError(f"Formato de fecha inválido recibido en ausencias: {f}")


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

        # Lista de strings YYYY-MM-DD → normalizar formato
        ausencias_str = data.get("ausencias", [])
        ausencias = [parse_fecha(f) for f in ausencias_str]

        resultado = calcular_horas_extra(
            horas_trabajadas,
            jornada,
            mes,
            servicio,
            ausencias
        )

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
