## ============================================================================
## AURA+ | ORQUESTADOR MAESTRO Y ENTRADA PRINCIPAL
## ============================================================================
## Proyecto: AURA+ (Sube de nivel, cuida tu mente)
##
## Este script gestiona:
## 1. El arranque del juego y la validación clínica de acceso.
## 2. El enrutamiento hacia el Selector de Bloques (S0 Prólogo vs S1 Bloque 1).
## 3. Las declaraciones centrales de personajes y configuraciones maestras.
## ============================================================================

## ----------------------------------------------------------------------------
## 1. DECLARACIÓN DE PERSONAJES Y ESTILOS
## ----------------------------------------------------------------------------
define narrator = Character(None, what_italic=True)

define geo = Character("Geo", color="#2ec4b6", who_bold=True, image="geo")
define david = Character("David", color="#3a86ff", who_bold=True, image="david")
define ygritte = Character("Ygritte", color="#a855f7", who_bold=True, image="ygritte")

define director_escolar = Character("Director", color="#64748b", who_bold=True)
define profesor_mate = Character("Profesor de Matemáticas", color="#475569", who_bold=True)
define profesora_historia = Character("Profesora de Historia", color="#475569", who_bold=True)

define p = DynamicCharacter("patient_display_name", color="#f97316", who_bold=True)


## ----------------------------------------------------------------------------
## 2. PUNTO DE ENTRADA PRINCIPAL DEL JUEGO
## ----------------------------------------------------------------------------
label start:
    # Si no hay un paciente seleccionado, se exige el PIN del terapeuta
    # y se abre el panel de gestión de pacientes.
    if active_patient is None:
        call screen therapist_keypad_modal(success_action=Show("patient_manager_screen"))
        return

    # Si ya hay un paciente activo, se conduce directamente al Selector de Bloques
    jump selector_bloques


## ----------------------------------------------------------------------------
## 3. SELECTOR DE BLOQUES (PANTALLA DE ELECCIÓN DE MÓDULOS)
## ----------------------------------------------------------------------------
label selector_bloques:
    # Ocultamos cualquier HUD activo antes de mostrar el selector
    hide screen hud_boton_atras

    # Verificamos si existe un paciente cargado
    if active_patient is None:
        call screen therapist_keypad_modal(success_action=Show("patient_manager_screen"))
        return

    # Desplegamos la pantalla del selector de bloques
    call screen block_selector_screen
    return


## ----------------------------------------------------------------------------
## 4. REDIRECCIÓN DE COMPATIBILIDAD
## ----------------------------------------------------------------------------
label session_0:
    jump iniciar_bloque_prologo_s0
