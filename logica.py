from datetime import date, datetime
import calendar

# ========== CONFIG ==========
# Feriados nacionales de Argentina en 2025
FERIADOS_COLES_2025 = [
    date(2025, 1, 1), date(2025, 3, 3), date(2025, 3, 4), date(2025, 3, 24),
    date(2025, 4, 2), date(2025, 4, 17), date(2025, 4, 18), date(2025, 5, 1),
    date(2025, 5, 25), date(2025, 6, 16), date(2025, 6, 20), date(2025, 7, 9),
    date(2025, 8, 15), date(2025, 9, 30), date(2025, 10, 10), date(2025, 11, 21),
    date(2025, 11, 24), date(2025, 12, 8), date(2025, 12, 25)
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


# ========== FUNCIONES ==========
def obtener_dias_laborales(servicio, año, mes):
    dias = []
    cal = calendar.Calendar()

    for dia in cal.itermonthdates(año, mes):
        if dia.month != mes:
            continue

        if servicio == "Supermercado":
            if dia not in FERIADOS_SUPER_2025:
                dias.append(dia)

        elif servicio == "Hospital":
            if dia not in FERIADOS_COLES_2025:
                dias.append(dia)

        elif servicio == "Colegio":
            if dia.weekday() < 5 and dia not in FERIADOS_COLES_2025:  # Lun-Vie
                dias.append(dia)

        elif servicio == "Lunes a Sábado":
            if dia.weekday() < 6 and dia not in FERIADOS_COLES_2025:
                dias.append(dia)

        else:
            # Default: Lun-Vie
            if dia.weekday() < 5:
                dias.append(dia)

    return dias


# ==========================================================
def parse_fecha(f):
    if isinstance(f, date):
        return f

    s = str(f).strip()
    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]

    for fmt in formatos:
        try:
            return datetime.strptime(s, fmt).date()
        except:
            pass

    return None


# ==========================================================
def calcular_horas_extra(horas_trabajadas, jornada_semanal, mes, servicio, ausencias, año=2025):

    # Normalizo fechas válidas
    ausencias = [dt for dt in (parse_fecha(f) for f in ausencias) if dt]

    dias_laborales = obtener_dias_laborales(servicio, año, mes)

    # Filtrar ausencias que realmente caen en días laborales
    ausencias_validas = [f for f in ausencias if f in dias_laborales]

    # LOG: DEBUG AUSENCIAS
    print(f"\n--- [{servicio}] ---")
    print(f"Ausencias recibidas: {ausencias}")
    print(f"Ausencias válidas: {ausencias_validas}")
    print(f"Días laborales totales antes de ajustes: {len(dias_laborales)}")

    # ===== ORDEN CORRECTO =====
    # 1️⃣ Restar ausencias
    dias_post_ausencias = [d for d in dias_laborales if d not in ausencias_validas]

    # 2️⃣ Restar francos según servicio y jornada semanal
    dias_post_francos = dias_post_ausencias.copy()

    if servicio == "Supermercado":
        if jornada_semanal == 44:
            dias_post_francos = dias_post_francos[:-6]
            print("Se descontaron 6 francos (Jornada 44)")
        else:
            dias_post_francos = dias_post_francos[:-8]
            print("Se descontaron 8 francos (Jornada ≠ 44)")

    print(f"Días luego de restar ausencias: {len(dias_post_ausencias)}")
    print(f"Días finales luego de francos: {len(dias_post_francos)}")

    # ===== Cálculo de horas teóricas =====
    horas_teoricas = 0
    for dia in dias_post_francos:
        if servicio == "Lunes a Sábado" and jornada_semanal == 44:
            horas_teoricas += 4 if dia.weekday() == 5 else 8
        elif servicio == "Lunes a Sábado" and jornada_semanal == 36:
            horas_teoricas += 6
        else:
            if jornada_semanal in [40, 44]:
                horas_diarias = 8
            elif jornada_semanal == 30:
                horas_diarias = 6
            else:
                horas_diarias = jornada_semanal / 5
            horas_teoricas += horas_diarias

    horas_extra = horas_trabajadas - horas_teoricas

    print(f"Horas teóricas calculadas: {horas_teoricas}")
    print(f"Horas trabajadas: {horas_trabajadas}")
    print(f"➡ HORAS EXTRA => {horas_extra}")

    return {
        "horas_teoricas": round(horas_teoricas, 2),
        "horas_extra": round(horas_extra, 2)
    }
