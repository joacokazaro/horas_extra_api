from datetime import date, datetime
import calendar

# Feriados nacionales de Argentina en 2025
FERIADOS_COLES_2025 = [
    date(2025, 1, 1), date(2025, 3, 3), date(2025, 3, 4), date(2025, 3, 24),
    date(2025, 4, 2), date(2025, 4, 17), date(2025, 4, 18), date(2025, 5, 1),
    date(2025, 5, 25), date(2025, 6, 16), date(2025, 6, 20), date(2025, 7, 9),
    date(2025, 12, 8), date(2025, 12, 25)
]

FERIADOS_SUPER_2025 = [
    date(2025, 1, 1),
    date(2025, 5, 1),
    date(2025, 12, 25)
]

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

def obtener_dias_laborales(servicio, año, mes):
    dias_laborales = []
    cal = calendar.Calendar()
    for dia in cal.itermonthdates(año, mes):
        if dia.month != mes:
            continue
        if servicio in ["Supermercado", "Hospital", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Cuadrilla CA Gustavo"]:
            if dia not in FERIADOS_SUPER_2025:
                dias_laborales.append(dia)
        elif servicio in ["Colegio", "Cuadrilla CA Dani F", "Cuadrilla EV Dani F", "Cuadrilla CA Felipe", "Cuadrilla CA Ricardo", "Puerto del águila"]:
            if dia.weekday() < 5 and dia not in FERIADOS_COLES_2025:
                dias_laborales.append(dia)
        elif servicio in ["Lunes a Sábado", "Cuadrilla CA Natalia"]:
            if dia.weekday() < 6 and dia not in FERIADOS_COLES_2025:
                dias_laborales.append(dia)
        elif servicio in ["Cuadrilla EV Diana", "FADEA"]:
            if dia.weekday() < 5 and dia not in FERIADOS_SUPER_2025:
                dias_laborales.append(dia)
    return dias_laborales

def calcular_horas_extra(horas_trabajadas, jornada_semanal, mes, servicio, ausencias, año=2025):
    # Asegurarse que las ausencias estén en formato date
    ausencias = [f if isinstance(f, date) else datetime.strptime(f, "%Y-%m-%d").date() for f in ausencias]

    dias_laborales = obtener_dias_laborales(servicio, año, mes)

    # Filtrar ausencias válidas (solo si caen en días laborales)
    ausencias_validas = [f for f in ausencias if f in dias_laborales]

    # Aplicar descuento de francos si corresponde
    if servicio in ["Supermercado", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Hospital", "Cuadrilla CA Gustavo"]:
        if jornada_semanal == 44:
            dias_laborales = dias_laborales[:-6]
        else:
            dias_laborales = dias_laborales[:-8]

    # Quitar ausencias válidas
    dias_laborales_efectivos = [d for d in dias_laborales if d not in ausencias_validas]

    horas_teoricas = 0
    for dia in dias_laborales_efectivos:
        if servicio == "Lunes a Sábado" and jornada_semanal == 44:
            horas_teoricas += 4 if dia.weekday() == 5 else 8
        else:
            if servicio == "Supermercado":
                if jornada_semanal in [40, 44]:
                    horas_diarias = 8
                elif jornada_semanal == 30:
                    horas_diarias = 6
                else:
                    horas_diarias = 4
            elif servicio in ["Hospital", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Cuadrilla CA Gustavo"]:
                if jornada_semanal in [40, 44]:
                    horas_diarias = 8
                elif jornada_semanal == 30:
                    horas_diarias = 6
                else:
                    horas_diarias = 4
            elif servicio == "Cuadrilla CA Natalia":
                if jornada_semanal in [40, 44]:
                    horas_diarias = 8
                elif jornada_semanal == 30:
                    horas_diarias = 6
                else:
                    horas_diarias = 4
            else:
                horas_diarias = jornada_semanal / 5
            horas_teoricas += horas_diarias

    horas_extra = horas_trabajadas - horas_teoricas

    return {
        "horas_teoricas": round(horas_teoricas, 2),
        "horas_extra": round(horas_extra, 2)
    }
