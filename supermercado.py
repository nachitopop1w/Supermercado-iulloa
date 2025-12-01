# Importa pandas para leer y trabajar con datos
import pandas as pd
import csv

print("Leyendo archivo productos.csv desde el entorno local...")

# Nombre del archivo (local, NO Colab)
archivo = "productos.csv"

# Leer el archivo sin encabezados (porque tu archivo NO tiene títulos)
df = pd.read_csv(archivo, header=None)

# Columna 1: nombre del producto
# Columna 2: precio del producto
col_nombre = 1
col_precio = 2

# Convertir la columna de precios a número (por si viene como texto)
df[col_precio] = pd.to_numeric(df[col_precio], errors="coerce")

# Buscar la fila donde el precio es máximo (producto más caro)
fila_mas_cara = df.loc[df[col_precio].idxmax()]

# Mostrar resultados
print("\nEl producto más caro es:", fila_mas_cara[col_nombre])
print("Con un precio de:", fila_mas_cara[col_precio])

# -------------------------------------------------------
# FUNCIÓN valorTotalBodega (tu mismo código, sin cambios)
# -------------------------------------------------------

def valorTotalBodega(archivo):
    total = 0
    lector = csv.reader(archivo)
    for fila in lector:
        precio = int(fila[2])
        cantidad = int(fila[3])
        total += precio * cantidad
    return total

with open("productos.csv", "r") as productos:
    print(f"La bodega vale en total {valorTotalBodega(productos)}")

# -------------------------------------------------------
# Código para items y productos (igual que tu código)
# -------------------------------------------------------

ITEMS_PATH = "items.csv"
PRODUCTOS_PATH = "productos.csv"

def leer_lineas(path):
    with open(path, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    lineas = [l.rstrip("\n\r") for l in lineas]
    lineas = [l for l in lineas if l.strip() != ""]
    return lineas

def separar_fila(linea):
    if ";" in linea:
        return [c.strip() for c in linea.split(";")]
    else:
        return [c.strip() for c in linea.split(",")]

lineas_items = leer_lineas(ITEMS_PATH)
lineas_productos = leer_lineas(PRODUCTOS_PATH)

rows_items = [separar_fila(l) for l in lineas_items]
rows_productos = [separar_fila(l) for l in lineas_productos]

start_items = 0
if rows_items and not rows_items[0][0].isdigit():
    start_items = 1

start_prod = 0
if rows_productos and not rows_productos[0][0].isdigit():
    start_prod = 1

# Construir diccionario id → (nombre, precio)
info_productos = {}
for fila in rows_productos[start_prod:]:
    if len(fila) < 3:
        continue
    id_prod = fila[0]
    nombre = fila[1]
    try:
        precio = float(fila[2])
    except:
        t = fila[2].replace(".", "").replace(",", ".")
        try:
            precio = float(t)
        except:
            precio = 0.0
    info_productos[id_prod] = (nombre, precio)

# Acumular ingresos
ingresos = {}
for fila in rows_items[start_items:]:
    if len(fila) < 3:
        continue
    id_prod = fila[1]

    try:
        cantidad = float(fila[2])
    except:
        t = fila[2].replace(".", "").replace(",", ".")
        try:
            cantidad = float(t)
        except:
            cantidad = 0.0

    if id_prod in info_productos:
        nombre, precio = info_productos[id_prod]
        ingreso = precio * cantidad
        ingresos[nombre] = ingresos.get(nombre, 0) + ingreso

# Mostrar resultado
if not ingresos:
    print("No se pudieron calcular ingresos.")
else:
    orden = sorted(ingresos.items(), key=lambda x: x[1], reverse=True)
    print("\nIngresos por producto:")
    for nombre, ingreso in orden:
        print(f" - {nombre}: {ingreso}")
    print("\nProducto con más ingresos:", orden[0][0])
    print("Valor:", orden[0][1])
