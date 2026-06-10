import pytest

from main import (
    calcular_importe,
    ordenar_registros,
    calcular_total_producto,
    actualizar_mayor_producto,
    actualizar_menor_producto,
    procesar_registros,
    elegir_archivo,
    ARCHIVO_ORDENADO,
    ARCHIVO_DESORDENADO,
)


def test_calcular_importe():
    cantidad = 3
    precio = 1500

    resultado = calcular_importe(cantidad, precio)

    assert resultado == 4500


def test_ordenar_registros_por_sucursal_y_producto():
    registros = [
        ["Sucursal B", "Pan", "x", "x", "2", "1000"],
        ["Sucursal A", "Leche", "x", "x", "1", "1500"],
        ["Sucursal A", "Arroz", "x", "x", "3", "800"],
    ]

    resultado = ordenar_registros(registros)

    assert resultado[0][0] == "Sucursal A"
    assert resultado[0][1] == "Arroz"
    assert resultado[1][0] == "Sucursal A"
    assert resultado[1][1] == "Leche"
    assert resultado[2][0] == "Sucursal B"
    assert resultado[2][1] == "Pan"


def test_calcular_total_producto():
    registros = [
        ["Sucursal A", "Leche", "x", "x", "2", "1000"],
        ["Sucursal A", "Leche", "x", "x", "3", "1000"],
        ["Sucursal A", "Pan", "x", "x", "1", "500"],
    ]

    total_unidades, total_pesos, nuevo_indice = calcular_total_producto(
        registros,
        0,
        "Sucursal A",
        "Leche",
    )

    assert total_unidades == 5
    assert total_pesos == 5000
    assert nuevo_indice == 2


def test_actualizar_mayor_y_menor_producto():
    mayor_producto, mayor_importe = actualizar_mayor_producto(
        "Leche",
        5000,
        None,
        0,
    )

    menor_producto, menor_importe = actualizar_menor_producto(
        "Pan",
        800,
        None,
        0,
    )

    assert mayor_producto == "Leche"
    assert mayor_importe == 5000
    assert menor_producto == "Pan"
    assert menor_importe == 800


def test_procesar_registros_calcula_totales_generales():
    registros = [
        ["Sucursal B", "Pan", "x", "x", "2", "1000"],
        ["Sucursal A", "Leche", "x", "x", "1", "1500"],
        ["Sucursal A", "Leche", "x", "x", "2", "1500"],
        ["Sucursal A", "Arroz", "x", "x", "3", "800"],
    ]

    resultado = procesar_registros(registros)

    assert resultado["cantidad_sucursales"] == 2
    assert resultado["importe_total_general"] == 8900

    sucursal_a = resultado["sucursales"][0]

    assert sucursal_a["sucursal"] == "Sucursal A"
    assert sucursal_a["total_unidades_sucursal"] == 6
    assert sucursal_a["mayor_producto"] == "Leche"
    assert sucursal_a["mayor_importe"] == 4500
    assert sucursal_a["menor_producto"] == "Arroz"
    assert sucursal_a["menor_importe"] == 2400


def test_elegir_archivo():
    assert elegir_archivo("1") == ARCHIVO_ORDENADO
    assert elegir_archivo("2") == ARCHIVO_DESORDENADO

    with pytest.raises(ValueError):
        elegir_archivo("3")
