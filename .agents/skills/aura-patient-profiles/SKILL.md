---
name: aura-patient-profiles
description: >-
  Use this skill to implement, modify, or extend the AURA+ Patient Management & Therapist Security System. Covers overriding the default main_menu, PIN pad therapist security authentication, patient profile creation wizard (Name, Age, Gender with renpy.input), and persistent profile storage via JSON and persistent.patient_profiles.
---

# AURA+ Sistema de Perfiles y Seguridad de Acceso para Profesionales

Esta habilidad detalla la implementación y arquitectura del **Sistema de Perfiles y Seguridad (Login/Gestor de Pacientes)** en Ren'Py 8.

---

## 1. Principios Clínicos y de Seguridad

AURA+ es una herramienta de intervención preventiva en salud mental para adolescentes. Por protocolo clínico:
1. **Acceso Exclusivo del Terapeuta**: El paciente jamás debe iniciar o reanudar una sesión de forma autónoma. Un profesional de la salud debe desbloquear el juego mediante una contraseña o PIN de seguridad.
2. **Identificación y Trazabilidad**: Cada paciente cuenta con su propia ficha (ID único, Nombre, Edad, Género, fecha de registro e historial de sesiones).
3. **Persistencia Dual**: Los perfiles se almacenan tanto en `persistent.patient_profiles` como en un archivo JSON local (`profiles.json`) para facilitar respaldos y auditorías externas.

---

## 2. Capa de Dominio en Python (`systems/profiles.rpy`)

Se define la estructura de datos orientada a objetos en Python puro:

```renpy
init -2 python:
    import json
    import os
    import time
    from datetime import datetime

    class PatientProfile(object):
        """Representa el perfil clínico de un paciente en AURA+."""
        def __init__(self, patient_id, name, age, gender):
            self.patient_id = patient_id
            self.name = name.strip()
            self.age = int(age)
            # gender: 'chico', 'chica', 'no_binario'
            self.gender = gender.lower()
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.sessions_count = 0
            self.last_session = None

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
            p = cls(data["patient_id"], data["name"], data["age"], data["gender"])
            p.created_at = data.get("created_at", "")
            p.sessions_count = data.get("sessions_count", 0)
            p.last_session = data.get("last_session", None)
            return p


    class ProfileManager(object):
        """Gestor de persistencia de perfiles de pacientes."""
        PROFILES_FILE = "patient_profiles.json"

        @classmethod
        def get_all_profiles(cls):
            """Obtiene la lista de perfiles guardados."""
            if persistent.patient_profiles is None:
                persistent.patient_profiles = {}
            return persistent.patient_profiles

        @classmethod
        def create_profile(cls, name, age, gender):
            """Crea y persiste un nuevo paciente."""
            all_p = cls.get_all_profiles()
            new_id = "PAC-{:04d}".format(len(all_p) + 1)
            profile = PatientProfile(new_id, name, age, gender)
            all_p[new_id] = profile.to_dict()
            renpy.save_persistent()
            cls.export_to_json()
            return profile

        @classmethod
        def get_profile(cls, patient_id):
            all_p = cls.get_all_profiles()
            data = all_p.get(patient_id)
            if data:
                return PatientProfile.from_dict(data)
            return None

        @classmethod
        def update_session(cls, patient_id):
            all_p = cls.get_all_profiles()
            if patient_id in all_p:
                all_p[patient_id]["sessions_count"] += 1
                all_p[patient_id]["last_session"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                renpy.save_persistent()
                cls.export_to_json()

        @classmethod
        def export_to_json(cls):
            try:
                base_dir = config.basedir
                filepath = os.path.join(base_dir, cls.PROFILES_FILE)
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(persistent.patient_profiles, f, ensure_ascii=False, indent=2)
            except Exception as e:
                renpy.log("Error exportando perfiles JSON: {}".format(e))
```

---

## 3. Seguridad Hardcodeada: Teclado Numérico y Validación de PIN

Se define el PIN del terapeuta y el gestor de validación:

```renpy
## Archivo: game/systems/security.rpy

define config.therapist_pin = "AURA2026"  # También puede ser "1234"
default therapist_authenticated = False
default pin_input_buffer = ""
default auth_error_message = ""

init python:
    def verify_therapist_pin(entered_pin):
        """Valida el PIN ingresado contra la clave de seguridad del terapeuta."""
        global therapist_authenticated, auth_error_message, pin_input_buffer
        if entered_pin.strip() == config.therapist_pin:
            therapist_authenticated = True
            auth_error_message = ""
            pin_input_buffer = ""
            return True
        else:
            therapist_authenticated = False
            auth_error_message = "PIN Incorrecto. Acceso Restringido a Profesionales."
            pin_input_buffer = ""
            renpy.play("audio/denied.ogg", channel="sound")
            return False

    def append_pin_digit(digit):
        global pin_input_buffer
        if len(pin_input_buffer) < 8:
            pin_input_buffer += str(digit)

    def clear_pin():
        global pin_input_buffer, auth_error_message
        pin_input_buffer = ""
        auth_error_message = ""
```

### Pantalla del Teclado Numérico (`screens/screen_auth.rpy`):

```renpy
screen therapist_keypad_modal(success_action):
    modal True
    zorder 100
    style_prefix "keypad"

    add Solid("#000000cc")

    frame:
        align (0.5, 0.5)
        xsize 480
        padding (30, 30)

        vbox:
            spacing 15
            align (0.5, 0.5)

            text "Autorización Profesional":
                size 26
                bold True
                xalign 0.5
                color "#3a86ff"

            text "Ingrese la clave de seguridad de terapeuta":
                size 16
                color "#cccccc"
                xalign 0.5

            # Display visual de caracteres ingresados
            frame:
                xsize 400
                ysize 50
                background Solid("#22222b")
                align (0.5, 0.5)
                text ("*" * len(pin_input_buffer) if pin_input_buffer else "Ingrese PIN"):
                    align (0.5, 0.5)
                    size 24
                    color ("#ffffff" if pin_input_buffer else "#666666")

            if auth_error_message:
                text auth_error_message:
                    color "#ff4d4d"
                    size 14
                    xalign 0.5

            # Teclado Numérico en Grid 3x4
            grid 3 4:
                spacing 10
                xalign 0.5

                for i in range(1, 10):
                    textbutton str(i):
                        action Function(append_pin_digit, str(i))
                        xsize 90
                        ysize 60

                textbutton "Borrar":
                    action Function(clear_pin)
                    xsize 90
                    ysize 60

                textbutton "0":
                    action Function(append_pin_digit, "0")
                    xsize 90
                    ysize 60

                textbutton "Entrar":
                    action If(
                        verify_therapist_pin(pin_input_buffer),
                        [Hide("therapist_keypad_modal"), success_action],
                        NullAction()
                    )
                    xsize 90
                    ysize 60

            textbutton "Cancelar":
                xalign 0.5
                action [Function(clear_pin), Hide("therapist_keypad_modal")]
```

---

## 4. Reemplazo del Menú Principal (`main_menu`)

Para garantizar que el juego inicie directamente en el panel clínico de AURA+, se sobrescribe la pantalla `main_menu` en `screens/screen_profiles.rpy`:

```renpy
screen main_menu():
    tag menu

    # Fondo clínico / terapéutico de AURA+
    add Solid("#121824")

    vbox:
        align (0.5, 0.2)
        spacing 10
        text "AURA+":
            size 64
            bold True
            color "#4ba3e3"
            xalign 0.5
        text "Acompañamiento Digital y Regulación Emocional Preventiva":
            size 20
            color "#90a4ae"
            xalign 0.5

    vbox:
        align (0.5, 0.6)
        spacing 25

        textbutton "Iniciar Sesión de Paciente":
            xalign 0.5
            text_size 24
            action Show("therapist_keypad_modal", success_action=Show("patient_manager_screen"))

        textbutton "Configuración / Opciones":
            xalign 0.5
            action ShowMenu("preferences")

        textbutton "Salir del Programa":
            xalign 0.5
            action Quit(confirm=True)
```

---

## 5. Pantalla del Gestor de Pacientes (`patient_manager_screen`)

Permite seleccionar entre **Crear Nuevo Perfil** o **Cargar Perfil Existente**:

```renpy
screen patient_manager_screen():
    tag menu
    modal True

    add Solid("#0d131f")

    vbox:
        align (0.5, 0.1)
        spacing 10
        text "Panel de Gestión de Pacientes":
            size 36
            bold True
            color "#ffffff"
            xalign 0.5
        text "Seleccione un paciente existente o registre uno nuevo para comenzar":
            size 18
            color "#78909c"
            xalign 0.5

    hbox:
        align (0.5, 0.55)
        spacing 40

        # Tarjeta 1: Crear Nuevo Perfil
        frame:
            xsize 420
            ysize 400
            padding (25, 25)
            background Solid("#1b2434")

            vbox:
                spacing 20
                align (0.5, 0.5)
                text "Nuevo Paciente":
                    size 24
                    bold True
                    color "#2ec4b6"
                    xalign 0.5
                text "Registra Nombre, Edad y Género para personalizar las sesiones e iniciar la telemetría clínica.":
                    size 16
                    color "#b0bec5"
                    justify True
                textbutton "Crear Perfil":
                    xalign 0.5
                    action [Hide("patient_manager_screen"), Jump("wizard_crear_perfil")]

        # Tarjeta 2: Cargar Perfil Existente
        frame:
            xsize 520
            ysize 400
            padding (25, 25)
            background Solid("#1b2434")

            vbox:
                spacing 15
                text "Pacientes Registrados":
                    size 24
                    bold True
                    color "#3a86ff"
                    xalign 0.5

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    ysize 260

                    vbox:
                        spacing 10
                        $ profiles_dict = ProfileManager.get_all_profiles()
                        if not profiles_dict:
                            text "No hay perfiles registrados en el sistema.":
                                size 16
                                color "#78909c"
                                xalign 0.5
                        else:
                            for pid, pdata in profiles_dict.items():
                                frame:
                                    xfill True
                                    padding (10, 10)
                                    background Solid("#253248")
                                    hbox:
                                        vbox:
                                            text "[pdata['name']] ([pdata['age']] años)":
                                                size 18
                                                bold True
                                                color "#ffffff"
                                            text "ID: [pid] | Género: [pdata['gender']] | Sesiones: [pdata['sessions_count']]":
                                                size 13
                                                color "#90a4ae"
                                        textbutton "Cargar":
                                            align (1.0, 0.5)
                                            action [
                                                Hide("patient_manager_screen"),
                                                Function(ProfileManager.update_session, pid),
                                                SetVariable("active_patient_id", pid),
                                                Jump("cargar_paciente_seleccionado")
                                            ]

    textbutton "Volver al Menú Principal":
        align (0.5, 0.92)
        action [Hide("patient_manager_screen"), Return()]
```

---

## 6. Wizard de Creación de Perfil con `renpy.input`

Flujo narrativo seguro para la captura de datos:

```renpy
## Archivo: game/scripts/wizard_perfil.rpy

default temp_patient_name = ""
default temp_patient_age = 15
default temp_patient_gender = "chico"
default active_patient = None

label wizard_crear_perfil:
    scene bg_consultorio with fade

    "Iniciando registro de nuevo paciente adolescente en el sistema AURA+."

    # 1. Captura de Nombre
    python:
        temp_patient_name = ""
        while not temp_patient_name.strip():
            temp_patient_name = renpy.input("Ingrese el nombre o apodo del paciente:", length=20).strip()
            if not temp_patient_name:
                renpy.notify("El nombre no puede quedar vacío.")

    # 2. Captura de Edad con validación
    python:
        valid_age = False
        while not valid_age:
            age_str = renpy.input("Ingrese la edad del paciente (12 a 18 años):", length=2).strip()
            if age_str.isdigit() and 10 <= int(age_str) <= 25:
                temp_patient_age = int(age_str)
                valid_age = True
            else:
                renpy.notify("Por favor ingrese una edad válida en formato numérico.")

    # 3. Selección de Género
    menu:
        "Seleccione la identidad de género del paciente para adaptar el lenguaje y la gramática del programa:"
        "Chico (Masculino: bienvenido, amigo)":
            $ temp_patient_gender = "chico"
        "Chica (Femenino: bienvenida, amiga)":
            $ temp_patient_gender = "chica"
        "No Binario (Inclusivo: bienvenide, amigue)":
            $ temp_patient_gender = "no_binario"

    # 4. Creación y Persistencia del Perfil
    python:
        new_profile = ProfileManager.create_profile(
            temp_patient_name,
            temp_patient_age,
            temp_patient_gender
        )
        ProfileManager.update_session(new_profile.patient_id)
        active_patient = new_profile

        # Aplicar el género dinámico
        aplicar_genero_paciente(temp_patient_gender)

    "Perfil registrado con éxito: [temp_patient_name] (ID: [active_patient.patient_id])."
    "Iniciando Sesión 0 con supervisión clínica..."
    jump session_0

label cargar_paciente_seleccionado:
    python:
        active_patient = ProfileManager.get_profile(active_patient_id)
        aplicar_genero_paciente(active_patient.gender)

    "Bienvenido/a de regreso, [active_patient.name]."
    "Cargando sesión supervisada de AURA+..."
    jump session_0
```
