from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey123"

def get_db():

    conexion = sqlite3.connect("database.db")

    conexion.row_factory = sqlite3.Row

    return conexion

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/validar", methods=["POST"])
def validar():

    usuario = request.form.get("usuario")
    password = request.form.get("password")

    if usuario == "cfgomez@sdis.gov.co" and password == "123":

        session["usuario"] = usuario

        return redirect(url_for("admin_oferta"))

    return render_template(
        "login.html",
        error="Usuario o contraseña incorrecta"
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/admin_oferta")
def admin_oferta():

    if "usuario" not in session:

        return redirect("/")

    conexion = get_db()

    cursor = conexion.cursor()

    cursor.execute("""

        SELECT *
        FROM ofertas
        ORDER BY id DESC

    """)

    ofertas = cursor.fetchall()

    conexion.close()

    return render_template(
        "admin_oferta.html",
        ofertas=ofertas
    )

@app.route("/nueva_oferta")
def nueva_oferta():

    if "usuario" not in session:
        return redirect("/")

    return render_template(
        "nueva_oferta.html"
    )


@app.route(
    "/crear_oferta",
    methods=["POST"]
)
def crear_oferta():

    titulo_curso = request.form.get(
        "titulo_curso"
    )

    descripcion = request.form.get(
        "descripcion"
    )

    tematica = request.form.get(
        "tematica"
    )

    entidad_oferente = request.form.get(
        "entidad_oferente"
    )

    localidad = request.form.get(
        "localidad"
    )

    unidad_operativa = request.form.get(
        "unidad_operativa"
    )

    espacio_fisico = request.form.get(
        "espacio_fisico"
    )

    fecha_inicio = request.form.get(
        "fecha_inicio"
    )

    fecha_finalizacion = request.form.get(
        "fecha_finalizacion"
    )

    horario = request.form.get(
        "horario"
    )

    asignacion_oferta = request.form.get(
        "asignacion_oferta"
    )

    numero_cupos = request.form.get(
        "numero_cupos"
    )

    requisitos = request.form.get(
        "requisitos"
    )

    modalidad = request.form.get(
        "modalidad"
    )

    costo = request.form.get(
        "costo"
    )

    componente_inclusion = request.form.get(
        "componente_inclusion"
    )

    actividades = request.form.get(
        "actividades"
    )

    observaciones = request.form.get(
        "observaciones"
    )

    documentos = request.form.getlist(
        "documentos"
    )

    documentos = ", ".join(documentos)

    nombre_imagen = None

    archivo = request.files.get(
        "imagen_representativa"
    )

    if archivo and archivo.filename:

        nombre_imagen = archivo.filename

        archivo.save(
            f"static/uploads/{nombre_imagen}"
        )

    conexion = get_db()

    cursor = conexion.cursor()

    cursor.execute("""

INSERT INTO ofertas(

    titulo_curso,
    descripcion,
    tematica,
    entidad_oferente,
    localidad,
    unidad_operativa,
    espacio_fisico,
    fecha_inicio,
    fecha_finalizacion,
    horario,
    asignacion_oferta,
    numero_cupos,
    requisitos,
    imagen_representativa,
    modalidad,
    costo,
    componente_inclusion,
    actividades,
    documentos,
    observaciones

)

VALUES(

    ?, ?, ?, ?, ?,
    ?, ?, ?, ?, ?,
    ?, ?, ?, ?, ?,
    ?, ?, ?, ?, ?

)

""",
(
    titulo_curso,
    descripcion,
    tematica,
    entidad_oferente,
    localidad,
    unidad_operativa,
    espacio_fisico,
    fecha_inicio,
    fecha_finalizacion,
    horario,
    asignacion_oferta,
    numero_cupos,
    requisitos,
    nombre_imagen,
    modalidad,
    costo,
    componente_inclusion,
    actividades,
    documentos,
    observaciones
))

    conexion.commit()

    conexion.close()

    flash(
        "Oferta creada correctamente",
        "success"
    )

    return redirect(
        url_for("admin_oferta")
    )


@app.route("/ver_oferta/<int:id>")
def ver_oferta(id):

    conexion = get_db()

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM ofertas WHERE id=?",
        (id,)
    )

    oferta = cursor.fetchone()

    conexion.close()

    return render_template(
        "ver_oferta.html",
        oferta=oferta
    )

@app.route(
    "/editar_oferta/<int:id>",
    methods=["GET", "POST"]
)
def editar_oferta(id):

    conexion = get_db()
    cursor = conexion.cursor()

    if request.method == "POST":

        cursor.execute("""
            UPDATE ofertas
            SET
                titulo_curso = ?,
                descripcion = ?,
                tematica = ?,
                entidad_oferente = ?,
                localidad = ?,
                unidad_operativa = ?,
                espacio_fisico = ?,
                fecha_inicio = ?,
                fecha_finalizacion = ?,
                horario = ?,
                asignacion_oferta = ?,
                numero_cupos = ?,
                requisitos = ?,
                modalidad = ?,
                costo = ?,
                componente_inclusion = ?,
                actividades = ?,
                observaciones = ?
            WHERE id = ?
        """,
        (
            request.form.get("titulo_curso"),
            request.form.get("descripcion"),
            request.form.get("tematica"),
            request.form.get("entidad_oferente"),
            request.form.get("localidad"),
            request.form.get("unidad_operativa"),
            request.form.get("espacio_fisico"),
            request.form.get("fecha_inicio"),
            request.form.get("fecha_finalizacion"),
            request.form.get("horario"),
            request.form.get("asignacion_oferta"),
            request.form.get("numero_cupos"),
            request.form.get("requisitos"),
            request.form.get("modalidad"),
            request.form.get("costo"),
            request.form.get("componente_inclusion"),
            request.form.get("actividades"),
            request.form.get("observaciones"),
            id
        ))

        conexion.commit()
        conexion.close()

        flash(
            "Oferta actualizada correctamente",
            "success"
        )

        return redirect(
            url_for("admin_oferta")
        )

    cursor.execute(
        "SELECT * FROM ofertas WHERE id = ?",
        (id,)
    )

    oferta = cursor.fetchone()

    conexion.close()

    if not oferta:

        flash(
            "La oferta no existe",
            "danger"
        )

        return redirect(
            url_for("admin_oferta")
        )

    return render_template(
        "editar_oferta.html",
        oferta=oferta
    )

@app.route("/eliminar_oferta/<int:id>")
def eliminar_oferta(id):

    conexion = get_db()

    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM ofertas WHERE id=?",
        (id,)
    )

    conexion.commit()

    conexion.close()

    flash(
        "Oferta eliminada correctamente",
        "success"
    )

    return redirect(
        url_for("admin_oferta")
    )

if __name__ == "__main__":
    app.run(debug=True)