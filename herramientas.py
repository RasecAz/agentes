import os
import requests
from dotenv import load_dotenv


load_dotenv()


def obtener_configuracion_salesforce():
    instance_url = os.getenv("SALESFORCE_INSTANCE_URL")
    api_version = os.getenv(
        "SALESFORCE_API_VERSION",
        "v66.0"
    )
    access_token = os.getenv("SALESFORCE_ACCESS_TOKEN")

    if not instance_url:
        return None, None, None, {
            "error": "No está configurado SALESFORCE_INSTANCE_URL"
        }

    if not access_token:
        return None, None, None, {
            "error": "No está configurado SALESFORCE_ACCESS_TOKEN"
        }

    return (
        instance_url,
        api_version,
        access_token,
        None
    )


def ejecutar_soql(soql):
    (
        instance_url,
        api_version,
        access_token,
        error
    ) = obtener_configuracion_salesforce()

    if error:
        return error

    url = (
        f"{instance_url}/services/data/"
        f"{api_version}/query"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        respuesta = requests.get(
            url,
            headers=headers,
            params={"q": soql},
            timeout=30
        )

        if respuesta.status_code != 200:
            return {
                "error": "Salesforce devolvió un error",
                "status": respuesta.status_code,
                "detalle": respuesta.text
            }

        return respuesta.json()

    except requests.RequestException as error:
        return {
            "error": (
                "Error de conexión con Salesforce: "
                f"{error}"
            )
        }


def buscar_lead(nombre):
    nombre = nombre.replace("'", "\\'")

    soql = (
        "SELECT Id, FirstName, LastName, "
        "Company, Email, Status "
        "FROM Lead "
        f"WHERE Name LIKE '%{nombre}%' "
        "ORDER BY CreatedDate DESC "
        "LIMIT 20"
    )

    datos = ejecutar_soql(soql)

    if isinstance(datos, dict) and "error" in datos:
        return datos

    resultados = []

    for lead in datos.get("records", []):
        resultados.append(
            {
                "id": lead.get("Id"),
                "nombre": (
                    f"{lead.get('FirstName', '')} "
                    f"{lead.get('LastName', '')}"
                ).strip(),
                "empresa": lead.get("Company"),
                "email": lead.get("Email"),
                "estado": lead.get("Status")
            }
        )

    return resultados


def buscar_contacto(nombre):
    nombre = nombre.replace("'", "\\'")

    soql = (
        "SELECT Id, FirstName, LastName, "
        "Account.Name, Email, Phone "
        "FROM Contact "
        f"WHERE Name LIKE '%{nombre}%' "
        "ORDER BY CreatedDate DESC "
        "LIMIT 20"
    )

    datos = ejecutar_soql(soql)

    if isinstance(datos, dict) and "error" in datos:
        return datos

    resultados = []

    for contacto in datos.get("records", []):
        cuenta = contacto.get("Account")

        resultados.append(
            {
                "id": contacto.get("Id"),
                "nombre": (
                    f"{contacto.get('FirstName', '')} "
                    f"{contacto.get('LastName', '')}"
                ).strip(),
                "empresa": (
                    cuenta.get("Name")
                    if cuenta
                    else None
                ),
                "email": contacto.get("Email"),
                "telefono": contacto.get("Phone")
            }
        )

    return resultados


def buscar_cuenta(nombre):
    nombre = nombre.replace("'", "\\'")

    soql = (
        "SELECT Id, Name, Industry, "
        "BillingCity, Type "
        "FROM Account "
        f"WHERE Name LIKE '%{nombre}%' "
        "ORDER BY CreatedDate DESC "
        "LIMIT 20"
    )

    datos = ejecutar_soql(soql)

    if isinstance(datos, dict) and "error" in datos:
        return datos

    resultados = []

    for cuenta in datos.get("records", []):
        resultados.append(
            {
                "id": cuenta.get("Id"),
                "nombre": cuenta.get("Name"),
                "industria": cuenta.get("Industry"),
                "ciudad": cuenta.get("BillingCity"),
                "tipo": cuenta.get("Type")
            }
        )

    return resultados


def buscar_oportunidad(nombre):
    nombre = nombre.replace("'", "\\'")

    soql = (
        "SELECT Id, Name, Account.Name, Amount, "
        "StageName, CloseDate "
        "FROM Opportunity "
        f"WHERE Name LIKE '%{nombre}%' "
        "OR Account.Name LIKE '%"
        f"{nombre}%' "
        "ORDER BY CreatedDate DESC "
        "LIMIT 20"
    )

    datos = ejecutar_soql(soql)

    if isinstance(datos, dict) and "error" in datos:
        return datos

    resultados = []

    for oportunidad in datos.get("records", []):
        cuenta = oportunidad.get("Account")

        resultados.append(
            {
                "id": oportunidad.get("Id"),
                "nombre": oportunidad.get("Name"),
                "cuenta": (
                    cuenta.get("Name")
                    if cuenta
                    else None
                ),
                "importe": oportunidad.get("Amount"),
                "etapa": oportunidad.get("StageName"),
                "fecha_cierre": oportunidad.get("CloseDate")
            }
        )

    return resultados


def listar_oportunidades():
    soql = (
        "SELECT Id, Name, Account.Name, Amount, "
        "StageName, CloseDate "
        "FROM Opportunity "
        "ORDER BY Amount DESC NULLS LAST "
        "LIMIT 100"
    )

    datos = ejecutar_soql(soql)

    if isinstance(datos, dict) and "error" in datos:
        return datos

    resultados = []

    for oportunidad in datos.get("records", []):
        cuenta = oportunidad.get("Account")

        resultados.append(
            {
                "id": oportunidad.get("Id"),
                "nombre": oportunidad.get("Name"),
                "cuenta": (
                    cuenta.get("Name")
                    if cuenta
                    else None
                ),
                "importe": oportunidad.get("Amount"),
                "etapa": oportunidad.get("StageName"),
                "fecha_cierre": oportunidad.get("CloseDate")
            }
        )

    return resultados


def crear_lead(nombre, empresa, email, estado="Nuevo"):
    (
        instance_url,
        api_version,
        access_token,
        error
    ) = obtener_configuracion_salesforce()

    if error:
        return error

    partes = nombre.strip().split(" ", 1)

    first_name = partes[0]

    if len(partes) > 1:
        last_name = partes[1]
    else:
        last_name = "Sin Apellido"

    url = (
        f"{instance_url}/services/data/"
        f"{api_version}/sobjects/Lead"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    datos = {
        "FirstName": first_name,
        "LastName": last_name,
        "Company": empresa,
        "Email": email,
        "Status": estado
    }

    try:
        respuesta = requests.post(
            url,
            headers=headers,
            json=datos,
            timeout=30
        )

        if respuesta.status_code not in (200, 201):
            return {
                "error": "No se pudo crear el Lead en Salesforce",
                "status": respuesta.status_code,
                "detalle": respuesta.text
            }

        resultado = respuesta.json()

        return {
            "mensaje": "Lead creado correctamente en Salesforce",
            "lead": {
                "id": resultado.get("id"),
                "nombre": nombre,
                "empresa": empresa,
                "email": email,
                "estado": estado
            }
        }

    except requests.RequestException as error:
        return {
            "error": (
                "Error de conexión con Salesforce: "
                f"{error}"
            )
        }
