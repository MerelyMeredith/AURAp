## ============================================================================
## AURA+ | ACTORES, EMOCIONES ANIME/MANGA Y CUADRÍCULA 192x108
## ============================================================================
## Este módulo define:
## 1. El sistema de cuadrícula matemática estricta de 192x108 celdas
##    (1 celda de cuadrícula = exactamente 10x10 píxeles a resolución 1920x1080)
##    garantizando que el arte pixel-art nunca se desfase ni sufra interpolación borrosa.
## 2. Los actores y sus estados emocionales (Geo, David, Ygritte).
## 3. Animaciones expresivas y efectos visuales estilo Anime / Manga / Manwha:
##    - Gotita de sudor (sweat drop / apuro o vergüenza)
##    - Temblor de shock / sorpresa (anime shock)
##    - Salto de entusiasmo (anime hop)
##    - Venita de exasperación (anime vein)
##    - Destellos de aliento (anime sparkles)
##    - Signos de interrogación y exclamación flotantes
## ============================================================================

init offset = -3

## ----------------------------------------------------------------------------
## 1. SISTEMA DE CUADRÍCULA ESTRICTA DE 192x108 (PIXEL ART GRID SYSTEM)
## ----------------------------------------------------------------------------
init -3 python:
    def grid_px(units):
        """Convierte unidades de cuadrícula (192x108) a píxeles exactos (1920x1080)."""
        return int(units * 10)

    def grid_pos(gx, gy):
        """Retorna tupla (x, y) en píxeles alineada estrictamente a la cuadrícula."""
        return (int(gx * 10), int(gy * 10))

    def snap_grid(pixels):
        """Ajusta cualquier dimensión o coordenada al múltiplo de 10 más cercano."""
        return int(round(pixels / 10.0) * 10)


## ----------------------------------------------------------------------------
## 2. POSICIONES CANÓNICAS DE LOS ACTORES EN CUADRÍCULA 192x108
## ----------------------------------------------------------------------------
## Se desactiva el subpíxel (subpixel False) para preservar los bordes nítidos de pixel art.

transform grid_pos_left:
    pos (200, 220)       # Cuadrícula: gx=20, gy=22
    subpixel False

transform grid_pos_center:
    pos (720, 220)       # Cuadrícula: gx=72, gy=22
    subpixel False

transform grid_pos_right:
    pos (1240, 220)      # Cuadrícula: gx=124, gy=22
    subpixel False

transform grid_david_front:
    pos (720, 180)       # Cuadrícula: gx=72, gy=18 (sentado al frente del jugador)
    subpixel False


## ----------------------------------------------------------------------------
## 3. ANIMACIONES ATL ESTILO ANIME / MANGA / MANWHA
## ----------------------------------------------------------------------------

## Salto elástico de emoción o saludo (Hop)
transform anime_hop:
    subpixel False
    easein 0.12 yoffset -30
    easeout 0.12 yoffset 0
    easein 0.08 yoffset -10
    easeout 0.08 yoffset 0

## Temblor rápido de shock / sobresalto ante noticias inesperadas
transform anime_shock:
    subpixel False
    easein 0.03 xoffset -20
    easeout 0.03 xoffset 20
    easein 0.03 xoffset -10
    easeout 0.03 xoffset 10
    easein 0.03 xoffset -5
    easeout 0.03 xoffset 5
    easeout 0.05 xoffset 0

## Balanceo suave de nerviosismo o duda
transform anime_nervous_sway:
    subpixel False
    easein 0.35 xoffset -10
    easeout 0.35 xoffset 10
    easein 0.25 xoffset -5
    easeout 0.25 xoffset 5
    easeout 0.15 xoffset 0

## Entrada con rebote elástico (Pop-in estilo Manwha)
transform anime_pop_in:
    subpixel False
    zoom 0.88 alpha 0.0
    easein 0.15 zoom 1.04 alpha 1.0
    easeout 0.10 zoom 1.0

## Caída de la gota de sudor (Sweat drop)
transform anime_sweatdrop_anim:
    subpixel False
    alpha 0.0 yoffset 0
    easein 0.10 alpha 1.0
    easeout 0.70 yoffset 40
    easeout 0.25 alpha 0.0

## Palpitación de venita de enojo / apuro (Anger vein)
transform anime_vein_pulse:
    subpixel False
    zoom 0.9
    easein 0.15 zoom 1.3
    easeout 0.15 zoom 0.9
    easein 0.15 zoom 1.3
    easeout 0.15 zoom 0.9
    repeat 2

## Flotación de emoticono superior (Signo ! o ?)
transform anime_float_icon:
    subpixel False
    alpha 0.0 yoffset 10
    easein 0.12 alpha 1.0 yoffset -20
    pause 0.60
    easeout 0.25 alpha 0.0 yoffset -40

## Destello de estrellas / optimismo
transform anime_sparkle_anim:
    subpixel False
    zoom 0.5 alpha 0.0
    easein 0.2 zoom 1.2 alpha 1.0
    easeout 0.2 zoom 0.9 alpha 0.8
    easeout 0.3 alpha 0.0


## ----------------------------------------------------------------------------
## 4. EMOTICONOS Y SÍMBOLOS EXPRESIVOS VISUALES (EMOTE OVERLAYS)
## ----------------------------------------------------------------------------
## Gráficos generados mediante Displayables con dimensiones
## de cuadrícula exacta para acompañar a los actores en sus cambios de humor.

image anime_sweatdrop:
    Solid("#38bdf8", xsize=30, ysize=40)
    subpixel False
    alpha 0.0 yoffset 0
    easein 0.10 alpha 1.0
    easeout 0.70 yoffset 40
    easeout 0.25 alpha 0.0

image anime_exclamation:
    Solid("#facc15", xsize=20, ysize=50)
    subpixel False
    alpha 0.0 yoffset 10
    easein 0.12 alpha 1.0 yoffset -20
    pause 0.60
    easeout 0.25 alpha 0.0 yoffset -40

image anime_question_mark:
    Solid("#c084fc", xsize=30, ysize=50)
    subpixel False
    alpha 0.0 yoffset 10
    easein 0.12 alpha 1.0 yoffset -20
    pause 0.60
    easeout 0.25 alpha 0.0 yoffset -40

image anime_anger_vein:
    Solid("#ef4444", xsize=40, ysize=40)
    subpixel False
    zoom 0.9
    easein 0.15 zoom 1.3
    easeout 0.15 zoom 0.9
    easein 0.15 zoom 1.3
    easeout 0.15 zoom 0.9

image anime_sparkles:
    Solid("#fde047", xsize=40, ysize=40)
    subpixel False
    zoom 0.5 alpha 0.0
    easein 0.2 zoom 1.2 alpha 1.0
    easeout 0.2 zoom 0.9 alpha 0.8
    easeout 0.3 alpha 0.0


## ----------------------------------------------------------------------------
## 5. SPRITES DE ACTORES CON EMOCIONES MODULARES
## ----------------------------------------------------------------------------
## Cada actor tiene dimensiones de 48x86 celdas (480x860 px), encajando a la perfección
## en la cuadrícula 192x108. Las emociones se componen visualmente para pruebas inmediatas
## y aceptan sustitución directa con sprites PNG finales.

# ==================== GEO (GUÍA INSTITUCIONAL / ANALÍTICO) ====================
image geo neutral = Composite(
    (480, 860),
    (0, 0), Solid("#0f766e", xsize=480, ysize=860),                     # Traje / Silueta
    (60, 60), Solid("#14b8a6", xsize=360, ysize=260),                   # Rostro sereno
    (100, 360), Text("GEO: Neutral\n(Analítico y sereno)", size=22, color="#ffffff")
)

image geo sonriendo = Composite(
    (480, 860),
    (0, 0), Solid("#0f766e", xsize=480, ysize=860),
    (60, 60), Solid("#2dd4bf", xsize=360, ysize=260),                   # Iluminación de alegría
    (100, 360), Text("GEO: Sonriendo\n(Cálido y receptor)", size=22, color="#ffffff")
)

image geo explicativo = Composite(
    (480, 860),
    (0, 0), Solid("#0f766e", xsize=480, ysize=860),
    (60, 60), Solid("#5eead4", xsize=360, ysize=260),                   # Foco mental
    (100, 360), Text("GEO: Explicativo\n(Paso a paso)", size=22, color="#ffffff")
)

image geo alentador = Composite(
    (480, 860),
    (0, 0), Solid("#115e59", xsize=480, ysize=860),
    (60, 60), Solid("#2dd4bf", xsize=360, ysize=260),
    (100, 360), Text("GEO: Alentador\n(Inspirador)", size=22, color="#ffffff")
)

# ==================== DAVID (EL AMIGO CERCANO / COMPAÑERO) ====================
image david alegre = Composite(
    (480, 860),
    (0, 0), Solid("#1d4ed8", xsize=480, ysize=860),                     # Ropa escolar azul
    (60, 60), Solid("#60a5fa", xsize=360, ysize=260),                   # Rostro animado
    (100, 360), Text("DAVID: Alegre\n(Saluda con energía)", size=22, color="#ffffff")
)

image david preocupado = Composite(
    (480, 860),
    (0, 0), Solid("#1e3a8a", xsize=480, ysize=860),                     # Tono más apagado
    (60, 60), Solid("#3b82f6", xsize=360, ysize=260),                   # Rostro con duda
    (100, 360), Text("DAVID: Preocupado\n(Inseguro por la clase)", size=22, color="#ffffff")
)

image david sorprendido = Composite(
    (480, 860),
    (0, 0), Solid("#1e40af", xsize=480, ysize=860),
    (60, 60), Solid("#93c5fd", xsize=360, ysize=260),                   # Rostro pálido de asombro
    (100, 360), Text("DAVID: Sorprendido\n(¡¿No hiciste tarea?!)", size=22, color="#ffffff")
)

image david aliviado = Composite(
    (480, 860),
    (0, 0), Solid("#1d4ed8", xsize=480, ysize=860),
    (60, 60), Solid("#60a5fa", xsize=360, ysize=260),
    (100, 360), Text("DAVID: Aliviado\n(Sonrisa de respiro)", size=22, color="#ffffff")
)

# ==================== YGRITTE (GUÍA DE REGULACIÓN / COMPAÑERA) ================
image ygritte calmada = Composite(
    (480, 860),
    (0, 0), Solid("#6b21a8", xsize=480, ysize=860),                     # Estilo morado terapéutico
    (60, 60), Solid("#c084fc", xsize=360, ysize=260),                   # Rostro sereno
    (100, 360), Text("YGRITTE: Calmada\n(Respirando en paz)", size=22, color="#ffffff")
)

image ygritte sonriendo = Composite(
    (480, 860),
    (0, 0), Solid("#7e22ce", xsize=480, ysize=860),
    (60, 60), Solid("#d8b4fe", xsize=360, ysize=260),                   # Rostro entusiasta
    (100, 360), Text("YGRITTE: Sonriendo\n(Motivadora)", size=22, color="#ffffff")
)

image ygritte empatica = Composite(
    (480, 860),
    (0, 0), Solid("#581c87", xsize=480, ysize=860),
    (60, 60), Solid("#a855f7", xsize=360, ysize=260),                   # Mirada de comprensión
    (100, 360), Text("YGRITTE: Empática\n(Validación emocional)", size=22, color="#ffffff")
)

image ygritte concentrada = Composite(
    (480, 860),
    (0, 0), Solid("#6b21a8", xsize=480, ysize=860),
    (60, 60), Solid("#c084fc", xsize=360, ysize=260),
    (100, 360), Text("YGRITTE: Concentrada\n(Guiando el 4x4)", size=22, color="#ffffff")
)

image ygritte energica = Composite(
    (480, 860),
    (0, 0), Solid("#9333ea", xsize=480, ysize=860),
    (60, 60), Solid("#e9d5ff", xsize=360, ysize=260),                   # Luz vibrante
    (100, 360), Text("YGRITTE: Enérgica\n(¡Qué onda!)", size=22, color="#ffffff")
)
