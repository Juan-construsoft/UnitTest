def calcular_total(items):
    """
    Calcula el total de una orden.
    items: lista de diccionarios con 'precio' y 'cantidad'.
    """
    if not isinstance(items, list):
        raise ValueError("La orden debe ser una lista de ítems.")
    
    total = 0
    for item in items:
        if 'precio' not in item or 'cantidad' not in item:
            raise ValueError("Cada ítem debe tener 'precio' y 'cantidad'.")
        if not isinstance(item['precio'], (int, float)) or item['precio'] < 0:
            raise ValueError("El precio debe ser un número positivo.")
        if not isinstance(item['cantidad'], int) or item['cantidad'] <= 0:
            raise ValueError("La cantidad debe ser un entero mayor a cero.")
        
        total += item['precio'] * item['cantidad']
    
    return round(total, 2)