from herramientas import ejecutar_soql
from datetime import date


def analizar_oportunidades_sin_actividad(dias=30):
    soql = """
        SELECT Id, Name, Account.Name, Amount, StageName,
               CloseDate, LastActivityDate
        FROM Opportunity
        WHERE IsClosed = false
        ORDER BY LastActivityDate ASC NULLS FIRST
        LIMIT 100
    """

    datos = ejecutar_soql(soql)

    if isinstance(datos, dict) and "error" in datos:
        return datos

    resultados = []
    hoy = date.today()

    for oportunidad in datos.get("records", []):
        ultima_actividad = oportunidad.get("LastActivityDate")

        if ultima_actividad:
            fecha_actividad = date.fromisoformat(ultima_actividad)
            dias_sin_actividad = (hoy - fecha_actividad).days
        else:
            dias_sin_actividad = None

        if (
            dias_sin_actividad is None
            or dias_sin_actividad >= dias
        ):
            cuenta = oportunidad.get("Account")

            resultados.append(
                {
                    "id": oportunidad.get("Id"),
                    "oportunidad": oportunidad.get("Name"),
                    "cuenta": (
                        cuenta.get("Name")
                        if cuenta
                        else None
                    ),
                    "importe": oportunidad.get("Amount"),
                    "etapa": oportunidad.get("StageName"),
                    "fecha_cierre": oportunidad.get("CloseDate"),
                    "ultima_actividad": ultima_actividad,
                    "dias_sin_actividad": dias_sin_actividad,
                    "recomendacion": (
                        "Revisar y realizar seguimiento"
                    )
                }
            )

    return resultados


if __name__ == "__main__":
    print()
    print("======================================")
    print("     SUPERVISOR COMERCIAL")
    print("======================================")
    print()

    resultados = analizar_oportunidades_sin_actividad(30)

    if isinstance(resultados, dict) and "error" in resultados:
        print("ERROR:")
        print(resultados)
    elif not resultados:
        print("No hay oportunidades que necesiten atención.")
    else:
        print(
            f"Se encontraron {len(resultados)} "
            "oportunidades que necesitan revisión:"
        )
        print()

        for oportunidad in resultados:
            print("--------------------------------------")
            print(
                f"Oportunidad: "
                f"{oportunidad['oportunidad']}"
            )
            print(
                f"Cuenta: "
                f"{oportunidad['cuenta']}"
            )
            print(
                f"Importe: "
                f"{oportunidad['importe']}"
            )
            print(
                f"Etapa: "
                f"{oportunidad['etapa']}"
            )
            print(
                f"Última actividad: "
                f"{oportunidad['ultima_actividad']}"
            )
            print(
                f"Días sin actividad: "
                f"{oportunidad['dias_sin_actividad']}"
            )
            print(
                f"Recomendación: "
                f"{oportunidad['recomendacion']}"
            )
