## ============================================================================
## AURA+ | SISTEMA DE TELEMETRÍA Y MÉTRICAS CLÍNICAS (PILAR 3)
## ============================================================================
## Este módulo rastrea de forma silenciosa e invisible para el paciente
## todas sus respuestas, latencias de decisión y patrones psicológicos.
## Permite al profesional de la salud mental evaluar 4 rasgos conductuales:
##
## 1. Asertividad (comunicación respetuosa, límites saludables y búsqueda de ayuda)
## 2. Amabilidad / Empatía (colaboración y apoyo interpersonal)
## 3. Evitación (retirada pasiva, escape emocional y no confrontación)
## 4. Agresividad (hostilidad, reactividad impulsiva y confrontación destructiva)
##
## Además mide con precisión de centésimas de segundo (time.time()) el tiempo
## de respuesta (latencia) y exporta un informe estructurado CSV para Excel.
## ============================================================================

init offset = -2

## ----------------------------------------------------------------------------
## 1. VARIABLES GLOBALES DE TELEMETRÍA PARA GUARDADOS DE REN'PY (DEFAULT)
## ----------------------------------------------------------------------------
default score_asertividad = 0
default score_amabilidad = 0
default score_evitacion = 0
default score_agresividad = 0
default contador_riesgo = 0
default fallos_emocionales = 0
default ultimo_tiempo_respuesta = 0.0
default telemetria_ultimo_archivo_generado = ""


## ----------------------------------------------------------------------------
## 2. CLASES Y MOTOR DE TELEMETRÍA EN PYTHON (INIT -2 PYTHON)
## ----------------------------------------------------------------------------
init -2 python:
    import time
    import csv
    import os
    from datetime import datetime

    class DecisionLogEntry(object):
        """
        Representa una decisión individual tomada por el paciente durante un menú.
        """
        def __init__(self, decision_id, prompt, choice_text, trait_deltas, is_risk, response_time):
            self.decision_id = str(decision_id)
            self.prompt = str(prompt).replace("\n", " ").strip()
            self.choice_text = str(choice_text).strip()
            self.trait_deltas = trait_deltas or {}
            self.is_risk = bool(is_risk)
            self.response_time = round(float(response_time), 2)
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def to_row(self):
            """Retorna los datos formateados para una fila del reporte CSV."""
            return [
                self.timestamp,
                self.decision_id,
                self.prompt,
                self.choice_text,
                self.trait_deltas.get("asertividad", 0),
                self.trait_deltas.get("amabilidad", 0),
                self.trait_deltas.get("evitacion", 0),
                self.trait_deltas.get("agresividad", 0),
                "SÍ (ALERTA)" if self.is_risk else "NO",
                "{:.2f}".format(self.response_time)
            ]


    class TelemetryEngine(object):
        """
        Motor central de recolección invisible de métricas psicológicas y
        cronometraje de decisiones críticas.
        """
        def __init__(self):
            self.reset_session()

        def reset_session(self):
            """Restablece los contadores para una nueva sesión clínica."""
            self.patient_id = "PAC-0000"
            self.patient_name = "Anónimo"
            self.session_number = 1
            self.scores = {
                "asertividad": 0,
                "amabilidad": 0,
                "evitacion": 0,
                "agresividad": 0
            }
            self.contador_riesgo = 0
            self.fallos_emocionales = 0
            self.log_entries = []
            self.timer_start = 0.0
            self.current_decision_id = ""
            self.current_prompt = ""

        def start_session(self, patient_profile, session_number=1):
            """Vincula el paciente activo al motor de telemetría."""
            self.reset_session()
            if patient_profile:
                self.patient_id = getattr(patient_profile, "patient_id", "PAC-0000")
                self.patient_name = getattr(patient_profile, "name", "Anónimo")
                self.session_number = session_number

        def iniciar_cronometro(self, decision_id, prompt):
            """
            Marca el inicio del tiempo de respuesta. Debe llamarse inmediatamente
            antes de mostrar la línea de diálogo o menú crítico en Ren'Py.
            """
            self.current_decision_id = decision_id
            self.current_prompt = prompt
            self.timer_start = time.time()

        def registrar_decision(self, choice_text, asertividad=0, amabilidad=0, evitacion=0, agresividad=0, is_risk=False):
            """
            Calcula la latencia transcurrida desde iniciar_cronometro, actualiza
            los acumuladores de personalidad y riesgo, y archiva el evento.
            """
            elapsed = 0.0
            if self.timer_start > 0:
                elapsed = max(0.01, time.time() - self.timer_start)

            deltas = {
                "asertividad": asertividad,
                "amabilidad": amabilidad,
                "evitacion": evitacion,
                "agresividad": agresividad
            }

            # Actualizar puntajes acumulativos
            for trait, value in deltas.items():
                self.scores[trait] += value
                setattr(renpy.store, "score_" + trait, self.scores[trait])

            # Actualizar contadores de riesgo
            if is_risk:
                self.contador_riesgo += 1
                self.fallos_emocionales += 1
                renpy.store.contador_riesgo = self.contador_riesgo
                renpy.store.fallos_emocionales = self.fallos_emocionales

            # Guardar el último tiempo para visualización opcional del terapeuta
            renpy.store.ultimo_tiempo_respuesta = round(elapsed, 2)

            entry = DecisionLogEntry(
                decision_id=self.current_decision_id,
                prompt=self.current_prompt,
                choice_text=choice_text,
                trait_deltas=deltas,
                is_risk=is_risk,
                response_time=elapsed
            )
            self.log_entries.append(entry)

            # Reiniciar cronómetro
            self.timer_start = 0.0
            return elapsed

        def exportar_telemetria(self):
            """
            Exporta el informe psicométrico de la sesión en un archivo CSV
            delimitado por punto y coma (;) con cabecera BOM UTF-8 (utf-8-sig)
            para que Microsoft Excel en Windows lo abra perfectamente sin deformar tildes.
            
            Nombre del archivo: paciente_[Nombre]_sesion[N].csv
            """
            base_dir = config.basedir
            safe_name = "".join(c for c in self.patient_name if c.isalnum() or c in (' ', '_')).strip()
            safe_name = safe_name.replace(" ", "_") if safe_name else "Paciente"
            filename = "paciente_{}_sesion{}.csv".format(safe_name, self.session_number)
            filepath = os.path.join(base_dir, filename)

            try:
                with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f, delimiter=";")

                    # 1. Cabecera Institucional y Datos de Ficha
                    writer.writerow(["PROGRAMA AURA+ | REPORTE PSICOMÉTRICO DE SESIÓN CLÍNICA"])
                    writer.writerow(["Fecha y Hora de Cierre", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    writer.writerow(["ID Paciente", self.patient_id])
                    writer.writerow(["Nombre del Paciente", self.patient_name])
                    writer.writerow(["Número de Sesión", self.session_number])
                    writer.writerow([])

                    # 2. Resumen Cuantitativo de Rasgos Psicológicos
                    writer.writerow(["DIMENSIÓN CONDUCTUAL", "PUNTAJE ACUMULADO", "DESCRIPCIÓN CLÍNICA"])
                    writer.writerow(["Asertividad", self.scores["asertividad"], "Expresión clara de necesidades y límites saludables"])
                    writer.writerow(["Amabilidad", self.scores["amabilidad"], "Cooperación, empatía e interés pro-social"])
                    writer.writerow(["Evitación", self.scores["evitacion"], "Conducta de huida pasiva, silencio o aislamiento"])
                    writer.writerow(["Agresividad", self.scores["agresividad"], "Reactividad impulsiva, confrontación u hostilidad"])
                    writer.writerow(["Contador de Riesgo / Fallos", self.contador_riesgo, "Decisiones de riesgo emocional o vulnerabilidad"])
                    writer.writerow([])

                    # 3. Detalle Paso a Paso de Decisiones y Tiempos de Respuesta
                    writer.writerow([
                        "Timestamp",
                        "ID Decisión",
                        "Contexto / Pregunta",
                        "Opción Seleccionada",
                        "Delta Asertividad",
                        "Delta Amabilidad",
                        "Delta Evitación",
                        "Delta Agresividad",
                        "Riesgo / Fallo",
                        "Tiempo de Respuesta (Segundos)"
                    ])

                    total_response_time = 0.0
                    for entry in self.log_entries:
                        writer.writerow(entry.to_row())
                        total_response_time += entry.response_time

                    count = len(self.log_entries)
                    avg_time = round(total_response_time / count, 2) if count > 0 else 0.0

                    writer.writerow([])
                    writer.writerow(["Total de Decisiones Evaluadas", count])
                    writer.writerow(["Tiempo Medio de Respuesta (segundos)", avg_time])

                renpy.log("AURA+ [Telemetría] Archivo generado con éxito en: {}".format(filepath))
                renpy.store.telemetria_ultimo_archivo_generado = filename
                return filepath
            except Exception as e:
                renpy.log("AURA+ [Telemetría] Error exportando CSV: {}".format(e))
                return None


    # Singleton del motor de telemetría disponible en todos los scripts
    telemetria = TelemetryEngine()

    def exportar_telemetria():
        """Función pública en Python para llamar al final de cada sesión."""
        return telemetria.exportar_telemetria()
