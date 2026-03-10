import json
import random

ARCHIVO = "citas.json"

HORARIOS = [
    "9:00","10:00","11:00","12:00",
    "14:00","15:00","16:00","17:00","18:00"
]

def cargar_citas():
    try:
        with open(ARCHIVO, "r") as archivo:
            return json.load(archivo)
    except:
        return []

def guardar_citas(citas):
    with open(ARCHIVO, "w") as archivo:
        json.dump(citas, archivo, indent=4)

def generar_codigo(citas):
    while True:
        codigo = str(random.randint(1000,9999))
        existe = any(cita.get("codigo") == codigo for cita in citas)
        if not existe:
            return codigo

def mostrar_menu():
    print("\n💈 Barbería Elite 💈")
    print("1 Ver precios")
    print("2 Horarios")
    print("3 Ubicación")
    print("4 Agendar cita")
    print("5 Ver citas")
    print("6 Cancelar cita")
    print("7 Salir")

def obtener_horas_disponibles(citas, dia):
    horas_ocupadas = []
    for cita in citas:
        if cita.get("fecha") == dia:
            horas_ocupadas.append(cita.get("hora"))

    disponibles = []
    for hora in HORARIOS:
        if hora not in horas_ocupadas:
            disponibles.append(hora)

    return disponibles

def agendar_cita():
    citas = cargar_citas()

    print("\n📅 Nueva cita")

    nombre = input("Nombre: ")
    servicio = input("Servicio: ")
    dia = input("Fecha (ej: 2026-03-10): ")

    disponibles = obtener_horas_disponibles(citas, dia)

    if len(disponibles) == 0:
        print("No hay horas disponibles")
        return

    print("\nHoras disponibles")
    for i, hora in enumerate(disponibles, 1):
        print(i, "-", hora)

    seleccion = int(input("Seleccione: "))
    hora = disponibles[seleccion - 1]

    codigo = generar_codigo(citas)

    nueva_cita = {
        "codigo": codigo,
        "nombre": nombre,
        "servicio": servicio,
        "fecha": dia,
        "hora": hora
    }

    citas.append(nueva_cita)
    guardar_citas(citas)

    print("\n✅ Cita agendada")
    print("Código:", codigo)
    print("Nombre:", nombre)
    print("Servicio:", servicio)
    print("Fecha:", dia)
    print("Hora:", hora)

def ver_citas():
    citas = cargar_citas()

    print("\n📋 Citas registradas\n")

    if len(citas) == 0:
        print("No hay citas")
        return

    for cita in citas:
        print(
            cita.get("codigo", "?"), "-",
            cita.get("nombre", "?"), "-",
            cita.get("servicio", "?"), "-",
            cita.get("fecha", "?"), "-",
            cita.get("hora", "?")
        )

def cancelar_cita():
    citas = cargar_citas()

    codigo = input("Código de cita: ")

    nuevas = []
    eliminada = False

    for cita in citas:
        if cita.get("codigo") == codigo:
            eliminada = True
        else:
            nuevas.append(cita)

    guardar_citas(nuevas)

    if eliminada:
        print("✅ Cita cancelada")
    else:
        print("Código no encontrado")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione: ")

        if opcion == "1":
            print("\nCorte $15000")
            print("Barba $10000")

        elif opcion == "2":
            print("\nLunes a sábado 9:00-18:00")

        elif opcion == "3":
            print("\nCalle 20 #15-30")

        elif opcion == "4":
            agendar_cita()

        elif opcion == "5":
            ver_citas()

        elif opcion == "6":
            cancelar_cita()

        elif opcion == "7":
            print("Hasta luego")
            break

main()