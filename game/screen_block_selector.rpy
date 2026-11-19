## ============================================================================
## AURA+ | SELECTOR DE BLOQUES Y SESIONES CLÍNICAS (CUADRÍCULA 192x108)
## ============================================================================
## Esta pantalla permite al profesional y al paciente seleccionar libremente
## qué bloque o sesión trabajar:
## - PRÓLOGO: S0 Entrenamiento para la Interacción en el Software
## - BLOQUE 1: S1 Introducción al Programa AURA+ y Regulación Emocional
## - BLOQUES FUTUROS: S2 a S13 (Prevención, Asertividad, Acoso Escolar)
## ============================================================================

init offset = -1

screen block_selector_screen():
    tag menu
    modal True

    # Fondo clínico oscuro
    add Solid("#090f1d", xsize=1920, ysize=1080)

    # 1. Barra Superior con Datos del Paciente Activo (gx=8, gy=4, gw=176, gh=8) -> (80, 40, 1760, 80)
    frame:
        pos (80, 40)
        xsize 1760
        ysize 80
        background Solid("#161f30")
        padding (25, 15)

        hbox:
            align (0.5, 0.5)
            spacing 40

            text "AURA+":
                size 28
                bold True
                color "#38bdf8"
                yalign 0.5

            if active_patient:
                text "PACIENTE: [active_patient.name] ([active_patient.age] años)":
                    size 20
                    bold True
                    color "#f1f5f9"
                    yalign 0.5

                text "ID: [active_patient.patient_id]":
                    size 16
                    color "#94a3b8"
                    yalign 0.5

                text "Identidad: [p_genero_nombre]":
                    size 16
                    color "#2dd4bf"
                    yalign 0.5

            button:
                xsize 220
                ysize 46
                background Solid("#334155")
                hover_background Solid("#e11d48")
                yalign 0.5
                action [
                    Hide("block_selector_screen"),
                    Show("patient_manager_screen")
                ]
                text "Cambiar Paciente":
                    align (0.5, 0.5)
                    size 15
                    bold True
                    color "#ffffff"

    # 2. Encabezado Central (gx=16, gy=14, gw=160, gh=6) -> (160, 140, 1600, 60)
    vbox:
        pos (160, 140)
        xsize 1600
        spacing 6

        text "SELECTOR DE BLOQUES Y MÓDULOS DE ACOMPAÑAMIENTO":
            size 28
            bold True
            color "#f8fafc"
            xalign 0.5

        text "Elige el bloque de trabajo asignado por el terapeuta para comenzar la sesión:":
            size 16
            color "#94a3b8"
            xalign 0.5

    # 3. Contenedor de Tarjetas de Bloques en Cuadrícula 192x108
    # Fila de tarjetas: y=230, altura=580
    hbox:
        pos (100, 230)
        spacing 40

        # ---------------------------------------------------------------------
        # TARJETA 1: PRÓLOGO (S0 ENTRENAMIENTO EN EL SOFTWARE)
        # ---------------------------------------------------------------------
        # Tamaño: gx=40, gy=58 -> 400x580 px
        frame:
            xsize 400
            ysize 580
            background Solid("#111827")
            padding (25, 25)

            vbox:
                spacing 16
                align (0.5, 0.0)

                # Icono y Etiqueta
                text "🎮 PRÓLOGO":
                    size 22
                    bold True
                    color "#38bdf8"
                    xalign 0.5

                text "S0: Entrenamiento de Interacción":
                    size 18
                    bold True
                    color "#f1f5f9"
                    xalign 0.5
                    text_align 0.5

                add Solid("#1f2937", xsize=350, ysize=4) xalign 0.5

                text "Aprende a navegar en Point-and-Click sin teclado. Explora el patio de la escuela, entra a tu salón de clases y responde al dilema con tu amigo David sobre la tarea de matemáticas.":
                    size 15
                    color "#cbd5e1"
                    justify True

                vbox:
                    spacing 6
                    text "✦ Modos: Point-and-Click" size 13 color "#2dd4bf"
                    text "✦ Decisión: Amigo David" size 13 color "#60a5fa"
                    text "✦ Telemetría: Latencia y Asertividad" size 13 color "#a78bfa"

                null ysize 20

                button:
                    xsize 320
                    ysize 56
                    xalign 0.5
                    background Solid("#0284c7")
                    hover_background Solid("#38bdf8")
                    action [
                        Hide("block_selector_screen"),
                        Jump("iniciar_bloque_prologo_s0")
                    ]
                    text "Iniciar Prólogo (S0)":
                        align (0.5, 0.5)
                        size 17
                        bold True
                        color "#ffffff"

        # ---------------------------------------------------------------------
        # TARJETA 2: BLOQUE 1 (S1 INTRODUCCIÓN A AURA+)
        # ---------------------------------------------------------------------
        # Tamaño: gx=40, gy=58 -> 400x580 px
        frame:
            xsize 400
            ysize 580
            background Solid("#111827")
            padding (25, 25)

            vbox:
                spacing 16
                align (0.5, 0.0)

                text "🌱 BLOQUE 1":
                    size 22
                    bold True
                    color "#10b981"
                    xalign 0.5

                text "S1: Introducción a AURA+":
                    size 18
                    bold True
                    color "#f1f5f9"
                    xalign 0.5
                    text_align 0.5

                add Solid("#1f2937", xsize=350, ysize=4) xalign 0.5

                text "Conoce a Geo, crea tu tarjeta digital de presentación, elige tus metas y firma los compromisos del grupo. Practica la Respiración en Cuadro (4x4) con Ygritte y guarda tus frases positivas.":
                    size 15
                    color "#cbd5e1"
                    justify True

                vbox:
                    spacing 6
                    text "✦ Guía: Geo y los 3 Ejes Positivos" size 13 color "#2dd4bf"
                    text "✦ Regulación: Respiración 4x4 (Ygritte)" size 13 color "#a855f7"
                    text "✦ Cierre: Urna de Pensamientos" size 13 color "#facc15"

                null ysize 20

                button:
                    xsize 320
                    ysize 56
                    xalign 0.5
                    background Solid("#059669")
                    hover_background Solid("#10b981")
                    action [
                        Hide("block_selector_screen"),
                        Jump("iniciar_bloque_1_s1")
                    ]
                    text "Iniciar Bloque 1 (S1)":
                        align (0.5, 0.5)
                        size 17
                        bold True
                        color "#ffffff"

        # ---------------------------------------------------------------------
        # TARJETA 3: BLOQUES FUTUROS (S2 A S13)
        # ---------------------------------------------------------------------
        # Tamaño: gx=40, gy=58 -> 400x580 px
        frame:
            xsize 400
            ysize 580
            background Solid("#0b0f19")
            padding (25, 25)

            vbox:
                spacing 16
                align (0.5, 0.0)

                text "🔒 SESIONES 2 A 13":
                    size 22
                    bold True
                    color "#64748b"
                    xalign 0.5

                text "Módulos de Afrontamiento":
                    size 18
                    bold True
                    color "#94a3b8"
                    xalign 0.5

                add Solid("#1f2937", xsize=350, ysize=4) xalign 0.5

                text "Sesiones avanzadas del programa:\n\n· S2: La ley del hielo\n· S3: Se ríen cuando te equivocas\n· S4: Rumores y mentiras\n· S5: Situaciones de acoso\n· S6 - S13: Prevención y Redes de Apoyo":
                    size 14
                    color "#64748b"
                    justify True

                null ysize 40

                frame:
                    xsize 320
                    ysize 56
                    background Solid("#1f2937")
                    xalign 0.5
                    text "Próximamente / Supervisado":
                        align (0.5, 0.5)
                        size 15
                        color "#64748b"

    # 4. Pie de Pantalla: Botón Volver al Menú Principal
    button:
        pos (800, 960)
        xsize 320
        ysize 50
        background Solid("#1e293b")
        hover_background Solid("#334155")
        action [
            Hide("block_selector_screen"),
            Return()
        ]
        text "← Menú Principal de Inicio":
            align (0.5, 0.5)
            size 16
            bold True
            color "#cbd5e1"
