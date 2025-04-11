def calcular_total(items):
    if not isinstance(items, list):
        raise ValueError("La orden debe ser una lista de ítems.")
    total = 0
    for item in items:
        if 'precio' not in item or 'cantidad' not in item:
            raise ValueError("Cada ítem debe tener 'precio' y 'cantidad'.")
        total += item['precio'] * item['cantidad']
    return round(total, 2)

def crear_orden(cliente_id, items, repo):
    cliente = repo.obtener_cliente_por_id(cliente_id)
    
    if cliente is None:
        raise ValueError("Cliente no encontrado.")
    if not cliente.get("activo", False):
        raise ValueError("Cliente inactivo.")

    total = calcular_total(items)
    
    orden = {
        "cliente_id": cliente_id,
        "items": items,
        "total": total
    }

    repo.guardar_orden(orden)

    return f"Orden creada para {cliente['nombre']}, total: ${total}"