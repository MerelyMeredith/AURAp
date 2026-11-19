## ============================================================================
## AURA+ | BLOQUE 1 - S1: INTRODUCCIÓN A AURA+ Y REGULACIÓN EMOCIONAL
## ============================================================================
## Basado en el documento de especificaciones técnicas:
## references/sprint1/Script Aura+ Entrega a Ing.docx.txt (Líneas 169-295)
## y references/sprint1/Dialogos Vídeos .docx.txt (Técnica 1: El Cuadrado 4x4)
##
## Este bloque cubre:
## 1. Bienvenida institucional de Geo al programa AURA+.
## 2. Creación de la Tarjeta Digital de Presentación.
## 3. Selección interactiva de Metas y Notas Adhesivas en el Pizarrón.
## 4. Presentación de los 3 Ejes Centrales de la Psicología Positiva.
## 5. Acuerdos de Grupo y Firma Digital de Compromiso.
## 6. Pausa Activa de Relajación: Intervención de YGRITTE (Respiración 4x4).
## 7. Urna de Pensamientos Positivos (Tarea semanal de 3 frases).
## 8. Cierre de la Sesión 1 y exportación de telemetría clínica.
## ============================================================================

label iniciar_bloque_1_s1:
    # Vinculamos la sesión al motor de telemetría como Sesión 1
    python:
        if active_patient:
            telemetria.start_session(active_patient, session_number=1)

    # Mostramos el botón de Atrás accesible en pantalla
    show screen hud_boton_atras

    # -------------------------------------------------------------------------
    # 1. BIENVENIDA INSTITUCIONAL POR GEO
    # -------------------------------------------------------------------------
    scene bg consultorio with fade

    narrator "AURA+ sube de nivel, cuida tu mente."

    show geo sonriendo at grid_pos_center, anime_pop_in
    show anime_sparkles:
        pos (940, 240)
    geo "¡Hola, [active_patient.name]! Te damos la más cordial bienvenida a AURA plus (+)."
    geo "Este es un programa digital de acompañamiento preventivo para el riesgo suicida en adolescentes, diseñado para fortalecer tu bienestar y potenciar tus virtudes."

    show geo explicativo
    geo "Yo soy Geo y seré tu guía a lo largo de este camino."
    geo "Hoy trabajaremos en el BLOQUE 1: Introducción a AURA+, donde estableceremos nuestras metas, nuestros acuerdos y nuestras herramientas de calma."

    # -------------------------------------------------------------------------
    # 2. ACTIVIDAD 1: TARJETA DIGITAL DE PRESENTACIÓN
    # -------------------------------------------------------------------------
    show geo alentador at anime_hop
    geo "Comenzaremos creando tu tarjeta digital de presentación."
    geo "Escribe cómo te gustaría que tus compañeros y tu orientador te identifiquen en nuestra comunidad."

    # Se inicializa el texto con el nombre del paciente si está vacío
    python:
        if not s1_tarjeta_identificacion and active_patient:
            s1_tarjeta_identificacion = active_patient.name

    # Se llama al modal interactivo de la tarjeta de presentación
    call screen tarjeta_presentacion_modal

    # Asegura que si se dejó en blanco, mantenga el nombre del perfil
    python:
        if not s1_tarjeta_identificacion.strip() and active_patient:
            s1_tarjeta_identificacion = active_patient.name

    show geo sonriendo at anime_hop
    show anime_sparkles:
        pos (940, 240)
    geo "¡Excelente! Tu tarjeta ya forma parte del mural de nuestro grupo."

    # -------------------------------------------------------------------------
    # 3. ACTIVIDAD 2: METAS Y NOTAS ADHESIVAS EN EL PIZARRÓN
    # -------------------------------------------------------------------------
    show geo explicativo
    geo "Todo proyecto requiere de nuestra voluntad y motivación."
    geo "¿Qué te impulsó a unirte al programa AURA+ y qué esperas de esta experiencia?"
    geo "En el pizarrón podrás seleccionar tus notas adhesivas y redactar tus expectativas personales."

    # Pantalla interactiva del pizarrón de notas
    call screen metas_pizarron_modal

    show geo sonriendo at anime_hop
    geo "Tus respuestas han quedado registradas en tu Guía Digital del Participante para recordar tu punto de partida."

    # -------------------------------------------------------------------------
    # 4. ACTIVIDAD 3: LOS 3 EJES CENTRALES DE LA PSICOLOGÍA POSITIVA
    # -------------------------------------------------------------------------
    show geo explicativo
    geo "AURA+ se fundamenta en la psicología positiva y busca potenciar tu bienestar a través de tres ejes centrales:"

    # Se despliega el esquema interactivo de los 3 ejes
    call screen ejes_psicologia_positiva_modal

    show geo alentador at anime_hop
    geo "Además, en cada sesión practicaremos ejercicios de relajación y respiración para ayudarte a regular tu cuerpo y calmar tu mente."

    # -------------------------------------------------------------------------
    # 5. ACTIVIDAD 4: COMPROMISOS DE GRUPO Y FIRMA DIGITAL
    # -------------------------------------------------------------------------
    show geo neutral
    geo "Para que este programa sea un espacio seguro para todos, establecemos acuerdos claros de convivencia:"

    # Se despliega la pantalla modal de firma de acuerdos
    call screen acuerdos_firma_modal

    show geo sonriendo at anime_hop
    show anime_sparkles:
        pos (940, 240)
    geo "¡Tu compromiso digital ha quedado firmado! El respeto mutuo y la confidencialidad son nuestra base."

    # -------------------------------------------------------------------------
    # 6. ACTIVIDAD 5: PAUSA ACTIVA - INTERVENCIÓN DE YGRITTE (RESPIRACIÓN 4x4)
    # -------------------------------------------------------------------------
    show geo explicativo
    geo "Para cerrar la primera parte de esta sesión, realizaremos una pausa activa:"
    geo "La Respiración en Cuadro para reducir tensiones fisiológicas y calmar el ritmo cardíaco."

    show geo sonriendo at anime_hop
    geo "Te presento a Ygritte, quien te guiará paso a paso en esta técnica."

    hide geo with dissolve

    # Entrada de Ygritte con salto anime y destellos
    show ygritte energica at grid_pos_center, anime_hop
    show anime_sparkles:
        pos (940, 240)
    ygritte "¡Qué onda! Qué bueno que te conectas. Este espacio es para que tengas herramientas cuando sientas que el mundo te sobrepasa."

    show ygritte sonriendo
    ygritte "Soy Ygritte, tengo 13 años y, al igual que tú, estoy en la secundaria."
    ygritte "Hace unos meses tomé este curso y la neta me sirvió mucho para no explotar en los exámenes o cuando hay dramas con los amigos."

    show ygritte empatica at anime_nervous_sway
    ygritte "¿Sabías que puedes 'apagar' el estrés usando solo tu respiración? Suena simple, pero funciona increíble."

    show ygritte concentrada
    ygritte "Vamos a probar la técnica de 'Respiración en Cuadro' o 4x4:"
    ygritte "Imagina un cuadrado en tu mente: subes por un lado inhalando en 4 segundos... cruzas por arriba aguantando el aire 4 segundos..."
    ygritte "Bajas por el otro lado soltando el aire en 4 segundos... y cruzas por abajo quedándote sin aire 4 segundos."

    show ygritte energica at anime_hop
    ygritte "Vamos a practicarla junt[p_o]s ahora mismo. Sigue el ritmo del cuadro en pantalla:"

    # Se ejecuta la pantalla interactiva de Respiración 4x4
    call screen minijuego_respiracion_4x4(target_cycles=3)

    # Retorno tras la respiración
    show ygritte sonriendo at grid_pos_center, anime_hop
    show anime_sparkles:
        pos (940, 240)
    ygritte "¡Bien hecho, [active_patient.name]! Si quieres relajarte al 100 por ciento, te recomiendo repetir este ciclo cuando te sientas presionado."
    ygritte "¡Acompáñame a la última actividad de la sesión!"

    hide ygritte with dissolve

    # -------------------------------------------------------------------------
    # 7. ACTIVIDAD 6: URNA DE PENSAMIENTOS POSITIVOS
    # -------------------------------------------------------------------------
    show geo explicativo at grid_pos_center, anime_pop_in
    geo "Tu tarea de esta semana es la Urna de Pensamientos Positivos."
    geo "Escribe tres frases que te sean útiles para recordar aspectos valiosos de tu vida y tus fortalezas."

    # Se invoca la pantalla interactiva de la urna digital
    call screen urna_pensamientos_modal

    # -------------------------------------------------------------------------
    # 8. CIERRE DE LA SESIÓN 1 Y EXPORTACIÓN CLÍNICA
    # -------------------------------------------------------------------------
    show geo sonriendo at anime_hop
    show anime_sparkles:
        pos (940, 240)
    geo "¡Excelente trabajo! Has completado exitosamente la primera sesión del programa AURA+."
    geo "Tus frases quedarán guardadas en tu urna digital para leerlas durante la semana."
    geo "Nos vemos en la sesión 2 para seguir fortaleciendo tu bienestar y tus herramientas de afrontamiento."

    # Exportación automática del reporte psicométrico de la Sesión 1
    $ export_path = exportar_telemetria()

    if export_path:
        narrator "El informe clínico de la Sesión 1 ha sido exportado exitosamente a Excel: [telemetria_ultimo_archivo_generado]"

    hide screen hud_boton_atras

    # Retorno al selector de bloques
    jump selector_bloques
