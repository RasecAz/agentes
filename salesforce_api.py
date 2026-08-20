import os
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE_URL = os.getenv("SALESFORCE_INSTANCE_URL")
API_VERSION = os.getenv("SALESFORCE_API_VERSION", "v66.0")

ACCESS_TOKEN = os.getenv("SALESFORCE_ACCESS_TOKEN")


def probar_conexion():

    if not INSTANCE_URL:
        print("Falta SALESFORCE_INSTANCE_URL en .env")
        return

    if not ACCESS_TOKEN:
        print("Falta SALESFORCE_ACCESS_TOKEN en .env")
        return

    url = f"{INSTANCE_URL}/services/data/{API_VERSION}/limits"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    respuesta = requests.get(
        url,
        headers=headers
    )

    print("Status:", respuesta.status_code)
    print()

    if respuesta.status_code == 200:
        print("======================================")
        print(" CONEXIÓN CON SALESFORCE EXITOSA")
        print("======================================")
        print()
        print(respuesta.json())
    else:
        print("ERROR:")
        print(respuesta.text)


if __name__ == "__main__":
    probar_conexion()
