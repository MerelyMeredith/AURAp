---
name: aura-clinical-telemetry
description: >-
  Use this skill to implement, calibrate, or extend the AURA+ Clinical Telemetry & Metrics System. Covers invisible behavioral scoring (agresividad, amabilidad, evitación, asertividad), critical risk and stress-failure counters, high-precision decision response time tracking with Python time.time(), and exporting session reports to Excel-ready CSV/TXT files (paciente_Juan_sesion1.csv).
---

# AURA+ Sistema de Telemetría y Métricas Clínicas

Esta habilidad detalla la arquitectura, el modelo de datos y la exportación del **Sistema de Telemetría y Métricas para el Profesional** en Ren'Py 8.

---

## 1. Fundamentos y Objetivos Clínicos

En la prevención e intervención del riesgo suicida en adolescentes:
1. **Recolección No Invasiva**: El paciente no debe percibir cronómetros visibles que aumenten su ansiedad, ni saber qué respuestas otorgan "puntos". La telemetría opera en segundo plano (*silent telemetry*).
2. **Dimensiones de Personalidad y Afrontamiento**:
   - **Asertividad**: Capacidad de expresar límites sanos, pedir ayuda y comunicar necesidades respetuosamente.
   - **Amabilidad / Empatía**: Inclinación pro-social, búsqueda de acuerdos y validación del otro.
   - **Evitación**: Retirada pasiva, escape emocional, aislamiento y postergación de conflictos.
   - **Agresividad**: Reacciones hostiles, confrontación impulsiva y desregulación de la ira.
3. **Indicador de Riesgo y Fallos**: Detección de patrones de desesperanza, aislamiento extremo, autolesión encubierta o reactividad explosiva ante situaciones de acoso (*bullying*).
4. **Tiempo de Decisión (Latencia)**: La vacilación prolongada (>10-15s) o la impulsividad extrema (<1s) ante dilemas críticos son biomarcadores conductuales de alto valor diagnóstico para el terapeuta.

---

## 2. Capa de Dominio en Python (`systems/telemetry.rpy`)

Se implementa el gestor de telemetría en Python puro:

```renpy
init -2 python:
    import time
    import csv
    import os
    from datetime import datetime

    class DecisionLogEntry(object):
        """Registro individual de una decisión tomada por el paciente."""
        def __init__(self, decision_id, prompt, choice_text, trait_deltas, is_risk, response_time):
            self.decision_id = decision_id
            self.prompt = prompt.replace("\n", " ").strip()
            self.choice_text = choice_text.strip()
            self.trait_deltas = trait_deltas  # dict: {"asertividad": 1, ...}
            self.is_risk = bool(is_risk)
            self.response_time = round(float(response_time), 2)
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def to_row(self):
            return [
                self.timestamp,
                self.decision_id,
                self.prompt,
                self.choice_text,
                self.trait_deltas.get("asertividad", 0),
                self.trait_deltas.get("amabilidad", 0),
                self.trait_deltas.get("evitacion", 0),
                self.trait_deltas.get("agresividad", 0),
                "SÍ" if self.is_risk else "NO",
                self.response_time
            ]


    class TelemetryEngine(object):
        """Motor central de recolección y exportación de métricas clínicas."""
        def __init__(self):
            self.reset_session()

        def reset_session(self):
            self.patient_id = "PAC-0000"
            self.patient_name = "Anonimo"
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
            self.current_prompt = ""
            self.current_decision_id = ""

        def start_session(self, patient_profile, session_number=1):
            """Vincula el paciente activo al motor de telemetría."""
            self.reset_session()
            if patient_profile:
                self.patient_id = getattr(patient_profile, "patient_id", "PAC-0000")
                self.patient_name = getattr(patient_profile, "name", "Anonimo")
                self.session_number = session_number

        def iniciar_cronometro(self, decision_id, prompt):
            """Marca el inicio del tiempo de respuesta antes de un menú."""
            self.current_decision_id = decision_id
            self.current_prompt = prompt
            self.timer_start = time.time()

        def registrar_decision(self, choice_text, asertividad=0, amabilidad=0, evitacion=0, agresividad=0, is_risk=False):
            """Registra la opción seleccionada, calcula latencia y actualiza puntajes."""
            elapsed = time.time() - self.timer_start if self.timer_start > 0 else 0.0

            deltas = {
                "asertividad": asertividad,
                "amabilidad": amabilidad,
                "evitacion": evitacion,
                "agresividad": agresividad
            }

            # Actualizar acumuladores
            for trait, val in deltas.items():
                self.scores[trait] += val
                # Reflejar en variables de store para scripts
                store_var = "score_" + trait
                setattr(renpy.store, store_var, self.scores[trait])

            if is_risk:
                self.contador_riesgo += 1
                self.fallos_emocionales += 1
                renpy.store.contador_riesgo = self.contador_riesgo

            entry = DecisionLogEntry(
                self.current_decision_id,
                self.current_prompt,
                choice_text,
                deltas,
                is_risk,
                elapsed
            )
            self.log_entries.append(entry)
            self.timer_start = 0.0
            return elapsed

        def exportar_telemetria(self):
            """
            Exporta las métricas a un archivo CSV estructurado con BOM UTF-8
            para que el terapeuta lo abra directamente en Microsoft Excel.
            """
            base_dir = config.basedir
            # Formato de nombre: paciente_Juan_sesion1.csv
            safe_name = "".join(c for c in self.patient_name if c.isalnum() or c in (' ', '_')).rstrip()
            safe_name = safe_name.replace(" ", "_")
            filename = "paciente_{}_sesion{}.csv".format(safe_name, self.session_number)
            filepath = os.path.join(base_dir, filename)

            try:
                with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f, delimiter=";")

                    # Encabezado Clínico de Resumen
                    writer.writerow(["REPORTE CLÍNICO DE SESIÓN - PROGRAMA AURA+"])
                    writer.writerow(["Fecha del Reporte", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    writer.writerow(["ID Paciente", self.patient_id])
                    writer.writerow(["Nombre del Paciente", self.patient_name])
                    writer.writerow(["Número de Sesión", self.session_number])
                    writer.writerow([])

                    # Tabla de Puntuaciones Acumuladas
                    writer.writerow(["DIMENSIÓN CONDUCTUAL", "PUNTUACIÓN FINAL", "INTERPRETACIÓN CLÍNICA PRELIMINAR"])
                    writer.writerow(["Asertividad", self.scores["asertividad"], "Defensa adecuada de límites y comunicación"])
                    writer.writerow(["Amabilidad", self.scores["amabilidad"], "Búsqueda de empatía y cooperación"])
                    writer.writerow(["Evitación", self.scores["evitacion"], "Conducta de huida o aislamiento"])
                    writer.writerow(["Agresividad", self.scores["agresividad"], "Reactividad hostil o defensiva"])
                    writer.writerow(["Contador de Riesgo / Fallos", self.contador_riesgo, "Decisiones de riesgo o vulnerabilidad"])
                    writer.writerow([])

                    # Registro Detallado de Decisiones y Cronometraje
                    writer.writerow([
                        "Timestamp",
                        "ID Decisión",
                        "Contexto / Pregunta",
                        "Opción Elegida",
                        "Delta Asertividad",
                        "Delta Amabilidad",
                        "Delta Evitación",
                        "Delta Agresividad",
                        "Indicador de Riesgo",
                        "Tiempo de Respuesta (Segundos)"
                    ])

                    total_time = 0.0
                    for entry in self.log_entries:
                        writer.writerow(entry.to_row())
                        total_time += entry.response_time

                    avg_time = round(total_time / len(self.log_entries), 2) if self.log_entries else 0.0
                    writer.writerow([])
                    writer.writerow(["Tiempo Medio de Respuesta (seg)", avg_time])
                    writer.writerow(["Total Decisiones Evaluadas", len(self.log_entries)])

                renpy.log("Telemetría exportada exitosamente a: {}".format(filepath))
                return filepath
            except Exception as e:
                renpy.log("Error exportando telemetría: {}".format(e))
                return None


    # Instancia singleton del motor de telemetría
    telemetria = TelemetryEngine()

    def exportar_telemetria():
        """Función pública en Python para llamar al final de la sesión."""
        return telemetria.exportar_telemetria()
```

---

## 3. Variables de Estado en Ren'Py (`default`)

Para garantizar que los puntajes se sincronicen con el motor de guardado de Ren'Py:

```renpy
default score_asertividad = 0
default score_amabilidad = 0
default score_evitacion = 0
default score_agresividad = 0
default contador_riesgo = 0
default ultimo_tiempo_respuesta = 0.0
```

---

## 4. Patrón de Integración en Menús de Decisión (`menu:`)

Para registrar fielmente el tiempo de respuesta y los rasgos sin ensuciar la redacción del diálogo:

```renpy
label decision_david_bullying:
    # 1. Iniciar cronómetro inmediatamente antes de presentar el dilema
    $ telemetria.iniciar_cronometro(
        decision_id="DEC_D01_BULLYING",
        prompt="David pregunta qué hacer ante los insultos recibidos en el pasillo."
    )

    david "¿Viste lo que dijeron en el pasillo? No sé qué hacer... ¿Tú qué harías en mi lugar?"

    # 2. Menú con impacto en rasgos y riesgo
    menu:
        "\"Vamos a reportarlo de inmediato con la orientadora del colegio.\"":
            $ ultimo_tiempo = telemetria.registrar_decision(
                choice_text="Reportar con orientadora",
                asertividad=+2,
                amabilidad=+1,
                is_risk=False
            )
            david "Tienes razón. Es lo más maduro y seguro."

        "\"No te metas en problemas, David. Es mejor agachar la cabeza y no decir nada.\"":
            $ ultimo_tiempo = telemetria.registrar_decision(
                choice_text="Evitación pasiva",
                evitacion=+3,
                is_risk=True
            )
            david "Supongo... pero me hace sentir muy indefenso."

        "\"¡Esos tipos se van a arrepentir! Vamos a buscarlos para encararlos y pelear.\"":
            $ ultimo_tiempo = telemetria.registrar_decision(
                choice_text="Respuesta agresiva / confrontación",
                agresividad=+3,
                is_risk=True
            )
            david "No sé... pelear podría empeorar todo."

        "\"Tranquilo David, te entiendo. Yo me quedo contigo, respiremos juntos primero.\"":
            $ ultimo_tiempo = telemetria.registrar_decision(
                choice_text="Contención empática",
                amabilidad=+3,
                asertividad=+1,
                is_risk=False
            )
            david "Gracias... de verdad necesitaba escuchar eso."
```

---

## 5. Visualización del Reporte para el Terapeuta

Al ejecutarse `exportar_telemetria()`, se genera en la raíz del proyecto un archivo con la siguiente estructura:

```csv
REPORTE CLÍNICO DE SESIÓN - PROGRAMA AURA+
Fecha del Reporte;2026-11-18 16:50:00
ID Paciente;PAC-0001
Nombre del Paciente;Mateo
Número de Sesión;1

DIMENSIÓN CONDUCTUAL;PUNTUACIÓN FINAL;INTERPRETACIÓN CLÍNICA PRELIMINAR
Asertividad;4;Defensa adecuada de límites y comunicación
Amabilidad;3;Búsqueda de empatía y cooperación
Evitación;0;Conducta de huida o aislamiento
Agresividad;0;Reactividad hostil o defensiva
Contador de Riesgo / Fallos;0;Decisiones de riesgo o vulnerabilidad

Timestamp;ID Decisión;Contexto / Pregunta;Opción Elegida;Delta Asertividad;Delta Amabilidad;Delta Evitación;Delta Agresividad;Indicador de Riesgo;Tiempo de Respuesta (Segundos)
2026-11-18 16:48:12;DEC_D01_BULLYING;David pregunta qué hacer ante los insultos...;Reportar con orientadora;2;1;0;0;NO;4.35
2026-11-18 16:49:30;DEC_D02_PRESION;David duda si entrar al aula...;Acompañar y entrar juntos;1;2;0;0;NO;3.18

Tiempo Medio de Respuesta (seg);3.76
Total Decisiones Evaluadas;2
```
