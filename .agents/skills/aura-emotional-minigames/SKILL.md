---
name: aura-emotional-minigames
description: >-
  Use this skill to design, program, and calibrate therapeutic emotional regulation minigames in Ren'Py 8 for AURA+. Focuses on the Ygritte 4x4 Square Breathing (Box Breathing) mechanic with smooth ATL transforms, synchronized timers, visual biofeedback, and returning control to narrative dialogues, as well as guidelines for future clinical regulation activities.
---

# AURA+ Minijuegos de Regulación Emocional (Respiración 4x4 de Ygritte)

Esta habilidad documenta el diseño, la justificación clínica y la implementación técnica de los **Minijuegos de Regulación Emocional**, en particular la técnica de **Respiración Cuadrada (4x4 Box Breathing)** guiada por Ygritte en Ren'Py 8.

---

## 1. Justificación Clínica: La Respiración 4x4 (Box Breathing)

1. **Desactivación del Sistema Nervioso Simpático**: Ante situaciones de estrés escolar, angustia o ideación reactiva, la amígdala cerebral se hiperactiva. La respiración 4x4 estimula el nervio vago y activa el sistema parasimpático, disminuyendo la frecuencia cardíaca y la tensión muscular.
2. **Estructura de las 4 Fases**:
   - **Fase 1: Inhalar** (4 segundos) -> Expansión pulmonar controlada.
   - **Fase 2: Retener / Sostener** (4 segundos) -> Oxigenación y quietud interna.
   - **Fase 3: Exhalar** (4 segundos) -> Liberación suave de tensión.
   - **Fase 4: Sostener en vacío** (4 segundos) -> Estabilización neurofisiológica.
3. **Rol de Ygritte**: Ygritte no juzga ni presiona; actúa como ancla de seguridad, modulando la voz y marcando el ritmo con afecto y calidez.

---

## 2. Animaciones ATL para el Biofeedback Visual (`screens/screen_minigames.rpy`)

Se utiliza una figura geométrica suave (un círculo luminoso o flor de calma) que se expande durante la inhalación y se contrae durante la exhalación:

```renpy
init offset = -1

## Transformación ATL de Respiración 4x4
## Cada ciclo dura exactamente 16 segundos (4s + 4s + 4s + 4s)
transform breath_circle_animation:
    subpixel True
    xalign 0.5 yalign 0.5
    zoom 0.5 alpha 0.6

    # 1. Inhalar (4s): Expande y aumenta luminosidad
    easein 4.0 zoom 1.0 alpha 1.0

    # 2. Retener (4s): Mantener pulso sutil en máxima expansión
    ease 2.0 zoom 1.02
    ease 2.0 zoom 1.0

    # 3. Exhalar (4s): Contrae suavemente
    easeout 4.0 zoom 0.5 alpha 0.6

    # 4. Retener en vacío (4s): Reposo en quietud
    pause 4.0

    repeat
```

---

## 3. Pantalla de la Respiración 4x4 (`screen_respiracion_4x4`)

Se implementa una pantalla interactiva con máquina de estados basada en `timer` de Ren'Py:

```renpy
## Variables de control del minijuego
default breath_phase = 0          # 0: Inhala, 1: Sostén, 2: Exhala, 3: Sostén
default breath_phase_text = "Inhala suavemente por la nariz..."
default breath_seconds_left = 4
default breath_cycles_completed = 0
default breath_target_cycles = 3

screen minijuego_respiracion_4x4(target_cycles=3):
    modal True
    zorder 100

    # Fondo calmante oscuro / gradiente terapéutico
    add Solid("#0b1320")

    # Partículas o resplandor ambiental
    frame:
        align (0.5, 0.45)
        xsize 600
        ysize 600
        background None

        # Elemento visual expansivo animado
        add "images/interactive/breath_orb.png" at breath_circle_animation

    # Panel de Texto Guía de Ygritte
    vbox:
        align (0.5, 0.12)
        spacing 12

        text "Ygritte te acompaña":
            size 28
            bold True
            color "#a78bfa"
            xalign 0.5

        text "[breath_phase_text]":
            size 32
            bold True
            color "#f8fafc"
            xalign 0.5

        text "Cuenta: [breath_seconds_left] s":
            size 24
            color "#38bdf8"
            xalign 0.5

        text "Ciclo [breath_cycles_completed + 1] de [target_cycles]":
            size 16
            color "#94a3b8"
            xalign 0.5

    # Temporizador de 1 segundo para sincronizar la interfaz
    timer 1.0 repeat True action Function(update_breath_phase, target_cycles)

    # Botón accesible para terminar o pausar si el paciente se siente incómodo
    textbutton "Me siento mejor (Terminar ejercicio)":
        align (0.5, 0.92)
        text_color "#64748b"
        text_hover_color "#f8fafc"
        action [
            Function(finalizar_respiracion_exitosa),
            Return()
        ]
```

---

## 4. Lógica de Sincronización en Python (`systems/respiracion_logic.rpy`)

Se maneja la transición de fases y conteo de segundos:

```renpy
init python:
    def update_breath_phase(target_cycles=3):
        global breath_phase, breath_phase_text, breath_seconds_left, breath_cycles_completed

        breath_seconds_left -= 1

        if breath_seconds_left <= 0:
            breath_seconds_left = 4
            breath_phase = (breath_phase + 1) % 4

            if breath_phase == 0:
                breath_cycles_completed += 1
                if breath_cycles_completed >= target_cycles:
                    finalizar_respiracion_exitosa()
                    renpy.return_statement()
                    return

            # Actualizar mensajes de apoyo de Ygritte
            if breath_phase == 0:
                breath_phase_text = "Inhala despacio por la nariz... Siente cómo se expande tu pecho."
                renpy.play("audio/inhale.ogg", channel="sound")
            elif breath_phase == 1:
                breath_phase_text = "Sostén el aire con calma... No hay prisa."
            elif breath_phase == 2:
                breath_phase_text = "Exhala suavemente por la boca... Suelta toda la tensión."
                renpy.play("audio/exhale.ogg", channel="sound")
            elif breath_phase == 3:
                breath_phase_text = "Mantén el vacío unos segundos... Estás a salvo aquí."

    def finalizar_respiracion_exitosa():
        global breath_cycles_completed, breath_phase, breath_seconds_left
        # Registrar en la telemetría que el paciente completó la regulación
        if "telemetria" in renpy.store.__dict__:
            renpy.store.telemetria.registrar_decision(
                choice_text="Completó minijuego Respiración 4x4 ({} ciclos)".format(breath_cycles_completed),
                asertividad=+1,
                amabilidad=+1,
                is_risk=False
            )
        breath_phase = 0
        breath_seconds_left = 4
        breath_cycles_completed = 0
```

---

## 5. Invocación de Ygritte en el Flujo de la Narrativa

Cuando la tensión del paciente se eleva (por ejemplo, tras una discusión con compañeros o ante una decisión estresante), Ygritte interviene:

```renpy
label intervencion_ygritte_respiracion:
    scene bg_aula with dissolve

    show ygritte empática at center with dissolve

    ygritte "Espera un momento, [active_patient.name]..."
    ygritte "Puedo ver la tensión en tus hombros y cómo se acelera tu pulso. No tienes que responder ahora mismo."
    ygritte "Recuerda lo que practicamos: la técnica de respiración 4x4. Vamos a hacerla juntos durante unos instantes."
    ygritte "Sigue el ritmo de la luz: cuatro segundos para inhalar, cuatro para sostener, cuatro para soltar, y cuatro para descansar."

    # Se llama a la pantalla modal interactiva
    call screen minijuego_respiracion_4x4(target_cycles=3)

    # Retorno seguro a la narrativa tras completar el ejercicio
    show ygritte sonriendo at center with dissolve
    ygritte "Muy bien hecho. Respira normal ahora."
    ygritte "¿Sientes cómo tu cuerpo recupera su centro? Eso es. Tú tienes el control de tu respiración."
    ygritte "Ahora que tu mente está más despejada, volvamos con David."

    return
```

---

## 6. Framework para Añadir Futuros Minijuegos de Regulación

Para expandir AURA+ con nuevas herramientas terapéuticas (ej. Anclaje 5-4-3-2-1 o Termómetro Emocional):
1. **Regla de No Frustración**: Los minijuegos terapéuticos **nunca tienen condición de 'Game Over'**. El objetivo no es ganar puntos ni competir, sino modular el estado fisiológico.
2. **Salida Voluntaria Siempre Disponible**: Proveer un botón discreto ("Terminar ejercicio") para que el paciente nunca se sienta atrapado.
3. **Registro Automático en Telemetría**: Registrar siempre si el paciente completó la técnica, el tiempo dedicado y si hubo interrupción temprana.
