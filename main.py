import csv
from pathlib import Path


ARCHIVO_ORDENADO = "COMPRAS_supermercado(2).csv"
ARCHIVO_DESORDENADO = "COMPRAS_supermercado_desordenado_solo_sucursal(1).csv"


def buscar_archivo(nombre_archivo):
    """
    Busca el archivo primero en la carpeta actual y después en la carpeta data.

    Esto permite usar los CSV con su nombre original, sin tener que renombrarlos.
    """
    rutas_posibles = [
        Path(nombre_archivo),
        Path("data") / nombre_archivo,
    ]

    for ruta in rutas_posibles:
        if ruta.exists():
            return ruta

    raise FileNotFoundError(f"No se encontró el archivo: {nombre_archivo}")


def leer_csv(path_csv):
    """Lee un archivo CSV y devuelve los registros sin el encabezado."""
    with open(path_csv, "r", encoding="utf-8") as archivo:
        lector = list(csv.reader(archivo))

    return lector[1:]


def obtener_sucursal(registro):
    """Devuelve la sucursal de un registro."""
    return registro[0]


def obtener_producto(registro):
    """Devuelve el producto de un registro."""
    return registro[1]


def obtener_cantidad(registro):
    """Devuelve la cantidad vendida como entero."""
    return int(registro[4])


def obtener_precio(registro):
    """Devuelve el precio unitario como float."""
    return float(registro[5])


def calcular_importe(cantidad, precio):
    """Calcula el importe total de una compra."""
    return cantidad * precio


def ordenar_registros(registros):
    """Ordena los registros por sucursal y producto."""
    return sorted(registros, key=lambda registro: (obtener_sucursal(registro), obtener_producto(registro)))


def calcular_total_producto(registros, indice_inicio, sucursal_actual, producto_actual):
    """Calcula unidades e importe total de un producto dentro de una sucursal."""
    total_unidades = 0
    total_pesos = 0
    i = indice_inicio

    while (
        i < len(registros)
        and obtener_sucursal(registros[i]) == sucursal_actual
        and obtener_producto(registros[i]) == producto_actual
    ):
        cantidad = obtener_cantidad(registros[i])
        precio = obtener_precio(registros[i])
        importe = calcular_importe(cantidad, precio)

        total_unidades += cantidad
        total_pesos += importe

        i += 1

    return total_unidades, total_pesos, i


def actualizar_mayor_producto(producto, importe, mayor_producto, mayor_importe):
    """Actualiza el producto con mayor importe."""
    if mayor_producto is None or importe > mayor_importe:
        return producto, importe

    return mayor_producto, mayor_importe


def actualizar_menor_producto(producto, importe, menor_producto, menor_importe):
    """Actualiza el producto con menor importe."""
    if menor_producto is None or importe < menor_importe:
        return producto, importe

    return menor_producto, menor_importe


def procesar_sucursal(registros, indice_inicio):
    """Procesa todos los productos de una sucursal."""
    sucursal_actual = obtener_sucursal(registros[indice_inicio])

    productos = []
    total_unidades_sucursal = 0
    total_importe_sucursal = 0

    mayor_producto = None
    mayor_importe = 0

    menor_producto = None
    menor_importe = 0

    i = indice_inicio

    while i < len(registros) and obtener_sucursal(registros[i]) == sucursal_actual:
        producto_actual = obtener_producto(registros[i])

        total_unidades, total_pesos, nuevo_indice = calcular_total_producto(
            registros,
            i,
            sucursal_actual,
            producto_actual,
        )

        productos.append({
            "producto": producto_actual,
            "total_unidades": total_unidades,
            "total_pesos": total_pesos,
        })

        total_unidades_sucursal += total_unidades
        total_importe_sucursal += total_pesos

        mayor_producto, mayor_importe = actualizar_mayor_producto(
            producto_actual,
            total_pesos,
            mayor_producto,
            mayor_importe,
        )

        menor_producto, menor_importe = actualizar_menor_producto(
            producto_actual,
            total_pesos,
            menor_producto,
            menor_importe,
        )

        i = nuevo_indice

    return {
        "sucursal": sucursal_actual,
        "productos": productos,
        "total_unidades_sucursal": total_unidades_sucursal,
        "mayor_producto": mayor_producto,
        "mayor_importe": mayor_importe,
        "menor_producto": menor_producto,
        "menor_importe": menor_importe,
        "total_importe_sucursal": total_importe_sucursal,
        "nuevo_indice": i,
    }


def procesar_registros(registros):
    """
    Procesa todos los registros.

    Los registros se ordenan antes de procesarse, por eso funciona tanto
    con el archivo ordenado como con el archivo desordenado.
    """
    registros_ordenados = ordenar_registros(registros)

    sucursales = []
    cantidad_sucursales = 0
    importe_total_general = 0

    i = 0

    while i < len(registros_ordenados):
        resultado_sucursal = procesar_sucursal(registros_ordenados, i)

        sucursales.append(resultado_sucursal)
        cantidad_sucursales += 1
        importe_total_general += resultado_sucursal["total_importe_sucursal"]

        i = resultado_sucursal["nuevo_indice"]

    return {
        "sucursales": sucursales,
        "cantidad_sucursales": cantidad_sucursales,
        "importe_total_general": importe_total_general,
    }


def procesar_archivo(nombre_archivo):
    """Busca, lee y procesa un archivo CSV."""
    path_csv = buscar_archivo(nombre_archivo)
    registros = leer_csv(path_csv)
    return procesar_registros(registros)


def mostrar_resultado_sucursal(resultado_sucursal):
    """Muestra los resultados de una sucursal."""
    print(f"\nSUCURSAL: {resultado_sucursal['sucursal']}")

    for producto in resultado_sucursal["productos"]:
        print(
            f"Producto: {producto['producto']} - "
            f"Total unidades: {producto['total_unidades']} - "
            f"Total pesos: {producto['total_pesos']:.2f}"
        )

    print(f"Total unidades sucursal: {resultado_sucursal['total_unidades_sucursal']}")
    print(
        f"Mayor compra en pesos: "
        f"{resultado_sucursal['mayor_producto']} - "
        f"{resultado_sucursal['mayor_importe']:.2f}"
    )
    print(
        f"Menor compra en pesos: "
        f"{resultado_sucursal['menor_producto']} - "
        f"{resultado_sucursal['menor_importe']:.2f}"
    )


def mostrar_resultado_general(resultado):
    """Muestra los resultados generales."""
    for sucursal in resultado["sucursales"]:
        mostrar_resultado_sucursal(sucursal)

    print("\nTOTALES GENERALES")
    print(f"Cantidad de sucursales: {resultado['cantidad_sucursales']}")
    print(f"Importe total de todas las sucursales: {resultado['importe_total_general']:.2f}")


def elegir_archivo(opcion):
    """Devuelve el nombre del archivo según la opción elegida."""
    if opcion == "1":
        return ARCHIVO_ORDENADO

    if opcion == "2":
        return ARCHIVO_DESORDENADO

    raise ValueError("Opción inválida")


def menu():
    """Función principal del programa."""
    print("Seleccione el archivo a procesar:")
    print(f"1 - {ARCHIVO_ORDENADO}")
    print(f"2 - {ARCHIVO_DESORDENADO}")

    opcion = input("Ingrese una opción: ").strip()

    try:
        nombre_archivo = elegir_archivo(opcion)
        resultado = procesar_archivo(nombre_archivo)
        mostrar_resultado_general(resultado)

    except FileNotFoundError as error:
        print(f"Error: {error}")
        print("Verificá que el archivo esté en la carpeta principal del proyecto o dentro de la carpeta data.")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    menu()
