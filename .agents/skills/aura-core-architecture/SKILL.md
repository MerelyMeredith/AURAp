---
name: aura-core-architecture
description: >-
  Use this skill to design, structure, and maintain the base architecture of AURA+ in Ren'Py 8. Covers project file organization, separation of Python domain logic from Ren'Py screen and dialogue layers, state persistence rules (default vs define vs persistent), character declarations, and session lifecycle management.
---

# AURA+ Base Architecture & Engineering Standards

Esta habilidad define la arquitectura central, los patrones de diseño y las convenciones de programación para el proyecto **AURA+** en **Ren'Py 8** y **Python 3**.

---

## 1. Organización del Proyecto y Estructura de Directorios

Para mantener un proyecto escalable, mantenible y limpio, el código fuente dentro del directorio `game/` debe organizarse en módulos temáticos específicos:

```text
game/
├── audio/                          # Efectos de sonido (SFX), música (BGM) y ambiente
├── gui/                            # Assets gráficos de la interfaz de usuario
├── images/                         # Fondos (backgrounds) y sprites de personajes
│   ├── backgrounds/                # Escenarios (patio, aula, consultorio)
│   ├── characters/                 # Sprites de David, Ygritte, Geo
│   └── interactive/                # Íconos y botones para Point-and-Click
├── systems/                        # LÓGICA PURA DE PYTHON (init python)
│   ├── profiles.rpy                # Clases de Perfil y Gestor de Pacientes
│   ├── security.rpy                # Lógica de validación de PIN del terapeuta
│   ├── dynamic_gender.rpy          # Motor de flexión gramatical de género
│   └── telemetry.rpy               # Motor de telemetría y exportador CSV
├── screens/                        # CAPA VISUAL Y PANTALLAS (Screen Language)
│   ├── screen_auth.rpy             # Teclado numérico y PIN de terapeuta
│   ├── screen_profiles.rpy         # Pantalla principal y gestor de perfiles
│   ├── screen_exploration.rpy      # Pantallas Point-and-Click (patio, aula)
│   └── screen_minigames.rpy        # Minijuegos (Respiración 4x4)
├── scripts/                        # CAPA NARRATIVA (Labels, diálogos, menús)
│   ├── characters.rpy              # Declaración de personajes y estilos
│   ├── session_0.rpy               # Flujo completo de la Sesión 0
│   └── script.rpy                  # Punto de entrada y orquestador maestro
├── gui.rpy                         # Configuración base de la GUI de Ren'Py
├── options.rpy                     # Opciones del motor Ren'Py (1920x1080)
└── screens.rpy                     # Pantallas del sistema por defecto
```

---

## 2. Separación Estricta de Responsabilidades

El proyecto AURA+ divide su código en tres capas fundamentales:

```
+-------------------------------------------------------------+
|               1. CAPA DE DOMINIO (Python Puro)               |
|  - Clases: TelemetryManager, ProfileManager, GenderEngine    |
|  - Ejecución en: init python: o init python in aura_store:  |
|  - Sin dependencias directas de diálogos o pantallas        |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|          2. CAPA DE PRESENTACIÓN (Screen Language)          |
|  - screens: auth_pin, profile_selector, exploration_patio   |
|  - Eventos de usuario: Action, Show, Hide, Call             |
|  - Animaciones y efectos: ATL (Animation & Transform)       |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|           3. CAPA NARRATIVA (Labels y Diálogos)             |
|  - labels: start, session_0, interact_david, session_end    |
|  - Invocación de pantallas: call screen                     |
|  - Menús de decisiones clínicas: menu con telemetría        |
+-------------------------------------------------------------+
```

---

## 3. Reglas de Estado: `default`, `define` y `persistent`

El uso incorrecto de declaraciones en Ren'Py corrompe el sistema de guardado de partidas (*Save/Load*). En AURA+ se aplican las siguientes reglas sin excepción:

### A. Uso de `define` (Constantes e Inmutables)
- Se evalúa en tiempo de inicialización (`init`). **No se guarda en el archivo de guardado**.
- **Usar para**: Personajes (`Character`), constantes del sistema, configuraciones inmutables de UI, transformaciones ATL globales.
```renpy
# Correcto
define config.therapist_pin = "AURA2026"
define david = Character("David", color="#4ba3e3")
define ygritte = Character("Ygritte", color="#9b5de5")
define geo = Character("Geo", color="#2ec4b6")
```

### B. Uso de `default` (Variables Mutables del Juego)
- Se reinicia y se incluye en el estado de guardado de la partida (*savefile*).
- **Usar para**: Cualquier variable que cambie durante la sesión de un paciente (puntuaciones de rasgos, temporizadores de telemetría, variables de género activo, flags de exploración).
```renpy
# Correcto
default current_patient = None
default session_id = "SES-001"
default score_asertividad = 0
default score_agresividad = 0
default score_evitacion = 0
default score_amabilidad = 0
default contador_riesgo = 0
default aula_puerta_desbloqueada = False
```

### C. Uso de `persistent` (Datos Globales entre Sesiones)
- Persiste en el equipo independientemente de las partidas guardadas.
- **Usar para**: Registro global de perfiles creados por el terapeuta, configuraciones de accesibilidad y logs de auditoría del sistema.
```renpy
# Inicialización de persistencia
init python:
    if persistent.patient_registry is None:
        persistent.patient_registry = []
```

---

## 4. Declaración de Personajes y Diálogos

Los personajes centrales de AURA+ representan arquetipos de apoyo emocional e interacción terapéutica:

```renpy
## Archivo: game/scripts/characters.rpy

# Personajes del Sistema AURA+
define narrator = Character(None, what_italic=True)
define david = Character("David", color="#3a86ff", who_bold=True)
define ygritte = Character("Ygritte", color="#8338ec", who_bold=True)
define geo = Character("Geo", color="#ff006e", who_bold=True)
define terapeuta = Character("Terapeuta", color="#2a9d8f", who_bold=True)

# El personaje del Paciente se define dinámicamente con su nombre real
define p = DynamicCharacter("patient_display_name", color="#fb5607")
```

---

## 5. Ciclo de Vida de una Sesión Clínica

Toda sesión en AURA+ debe seguir rigurosamente este ciclo de vida:

```
[Inicio de la Aplicación]
           │
           ▼
[Pantalla de Autenticación de Terapeuta: PIN Gate]
           │ (Éxito)
           ▼
[Gestor de Perfiles: Crear Nuevo o Cargar Existente]
           │ (Selección)
           ▼
[Inicialización del Paciente & Motor de Género Dinámico]
           │
           ▼
[Inicialización de Telemetría: Registro Silencioso]
           │
           ▼
[Sesión Narrativa / Exploración Point-and-Click]
           │
           ▼
[Eventos de Decisión Crítica & Cronometraje de Latencia]
           │
           ▼
[Minijuego de Regulación Emocional: Ygritte Respiración 4x4]
           │
           ▼
[Cierre de Sesión: exportar_telemetria()]
           │
           ▼
[Retorno a Pantalla Principal o Salida Segura]
```

---

## 6. Pautas para Desarrolladores: Cómo Extender el Juego

1. **Añadir un Nuevo Menú de Decisión Clínica**:
   - Inicia siempre el temporizador antes de mostrar el menú: `$ telemetria.iniciar_decision("ID_DECISION")`.
   - En cada rama del menú, llama al registrador: `$ telemetria.registrar_opcion(...)`.
2. **Añadir un Nuevo Escenario Point-and-Click**:
   - Crea un archivo en `screens/` con nombre `screen_exploration_[nombre].rpy`.
   - Define los `imagebutton` con `focus_mask True` y transformaciones de brillo hover.
   - Usa `call screen [nombre]` desde el flujo del script para suspender la narrativa y permitir la exploración del paciente.
3. **Mantener la Compatibilidad de Género**:
   - Redacta todos los textos dirigidos al paciente usando los tags dinámicos: `amig[p_o]`, `bienvenid[p_o]`, `[p_art]`, `[p_pron]`.
