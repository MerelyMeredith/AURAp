## ============================================================================
## AURA+ | MECÁNICAS DE EXPLORACIÓN POINT-AND-CLICK (PILAR 4)
## ============================================================================
## Este módulo implementa la exploración visual interactiva en Ren'Py 8.
##
## REGLA ESTRICTA DE CUADRÍCULA 192x108:
## Todas las posiciones (pos, xpos, ypos) y dimensiones (xsize, ysize) están
## matemáticamente ancladas a múltiplos enteros de 10 píxeles.
## (1920/192 = 10px, 1080/108 = 10px).
## Esto evita que el pixel-art se desfase, se distorsione o sufra bleeding visual.
## ============================================================================

init offset = -1

## ----------------------------------------------------------------------------
## 1. TRANSFORMACIONES ATL PARA OBJETOS BRILLANTES (PIXEL-PERFECT)
## ----------------------------------------------------------------------------

## Transformación ATL: Resplandor pulsante continuo con subpixel False
transform hotspot_pulse:
    subpixel False
    zoom 1.0 alpha 0.90
    easein 1.0 zoom 1.03 alpha 1.0
    easeout 1.0 zoom 1.0 alpha 0.90
    repeat

## Transformación ATL: Acento en hover
transform hotspot_hover:
    subpixel False
    zoom 1.05 alpha 1.0


## ----------------------------------------------------------------------------
## 2. VARIABLES DE ESTADO DE EXPLORACIÓN
## ----------------------------------------------------------------------------
default patio_inspeccion_puerta = False
default patio_inspeccion_tablon = False
default patio_inspeccion_banca = False

default aula_inspeccion_mochila = False
default aula_inspeccion_pizarron = False
default aula_inspeccion_david = False


## ----------------------------------------------------------------------------
## 3. DISPLAYABLES AUTÓNOMOS DE ESCENARIOS (ALINEADOS A CUADRÍCULA)
## ----------------------------------------------------------------------------
init python:
    # 192x108 celdas (1920x1080 px)
    renpy.image("bg patio_escuela", Solid("#1e293b", xsize=1920, ysize=1080))
    renpy.image("bg aula_clases", Solid("#0f172a", xsize=1920, ysize=1080))
    renpy.image("bg consultorio", Solid("#0a0f1d", xsize=1920, ysize=1080))


## ----------------------------------------------------------------------------
## 4. PANTALLA POINT-AND-CLICK: PATIO DE LA ESCUELA (CUADRÍCULA 192x108)
## ----------------------------------------------------------------------------
screen patio_escuela_exploration():
    tag exploration
    modal True

    # 1. Fondo del patio dividido en cuadrícula exacta
    # Cielo: 192x40 celdas (1920x400 px) en gx=0, gy=0
    add Solid("#0284c7", xsize=1920, ysize=400) pos (0, 0)
    # Suelo del patio: 192x68 celdas (1920x680 px) en gx=0, gy=40
    add Solid("#334155", xsize=1920, ysize=680) pos (0, 400)

    # 2. Encabezado de Orientación (gx=16, gy=4, gw=160, gh=7) -> (160, 40, 1600, 70)
    frame:
        pos (160, 40)
        xsize 1600
        ysize 70
        background Solid("#000000bb")
        padding (20, 10)
        vbox:
            spacing 2
            text "PATIO ESCOLAR - MODO DE EXPLORACIÓN POINT-AND-CLICK (Cuadrícula 192x108)":
                size 18
                bold True
                color "#38bdf8"
                xalign 0.5
            text "Haz clic en los objetos interactivos destacados para investigar o entrar a clases":
                size 14
                color "#e2e8f0"
                xalign 0.5

    # 3. Hotspot Brillante 1: Puerta del Salón (AVANZA A LA HISTORIA)
    # Cuadrícula: gx=125, gy=28, gw=22, gh=40 -> (1250, 280, 220, 400)
    button:
        pos (1250, 280)
        xsize 220
        ysize 400
        background Solid("#1e3a8a")
        hover_background Solid("#2563eb")
        at hotspot_pulse
        tooltip "Puerta hacia tu salón de clases (Aquí te espera David)"
        action [
            SetVariable("patio_inspeccion_puerta", True),
            Hide("patio_escuela_exploration"),
            Jump("transicion_entrada_aula")
        ]
        vbox:
            align (0.5, 0.5)
            spacing 10
            text "🚪":
                size 60
                xalign 0.5
            text "ENTRADA AL\nSALÓN":
                size 16
                bold True
                color "#ffffff"
                xalign 0.5
                text_align 0.5
            text "✦ Objeto Clave":
                size 12
                color "#fbbf24"
                xalign 0.5

    # 4. Hotspot Brillante 2: Cartelera Estudiantil / Salud Mental
    # Cuadrícula: gx=40, gy=36, gw=20, gh=26 -> (400, 360, 200, 260)
    button:
        pos (400, 360)
        xsize 200
        ysize 260
        background Solid("#065f46")
        hover_background Solid("#059669")
        at hotspot_pulse
        tooltip "Cartelera escolar con información de apoyo y bienestar adolescente"
        action Show("modal_inspeccion_objeto", objeto="tablon")
        vbox:
            align (0.5, 0.5)
            spacing 8
            text "📋":
                size 48
                xalign 0.5
            text "CARTELERA DE\nORIENTACIÓN":
                size 15
                bold True
                color "#ffffff"
                xalign 0.5
                text_align 0.5
            text "✦ Inspeccionar":
                size 12
                color "#a7f3d0"
                xalign 0.5

    # 5. Hotspot Brillante 3: Banca bajo el Árbol
    # Cuadrícula: gx=75, gy=52, gw=24, gh=15 -> (750, 520, 240, 150)
    button:
        pos (750, 520)
        xsize 240
        ysize 150
        background Solid("#581c87")
        hover_background Solid("#7e22ce")
        at hotspot_pulse
        tooltip "Banca del patio: Un rincón tranquilo para tomar aire antes de clase"
        action Show("modal_inspeccion_objeto", objeto="banca")
        vbox:
            align (0.5, 0.5)
            spacing 6
            text "🪑":
                size 42
                xalign 0.5
            text "BANCA DEL PATIO":
                size 15
                bold True
                color "#ffffff"
                xalign 0.5
            text "✦ Inspeccionar":
                size 12
                color "#e9d5ff"
                xalign 0.5

    # 6. Tooltip Dinámico (gx=36, gy=97, gw=120, gh=6) -> (360, 970, 1200, 60)
    $ current_tip = GetTooltip()
    if current_tip:
        frame:
            pos (360, 970)
            xsize 1200
            ysize 60
            background Solid("#0f172acc")
            padding (10, 8)
            text "[current_tip]":
                size 16
                bold True
                color "#38bdf8"
                align (0.5, 0.5)


## ----------------------------------------------------------------------------
## 5. PANTALLA POINT-AND-CLICK: SALÓN DE CLASES (CUADRÍCULA 192x108)
## ----------------------------------------------------------------------------
screen aula_exploration():
    tag exploration
    modal True

    # 1. Fondo de aula dividido en cuadrícula
    # Pared del aula: 192x50 celdas (1920x500 px) en gx=0, gy=0
    add Solid("#1e293b", xsize=1920, ysize=500) pos (0, 0)
    # Suelo del aula: 192x58 celdas (1920x580 px) en gx=0, gy=50
    add Solid("#334155", xsize=1920, ysize=580) pos (0, 500)

    # 2. Encabezado de Orientación (gx=16, gy=4, gw=160, gh=7) -> (160, 40, 1600, 70)
    frame:
        pos (160, 40)
        xsize 1600
        ysize 70
        background Solid("#000000bb")
        padding (20, 10)
        vbox:
            spacing 2
            text "SALÓN DE CLASES - SESIÓN 0 (Cuadrícula 192x108)":
                size 18
                bold True
                color "#38bdf8"
                xalign 0.5
            text "Haz clic en tu pupitre para colocar tu mochila y tomar asiento antes de que inicie la clase":
                size 14
                color "#e2e8f0"
                xalign 0.5

    # 3. Pizarrón del Aula (gx=66, gy=14, gw=60, gh=26) -> (660, 140, 600, 260)
    button:
        pos (660, 140)
        xsize 600
        ysize 260
        background Solid("#064e3b")
        hover_background Solid("#047857")
        at hotspot_pulse
        tooltip "Pizarrón del salón: 'Tarea de Matemáticas - Ecuaciones y Gráficas'"
        action Show("modal_inspeccion_objeto", objeto="pizarron")
        vbox:
            align (0.5, 0.5)
            spacing 6
            text "📐 PIZARRÓN":
                size 20
                bold True
                color "#ffffff"
                xalign 0.5
            text "✦ Revisar apuntes":
                size 13
                color "#6ee7b7"
                xalign 0.5

    # 4. Hotspot Brillante 1: Pupitre del Jugador (AVANZA: DEJA MOCHILA Y LLEGA DAVID)
    # Cuadrícula: gx=48, gy=48, gw=28, gh=24 -> (480, 480, 280, 240)
    button:
        pos (480, 480)
        xsize 280
        ysize 240
        background Solid("#1e3a8a")
        hover_background Solid("#2563eb")
        at hotspot_pulse
        tooltip "Tu pupitre asignado. Haz clic para colocar tu mochila y sentarte."
        action [
            SetVariable("aula_inspeccion_mochila", True),
            Hide("aula_exploration"),
            Jump("sesion_0_encuentro_david")
        ]
        vbox:
            align (0.5, 0.5)
            spacing 10
            text "🎒":
                size 54
                xalign 0.5
            text "TU PUPITRE":
                size 18
                bold True
                color "#ffffff"
                xalign 0.5
            text "✦ Dejar Mochila":
                size 13
                color "#fbbf24"
                xalign 0.5

    # 5. Hotspot Brillante 2: Pupitre de David
    # Cuadrícula: gx=116, gy=48, gw=28, gh=24 -> (1160, 480, 280, 240)
    button:
        pos (1160, 480)
        xsize 280
        ysize 240
        background Solid("#312e81")
        hover_background Solid("#4338ca")
        at hotspot_pulse
        tooltip "El pupitre de enfrente donde se sienta tu amigo David."
        action Show("modal_inspeccion_objeto", objeto="pupitre_david")
        vbox:
            align (0.5, 0.5)
            spacing 10
            text "🪑":
                size 54
                xalign 0.5
            text "PUPITRE DE DAVID":
                size 18
                bold True
                color "#ffffff"
                xalign 0.5
            text "✦ Inspeccionar":
                size 13
                color "#cbd5e1"
                xalign 0.5

    # 6. Tooltip Dinámico (gx=36, gy=97, gw=120, gh=6) -> (360, 970, 1200, 60)
    $ current_tip = GetTooltip()
    if current_tip:
        frame:
            pos (360, 970)
            xsize 1200
            ysize 60
            background Solid("#0f172acc")
            padding (10, 8)
            text "[current_tip]":
                size 16
                bold True
                color "#38bdf8"
                align (0.5, 0.5)


## ----------------------------------------------------------------------------
## 6. MODAL DE INSPECCIÓN (CUADRÍCULA 192x108: gx=60, gy=30, gw=72, gh=48)
## ----------------------------------------------------------------------------
screen modal_inspeccion_objeto(objeto):
    modal True
    zorder 80

    add Solid("#000000cc")

    frame:
        pos (600, 300)
        xsize 720
        ysize 480
        padding (30, 30)
        background Solid("#1e293b")

        vbox:
            spacing 16
            align (0.5, 0.5)

            if objeto == "tablon":
                text "CARTELERA: BIENESTAR Y ORIENTACIÓN":
                    size 22
                    bold True
                    color "#38bdf8"
                    xalign 0.5

                text "Hay un cartel colorido con un mensaje amigable:\n\n\"No tienes que cargar con todo tú sol[p_o]. Pedir ayuda es un acto de valentía. La orientadora escolar y el equipo de AURA+ están aquí para escucharte sin juzgarte.\"":
                    size 17
                    color "#f1f5f9"
                    justify True

            elif objeto == "banca":
                text "BANCA BAJO EL LAUREL":
                    size 22
                    bold True
                    color "#a855f7"
                    xalign 0.5

                text "Es un rincón tranquilo donde las hojas caen suavemente. Sentarte aquí un par de minutos antes de entrar a clase te ayuda a regular la respiración y ordenar tus pensamientos.":
                    size 17
                    color "#f1f5f9"
                    justify True

            elif objeto == "pizarron":
                text "PIZARRÓN DE MATEMÁTICAS":
                    size 22
                    bold True
                    color "#34d399"
                    xalign 0.5

                text "En una esquina del pizarrón verde se lee con gis blanco:\n\n\"Recordatorio: Revisión de la tarea de álgebra al inicio de la sesión. Quien tenga dudas puede preguntar con toda confianza.\"":
                    size 17
                    color "#f1f5f9"
                    justify True

            elif objeto == "pupitre_david":
                text "LUGAR DE DAVID":
                    size 22
                    bold True
                    color "#60a5fa"
                    xalign 0.5

                text "Es el pupitre de tu amigo David. Ves que tiene su cuaderno abierto y luce algo estresado por el examen que viene. En breve se dará la vuelta para platicar contigo.":
                    size 17
                    color "#f1f5f9"
                    justify True

            # Botón para cerrar (gx=24, gy=5) -> (240, 50)
            button:
                xsize 240
                ysize 50
                xalign 0.5
                background Solid("#0284c7")
                hover_background Solid("#38bdf8")
                action Hide("modal_inspeccion_objeto")
                text "Cerrar e Investigar":
                    align (0.5, 0.5)
                    size 16
                    bold True
                    color "#ffffff"
