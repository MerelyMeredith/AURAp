## ============================================================================
## AURA+ | PRÓLOGO - S0: ENTRENAMIENTO PARA LA INTERACCIÓN EN EL SOFTWARE
## ============================================================================
## Basado en el documento de especificaciones técnicas:
## references/sprint1/Script Aura+ Entrega a Ing.docx.txt (Líneas 57-166)
##
## Este bloque cubre:
## 1. Introducción al entorno de la escuela y movimiento visual.
## 2. Exploración Point-and-Click en el patio escolar (puerta del salón).
## 3. Entrada al salón de clases y pupitre para dejar la mochila.
## 4. Encuentro con David y dilema de la tarea de matemáticas (telemetría invisible).
## 5. Fin exacto del prólogo: David guarda silencio al entrar el profesor, fade a negro.
## ============================================================================

label iniciar_bloque_prologo_s0:
    # Vinculamos la sesión al motor de telemetría como Sesión 0 (Prólogo)
    python:
        if active_patient:
            telemetria.start_session(active_patient, session_number=0)

    # Mostramos el botón de Atrás accesible en pantalla
    show screen hud_boton_atras

    # -------------------------------------------------------------------------
    # INTRODUCCIÓN AL ENTORNO ESCOLAR
    # -------------------------------------------------------------------------
    scene bg consultorio with fade

    narrator "AURA+ sube de nivel, cuida tu mente."

    show geo sonriendo at grid_pos_center, anime_pop_in
    geo "¡Hola, [active_patient.name]! Iniciamos con el PRÓLOGO: Entrenamiento de Interacción."
    geo "En esta experiencia aprenderás a explorar los escenarios y relacionarte con tus compañeros."

    show geo alentador at anime_hop
    geo "Recuerda que no necesitas teclado: podrás investigar cada lugar dando clic izquierdo con el mouse."
    geo "¡Adelante, explora la entrada y el patio de tu escuela!"

    hide geo with dissolve

    # -------------------------------------------------------------------------
    # EXPLORACIÓN POINT-AND-CLICK: PATIO DE LA ESCUELA (CUADRÍCULA 192x108)
    # -------------------------------------------------------------------------
    scene bg patio_escuela with dissolve

    narrator "Llegas a la entrada de tu escuela. El sol ilumina los pasillos y el patio central."
    narrator "La campana de inicio de clases está por sonar. Busca la puerta brillante del salón para dirigirte a tu clase."

    # Se llama a la pantalla Point-and-Click del patio escolar
    call screen patio_escuela_exploration


## ----------------------------------------------------------------------------
## TRANSICIÓN AL SALÓN DE CLASES
## ----------------------------------------------------------------------------
label transicion_entrada_aula:
    scene bg aula_clases with fade

    narrator "Cruzas la puerta y entras al salón de clases. Varios alumnos conversan en sus lugares."
    narrator "Dirígete a tu pupitre brillante para colocar tu mochila y tomar asiento antes de que llegue el profesor."

    # Pantalla Point-and-Click del salón de clases
    call screen aula_exploration


## ----------------------------------------------------------------------------
## ENCUENTRO CON DAVID: DECISIÓN CRÍTICA CON TELEMETRÍA (FIN DEL PRÓLOGO)
## ----------------------------------------------------------------------------
label sesion_0_encuentro_david:
    narrator "Dejas tu mochila en el asiento y te sientas en tu lugar."
    narrator "En ese instante, David se acerca, se da la vuelta y se sienta en el pupitre que está al frente tuyo."

    show david alegre at grid_david_front, anime_hop
    david "¡Qué onda, [active_patient.name]! Qué bueno que llegaste a tiempo."

    show david preocupado at anime_nervous_sway
    show anime_sweatdrop:
        pos (940, 220)

    # Cronómetro invisible de telemetría
    $ telemetria.iniciar_cronometro(
        decision_id="S0_DEC_DAVID_TAREA",
        prompt="David pregunta qué tal fue con la tarea de matemáticas y si se realizó."
    )

    david "¿Qué tal te fue con la tarea de matemáticas? Sí la hiciste, ¿no?"

    menu:
        # Opción 1: Asertiva y Segura
        "\"Sí, estaba muy fácil\"":
            $ elapsed = telemetria.registrar_decision(
                choice_text="Sí, estaba muy fácil",
                asertividad=+2,
                amabilidad=+1,
                evitacion=0,
                agresividad=0,
                is_risk=False
            )
            show david sorprendido at anime_hop
            show anime_sparkles:
                pos (940, 220)
            david "¡Qué crack! Ojalá a mí se me diera tan fácil... Me costó un montón entender las fórmulas."

        # Opción 2: Asertiva, Cooperativa y Pro-social (Búsqueda de Ayuda)
        "\"No le entendí… Le voy a pedir ayuda al profesor\"":
            $ elapsed = telemetria.registrar_decision(
                choice_text="No le entendí, pediré ayuda al profesor",
                asertividad=+3,
                amabilidad=+2,
                evitacion=0,
                agresividad=0,
                is_risk=False
            )
            show david aliviado at anime_hop
            show anime_exclamation:
                pos (940, 190)
            david "Buena idea. A mí también me dio pena preguntar ayer, pero si tú vas, me acerco contigo."

        # Opción 3: Evitativa / Riesgo
        "\"¡¿Había tarea?! No recuerdo que haya dejado\"":
            $ elapsed = telemetria.registrar_decision(
                choice_text="¿Había tarea? No recuerdo que haya dejado",
                asertividad=0,
                amabilidad=0,
                evitacion=+3,
                agresividad=+1,
                is_risk=True
            )
            show david sorprendido at grid_david_front, anime_shock
            show anime_sweatdrop:
                pos (940, 220)
            show anime_exclamation:
                pos (940, 190)
            david "¡¿Cómo que no te acordabas?! Oye, no te descuides... sabes que me preocupas, ¿va?"

    # Diálogo de cierre de David según la referencia de Sprint 1
    show david preocupado
    david "Uff, espero que los temas siguientes no estén tan difíciles como este último."

    narrator "En ese momento entra el profesor de matemáticas al salón. Todos los alumnos guardan silencio y abren sus cuadernos."

    show david alegre at anime_hop
    david "Ya viene el profe. Lo platicamos en el recreo, ¿ok?"

    hide david with dissolve

    # -------------------------------------------------------------------------
    # CONCLUSIÓN EXACTA DEL PRÓLOGO (S0)
    # -------------------------------------------------------------------------
    scene black with fade

    narrator "Has completado satisfactoriamente el PRÓLOGO: S0 Entrenamiento en el software."

    # Exportación automática de la telemetría de esta sesión
    $ export_path = exportar_telemetria()

    if export_path:
        narrator "Reporte psicométrico del Prólogo generado: [telemetria_ultimo_archivo_generado]"

    # Opciones de continuación
    show geo sonriendo at grid_pos_center, anime_hop
    geo "¡Excelente trabajo! Has dominado el manejo del software y la toma de decisiones."
    geo "¿Deseas continuar directamente al BLOQUE 1 (S1 Introducción a AURA+) o regresar al selector de bloques?"

    hide screen hud_boton_atras

    menu:
        "Continuar al Bloque 1: S1 Introducción a AURA+":
            jump iniciar_bloque_1_s1

        "Volver al Selector de Bloques":
            jump selector_bloques
