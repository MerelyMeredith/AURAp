## ============================================================================
## AURA+ | SISTEMA DE SEGURIDAD Y AUTENTICACIÓN DEL TERAPEUTA (PILAR 1)
## ============================================================================
## Este módulo implementa la barrera de seguridad clínica de AURA+.
## Garantiza que ningún paciente adolescente pueda iniciar o reanudar una sesión
## sin la presencia, autorización y supervisión directa del profesional de la salud.
## ============================================================================

init offset = -2

## ----------------------------------------------------------------------------
## 1. CONFIGURACIÓN Y CONSTANTES DE SEGURIDAD
## ----------------------------------------------------------------------------
## Claves autorizadas de acceso para el profesional de la salud mental:
define therapist_pin_primary = "AURA2026"
define therapist_pin_secondary = "1234"

## Variables de estado mutables para la interfaz de ingreso de PIN
default therapist_authenticated = False
default pin_input_buffer = ""
default auth_error_message = ""
default auth_attempts = 0

## ----------------------------------------------------------------------------
## 2. LÓGICA DE VALIDACIÓN EN PYTHON PURO
## ----------------------------------------------------------------------------
init -2 python:
    def submit_therapist_pin(success_action):
        """
        Valida el PIN ingresado por el terapeuta al hacer clic en 'Entrar' o presionar Enter.
        IMPORTANTE: Solo se ejecuta al confirmar, nunca en tiempo de render de pantalla.
        """
        global therapist_authenticated, auth_error_message, pin_input_buffer, auth_attempts

        pin_clean = pin_input_buffer.strip()
        if pin_clean in (therapist_pin_primary, therapist_pin_secondary):
            therapist_authenticated = True
            auth_error_message = ""
            pin_input_buffer = ""
            auth_attempts = 0
            renpy.hide_screen("therapist_keypad_modal")
            renpy.run(success_action)
        else:
            therapist_authenticated = False
            auth_attempts += 1
            auth_error_message = "PIN Incorrecto. Acceso Restringido a Profesionales de la Salud."
            pin_input_buffer = ""
            renpy.restart_interaction()

    def append_pin_digit(digit):
        """Añade un dígito o carácter al búfer sin validar prematuramente."""
        global pin_input_buffer, auth_error_message
        auth_error_message = ""
        if len(pin_input_buffer) < 12:
            pin_input_buffer += str(digit)
            renpy.restart_interaction()

    def backspace_pin_digit():
        """Elimina el último dígito ingresado."""
        global pin_input_buffer, auth_error_message
        auth_error_message = ""
        if len(pin_input_buffer) > 0:
            pin_input_buffer = pin_input_buffer[:-1]
            renpy.restart_interaction()

    def clear_pin_buffer():
        """Limpia el búfer y el mensaje de error."""
        global pin_input_buffer, auth_error_message
        pin_input_buffer = ""
        auth_error_message = ""
        renpy.restart_interaction()


## ----------------------------------------------------------------------------
## 3. PANTALLA: TECLADO NUMÉRICO MODAL (KEYPAD DEL TERAPEUTA)
## ----------------------------------------------------------------------------
## Esta pantalla modal se superpone antes de crear un nuevo paciente o cargar uno.
## Recibe como parámetro la acción a ejecutar si la validación es exitosa.
screen therapist_keypad_modal(success_action):
    modal True
    zorder 100

    # Atajos de teclado físico para mayor comodidad del terapeuta
    key "K_RETURN" action Function(submit_therapist_pin, success_action)
    key "K_KP_ENTER" action Function(submit_therapist_pin, success_action)
    key "K_BACKSPACE" action Function(backspace_pin_digit)

    key "1" action Function(append_pin_digit, "1")
    key "2" action Function(append_pin_digit, "2")
    key "3" action Function(append_pin_digit, "3")
    key "4" action Function(append_pin_digit, "4")
    key "5" action Function(append_pin_digit, "5")
    key "6" action Function(append_pin_digit, "6")
    key "7" action Function(append_pin_digit, "7")
    key "8" action Function(append_pin_digit, "8")
    key "9" action Function(append_pin_digit, "9")
    key "0" action Function(append_pin_digit, "0")

    key "K_KP1" action Function(append_pin_digit, "1")
    key "K_KP2" action Function(append_pin_digit, "2")
    key "K_KP3" action Function(append_pin_digit, "3")
    key "K_KP4" action Function(append_pin_digit, "4")
    key "K_KP5" action Function(append_pin_digit, "5")
    key "K_KP6" action Function(append_pin_digit, "6")
    key "K_KP7" action Function(append_pin_digit, "7")
    key "K_KP8" action Function(append_pin_digit, "8")
    key "K_KP9" action Function(append_pin_digit, "9")
    key "K_KP0" action Function(append_pin_digit, "0")

    # Fondo oscurecido
    add Solid("#090d16ee")

    frame:
        align (0.5, 0.5)
        xsize 540
        padding (35, 30)
        background Solid("#161f30")

        vbox:
            spacing 18
            align (0.5, 0.5)

            # Encabezado Clínico de Seguridad
            text "AUTORIZACIÓN PROFESIONAL":
                size 24
                bold True
                xalign 0.5
                color "#38bdf8"

            text "Ingrese el PIN de supervisión clínica (puede usar el teclado físico o en pantalla):":
                size 15
                color "#94a3b8"
                xalign 0.5
                justify True

            # Display visual con asteriscos según la cantidad de dígitos ingresados
            frame:
                xsize 440
                ysize 52
                background Solid("#0f172a")
                align (0.5, 0.5)

                if pin_input_buffer:
                    text ("* " * len(pin_input_buffer)):
                        align (0.5, 0.5)
                        size 26
                        bold True
                        color "#38bdf8"
                else:
                    text "Ingrese PIN (ej. 1234 o AURA2026)":
                        align (0.5, 0.5)
                        size 16
                        color "#475569"

            # Mensaje de error visible si el PIN falló al presionar Entrar
            if auth_error_message:
                frame:
                    background Solid("#450a0a")
                    padding (10, 6)
                    align (0.5, 0.5)
                    text auth_error_message:
                        color "#f87171"
                        size 14
                        bold True
                        xalign 0.5

            # Teclado Numérico en Grid 3x4
            grid 3 4:
                spacing 12
                xalign 0.5

                # Dígitos del 1 al 9
                for digit in range(1, 10):
                    textbutton str(digit):
                        xsize 110
                        ysize 58
                        background Solid("#1e293b")
                        hover_background Solid("#0284c7")
                        text_align (0.5, 0.5)
                        text_size 24
                        text_bold True
                        text_color "#f1f5f9"
                        action Function(append_pin_digit, str(digit))

                # Botón de Borrar (retroceso)
                textbutton "← Borrar":
                    xsize 110
                    ysize 58
                    background Solid("#334155")
                    hover_background Solid("#e11d48")
                    text_align (0.5, 0.5)
                    text_size 16
                    text_color "#f8fafc"
                    action Function(backspace_pin_digit)

                # Dígito 0
                textbutton "0":
                    xsize 110
                    ysize 58
                    background Solid("#1e293b")
                    hover_background Solid("#0284c7")
                    text_align (0.5, 0.5)
                    text_size 24
                    text_bold True
                    text_color "#f1f5f9"
                    action Function(append_pin_digit, "0")

                # Botón de Validación / Entrar
                textbutton "Entrar":
                    xsize 110
                    ysize 58
                    background Solid("#059669")
                    hover_background Solid("#10b981")
                    text_align (0.5, 0.5)
                    text_size 18
                    text_bold True
                    text_color "#ffffff"
                    action Function(submit_therapist_pin, success_action)

            # Opciones de acceso rápido para pruebas o terapeuta
            hbox:
                align (0.5, 0.5)
                spacing 15
                textbutton "Autocompletar '1234'":
                    text_size 14
                    text_color "#38bdf8"
                    action [
                        SetVariable("pin_input_buffer", "1234")
                    ]
                textbutton "Autocompletar 'AURA2026'":
                    text_size 14
                    text_color "#38bdf8"
                    action [
                        SetVariable("pin_input_buffer", "AURA2026")
                    ]

            # Botón de Cancelación y retorno seguro
            textbutton "Cancelar y Volver":
                xalign 0.5
                text_size 15
                text_color "#64748b"
                text_hover_color "#f1f5f9"
                action [Function(clear_pin_buffer), Hide("therapist_keypad_modal")]
