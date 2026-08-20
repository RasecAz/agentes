def buscar_lead(nombre):
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
        }
    ]

    resultados = [
        lead
        for lead in leads
        if nombre.lower() in lead["nombre"].lower()
    ]

    return resultados


def buscar_contacto(nombre):
    contactos = [
        {
            "nombre": "Ana Martínez",
            "empresa": "Tecnología ABC",
            "email": "ana@abc.com",
            "telefono": "3001234567"
        },
        {
            "nombre": "Pedro López",
            "empresa": "Comercial XYZ",
            "email": "pedro@xyz.com",
            "telefono": "3109876543"
        },
        {
            "nombre": "Laura Rodríguez",
            "empresa": "Soluciones SAS",
            "email": "laura@soluciones.com",
            "telefono": "3205555555"
        }
    ]

    resultados = [
        contacto
        for contacto in contactos
        if nombre.lower() in contacto["nombre"].lower()
    ]

    return resultados


def buscar_cuenta(nombre):
    cuentas = [
        {
            "nombre": "Tecnología ABC",
            "industria": "Tecnología",
            "ciudad": "Bogotá",
            "estado": "Activa"
        },
        {
            "nombre": "Comercial XYZ",
            "industria": "Comercio",
            "ciudad": "Medellín",
            "estado": "Activa"
        },
        {
            "nombre": "Soluciones SAS",
            "industria": "Servicios",
            "ciudad": "Bucaramanga",
            "estado": "Activa"
        }
    ]

    resultados = [
        cuenta
        for cuenta in cuentas
        if nombre.lower() in cuenta["nombre"].lower()
    ]

    return resultados


def buscar_oportunidad(nombre):
    oportunidades = [
        {
            "nombre": "Implementación CRM Tecnología ABC",
            "cuenta": "Tecnología ABC",
            "importe": 25000000,
            "etapa": "Propuesta",
            "fecha_cierre": "2026-09-30"
        },
        {
            "nombre": "Software Comercial XYZ",
            "cuenta": "Comercial XYZ",
            "importe": 18000000,
            "etapa": "Negociación",
            "fecha_cierre": "2026-10-15"
        },
        {
            "nombre": "Proyecto ERP Soluciones SAS",
            "cuenta": "Soluciones SAS",
            "importe": 45000000,
            "etapa": "Análisis de necesidades",
            "fecha_cierre": "2026-11-20"
        }
    ]

    resultados = [
        oportunidad
        for oportunidad in oportunidades
        if nombre.lower() in oportunidad["nombre"].lower()
        or nombre.lower() in oportunidad["cuenta"].lower()
    ]
def listar_oportunidades():
    oportunidades = [
        {
            "nombre": "Implementación CRM Tecnología ABC",
            "cuenta": "Tecnología ABC",
            "importe": 25000000,
            "etapa": "Propuesta",
            "fecha_cierre": "2026-09-30"
        },
        {
            "nombre": "Software Comercial XYZ",
            "cuenta": "Comercial XYZ",
            "importe": 18000000,
            "etapa": "Negociación",
            "fecha_cierre": "2026-10-15"
        },
        {
            "nombre": "Proyecto ERP Soluciones SAS",
            "cuenta": "Soluciones SAS",
            "importe": 45000000,
            "etapa": "Análisis de necesidades",
            "fecha_cierre": "2026-11-20"
        }
    ]
def crear_lead(nombre, empresa, email, estado="Nuevo"):
    nuevo_lead = {
        "nombre": nombre,
        "empresa": empresa,
        "email": email,
        "estado": estado
    }

    return {
        "mensaje": "Lead creado correctamente",
        "lead": nuevo_lead
    }

    return oportunidades
