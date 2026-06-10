import csv


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
            producto_actual
        )

        productos.append({
            "producto": producto_actual,
            "total_unidades": total_unidades,
            "total_pesos": total_pesos
        })

        total_unidades_sucursal += total_unidades
        total_importe_sucursal += total_pesos

        mayor_producto, mayor_importe = actualizar_mayor_producto(
            producto_actual,
            total_pesos,
            mayor_producto,
            mayor_importe
        )

        menor_producto, menor_importe = actualizar_menor_producto(
            producto_actual,
            total_pesos,
            menor_producto,
            menor_importe
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
        "nuevo_indice": i
    }


def procesar_registros(registros):
    """
    Procesa todos los registros del CSV.

    Importante: los registros deben estar ordenados por sucursal y producto.
    """
    sucursales = []
    cantidad_sucursales = 0
    importe_total_general = 0

    i = 0

    while i < len(registros):
        resultado_sucursal = procesar_sucursal(registros, i)

        sucursales.append(resultado_sucursal)
        cantidad_sucursales += 1
        importe_total_general += resultado_sucursal["total_importe_sucursal"]

        i = resultado_sucursal["nuevo_indice"]

    return {
        "sucursales": sucursales,
        "cantidad_sucursales": cantidad_sucursales,
        "importe_total_general": importe_total_general
    }


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


def procesar_archivo(path_csv):
    """Lee y procesa el archivo CSV."""
    registros = leer_csv(path_csv)
    return procesar_registros(registros)


def menu():
    """Función principal del programa."""
    path_csv = input("Indique el path del csv: ")

    resultado = procesar_archivo(path_csv)

    mostrar_resultado_general(resultado)


if __name__ == "__main__":
    menu()