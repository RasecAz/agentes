import os
import base64
import hashlib
import secrets
import threading
import webbrowser

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode, urlparse, parse_qs

import requests
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")

AUTH_URL = "https://login.salesforce.com/services/oauth2/authorize"
TOKEN_URL = "https://login.salesforce.com/services/oauth2/token"

REDIRECT_URI = "http://localhost:8080/oauth/callback"


if not CLIENT_ID:
    raise ValueError("Falta SALESFORCE_CLIENT_ID en .env")

if not CLIENT_SECRET:
    raise ValueError("Falta SALESFORCE_CLIENT_SECRET en .env")


authorization_code = None


class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        global authorization_code

        parsed = urlparse(self.path)

        if parsed.path != "/oauth/callback":
            self.send_response(404)
            self.end_headers()
            return

        parametros = parse_qs(parsed.query)

        if "code" in parametros:

            authorization_code = parametros["code"][0]

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )
            self.end_headers()

            self.wfile.write(
                b"""
                <html>
                    <body>
                        <h1>Autenticacion correcta</h1>
                        <p>Puedes cerrar esta ventana.</p>
                    </body>
                </html>
                """
            )

        else:

            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        return


def generar_pkce():

    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(
            verifier.encode("utf-8")
        ).digest()
    ).decode("utf-8").rstrip("=")

    return verifier, challenge


def guardar_variable(nombre, valor):

    archivo = ".env"

    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    encontrada = False
    nuevas_lineas = []

    for linea in lineas:

        if linea.startswith(nombre + "="):

            nuevas_lineas.append(
                f"{nombre}={valor}\n"
            )

            encontrada = True

        else:

            nuevas_lineas.append(linea)

    if not encontrada:

        nuevas_lineas.append(
            f"{nombre}={valor}\n"
        )

    with open(archivo, "w", encoding="utf-8") as f:

        f.writelines(nuevas_lineas)


def autenticar():

    global authorization_code

    verifier, challenge = generar_pkce()

    parametros = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "api refresh_token offline_access openid",
        "code_challenge": challenge,
        "code_challenge_method": "S256"
    }

    url = AUTH_URL + "?" + urlencode(parametros)

    servidor = HTTPServer(
        ("localhost", 8080),
        CallbackHandler
    )

    hilo = threading.Thread(
        target=servidor.serve_forever
    )

    hilo.daemon = True
    hilo.start()

    print()
    print("======================================")
    print("     SALESFORCE OAUTH")
    print("======================================")
    print()
    print("Abriendo Salesforce en el navegador...")
    print()

    webbrowser.open(url)

    while authorization_code is None:
        pass

    servidor.shutdown()

    print()
    print("Codigo de autorizacion recibido.")
    print("Solicitando token a Salesforce...")
    print()

    datos = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": authorization_code,
        "code_verifier": verifier
    }

    respuesta = requests.post(
        TOKEN_URL,
        data=datos
    )

    if respuesta.status_code != 200:

        print("ERROR DE AUTENTICACION")
        print(respuesta.text)
        return

    tokens = respuesta.json()

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    instance_url = tokens.get("instance_url")

    if not access_token:

        print("No se recibió Access Token.")
        print(tokens)
        return

    print("======================================")
    print(" AUTENTICACION EXITOSA")
    print("======================================")
    print()

    print("Instance URL:")
    print(instance_url)

    print()
    print("Access Token recibido.")
    print(
        "Refresh Token recibido:",
        bool(refresh_token)
    )

    print()
    print("Guardando credenciales en .env...")

    guardar_variable(
        "SALESFORCE_ACCESS_TOKEN",
        access_token
    )

    guardar_variable(
        "SALESFORCE_INSTANCE_URL",
        instance_url
    )

    if refresh_token:

        guardar_variable(
            "SALESFORCE_REFRESH_TOKEN",
            refresh_token
        )

    print()
    print("Credenciales guardadas correctamente.")
    print()
    print("Ya podemos probar la API de Salesforce.")


if __name__ == "__main__":

    autenticar()
