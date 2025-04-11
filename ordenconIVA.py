def calcular_total_con_iva(items, pais):
    """
    Calcula el total con IVA dependiendo del país.
    Si el país es 'Colombia', se aplica el 19% de IVA.
    Si es 'México', se aplica el 16%.
    En otros países, no se aplica IVA.
    """
    tasas_iva = {
        "Colombia": 0.19,
        "México": 0.16
    }

    if not isinstance(items, list):
        raise ValueError("La orden debe ser una lista de ítems.")

    subtotal = 0
    for item in items:
        if 'precio' not in item or 'cantidad' not in item:
            raise ValueError("Cada ítem debe tener 'precio' y 'cantidad'.")
        subtotal += item['precio'] * item['cantidad']
    
    iva = tasas_iva.get(pais, 0)
    total = subtotal * (1 + iva)
    return round(total, 2)