from ordenBD import calcular_total

def crear_orden(token, items, auth_service, repo):
    cliente_id = auth_service.validar_token_y_extraer_id(token)
    
    if cliente_id is None:
        raise ValueError("Token inválido o expirado.")

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