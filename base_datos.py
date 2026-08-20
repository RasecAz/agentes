import sqlite3


DB_NAME = "crm_local.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def inicializar_base_datos():

    conexion = conectar()
    cursor = conexion.cursor()

    # ==============================
    # TABLA LEADS
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empresa TEXT NOT NULL,
            email TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    """)


    # ==============================
    # TABLA CONTACTOS
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empresa TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT
        )
    """)


    # ==============================
    # TABLA CUENTAS
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuentas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            industria TEXT,
            ciudad TEXT,
            estado TEXT
        )
    """)


    # ==============================
    # TABLA OPORTUNIDADES
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oportunidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cuenta TEXT NOT NULL,
            importe REAL NOT NULL,
            etapa TEXT NOT NULL,
            fecha_cierre TEXT NOT NULL
        )
    """)


    conexion.commit()
    conexion.close()


if __name__ == "__main__":

    inicializar_base_datos()

    print("Base de datos creada correctamente.")
    print(f"Archivo: {DB_NAME}")
