## ============================================================================
## AURA+ | SISTEMA DE TEXTO Y GÉNERO DINÁMICO (PILAR 2)
## ============================================================================
## Este módulo implementa el motor de flexión morfosintáctica en español para
## adaptar todos los textos narrativos, pensamientos y diálogos de los personajes
## (Geo, Ygritte, David) al género seleccionado por el paciente adolescente:
##
## 1. Chico      -> Masculino normativo   (-o, el, él, un, amigo, solo)
## 2. Chica      -> Femenino normativo    (-a, la, ella, una, amiga, sola)
## 3. No Binario -> Inclusivo / Neutro    (-e, le, elle, une, amigue, sole)
## ============================================================================

init offset = -2

## ----------------------------------------------------------------------------
## 1. VARIABLES DINÁMICAS POR DEFECTO (DEFAULT)
## ----------------------------------------------------------------------------
## Se declaran con default para asegurar compatibilidad total con el sistema de
## guardado/recuperación de Ren'Py y evitar NameError en cualquier diálogo.

default p_o = "o"               # Sufijo adjetival estándar: bienvenid[p_o], amig[p_o], cansad[p_o]
default p_a_e = "o"             # Equivalente morfológico para concordancia
default p_art = "el"            # Artículo determinado minúscula: [p_art] joven
default p_Art = "El"            # Artículo determinado mayúscula: [p_Art] paciente
default p_pron = "él"           # Pronombre personal minúscula: con [p_pron]
default p_Pron = "Él"           # Pronombre personal mayúscula: [p_Pron] sabe
default p_un = "un"             # Artículo indeterminado: [p_un] buen amigo
default p_del = "del"           # Contracción de preposición: al lado [p_del] chic[p_o]
default p_al = "al"             # Contracción acusativa: acompaña [p_al] estudiante
default p_amigo = "amigo"       # Sustantivo amigo/amiga/amigue
default p_chico = "chico"       # Sustantivo chico/chica/chique
default p_solo = "solo"         # Adjetivo solo/sola/sole: no estás [p_solo]
default p_listo = "listo"       # Adjetivo listo/lista/liste: ¿estás [p_listo]?
default p_genero_nombre = "Chico (Masculino)"


## ----------------------------------------------------------------------------
## 2. CLASE MOTOR DE GÉNERO EN PYTHON (INIT -1 PYTHON)
## ----------------------------------------------------------------------------
init -1 python:
    class GenderEngine(object):
        """
        Motor de gramática y concordancia morfológica en español para AURA+.
        Asigna dinámicamente el conjunto de sufijos, artículos y pronombres
        en el almacén global (store) de Ren'Py.
        """

        GENDER_MAP = {
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
                "p_genero_nombre": "Chico (Masculino)"
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
                "p_genero_nombre": "Chica (Femenino)"
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
                "p_genero_nombre": "No Binario (Inclusivo)"
            }
        }

        @classmethod
        def apply(cls, gender_key):
            """
            Inyecta las variables gramaticales correspondientes en el almacén de Ren'Py.
            """
            key = (gender_key or "chico").lower().strip()
            if key not in cls.GENDER_MAP:
                key = "chico"

            data = cls.GENDER_MAP[key]
            for var_name, var_value in data.items():
                setattr(renpy.store, var_name, var_value)

            return data


    def aplicar_genero_paciente(gender_key):
        """
        Función helper pública para aplicar la flexión lingüística
        directamente desde scripts o pantallas de Ren'Py.
        """
        return GenderEngine.apply(gender_key)


## ----------------------------------------------------------------------------
## 3. GUÍA DE REDACCIÓN PARA ESCRITORES Y DESARROLLADORES
## ----------------------------------------------------------------------------
## Al escribir diálogos para David, Ygritte, Geo o la narración, utiliza las
## variables interpoladas entre corchetes:
##
## Ejemplo 1:
## david "¡Bienvenid[p_o] a la escuela! Eres un buen amig[p_o]."
## Resultado:
## - Chico:      "¡Bienvenido a la escuela! Eres un buen amigo."
## - Chica:      "¡Bienvenida a la escuela! Eres una buena amiga."
## - No Binario: "¡Bienvenide a la escuela! Eres une buene amigue."
##
## Ejemplo 2:
## ygritte "No estás [p_solo], [active_patient.name]. Respira con calma."
##
## Ejemplo 3:
## geo "Como [p_art] protagonista de tu propio camino, tu bienestar importa."
