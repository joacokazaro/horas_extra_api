# API de Cálculo de Horas Extra - Kazaro (Python + AWS Elastic Beanstalk)

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)
![AWS Elastic Beanstalk](https://img.shields.io/badge/AWS-Elastic%20Beanstalk-orange.svg)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-success.svg)

---

## Descripción general

Servicio backend en **Python + Flask** desplegado en **AWS Elastic Beanstalk** que calcula:

- Horas teóricas mensuales
- Horas extra reales
- Ajustes por tipo de servicio
- Impacto de ausencias
- Ajustes por feriados (Argentina)
- Reglas específicas según jornada (30, 36, 40, 44 hs, etc.)

El servicio está pensado para ser consumido desde **Google Apps Script** integrado con Google Sheets.

---

## Arquitectura

```mermaid
flowchart TD
    A[Google Sheets\n(Apps Script)] -->|POST /calcular| B[API Horas Extra\nFlask + Gunicorn]
    B --> C[AWS Elastic Beanstalk\nAmazon Linux 2023\nNginx reverse proxy]
    C --> D[GitHub Actions CI/CD\nBuild & Deploy]


# 🚀 Endpoint Principal

## POST `/calcular`

### Request Body
```json
{
  "horas_trabajadas": 176,
  "jornada": 40,
  "mes": 11,
  "servicio": "Supermercado",
  "ausencias": ["2025-11-04", "2025-11-05"]
}


{
  "horas_teoricas": 160,
  "horas_extra": 16
}


horas_extra = horas_trabajadas - horas_teoricas


Reglas internas:
1. Días laborales según servicio

Supermercado: trabaja todos los días excepto feriados fijos nacionales.

Colegios: lunes a viernes + feriados educativos.

Lunes a Sábado: incluye sábados con 4–6 horas.

Hospital / Plagas: similar a Supermercado.

2. Ajustes por jornada semanal
Jornada	Regla aplicada
44 hs	Descuento de 6 días mensuales
40 hs	Descuento de 8 días
36 hs	6 hs/día (docente)
30 hs	6 hs/día
Lunes a Sábado	4 hrs sábados
3. Ausencias

Las ausencias se toman solo si caen dentro de los días laborales calculados.


Plataforma

Python 3.11 — Amazon Linux 2023

Gunicorn WSGI server

Nginx reverse proxy

Auto-restart de workers

Logs:

/var/log/web.stdout.log

/var/log/nginx/error.log

web: gunicorn --bind 127.0.0.1:8000 main:app


├── .elasticbeanstalk/
│   ├── app_versions/
│   └── config.yml
├── .github/workflows/deploy.yml
├── main.py
├── logica.py
├── openapi.yaml
├── Procfile
├── requirements.txt
└── README.md

git clone <repo>
cd horas_extra_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py


Joaquín Rojas
Kazaró 2025
