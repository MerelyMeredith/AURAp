---
name: aura-dynamic-gender
description: >-
  Use this skill to implement, maintain, or expand the Dynamic Gender and Adaptive Grammar System in AURA+. Covers Spanish morphological inflection for Chico (masculine), Chica (feminine), and No Binario (neutral/inclusive), variable interpolation in Ren'Py dialogue strings ([p_o], [p_art], [p_pron]), and integration across character lines (David, Ygritte, Geo).
---

# AURA+ Sistema de Texto y Género Dinámico

Esta habilidad define la implementación técnica, lingüística y arquitectónica del **Sistema de Texto y Género Dinámico** en Ren'Py 8 para el proyecto AURA+.

---

## 1. Justificación Terapéutica y Lingüística

AURA+ acompaña a adolescentes en situaciones de vulnerabilidad emocional. El sentido de pertenencia, respeto y validación identitaria es fundamental para el rapport terapéutico. 
El sistema garantiza que la totalidad de los diálogos, narraciones y reflexiones se adapten automáticamente a la identidad de género del paciente:
- **Chico** (Masculino normativo)
- **Chica** (Femenino normativo)
- **No Binario** (Inclusivo con morfema "-e")

---

## 2. Matriz Lingüística de Flexión en Español

Para evitar errores gramaticales o construcciones forzadas, se define la siguiente matriz de variables para interpolación en Ren'Py:

| Variable | Descripción | Chico (Masc) | Chica (Fem) | No Binario (Neutro) | Ejemplo de Uso en Diálogo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[p_o]` | Terminación adjetival estándar | `o` | `a` | `e` | `"¡Bienvenid[p_o]! Estás cansad[p_o]."` |
| `[p_art]` | Artículo determinado minúscula | `el` | `la` | `le` | `"Es [p_art] mejor de la clase."` |
| `[p_Art]` | Artículo determinado mayúscula | `El` | `La` | `Le` | `"[p_Art] paciente necesita espacio."` |
| `[p_pron]` | Pronombre personal minúscula | `él` | `ella` | `elle` | `"Hablé con [p_pron] esta mañana."` |
| `[p_Pron]` | Pronombre personal mayúscula | `Él` | `Ella` | `Elle` | `"[p_Pron] sabe cómo cuidarse."` |
| `[p_un]` | Artículo indeterminado | `un` | `una` | `une` | `"Eres [p_un] gran amig[p_o]."` |
| `[p_del]` | Contracción preposicional | `del` | `de la` | `de le` | `"Al lado [p_del] chic[p_o]."` |
| `[p_al]` | Contracción acusativa/dativa | `al` | `a la` | `a le` | `"Acompáñame [p_al] patio."` |
| `[p_amigo]` | Sustantivo amigo/a/e | `amigo` | `amiga` | `amigue` | `"Hola, mi [p_amigo]."` |
| `[p_chico]` | Sustantivo chico/a/e | `chico` | `chica` | `chique` | `"Eres un[p_o] [p_chico] valiente."` |
| `[p_solo]` | Adjetivo sólo/sola/sole | `solo` | `sola` | `sole` | `"No tienes que estar [p_solo]."` |
| `[p_listo]` | Adjetivo listo/lista/liste | `listo` | `lista` | `liste` | `"¿Estás [p_listo] para entrar?"` |

---

## 3. Implementación del Motor en Python (`systems/dynamic_gender.rpy`)

Se declara el motor y las variables por defecto en el almacén de Ren'Py (`store`):

```renpy
## Declaración de variables por defecto para evitar NameError en cualquier diálogo
default p_o = "o"
default p_a_e = "o"
default p_art = "el"
default p_Art = "El"
default p_pron = "él"
default p_Pron = "Él"
default p_un = "un"
default p_del = "del"
default p_al = "al"
default p_amigo = "amigo"
default p_chico = "chico"
default p_solo = "solo"
default p_listo = "listo"
default p_genero_nombre = "Chico"

init -1 python:
    class GenderEngine(object):
        """Motor de gramática y género dinámico para AURA+."""

        GENDER_TABLE = {
            "chico": {
                "p_o": "o",
                "p_a_e": "o",
                "p_art": "el",
                "p_Art": "El",
                "p_pron": "él",
                "p_Pron": "Él",
                "p_un": "un",
                "p_del": "del",
                "p_al": "al",
                "p_amigo": "amigo",
                "p_chico": "chico",
                "p_solo": "solo",
                "p_listo": "listo",
                "p_genero_nombre": "Chico"
            },
            "chica": {
                "p_o": "a",
                "p_a_e": "a",
                "p_art": "la",
                "p_Art": "La",
                "p_pron": "ella",
                "p_Pron": "Ella",
                "p_un": "una",
                "p_del": "de la",
                "p_al": "a la",
                "p_amigo": "amiga",
                "p_chico": "chica",
                "p_solo": "sola",
                "p_listo": "lista",
                "p_genero_nombre": "Chica"
            },
            "no_binario": {
                "p_o": "e",
                "p_a_e": "e",
                "p_art": "le",
                "p_Art": "Le",
                "p_pron": "elle",
                "p_Pron": "Elle",
                "p_un": "une",
                "p_del": "de le",
                "p_al": "a le",
                "p_amigo": "amigue",
                "p_chico": "chique",
                "p_solo": "sole",
                "p_listo": "liste",
                "p_genero_nombre": "No Binario"
            }
        }

        @classmethod
        def apply(cls, gender_key):
            """Aplica las variables gramaticales al almacén global de Ren'Py."""
            key = (gender_key or "chico").lower()
            if key not in cls.GENDER_TABLE:
                key = "chico"

            mapping = cls.GENDER_TABLE[key]
            for var_name, var_value in mapping.items():
                setattr(renpy.store, var_name, var_value)

            return mapping

    def aplicar_genero_paciente(gender_key):
        """Función helper para invocar desde scripts o pantallas."""
        return GenderEngine.apply(gender_key)
```

---

## 4. Ejemplos Prácticos en Diálogos de los Personajes

Todos los personajes del juego (**David**, **Ygritte**, **Geo**) deben hacer uso estricto de las variables interpoladas para dirigirse al paciente.

### A. Diálogos de David (El Amigo Cercano / Compañero)
David utiliza un tono cercano, coloquial y empático:

```renpy
define david = Character("David", color="#3a86ff")

label dialogo_david_ejemplo:
    david "¡Hola! ¡Qué bueno verte por aquí! Pensé que te habías quedado dormid[p_o]."
    david "Oye, ¿estás [p_listo] para la clase de hoy? Dicen que el examen va a estar difícil."
    david "Sabes que eres mi mejor [p_amigo], ¿verdad? Si algo te preocupa, dímelo. No tienes que estar [p_solo] con esto."
    david "¡Bienvenid[p_o] a la escuela! Eres [p_un] buen [p_amigo] y me alegra mucho tenerte de vuelta."
```

### B. Diálogos de Ygritte (La Guía Emocional y de Regulación)
Ygritte utiliza un tono calmante, reflexivo y terapéutico:

```renpy
define ygritte = Character("Ygritte", color="#8338ec")

label dialogo_ygritte_ejemplo:
    ygritte "Respira hondo... Puedo notar que estás muy abrumad[p_o]."
    ygritte "No hay prisa. [p_Pron] que aprende a escuchar su propio cuerpo encuentra la calma."
    ygritte "Permítete sentir esto sin juzgarte. Eres [p_un] [p_chico] profundamente valios[p_o]."
    ygritte "Ven conmigo. Vamos a hacer un ejercicio de respiración para que vuelvas a sentirte tranquil[p_o]."
```

### C. Diálogos de Geo (El Consejero Asertivo / Analítico)
Geo aporta perspectiva lógica, resolución de problemas y asertividad:

```renpy
define geo = Character("Geo", color="#ff006e")

label dialogo_geo_ejemplo:
    geo "Analicemos la situación con calma. Nadie puede obligarte a reaccionar si tú no estás [p_preparado]."
    geo "Mira a tu alrededor: eres [p_art] protagonist[p_a_e] de esta historia, no un simple espectador."
    geo "Si alguien te hace sentir pequeñ[p_o], recuerda que tu voz cuenta tanto como la de cualquiera."
    geo "Mantén la cabeza en alto. Eres muy inteligent[p_e] y saldremos de esta junt[p_o]s."
```

---

## 5. Reglas de Redacción y Buenas Prácticas para Escritores

1. **Evitar Doble Flexión Manual**: Nunca escribas `bienvenido/a/e` en el diálogo de los personajes; usa siempre `bienvenid[p_o]`.
2. **Neutralidad Natural Cuando Sea Posible**: Se aconseja alternar construcciones dinámicas con expresiones naturalmente neutras en español (`"me alegra tu presencia"`, `"te agradezco tu ayuda"`), para que la lectura sea fluida y no sobrecargada.
3. **Validación de Corchetes**: En Ren'Py, los corchetes `[` y `]` indican interpolación. Si necesitas mostrar un corchete literal en el texto, debes duplicarlo: `[[ejemplo]`.
4. **Verificación de Mayúsculas**:
   - Usa `[p_art]` para `el / la / le` dentro de una oración.
   - Usa `[p_Art]` para `El / La / Le` al inicio de una oración.
   - Usa `[p_pron]` para `él / ella / elle` y `[p_Pron]` para `Él / Ella / Elle`.
