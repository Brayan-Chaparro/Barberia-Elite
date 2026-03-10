from flask import Flask, render_template, request, redirect, jsonify, session
import json
import os
import random
from datetime import date

app = Flask(__name__)
app.secret_key = "barberia_elite_2026"

ARCHIVO_CITAS = "citas.json"
ADMIN_PASSWORD = "admin123"

HORARIOS = [
    "9:00","10:00","11:00","12:00",
    "14:00","15:00","16:00","17:00","18:00"
]

def cargar_citas():
    if not os.path.exists(ARCHIVO_CITAS):
        return []
    with open(ARCHIVO_CITAS, "r") as f:
        return json.load(f)

def guardar_citas(citas):
    with open(ARCHIVO_CITAS, "w") as f:
        json.dump(citas, f, indent=4)

def generar_codigo(citas):
    while True:
        codigo = str(random.randint(1000, 9999))
        if not any(c.get("codigo") == codigo for c in citas):
            return codigo

@app.route("/")
def inicio():
    confirmacion = session.pop("confirmacion", None)
    citas = cargar_citas()
    hoy = date.today().isoformat()
    return render_template("index.html", citas=citas, confirmacion=confirmacion, hoy=hoy)

@app.route("/horas_disponibles")
def horas_disponibles():
    fecha = request.args.get("fecha")
    citas = cargar_citas()
    ocupadas = [c.get("hora") for c in citas if c.get("fecha") == fecha]
    disponibles = [h for h in HORARIOS if h not in ocupadas]
    return jsonify(disponibles)

@app.route("/reservar", methods=["POST"])
def reservar():
    citas = cargar_citas()
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    hoy = date.today().isoformat()

    if fecha < hoy:
        return render_template("index.html", citas=citas, hoy=hoy,
            error="❌ No puedes reservar en una fecha pasada.")

    ocupadas = [c.get("hora") for c in citas if c.get("fecha") == fecha]
    if hora in ocupadas:
        return render_template("index.html", citas=citas, hoy=hoy,
            error="❌ Esa hora ya fue reservada, elige otra.")

    codigo = generar_codigo(citas)

    nueva_cita = {
        "codigo": codigo,
        "nombre": request.form["nombre"],
        "telefono": request.form["telefono"],
        "servicio": request.form["servicio"],
        "fecha": fecha,
        "hora": hora
    }

    citas.append(nueva_cita)
    guardar_citas(citas)

    session["confirmacion"] = {
        "codigo": codigo,
        "nombre": nueva_cita["nombre"],
        "servicio": nueva_cita["servicio"],
        "fecha": fecha,
        "hora": hora
    }

    return redirect("/")

@app.route("/cancelar", methods=["POST"])
def cancelar():
    codigo = request.form["codigo"]
    citas = cargar_citas()
    nuevas = [c for c in citas if c.get("codigo") != codigo]

    if len(nuevas) == len(citas):
        hoy = date.today().isoformat()
        return render_template("index.html", citas=citas, hoy=hoy,
            error="❌ Código no encontrado.")

    guardar_citas(nuevas)
    return redirect("/")

# ADMIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin"] = True
        else:
            return render_template("admin.html", error="❌ Contraseña incorrecta.", autenticado=False)

    if not session.get("admin"):
        return render_template("admin.html", autenticado=False)

    citas = cargar_citas()
    return render_template("admin.html", citas=citas, autenticado=True)

@app.route("/admin/cancelar/<codigo>")
def admin_cancelar(codigo):
    if not session.get("admin"):
        return redirect("/admin")
    citas = cargar_citas()
    nuevas = [c for c in citas if c.get("codigo") != codigo]
    guardar_citas(nuevas)
    return redirect("/admin")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)