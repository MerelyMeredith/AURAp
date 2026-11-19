---
name: aura-point-and-click
description: >-
  Use this skill to design, build, or customize 2D Point-and-Click exploration screens in Ren'Py 8. Covers replacement of keyboard movement with interactive imagebuttons and imagemaps, glowing/pulsing ATL visual feedback for interactive hotspots, pixel-perfect focus masks, investigation modals, and transitioning seamlessly between environmental exploration and narrative dialogue branches.
---

# AURA+ Mecánicas de Exploración Point-and-Click

Esta habilidad define la arquitectura, diseño visual y programación de las pantallas de exploración **Point-and-Click** en Ren'Py 8 para AURA+.

---

## 1. Justificación del Diseño Terapéutico y Cuadrícula 192x108

1. **Accesibilidad Universal y Foco Cognitivo**: En estados de crisis, ansiedad o depresión adolescente, los controles complejos de teclado o movimiento espacial (WASD) generan fatiga o frustración. El Point-and-Click permite centrar la atención en la observación, la introspección y la toma consciente de decisiones.
2. **Pistas Visuales Claras (Objetos Brillantes / Hotspots)**: Los elementos interactivos presentan una sutil animación de brillo o pulsación para indicar interactividad sin romper la inmersión clínica.
3. **Regla de Cuadrícula 192x108 (Pixel-Art Snapping)**: La resolución del proyecto es 1920x1080. Para evitar que los sprites pixel-art o fondos se desfase o sufran de "bleeding" y artefactos por interpolación, **todas las posiciones (pos, xpos, ypos) y dimensiones (xsize, ysize) deben ser múltiplos de 10 píxeles** (1920/192 = 10, 1080/108 = 10). Se debe usar `subpixel False` en todas las transformaciones ATL de pixel-art.
4. **Exploración No Lineal Guiada**: El paciente decide qué inspeccionar primero (un pupitre, una puerta, un cartel informativo), fomentando su sensación de agencia y control sobre el entorno.

---

## 2. Animaciones ATL para Hotspots Interactivos (`screens/screen_exploration.rpy`)

Se diseñan transformaciones en ATL (Animation & Transformation Language) para dotar a los objetos interactivos de un pulso de luz cálido y atractivo:

```renpy
init offset = -1

## Transformación ATL: Brillo y pulsación continua para objetos interactivos
transform hotspot_pulse:
    subpixel True
    zoom 1.0 alpha 0.85
    easein 1.2 zoom 1.03 alpha 1.0
    easeout 1.2 zoom 1.0 alpha 0.85
    repeat

## Transformación ATL: Efecto de iluminación en hover
transform hotspot_hover:
    subpixel True
    zoom 1.05
    matrixcolor BrightnessMatrix(0.2) + ContrastMatrix(1.1)
    easein 0.2 zoom 1.08
```

---

## 3. Pantalla de Exploración: El Patio de la Escuela

Ejemplo completo de pantalla con `imagebutton` que representa el patio escolar:

```renpy
## Estado de la exploración (default para persistir en guardados)
default exploracion_puerta_desbloqueada = False
default patio_inspeccion_banca = False
default patio_inspeccion_tablon = False
default patio_inspeccion_puerta = False

screen patio_escuela_exploration():
    tag exploration
    modal True

    # 1. Fondo del Patio Escolar
    add "images/backgrounds/patio_escuela.png"

    # 2. Encabezado de Orientación para el Paciente
    frame:
        align (0.5, 0.05)
        background Solid("#000000aa")
        padding (20, 10)
        text "Patio Central - Explora el entorno haciendo clic en los objetos destacados":
            color "#e0f2fe"
            size 18

    # 3. Hotspot: Puerta del Salón de Clases (Avanza a la historia / David)
    imagebutton:
        pos (1250, 320)
        idle "images/interactive/hotspot_puerta_idle.png"
        hover "images/interactive/hotspot_puerta_hover.png"
        at (hotspot_hover if renpy.get_screen("patio_escuela_exploration") else hotspot_pulse)
        focus_mask True
        tooltip "Puerta hacia el aula donde se encuentra David"
        action [
            SetVariable("patio_inspeccion_puerta", True),
            Hide("patio_escuela_exploration"),
            Jump("entrar_al_aula_david")
        ]

    # 4. Hotspot: Tablón de Anuncios / Afiche de Salud Mental
    imagebutton:
        pos (400, 380)
        idle "images/interactive/hotspot_tablon_idle.png"
        hover "images/interactive/hotspot_tablon_hover.png"
        at hotspot_pulse
        focus_mask True
        tooltip "Cartelera con información sobre bienestar estudiantil"
        action [
            SetVariable("patio_inspeccion_tablon", True),
            Show("modal_inspeccion_objeto", objeto="tablon")
        ]

    # 5. Hotspot: Banco Solitario bajo el Árbol
    imagebutton:
        pos (780, 560)
        idle "images/interactive/hotspot_banca_idle.png"
        hover "images/interactive/hotspot_banca_hover.png"
        at hotspot_pulse
        focus_mask True
        tooltip "Un banco tranquilo apartado del bullicio"
        action [
            SetVariable("patio_inspeccion_banca", True),
            Show("modal_inspeccion_objeto", objeto="banca")
        ]

    # 6. Tooltip Dinámico en la parte inferior
    $ current_tooltip = GetTooltip()
    if current_tooltip:
        frame:
            align (0.5, 0.95)
            background Solid("#1e293bcc")
            padding (15, 8)
            text "[current_tooltip]":
                size 16
                color "#38bdf8"
```

---

## 4. Modal de Inspección de Objetos

Cuando el paciente hace clic en un objeto que no avanza la trama principal (como un afiche o un pupitre), se despliega un visor modal detallado sin salir de la pantalla de exploración:

```renpy
screen modal_inspeccion_objeto(objeto):
    modal True
    zorder 50

    add Solid("#000000bb")

    frame:
        align (0.5, 0.5)
        xsize 700
        padding (30, 30)
        background Solid("#1e293b")

        vbox:
            spacing 20
            align (0.5, 0.5)

            if objeto == "tablon":
                text "Cartelera Estudiantil: Línea de Apoyo":
                    size 24
                    bold True
                    color "#38bdf8"
                    xalign 0.5

                text "Hay un cartel con colores cálidos colgado en el corcho:\n\n\"No tienes que cargar con todo tú sol[p_o]. Hablar de lo que sentimos es de valientes. La psicóloga del colegio atiende en el segundo piso de 8:00 a 16:00.\"":
                    size 18
                    color "#f1f5f9"
                    justify True

            elif objeto == "banca":
                text "Banca bajo el Laurel":
                    size 24
                    bold True
                    color "#a78bfa"
                    xalign 0.5

                text "Es un rincón silencioso del patio donde las hojas caen suavemente. Sentarse aquí te ayuda a tomar una pausa cuando el ruido de los demás se vuelve abrumador.":
                    size 18
                    color "#f1f5f9"
                    justify True

            textbutton "Cerrar e Investigar Más":
                xalign 0.5
                action Hide("modal_inspeccion_objeto")
```

---

## 5. Implementación Alternativa con `imagemap`

Si el equipo de arte proporciona una ilustración completa de fondo con sus respectivos estados de mapa de bits (Ground, Hover):

```renpy
screen aula_imagemap_exploration():
    tag exploration
    modal True

    imagemap:
        ground "images/backgrounds/aula_ground.png"
        hover "images/backgrounds/aula_hover.png"

        # Hotspot: Pupitre de David
        hotspot (340, 480, 220, 180):
            tooltip "Acercarse a hablar con David"
            action [Hide("aula_imagemap_exploration"), Jump("dialogo_david_sesion0")]

        # Hotspot: Mochila olvidada
        hotspot (720, 600, 150, 120):
            tooltip "Revisar mochila escolar"
            action Show("modal_inspeccion_objeto", objeto="mochila")

        # Hotspot: Ventana hacia el patio
        hotspot (1100, 200, 250, 350):
            tooltip "Mirar el cielo por la ventana"
            action Show("modal_inspeccion_objeto", objeto="ventana")
```

---

## 6. Integración Fluida con el Flujo de la Narrativa

Para invocar una fase de exploración desde el guion:

```renpy
label iniciar_fase_exploracion:
    scene bg_patio with fade
    "Llegas temprano al colegio. El aire está fresco y todavía no suena la campana."
    "Antes de entrar al salón, puedes echar un vistazo al patio."

    # Llama a la pantalla de exploración. El script se pausa aquí hasta que un botón ejecute Jump()
    call screen patio_escuela_exploration

label entrar_al_aula_david:
    scene bg_aula with dissolve
    "Abres la puerta y entras al salón de clases."
    "A lo lejos, ves a David sentado en su pupitre con la mirada baja."
    jump sesion_0_encuentro_david
```
