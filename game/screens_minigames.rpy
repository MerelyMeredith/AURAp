## ============================================================================
## AURA+ | MINIJUEGOS DE REGULACIÓN EMOCIONAL (PILAR 5)
## ============================================================================
## Este módulo implementa la técnica terapéutica de Respiración en Cuadro (4x4)
## guiada por el personaje Ygritte, basada en los documentos clínicos de Sprint 1:
##
## 1. Inhalar 4 segundos  -> Sube por un lado del cuadrado
## 2. Retener 4 segundos  -> Cruza por la parte superior
## 3. Exhalar 4 segundos  -> Baja por el otro lado
## 4. Vacío 4 segundos    -> Cruza por la base inferior
##
## Cuenta con retroalimentación visual animada mediante ATL y temporizadores
## sincronizados en Screen Language para desescalar el estrés fisiológico.
## ============================================================================

init offset = -1

## ----------------------------------------------------------------------------
## 1. VARIABLES DE ESTADO DEL MINIJUEGO (DEFAULT)
## ----------------------------------------------------------------------------
default breath_phase = 0                # 0: Inhala, 1: Sostén, 2: Exhala, 3: Vacío
default breath_phase_title = "Inhala (4 segundos)"
default breath_phase_desc = "Sube por un lado del cuadro inhalando despacio..."
default breath_seconds_left = 4
default breath_current_cycle = 1
default breath_target_cycles = 3
default breath_exercise_completed = False


## ----------------------------------------------------------------------------
## 2. TRANSFORMACIONES VISUALES EN ATL PARA EL CUADRO Y CÍRCULO DE RESPIRACIÓN
## ----------------------------------------------------------------------------
transform square_guide_glow:
    subpixel True
    zoom 1.0 alpha 0.85
    easein 2.0 zoom 1.05 alpha 1.0
    easeout 2.0 zoom 1.0 alpha 0.85
    repeat

transform expanding_orb_phase(p):
    subpixel True
    xalign 0.5 yalign 0.5
    # La escala y opacidad reflejan la fase de llenado pulmonar
    zoom (0.6 if p == 0 else (1.0 if p == 1 else (0.9 if p == 2 else 0.55)))


## ----------------------------------------------------------------------------
## 3. LÓGICA DE ACTUALIZACIÓN TEMPORIZADA EN PYTHON
## ----------------------------------------------------------------------------
init python:
    def update_respiracion_timer():
        """
        Función invocada cada segundo por el timer del screen.
        Gestiona la transición de las 4 fases de 4 segundos de la técnica.
        """
        global breath_phase, breath_phase_title, breath_phase_desc
        global breath_seconds_left, breath_current_cycle, breath_target_cycles
        global breath_exercise_completed

        breath_seconds_left -= 1

        if breath_seconds_left <= 0:
            breath_seconds_left = 4
            breath_phase = (breath_phase + 1) % 4

            # Al regresar a la fase 0 se completa un ciclo de 16 segundos
            if breath_phase == 0:
                breath_current_cycle += 1
                if breath_current_cycle > breath_target_cycles:
                    finalizar_ejercicio_respiracion()
                    renpy.return_statement()
                    return

            # Mensajes textuales guiados por Ygritte según las referencias de Sprint 1
            if breath_phase == 0:
                breath_phase_title = "1. INHALA SUAVEMENTE"
                breath_phase_desc = "Sube por un lado del cuadrado llenando tus pulmones de aire."
            elif breath_phase == 1:
                breath_phase_title = "2. SOSTÉN EL AIRE"
                breath_phase_desc = "Cruza por arriba aguantando el aire con calma... siente la quietud."
            elif breath_phase == 2:
                breath_phase_title = "3. EXHALA DESPACIO"
                breath_phase_desc = "Baja por el otro lado soltando el aire por la boca y liberando tensión."
            elif breath_phase == 3:
                breath_phase_title = "4. QUÉDATE EN VACÍO"
                breath_phase_desc = "Cruza por abajo quedándote sin aire... estás a salvo aquí."

    def finalizar_ejercicio_respiracion():
        """Registra el término exitoso en la telemetría clínica."""
        global breath_exercise_completed, breath_current_cycle
        breath_exercise_completed = True
        if "telemetria" in renpy.store.__dict__:
            renpy.store.telemetria.registrar_decision(
                choice_text="Completó regulación emocional: Respiración 4x4",
                asertividad=+2,
                amabilidad=+1,
                is_risk=False
            )


## ----------------------------------------------------------------------------
## 4. PANTALLA: MINIJUEGO INTERACTIVO RESPIRACIÓN 4x4 (YGRITTE)
## ----------------------------------------------------------------------------
screen minijuego_respiracion_4x4(target_cycles=3):
    modal True
    zorder 100

    # Fondo oscuro relajante de gradiente clínico
    add Solid("#070d18")

    # Encabezado con la voz guía de Ygritte
    vbox:
        align (0.5, 0.08)
        spacing 10

        text "TÉCNICA DE RESPIRACIÓN EN CUADRO (4x4)":
            size 30
            bold True
            color "#a855f7"
            xalign 0.5

        text "Guía de Ygritte: \"Apaga el estrés usando solo tu respiración.\"":
            size 18
            italic True
            color "#cbd5e1"
            xalign 0.5

    # Visualizador Central: Cuadrado Terapéutico y Círculo de Pulso
    frame:
        align (0.5, 0.48)
        xsize 420
        ysize 420
        background Solid("#0f172a")

        # Marco luminoso del cuadrado
        frame:
            align (0.5, 0.5)
            xsize 380
            ysize 380
            background Solid("#1e293b")
            at square_guide_glow

            # Contenido interior con indicador dinámico
            vbox:
                align (0.5, 0.5)
                spacing 16

                # Indicador de fase actual
                text "[breath_phase_title]":
                    size 24
                    bold True
                    color ("#38bdf8" if breath_phase in (0, 1) else "#a855f7")
                    xalign 0.5

                # Gran contador de cuenta regresiva
                text "[breath_seconds_left]":
                    size 84
                    bold True
                    color "#f8fafc"
                    xalign 0.5

                text "segundos":
                    size 16
                    color "#94a3b8"
                    xalign 0.5

    # Instrucción descriptiva inferior
    vbox:
        align (0.5, 0.82)
        spacing 8

        text "[breath_phase_desc]":
            size 20
            color "#f1f5f9"
            xalign 0.5

        text "Ciclo de regulación: [min(breath_current_cycle, target_cycles)] de [target_cycles]":
            size 16
            color "#38bdf8"
            xalign 0.5

    # Temporizador de 1 segundo que activa el motor en Python
    timer 1.0 repeat True action Function(update_respiracion_timer)

    # Botón voluntario de salida (diseño no frustrante)
    button:
        align (0.5, 0.94)
        xsize 360
        ysize 46
        background Solid("#1e293b")
        hover_background Solid("#334155")
        action [
            Function(finalizar_ejercicio_respiracion),
            Return()
        ]
        text "Me siento más tranquil[p_o] (Continuar)":
            align (0.5, 0.5)
            size 15
            color "#cbd5e1"
