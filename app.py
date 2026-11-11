"""BASE EDUCATIVA INSEGURA. Corregir los TODO antes de la entrega."""
import json
from seguridad import crear_hash, verificar_clave
from pathlib import Path
from datetime import datetime


RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"


def cargar_inventario():
    try:
        return json.loads(DATOS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("No se encontró el archivo inventario.json.")
    except json.JSONDecodeError:
        print("El archivo inventario.json contiene JSON inválido.")
    return None

def guardar_hash():
    usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))

    for usuario in usuarios:
        if "clave" in usuario:
            usuario["clave_hash"] = crear_hash(usuario["clave"])
            del usuario["clave"]

    USUARIOS.write_text(json.dumps(usuarios, indent=2), encoding="utf-8")

def registrar_evento(usuario, accion, resultado, **detalles):
    evento = {
        "fecha_hora": datetime.now().isoformat(timespec="seconds"),
        "usuario": usuario,
        "accion": accion,
        "resultado": resultado
    }

    if "producto" in detalles:
        evento["producto"] = detalles["producto"]

    if "anterior" in detalles:
        evento["anterior"] = detalles["anterior"]

    if "nueva" in detalles:
        evento["nueva"] = detalles["nueva"]

    linea = json.dumps(evento, ensure_ascii=False)

    with LOG.open("a", encoding="utf-8") as archivo:
        archivo.write(linea + "\n")

def autenticar(nombre, clave):
    usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))
    for usuario in usuarios:
        if usuario["usuario"] == nombre and verificar_clave(usuario["clave_hash"], clave):
            registrar_evento(nombre, "login", "exitoso")
            return {"usuario": nombre, "rol": usuario["rol"]}
    registrar_evento(nombre, "login", "fallido")
    print("Credenciales incorrectas.")
    return None


def consultar_inventario(sesion):
    if sesion is None:
        print("Debes iniciar sesión para consultar.")
        return
    productos = cargar_inventario()
    if productos is None:
        return False
    for producto in productos:
        print(producto["id"], producto["nombre"], producto["cantidad"])


def modificar_cantidad(sesion, identificador, entrada):
    if sesion is None:
        print("Debes iniciar sesión para modificar.")
        return False

    if sesion["rol"] != "admin":
        registrar_evento(sesion["usuario"], "modificar", "rechazado", producto=identificador)
        print("Solo el administrador puede modificar cantidades.")
        return False
    try:
        cantidad = int(entrada)
    except ValueError:
        print("La cantidad debe ser un número entero.")
        return False

    if cantidad < 0 or cantidad > 1000:
        print("La cantidad debe ser de 0 a 1000.")
        return False   
    productos = cargar_inventario()
    if productos is None:
        return False

    for producto in productos:
        if producto["id"] == identificador:
            anterior = producto["cantidad"]
            producto["cantidad"] = cantidad
            contenido = json.dumps(productos, ensure_ascii=False, indent=2)
            DATOS.write_text(contenido, encoding="utf-8")
            registrar_evento(
                sesion["usuario"], "modificar", "exitoso",
                producto=identificador, anterior=anterior, nueva=cantidad
            )
            print("Cantidad actualizada.")
            return True
    print("El producto ", identificador, " no fue encontrado.")
    return False    


def main():
    print("Inventario académico — BASE CON DEBILIDADES")
    print("Estudiante:", input("Escriba su nombre: "))
    sesion = None
    while True:
        if sesion is None:
            nombre = input("Usuario (o salir): ")
            if nombre == "salir":
                break
            sesion = autenticar(nombre, input("Contraseña de prueba: "))
            continue
        print("1. Consultar | 2. Modificar | 3. Cerrar sesión | 0. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            consultar_inventario(sesion)
        elif opcion == "2":
            identificador = input("ID del producto: ")
            entrada = input("Nueva cantidad: ")
            modificar_cantidad(sesion, identificador, entrada)
        elif opcion == "3":
            sesion = None
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
