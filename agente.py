from ollama import chat

from herramientas import (
    buscar_lead,
    buscar_contacto,
    buscar_cuenta,
    buscar_oportunidad,
    listar_oportunidades,
    crear_lead
)


MODELO = "qwen3:4b"


SYSTEM_PROMPT = """
Eres Salesforce Agent, un agente especializado en Salesforce.

Tu función es ayudar a administrar y analizar información relacionada
con Salesforce.

Herramientas disponibles:

- buscar_lead
- buscar_contacto
- buscar_cuenta
- buscar_oportunidad
- listar_oportunidades
- crear_lead

REGLAS:

1. Si el usuario pregunta por un Lead específico,
   utiliza buscar_lead.

2. Si el usuario pregunta por un Contacto específico,
   utiliza buscar_contacto.

3. Si el usuario pregunta por una Cuenta específica,
   utiliza buscar_cuenta.

4. Si el usuario pregunta por una Oportunidad específica,
   utiliza buscar_oportunidad.

5. Si el usuario solicita comparar, analizar, ordenar
   o evaluar oportunidades, utiliza listar_oportunidades.

6. Si el usuario solicita CREAR un Lead, utiliza crear_lead.

7. Para crear un Lead necesitas:
   - nombre
   - empresa
   - email
   - estado

8. Si faltan datos para crear un Lead, solicita los datos faltantes.

9. Nunca inventes información.

10. Si una herramienta devuelve información, utiliza esos datos.

11. Por ahora todos los datos son locales de prueba.

12. Nunca afirmes que estás conectado a Salesforce real.

13. Las acciones de escritura requieren confirmación.
"""


print("======================================")
print("     SALESFORCE AGENT - LOCAL")
print("======================================")
print("Modelo:", MODELO)
print("Herramientas: Leads, Contactos, Cuentas, Oportunidades")
print("Escribe 'salir' para terminar.")
print()


TOOLS = [
    buscar_lead,
    buscar_contacto,
    buscar_cuenta,
    buscar_oportunidad,
    listar_oportunidades,
    crear_lead
]


# ---------------------------------------------------------
# ESTADO DE CONFIRMACIÓN
# ---------------------------------------------------------

pendiente_creacion = None


# ---------------------------------------------------------
# FUNCIÓN PARA INTERPRETAR CONFIRMACIÓN
# ---------------------------------------------------------

def es_confirmacion(texto):

    texto = texto.strip().lower()

    return texto in [
        "si",
        "sí",
        "s",
        "yes",
        "y",
        "confirmo",
        "confirmar"
    ]


def es_cancelacion(texto):

    texto = texto.strip().lower()

    return texto in [
        "no",
        "n",
        "cancelar",
        "cancelado"
    ]


# ---------------------------------------------------------
# BUCLE PRINCIPAL
# ---------------------------------------------------------

while True:

    usuario = input("Tú > ").strip()

    if usuario.lower() in ["salir", "exit", "quit"]:

        print("Agente > Hasta luego.")
        break


    # =====================================================
    # SI HAY UNA CREACIÓN PENDIENTE
    # =====================================================

    if pendiente_creacion is not None:

        if es_confirmacion(usuario):

            print()
            print("Agente > Ejecutando creación...")
            print()

            resultado = crear_lead(**pendiente_creacion)

            pendiente_creacion = None

            print("Agente >")
            print(resultado)
            print()

            continue


        elif es_cancelacion(usuario):

            pendiente_creacion = None

            print()
            print("Agente > Creación cancelada.")
            print()

            continue


        else:

            print()
            print(
                "Agente > Responde solamente "
                "'Sí' para confirmar o 'No' para cancelar."
            )
            print()

            continue


    # =====================================================
    # CONVERSACIÓN CON QWEN
    # =====================================================

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": usuario
        }
    ]


    respuesta = chat(
        model=MODELO,
        messages=messages,
        tools=TOOLS
    )


    # =====================================================
    # QWEN SOLICITÓ UNA HERRAMIENTA
    # =====================================================

    if respuesta.message.tool_calls:

        messages.append(respuesta.message)


        for llamada in respuesta.message.tool_calls:

            nombre = llamada.function.name
            argumentos = llamada.function.arguments


            # ---------------------------------------------
            # BUSCAR LEAD
            # ---------------------------------------------

            if nombre == "buscar_lead":

                resultado = buscar_lead(**argumentos)


            # ---------------------------------------------
            # BUSCAR CONTACTO
            # ---------------------------------------------

            elif nombre == "buscar_contacto":

                resultado = buscar_contacto(**argumentos)


            # ---------------------------------------------
            # BUSCAR CUENTA
            # ---------------------------------------------

            elif nombre == "buscar_cuenta":

                resultado = buscar_cuenta(**argumentos)


            # ---------------------------------------------
            # BUSCAR OPORTUNIDAD
            # ---------------------------------------------

            elif nombre == "buscar_oportunidad":

                resultado = buscar_oportunidad(**argumentos)


            # ---------------------------------------------
            # LISTAR OPORTUNIDADES
            # ---------------------------------------------

            elif nombre == "listar_oportunidades":

                resultado = listar_oportunidades()


            # ---------------------------------------------
            # CREAR LEAD
            # ---------------------------------------------

            elif nombre == "crear_lead":

                # IMPORTANTE:
                # NO ejecutamos crear_lead todavía.

                pendiente_creacion = argumentos

                print()
                print("======================================")
                print("      CONFIRMACIÓN DE CREACIÓN")
                print("======================================")
                print()
                print("Voy a crear el siguiente Lead:")
                print()
                print(
                    "Nombre:",
                    argumentos.get("nombre")
                )
                print(
                    "Empresa:",
                    argumentos.get("empresa")
                )
                print(
                    "Email:",
                    argumentos.get("email")
                )
                print(
                    "Estado:",
                    argumentos.get("estado")
                )
                print()
                print(
                    "¿Confirmas la creación?"
                    " (Sí/No)"
                )
                print()

                # NO enviamos nada más a Qwen.
                break


            # ---------------------------------------------
            # HERRAMIENTA DESCONOCIDA
            # ---------------------------------------------

            else:

                resultado = {
                    "error":
                    f"Herramienta desconocida: {nombre}"
                }


            # =================================================
            # DEVOLVER RESULTADO DE HERRAMIENTA A QWEN
            # =================================================

            if nombre != "crear_lead":

                messages.append(
                    {
                        "role": "tool",
                        "content": str(resultado)
                    }
                )


        # =====================================================
        # SI NO HAY CREACIÓN PENDIENTE, QWEN RESPONDE
        # =====================================================

        if pendiente_creacion is None:

            respuesta = chat(
                model=MODELO,
                messages=messages,
                tools=TOOLS
            )


    # =====================================================
    # MOSTRAR RESPUESTA
    # =====================================================

    if pendiente_creacion is None:

        print()
        print("Agente >")
        print(respuesta.message.content)
        print()
