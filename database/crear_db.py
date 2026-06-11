import sqlite3

conexion = sqlite3.connect("database.db")

cursor = conexion.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS ofertas(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    titulo_curso TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    tematica TEXT NOT NULL,
    entidad_oferente TEXT NOT NULL,

    localidad TEXT NOT NULL,
    unidad_operativa TEXT NOT NULL,
    espacio_fisico TEXT NOT NULL,

    fecha_inicio DATE,
    fecha_finalizacion DATE,

    horario TEXT,

    asignacion_oferta TEXT,

    numero_cupos INTEGER,

    requisitos TEXT,

    imagen_representativa TEXT,

    modalidad TEXT,

    costo TEXT,

    componente_inclusion TEXT,

    actividades TEXT,

    documentos TEXT,

    observaciones TEXT,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")