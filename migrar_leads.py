import sqlite3

DB_NAME = "crm_local.db"


leads = [
    {
        "nombre": "Juan Pérez",
        "empresa": "Tecnología ABC",
        "email": "juan@abc.com",
        "estado": "Nuevo"
    },
    {
        "nombre": "María Gómez",
        "empresa": "Comercial XYZ",
        "email": "maria@xyz.com",
        "estado": "Contactado"
    },
    {
        "nombre": "Carlos Rodríguez",
        "empresa": "Soluciones SAS",
        "email": "carlos@soluciones.com",
        "estado": "Calificado"
    },
    {
        "nombre": "Andrés Gómez",
        "empresa": "Tech SAS",
        "email": "andres@tech.com",
        "estado": "Nuevo"
    }
]


conexion = sqlite3.connect(DB_NAME)
cursor = conexion.cursor()


for lead in leads:

    cursor.execute(
        """
        INSERT INTO leads
        (
            nombre,
            empresa,
            email,
            estado
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            lead["nombre"],
            lead["empresa"],
            lead["email"],
            lead["estado"]
        )
    )


conexion.commit()
conexion.close()


print("Leads migrados correctamente.")
