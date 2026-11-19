## ============================================================================
## AURA+ | SISTEMA DE PERFILES Y GESTOR DE PACIENTES (PILAR 1)
## ============================================================================
## Reemplaza el menú principal por defecto de Ren'Py (screen main_menu) y
## gestiona N cantidad de perfiles de pacientes mediante persistencia dual:
## 1. Variables persistentes de Ren'Py (persistent.patient_profiles)
## 2. Archivo estructurado JSON (patient_profiles.json) en la raíz del proyecto.
## ============================================================================

init offset = -2

## ----------------------------------------------------------------------------
## 1. MODELO DE DATOS Y GESTOR DE PERFILES EN PYTHON
## ----------------------------------------------------------------------------
init -2 python:
    import json
    import os
    from datetime import datetime

    class PatientProfile(object):
        """
        Representa la ficha clínica de un paciente adolescente en AURA+.
        Almacena su identificador único, nombre, edad, género y métricas de sesión.
        """
        def __init__(self, patient_id, name, age, gender):
            self.patient_id = patient_id
            self.name = name.strip()
            self.age = int(age)
            # Normalización del género: "chico", "chica", "no_binario"
            self.gender = gender.lower().strip()
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.sessions_count = 0
            self.last_session = "Sin sesiones previas"

        def to_dict(self):
            return {
                "patient_id": self.patient_id,
                "name": self.name,
                "age": self.age,
                "gender": self.gender,
                "created_at": self.created_at,
                "sessions_count": self.sessions_count,
                "last_session": self.last_session
            }

        @classmethod
        def from_dict(cls, data):
            profile = cls(
                patient_id=data.get("patient_id", "PAC-0000"),
                name=data.get("name", "Anónimo"),
                age=data.get("age", 14),
                gender=data.get("gender", "chico")
            )
            profile.created_at = data.get("created_at", "")
            profile.sessions_count = data.get("sessions_count", 0)
            profile.last_session = data.get("last_session", "Sin registro")
            return profile


    class ProfileManager(object):
        """
        Gestor de almacenamiento y consulta de perfiles de pacientes.
        Permite soportar N cantidad de perfiles sin límite.
        """
        PROFILES_FILE = "patient_profiles.json"

        @classmethod
        def get_all(cls):
            """Retorna el diccionario con todos los perfiles guardados."""
            if persistent.patient_profiles is None:
                persistent.patient_profiles = {}
            return persistent.patient_profiles

        @classmethod
        def create(cls, name, age, gender):
            """Crea un nuevo perfil y lo guarda tanto en persistencia como en JSON."""
            all_profiles = cls.get_all()
            new_id = "PAC-{:04d}".format(len(all_profiles) + 1)
            profile = PatientProfile(new_id, name, age, gender)
            all_profiles[new_id] = profile.to_dict()
            renpy.save_persistent()
            cls.sync_to_disk()
            return profile

        @classmethod
        def get(cls, patient_id):
            """Recupera un perfil específico por su ID."""
            all_profiles = cls.get_all()
            data = all_profiles.get(patient_id)
            if data:
                return PatientProfile.from_dict(data)
            return None

        @classmethod
        def register_session_increment(cls, patient_id):
            """Registra el inicio de una nueva sesión clínica para el paciente."""
            all_profiles = cls.get_all()
            if patient_id in all_profiles:
                all_profiles[patient_id]["sessions_count"] += 1
                all_profiles[patient_id]["last_session"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                renpy.save_persistent()
                cls.sync_to_disk()

        @classmethod
        def sync_to_disk(cls):
            """Exporta los perfiles al archivo JSON local para consulta externa."""
            try:
                filepath = os.path.join(config.basedir, cls.PROFILES_FILE)
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(persistent.patient_profiles, f, ensure_ascii=False, indent=2)
            except Exception as e:
                renpy.log("AURA+ [Perfil] Error guardando JSON: {}".format(e))


## ----------------------------------------------------------------------------
## 2. VARIABLES GLOBALES DE SESIÓN ACTIVA (DEFAULT)
## ----------------------------------------------------------------------------
default active_patient = None
default active_patient_id = ""
default patient_display_name = "Estudiante"
default temp_input_name = ""
default temp_input_age = 14
default temp_selected_gender = "chico"


## ----------------------------------------------------------------------------
## 3. PANTALLA: MENÚ PRINCIPAL PERSONALIZADO (REEMPLAZO DE MAIN_MENU)
## ----------------------------------------------------------------------------
## Esta pantalla sustituye por completo la pantalla main_menu original de Ren'Py.
screen main_menu():
    tag menu

    # Fondo clínico oscuro de AURA+
    add Solid("#0b1120")

    # Contenedor Central de Presentación
    vbox:
        align (0.5, 0.22)
        spacing 14

        text "AURA+":
            size 70
            bold True
            color "#38bdf8"
            xalign 0.5

        text "Sube de nivel, cuida tu mente.":
            size 26
            italic True
            color "#f1f5f9"
            xalign 0.5

        text "Programa digital de acompañamiento preventivo para el riesgo suicida en adolescentes":
            size 18
            color "#94a3b8"
            xalign 0.5

    # Acciones Principales Supervisadas por Terapeuta
    vbox:
        align (0.5, 0.65)
        spacing 18

        if active_patient:
            button:
                xsize 480
                ysize 60
                background Solid("#059669")
                hover_background Solid("#10b981")
                action Show("block_selector_screen")
                text "SELECCIONAR BLOQUE ([active_patient.name])":
                    align (0.5, 0.5)
                    size 18
                    bold True
                    color "#ffffff"

        # Botón protegido: exige PIN antes de acceder a los perfiles
        button:
            xsize 480
            ysize 60
            background Solid("#0284c7")
            hover_background Solid("#0369a1")
            action Show("therapist_keypad_modal", success_action=Show("patient_manager_screen"))
            text "ACCESO TERAPEUTA / GESTOR DE PACIENTES":
                align (0.5, 0.5)
                size 18
                bold True
                color "#ffffff"

        # Opciones de accesibilidad y sonido
        textbutton "Configuración y Accesibilidad":
            xalign 0.5
            text_size 18
            text_color "#94a3b8"
            text_hover_color "#ffffff"
            action ShowMenu("preferences")

        # Salir de la aplicación
        textbutton "Salir del Programa":
            xalign 0.5
            text_size 16
            text_color "#64748b"
            text_hover_color "#f87171"
            action Quit(confirm=True)

    # Pie de página con créditos clínicos
    frame:
        align (0.5, 0.96)
        background None
        text "AURA+ v1.0 | Protocolo Clínico y Supervisión Profesional de Salud Mental":
            size 13
            color "#475569"


## ----------------------------------------------------------------------------
## 4. PANTALLA: SELECTOR Y GESTOR DE PACIENTES (PATIENT_MANAGER_SCREEN)
## ----------------------------------------------------------------------------
screen patient_manager_screen():
    tag menu
    modal True

    add Solid("#070d19")

    vbox:
        align (0.5, 0.08)
        spacing 8

        text "PANEL DE GESTIÓN CLÍNICA DE PACIENTES":
            size 32
            bold True
            color "#38bdf8"
            xalign 0.5

        text "Seleccione un paciente registrado para continuar o cree un nuevo perfil de acompañamiento:":
            size 16
            color "#94a3b8"
            xalign 0.5

    # Contenedor en 2 columnas: Crear Nuevo vs Cargar Existente
    hbox:
        align (0.5, 0.55)
        spacing 40

        # Tarjeta 1: Crear Nuevo Perfil
        frame:
            xsize 440
            ysize 440
            padding (30, 30)
            background Solid("#0f172a")

            vbox:
                spacing 22
                align (0.5, 0.5)

                text "NUEVO PACIENTE":
                    size 24
                    bold True
                    color "#10b981"
                    xalign 0.5

                text "Permite dar de alta a un paciente adolescente. Solicitará nombre/apodo, edad y adaptación de lenguaje según su identidad de género.":
                    size 16
                    color "#cbd5e1"
                    justify True

                button:
                    xsize 320
                    ysize 55
                    xalign 0.5
                    background Solid("#059669")
                    hover_background Solid("#10b981")
                    action [
                        Hide("patient_manager_screen"),
                        Jump("wizard_crear_perfil")
                    ]
                    text "Crear Nuevo Perfil":
                        align (0.5, 0.5)
                        size 18
                        bold True
                        color "#ffffff"

        # Tarjeta 2: Cargar Perfil Existente (soporta N perfiles con Scroll)
        frame:
            xsize 620
            ysize 440
            padding (25, 25)
            background Solid("#0f172a")

            vbox:
                spacing 14
                text "PACIENTES REGISTRADOS":
                    size 24
                    bold True
                    color "#38bdf8"
                    xalign 0.5

                $ all_profiles = ProfileManager.get_all()

                if not all_profiles:
                    vbox:
                        align (0.5, 0.5)
                        spacing 10
                        text "No hay perfiles de pacientes guardados.":
                            size 16
                            color "#64748b"
                            xalign 0.5
                        text "Haga clic en 'Crear Nuevo Perfil' para registrar al primer paciente.":
                            size 14
                            color "#475569"
                            xalign 0.5
                else:
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        ysize 330

                        vbox:
                            spacing 10
                            for pid, pdata in all_profiles.items():
                                frame:
                                    xfill True
                                    padding (14, 12)
                                    background Solid("#1e293b")

                                    $ p_name = pdata.get('name', 'Anónimo')
                                    $ p_age = pdata.get('age', 14)
                                    $ p_gender = pdata.get('gender', 'chico').upper()
                                    $ p_sess = pdata.get('sessions_count', 0)
                                    $ p_last = pdata.get('last_session', 'Sin registro')

                                    hbox:
                                        vbox:
                                            spacing 3
                                            text "[p_name] ([p_age] años)":
                                                size 18
                                                bold True
                                                color "#f1f5f9"
                                            text "ID: [pid]  |  Género: [p_gender]  |  Sesiones: [p_sess]":
                                                size 13
                                                color "#94a3b8"
                                            text "Última sesión: [p_last]":
                                                size 12
                                                color "#64748b"

                                        button:
                                            align (1.0, 0.5)
                                            xsize 110
                                            ysize 42
                                            background Solid("#0284c7")
                                            hover_background Solid("#38bdf8")
                                            action [
                                                Hide("patient_manager_screen"),
                                                SetVariable("active_patient_id", pid),
                                                Jump("cargar_paciente_seleccionado")
                                            ]
                                            text "Cargar":
                                                align (0.5, 0.5)
                                                size 15
                                                bold True
                                                color "#ffffff"

    # Botón inferior para regresar al menú principal
    textbutton "← Volver a Pantalla de Inicio":
        align (0.5, 0.94)
        text_size 16
        text_color "#64748b"
        text_hover_color "#ffffff"
        action [Hide("patient_manager_screen"), Return()]


## ----------------------------------------------------------------------------
## 5. FLUJO DEL ASISTENTE (WIZARD) DE CREACIÓN Y CARGA DE PACIENTES
## ----------------------------------------------------------------------------

label wizard_crear_perfil:
    scene bg consultorio with fade

    "Iniciando el registro confidencial del paciente en el programa AURA+."

    # Paso 1: Captura de Nombre o Apodo
    python:
        temp_input_name = ""
        while not temp_input_name.strip():
            temp_input_name = renpy.input(
                "Ingrese el nombre o apodo con el que se identificará al participante:",
                default="",
                length=25
            ).strip()
            if not temp_input_name:
                renpy.notify("El nombre del paciente no puede estar en blanco.")

    # Paso 2: Captura de Edad con validación estricta (10 a 25 años)
    python:
        valid_age = False
        while not valid_age:
            age_raw = renpy.input(
                "Ingrese la edad del paciente en años cumplidos (ej. 14):",
                default="14",
                length=2
            ).strip()
            if age_raw.isdigit() and 10 <= int(age_raw) <= 25:
                temp_input_age = int(age_raw)
                valid_age = True
            else:
                renpy.notify("Por favor ingrese una edad válida entre 10 y 25 años.")

    # Paso 3: Selección de Género para adaptación lingüística dinámica
    menu:
        "Seleccione la identidad de género del paciente para adaptar el lenguaje y la gramática de AURA+:"
        "Chico (Masculino: bienvenido, amigo, él)":
            $ temp_selected_gender = "chico"
        "Chica (Femenino: bienvenida, amiga, ella)":
            $ temp_selected_gender = "chica"
        "No Binario (Inclusivo: bienvenide, amigue, elle)":
            $ temp_selected_gender = "no_binario"

    # Paso 4: Creación, Persistencia e Inicialización del Sistema
    python:
        new_profile = ProfileManager.create(
            name=temp_input_name,
            age=temp_input_age,
            gender=temp_selected_gender
        )
        ProfileManager.register_session_increment(new_profile.patient_id)
        active_patient = new_profile
        active_patient_id = new_profile.patient_id
        patient_display_name = new_profile.name

        # Inicializar el motor de flexión de género
        aplicar_genero_paciente(new_profile.gender)

        # Vincular con el motor de telemetría para registrar la sesión 1
        telemetria.start_session(active_patient, session_number=1)

    "Perfil clínico creado exitosamente: [active_patient.name] ([active_patient.patient_id])."
    "Configuración lingüística aplicada: [p_genero_nombre]."
    "Accediendo al selector de bloques de AURA+..."
    jump selector_bloques


label cargar_paciente_seleccionado:
    python:
        loaded_profile = ProfileManager.get(active_patient_id)
        if loaded_profile:
            ProfileManager.register_session_increment(active_patient_id)
            active_patient = loaded_profile
            patient_display_name = loaded_profile.name

            # Sincronizar género dinámico y telemetría
            aplicar_genero_paciente(active_patient.gender)
            telemetria.start_session(active_patient, session_number=active_patient.sessions_count)

    "Bienvenid[p_o] de nuevo al programa AURA+, [active_patient.name]."
    "Accediendo al selector de bloques de AURA+..."
    jump selector_bloques
