# Base educativa — COMP 2700

Esta versión contiene debilidades intencionales. Utilice únicamente los datos
ficticios incluidos, en su computadora. No es una aplicación de producción.

Requiere Python 3.10 o posterior. Desde esta carpeta:

    python -m venv .venv

Windows CMD:

    .venv\Scripts\activate.bat

macOS/Linux:

    source .venv/bin/activate

Luego:

    python -m pip install -r requirements.txt
    python app.py

En algunos sistemas debe utilizar python3 en lugar de python.

Cuentas públicas y exclusivamente ficticias:
- admin / AdminDemo2700!
- user / UserDemo2700!

Comience probando consulta y cambio de cantidad con admin. La base no aplica
todos los controles: user también puede modificar, las claves están legibles,
las entradas inválidas pueden causar errores y no se guarda auditoría.
Los TODO de app.py guían las correcciones; seguridad.py contiene funciones listas.

Para migrar las contraseñas, cree un pequeño script que llame crear_hash para
cada cuenta y guarde el resultado en un campo hash. Elimine el campo clave del
archivo final. Adapte autenticar para llamar verificar_clave. No compare dos
hashes recién generados: sus salts serán diferentes.

Los archivos se resuelven respecto a app.py. Guarde una copia del inventario
antes de las pruebas de errores. Use P001 con cantidad 10 al comenzar.

Puede hacer pruebas directas desde un script que importe app:

    import app
    sesion = app.autenticar("user", "UserDemo2700!")
    app.modificar_cantidad(sesion, "P001", "99")

Después de corregir los permisos, esa llamada debe rechazarse sin cambiar P001.
Repita con None como sesión. No fabrique un diccionario con rol admin para
simular una sesión válida: esta aplicación confía en su propio proceso.

JSON almacena un documento completo (lista de productos o usuarios).
Solamente auditoria.jsonl utiliza un objeto por línea.

Complete este README con su nombre, ejecución, pruebas, fuentes y uso de IA.
No suba .venv, __pycache__, credenciales reales ni datos personales de terceros.



# Proyecto: Evaluación y corrección de una miniaplicación
# COMP2700.CYBERSECURITYProyecto: Evaluación y corrección de una miniaplicación

Estudiante: Angel G. Sostre

El programa permite consultar un inventria ficticio en el que la cuenta admin puede consultar y modificar cantidades. La cuenta user solo puede consultar

## Requisitos y dependencias

Python 3.10
argon2-cffi, incluido en requirements.txt.

## Cómo ejecutar en Windows

Abre el PoweShel en la carpeta donde esta el proyecto y ejecuta:

En el powershell

py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py

## Cuentas de prueba ficticias

| Usuario | Contraseña de prueba |
|         |                      |
| admin   | AdminDemo2700!       |
| user    | UserDemo2700!        |

## Pruebas realizadas

- Probe el inicio de sesion con credeciales correctas, una contraseña incorrecta y un usuario que no existe
- Probe que user solo pueda consultar y que el programa rechace las modificaciones de user y sin inicio de sesion
- Probe que el programa rechace las cantidades invalidas o que sobrepasaran el limite de 0 a 1000
- Probe cambiando P001 a 20 cerrando el programa y confirmando que la cantidad se conservo al volver a abrirlo
- Revise auditoria.jsonl para confirmar que los registros fueron guardados en auditoria 
- Probe el archivo de inventario ausente y uno que sea JSON invalido. Luego probe que el inventario.Json pueda consultar correctamente

## Fuentes y uso de IA

Use Chatgpt para entender algunos requitos y para que me ayudara a codificar en algunas partes del programa, Utilice w3 school especialmente en la parte de Python Json. Otra fuente que utilice fue dev.programing 
Chatgpt me sugirio crear una funcion separada para guardar el inventario adapte esa sugerencia guardando los cambios dentro de modificar_cantidad().

## Límite del prototipo

Los permisos se aplican dentro del programa, una persona que tenga acceso a escribir a los archivos locales puede alterar el inventario o el registro de auditoria
