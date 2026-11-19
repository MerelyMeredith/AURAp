## ============================================================================
## AURA+ | HUD DE NAVEGACIÓN Y BOTÓN DE ATRÁS (CUADRÍCULA 192x108)
## ============================================================================
## Proporciona al paciente y terapeuta un botón accesible de "Atrás" en pantalla
## durante la ejecución de los bloques narrativos y de exploración.
## Permite pausar o regresar al Selector de Bloques con confirmación previa.
## ============================================================================

init offset = -1

## ----------------------------------------------------------------------------
## 1. PANTALLA HUD: BOTÓN ATRÁS PERMANENTE
## ----------------------------------------------------------------------------
## Coordenadas estrictas de cuadrícula 192x108:
## gx=4, gy=4, gw=18, gh=5 -> pos (40, 40), xsize 180, ysize 50
screen hud_boton_atras():
    zorder 90

    button:
        pos (40, 40)
        xsize 180
        ysize 50
        background Solid("#0f172acc")
        hover_background Solid("#1e293bcc")
        tooltip "Volver al Selector de Bloques / Menú de Sesiones"
        action Show("modal_confirmar_regreso_bloques")

        hbox:
            align (0.5, 0.5)
            spacing 8
            text "←":
                size 22
                bold True
                color "#38bdf8"
            text "Menú Bloques":
                size 15
                bold True
                color "#f1f5f9"


## ----------------------------------------------------------------------------
## 2. MODAL DE CONFIRMACIÓN PARA VOLVER AL SELECTOR DE BLOQUES
## ----------------------------------------------------------------------------
## Coordenadas de cuadrícula 192x108: gx=56, gy=32, gw=80, gh=44 -> pos (560, 320), xsize 800, ysize 440
screen modal_confirmar_regreso_bloques():
    modal True
    zorder 105

    add Solid("#000000cc")

    frame:
        pos (560, 320)
        xsize 800
        ysize 440
        padding (35, 30)
        background Solid("#161f30")

        vbox:
            spacing 20
            align (0.5, 0.5)

            text "VOLVER AL SELECTOR DE SESIONES":
                size 24
                bold True
                color "#38bdf8"
                xalign 0.5

            text "¿Deseas pausar esta sesión y regresar a la pantalla de selección de bloques?\n\nTu perfil actual ([active_patient.name if active_patient else 'Invitado']) se mantendrá activo.":
                size 17
                color "#cbd5e1"
                justify True
                xalign 0.5

            hbox:
                align (0.5, 0.5)
                spacing 30

                # Botón de Confirmación (gx=26, gy=5 -> 260x50 px)
                button:
                    xsize 260
                    ysize 50
                    background Solid("#e11d48")
                    hover_background Solid("#f43f5e")
                    action [
                        Hide("modal_confirmar_regreso_bloques"),
                        Hide("hud_boton_atras"),
                        Jump("selector_bloques")
                    ]
                    text "Sí, Salir al Menú":
                        align (0.5, 0.5)
                        size 16
                        bold True
                        color "#ffffff"

                # Botón de Cancelar / Continuar (gx=26, gy=5 -> 260x50 px)
                button:
                    xsize 260
                    ysize 50
                    background Solid("#0284c7")
                    hover_background Solid("#38bdf8")
                    action Hide("modal_confirmar_regreso_bloques")
                    text "Continuar Sesión":
                        align (0.5, 0.5)
                        size 16
                        bold True
                        color "#ffffff"
