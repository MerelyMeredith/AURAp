## ============================================================================
## AURA+ | PANTALLAS INTERACTIVAS DEL BLOQUE 1 - S1 (CUADRÍCULA 192x108)
## ============================================================================
## Basado en el documento de especificaciones técnicas:
## references/sprint1/Script Aura+ Entrega a Ing.docx.txt
##
## Implementa:
## 1. Tarjeta Digital de Presentación
## 2. Pizarrón de Metas y Notas Adhesivas
## 3. Esquema Interactivo de los 3 Ejes de Psicología Positiva
## 4. Firma Digital de Compromisos y Acuerdos de Grupo
## 5. Urna de Pensamientos Positivos (3 frases)
## ============================================================================

init offset = -1

## ----------------------------------------------------------------------------
## 1. VARIABLES DE ESTADO PARA EL BLOQUE 1 (DEFAULT)
## ----------------------------------------------------------------------------
default s1_tarjeta_identificacion = ""
default s1_meta_estres = True
default s1_meta_fortalezas = True
default s1_meta_conectar = True
default s1_meta_personal = ""
default s1_acuerdos_firmados = False

default s1_frase_positiva_1 = "Tengo personas en quienes confiar cuando las cosas se ponen difíciles."
default s1_frase_positiva_2 = "Mis errores no me definen; son oportunidades para aprender."
default s1_frase_positiva_3 = "Merezco respeto, tranquilidad y tiempo para cuidar mi mente."


## ----------------------------------------------------------------------------
## 2. PANTALLA: TARJETA DIGITAL DE PRESENTACIÓN
## ----------------------------------------------------------------------------
## Cuadrícula 192x108: gx=56, gy=26, gw=80, gh=56 -> pos (560, 260), xsize 800, ysize 560
screen tarjeta_presentacion_modal():
    modal True
    zorder 100

    # Atajos de teclado para que presionar Enter guarde inmediatamente
    key "K_RETURN" action [Hide("tarjeta_presentacion_modal"), Return(True)]
    key "K_KP_ENTER" action [Hide("tarjeta_presentacion_modal"), Return(True)]

    add Solid("#000000cc")

    frame:
        pos (560, 260)
        xsize 800
        ysize 560
        background Solid("#1e293b")
        padding (35, 30)

        vbox:
            spacing 18
            align (0.5, 0.5)

            text "TARJETA DIGITAL DE PRESENTACIÓN":
                size 24
                bold True
                color "#38bdf8"
                xalign 0.5

            text "Escribe tu nombre o apodo y comparte cómo te gustaría que tus compañeros y tu orientador te identifiquen en la comunidad AURA+:":
                size 16
                color "#e2e8f0"
                justify True
                xalign 0.5

            frame:
                xsize 700
                ysize 100
                background Solid("#0f172a")
                padding (15, 15)

                input:
                    value VariableInputValue("s1_tarjeta_identificacion", returnable=True)
                    default (active_patient.name if active_patient else "Mi nombre")
                    length 45
                    size 22
                    color "#f8fafc"

            text "Esta tarjeta formará parte del mural de bienvenida del grupo.":
                size 14
                italic True
                color "#94a3b8"
                xalign 0.5

            null ysize 10

            textbutton "Aceptar y Guardar en el Mural":
                xsize 420
                ysize 54
                xalign 0.5
                background Solid("#059669")
                hover_background Solid("#10b981")
                text_align (0.5, 0.5)
                text_size 17
                text_bold True
                text_color "#ffffff"
                action [Hide("tarjeta_presentacion_modal"), Return(True)]


## ----------------------------------------------------------------------------
## 3. PANTALLA: PIZARRÓN DE METAS Y NOTAS ADHESIVAS
## ----------------------------------------------------------------------------
## Cuadrícula 192x108: gx=46, gy=18, gw=100, gh=72 -> pos (460, 180), xsize 1000, ysize 720
screen metas_pizarron_modal():
    modal True
    zorder 100

    key "K_RETURN" action [Hide("metas_pizarron_modal"), Return(True)]
    key "K_KP_ENTER" action [Hide("metas_pizarron_modal"), Return(True)]

    add Solid("#000000cc")

    frame:
        pos (460, 180)
        xsize 1000
        ysize 720
        background Solid("#064e3b")
        padding (40, 30)

        vbox:
            spacing 18
            align (0.5, 0.5)

            text "NOTAS ADHESIVAS: TUS METAS EN AURA+":
                size 24
                bold True
                color "#facc15"
                xalign 0.5

            text "¿Qué te impulsó a unirte a AURA+ y qué esperas de esta experiencia? Selecciona tus prioridades:":
                size 16
                color "#ecfdf5"
                justify True
                xalign 0.5

            # Notas adhesivas seleccionables
            vbox:
                spacing 14
                xalign 0.5

                # Nota 1
                button:
                    xsize 880
                    ysize 65
                    background (Solid("#ca8a04") if s1_meta_estres else Solid("#1e293b"))
                    action ToggleVariable("s1_meta_estres")
                    hbox:
                        align (0.5, 0.5)
                        spacing 15
                        text ("☑" if s1_meta_estres else "☐"):
                            size 24
                            color "#ffffff"
                        text "Aprender a manejar el estrés o emociones difíciles":
                            size 17
                            bold True
                            color "#ffffff"

                # Nota 2
                button:
                    xsize 880
                    ysize 65
                    background (Solid("#2563eb") if s1_meta_fortalezas else Solid("#1e293b"))
                    action ToggleVariable("s1_meta_fortalezas")
                    hbox:
                        align (0.5, 0.5)
                        spacing 15
                        text ("☑" if s1_meta_fortalezas else "☐"):
                            size 24
                            color "#ffffff"
                        text "Conocerme mejor y valorar mis fortalezas personales":
                            size 17
                            bold True
                            color "#ffffff"

                # Nota 3
                button:
                    xsize 880
                    ysize 65
                    background (Solid("#7c3aed") if s1_meta_conectar else Solid("#1e293b"))
                    action ToggleVariable("s1_meta_conectar")
                    hbox:
                        align (0.5, 0.5)
                        spacing 15
                        text ("☑" if s1_meta_conectar else "☐"):
                            size 24
                            color "#ffffff"
                        text "Conectar con otros adolescentes y saber cómo pedir ayuda":
                            size 17
                            bold True
                            color "#ffffff"

            # Campo abierto personal
            text "Tu expectativa personal o mensaje adicional:":
                size 15
                bold True
                color "#a7f3d0"

            frame:
                xsize 880
                ysize 70
                background Solid("#022c22")
                padding (12, 10)
                input:
                    value VariableInputValue("s1_meta_personal")
                    default "Quiero sentirme con más seguridad en la escuela."
                    length 70
                    size 16
                    color "#f8fafc"

            textbutton "Aceptar y Guardar en mi Guía Digital":
                xsize 420
                ysize 54
                xalign 0.5
                background Solid("#059669")
                hover_background Solid("#10b981")
                text_align (0.5, 0.5)
                text_size 17
                text_bold True
                text_color "#ffffff"
                action [Hide("metas_pizarron_modal"), Return(True)]


## ----------------------------------------------------------------------------
## 4. PANTALLA: LOS 3 EJES CENTRALES DE LA PSICOLOGÍA POSITIVA
## ----------------------------------------------------------------------------
## Cuadrícula 192x108: gx=46, gy=16, gw=100, gh=76 -> pos (460, 160), xsize 1000, ysize 760
screen ejes_psicologia_positiva_modal():
    modal True
    zorder 100

    key "K_RETURN" action [Hide("ejes_psicologia_positiva_modal"), Return(True)]
    key "K_KP_ENTER" action [Hide("ejes_psicologia_positiva_modal"), Return(True)]

    add Solid("#000000cc")

    frame:
        pos (460, 160)
        xsize 1000
        ysize 760
        background Solid("#1e293b")
        padding (40, 30)

        vbox:
            spacing 20
            align (0.5, 0.5)

            text "LOS 3 EJES CENTRALES DEL PROGRAMA AURA+":
                size 24
                bold True
                color "#38bdf8"
                xalign 0.5

            text "Basado en la psicología positiva para potenciar tu bienestar integral:":
                size 16
                color "#94a3b8"
                xalign 0.5

            # Fila de 3 Ejes
            hbox:
                spacing 20
                xalign 0.5

                # Eje 1
                frame:
                    xsize 290
                    ysize 380
                    background Solid("#0f172a")
                    padding (20, 20)
                    vbox:
                        spacing 14
                        text "EJE 1" size 18 bold True color "#38bdf8" xalign 0.5
                        text "🌟\nAutovaloración" size 20 bold True color "#f8fafc" xalign 0.5 text_align 0.5
                        add Solid("#334155", xsize=250, ysize=2)
                        text "Aprender a valorarte, reconocer tus capacidades únicas y proponerte metas optimistas para tu futuro." size 15 color "#cbd5e1" justify True

                # Eje 2
                frame:
                    xsize 290
                    ysize 380
                    background Solid("#0f172a")
                    padding (20, 20)
                    vbox:
                        spacing 14
                        text "EJE 2" size 18 bold True color "#10b981" xalign 0.5
                        text "🛡️\nAfrontamiento" size 20 bold True color "#f8fafc" xalign 0.5 text_align 0.5
                        add Solid("#334155", xsize=250, ysize=2)
                        text "Desarrollar herramientas emocionales para afrontar problemas cotidianos y disfrutar de experiencias positivas." size 15 color "#cbd5e1" justify True

                # Eje 3
                frame:
                    xsize 290
                    ysize 380
                    background Solid("#0f172a")
                    padding (20, 20)
                    vbox:
                        spacing 14
                        text "EJE 3" size 18 bold True color "#a855f7" xalign 0.5
                        text "🤝\nRedes y Ayuda" size 20 bold True color "#f8fafc" xalign 0.5 text_align 0.5
                        add Solid("#334155", xsize=250, ysize=2)
                        text "Fortalecer tus relaciones con compañeros, servir a los demás y saber pedir ayuda cuando la necesites." size 15 color "#cbd5e1" justify True

            text "Dimensión transversal: En cada sesión realizaremos pausas de respiración y relajación.":
                size 15
                italic True
                color "#2dd4bf"
                xalign 0.5

            textbutton "Aceptar y Continuar":
                xsize 300
                ysize 52
                xalign 0.5
                background Solid("#0284c7")
                hover_background Solid("#38bdf8")
                text_align (0.5, 0.5)
                text_size 16
                text_bold True
                text_color "#ffffff"
                action [Hide("ejes_psicologia_positiva_modal"), Return(True)]


## ----------------------------------------------------------------------------
## 5. PANTALLA: ACUERDOS DE GRUPO Y FIRMA DIGITAL
## ----------------------------------------------------------------------------
## Cuadrícula 192x108: gx=50, gy=20, gw=92, gh=68 -> pos (500, 200), xsize 920, ysize 680
screen acuerdos_firma_modal():
    modal True
    zorder 100

    key "K_RETURN" action [SetVariable("s1_acuerdos_firmados", True), Hide("acuerdos_firma_modal"), Return(True)]
    key "K_KP_ENTER" action [SetVariable("s1_acuerdos_firmados", True), Hide("acuerdos_firma_modal"), Return(True)]

    add Solid("#000000cc")

    frame:
        pos (500, 200)
        xsize 920
        ysize 680
        background Solid("#1e293b")
        padding (40, 30)

        vbox:
            spacing 20
            align (0.5, 0.5)

            text "COMPROMISOS DE GRUPO - ESPACIO SEGURO":
                size 24
                bold True
                color "#38bdf8"
                xalign 0.5

            text "Para que AURA+ sea un espacio protegido para todos, establecemos los siguientes acuerdos:":
                size 16
                color "#cbd5e1"
                xalign 0.5

            vbox:
                spacing 14
                xalign 0.5

                frame:
                    xsize 840
                    padding (15, 12)
                    background Solid("#0f172a")
                    vbox:
                        text "• RESPETO:" size 17 bold True color "#38bdf8"
                        text "Valorar las opiniones, identidades y vivencias de los demás sin juzgar ni burlarse." size 15 color "#f1f5f9"

                frame:
                    xsize 840
                    padding (15, 12)
                    background Solid("#0f172a")
                    vbox:
                        text "• CONFIDENCIALIDAD:" size 17 bold True color "#10b981"
                        text "Lo compartido dentro del programa y la comunidad se mantiene protegido y privado." size 15 color "#f1f5f9"

                frame:
                    xsize 840
                    padding (15, 12)
                    background Solid("#0f172a")
                    vbox:
                        text "• ASISTENCIA Y PRÁCTICA:" size 17 bold True color "#f59e0b"
                        text "Compromiso de realizar las actividades y poner en práctica las técnicas de regulación." size 15 color "#f1f5f9"

            textbutton "✍ Aceptar los acuerdos y firmar mi compromiso digital":
                xsize 640
                ysize 58
                xalign 0.5
                background Solid("#059669")
                hover_background Solid("#10b981")
                text_align (0.5, 0.5)
                text_size 17
                text_bold True
                text_color "#ffffff"
                action [
                    SetVariable("s1_acuerdos_firmados", True),
                    Hide("acuerdos_firma_modal"),
                    Return(True)
                ]


## ----------------------------------------------------------------------------
## 6. PANTALLA: URNA DE PENSAMIENTOS POSITIVOS
## ----------------------------------------------------------------------------
## Cuadrícula 192x108: gx=46, gy=18, gw=100, gh=72 -> pos (460, 180), xsize 1000, ysize 720
screen urna_pensamientos_modal():
    modal True
    zorder 100

    key "K_RETURN" action [Hide("urna_pensamientos_modal"), Return(True)]
    key "K_KP_ENTER" action [Hide("urna_pensamientos_modal"), Return(True)]

    add Solid("#000000cc")

    frame:
        pos (460, 180)
        xsize 1000
        ysize 720
        background Solid("#1b2434")
        padding (40, 30)

        vbox:
            spacing 16
            align (0.5, 0.5)

            text "🏺 URNA DE PENSAMIENTOS POSITIVOS (TAREA SEMANAL)":
                size 24
                bold True
                color "#facc15"
                xalign 0.5

            text "Escribe tres frases positivas que te sean útiles para recordar aspectos valiosos de tu vida durante la semana:":
                size 16
                color "#cbd5e1"
                justify True
                xalign 0.5

            # Frase 1
            vbox:
                spacing 4
                text "Frase Positiva 1:" size 15 bold True color "#38bdf8"
                frame:
                    xsize 900
                    ysize 55
                    background Solid("#0f172a")
                    padding (10, 8)
                    input:
                        value VariableInputValue("s1_frase_positiva_1")
                        length 80
                        size 16
                        color "#f8fafc"

            # Frase 2
            vbox:
                spacing 4
                text "Frase Positiva 2:" size 15 bold True color "#10b981"
                frame:
                    xsize 900
                    ysize 55
                    background Solid("#0f172a")
                    padding (10, 8)
                    input:
                        value VariableInputValue("s1_frase_positiva_2")
                        length 80
                        size 16
                        color "#f8fafc"

            # Frase 3
            vbox:
                spacing 4
                text "Frase Positiva 3:" size 15 bold True color "#c084fc"
                frame:
                    xsize 900
                    ysize 55
                    background Solid("#0f172a")
                    padding (10, 8)
                    input:
                        value VariableInputValue("s1_frase_positiva_3")
                        length 80
                        size 16
                        color "#f8fafc"

            null ysize 10

            textbutton "Aceptar y Depositar Frases en la Urna Digital":
                xsize 460
                ysize 54
                xalign 0.5
                background Solid("#ca8a04")
                hover_background Solid("#eab308")
                text_align (0.5, 0.5)
                text_size 17
                text_bold True
                text_color "#000000"
                action [Hide("urna_pensamientos_modal"), Return(True)]
