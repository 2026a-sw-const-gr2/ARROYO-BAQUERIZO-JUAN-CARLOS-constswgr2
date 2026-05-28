from typing import Any

MAX_DESCRIPCION = 200
MAX_CATEGORIA = 50
CATEGORIAS_VALIDAS = {'Comida', 'Transporte', 'Educación', 'Salud', 'Otros'}


class ValidationError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _require_str(value: Any, field: str, max_len: int) -> str:
    if value is None or not isinstance(value, str):
        raise ValidationError(f"'{field}' debe ser una cadena de texto")
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError(f"'{field}' no puede estar vacío")
    if len(cleaned) > max_len:
        raise ValidationError(
            f"'{field}' excede el máximo de {max_len} caracteres"
        )
    return cleaned


def validate_gasto_payload(data: dict | None, *, partial: bool = False) -> dict:
    if data is None or not isinstance(data, dict):
        raise ValidationError('El cuerpo de la solicitud debe ser JSON válido')

    result: dict = {}

    if 'descripcion' in data or not partial:
        if 'descripcion' not in data and partial:
            pass
        else:
            result['descripcion'] = _require_str(
                data.get('descripcion'), 'descripcion', MAX_DESCRIPCION
            )

    if 'monto' in data or not partial:
        if 'monto' not in data and partial:
            pass
        else:
            monto = data.get('monto')
            if monto is None:
                raise ValidationError("'monto' es obligatorio")
            try:
                monto_f = float(monto)
            except (TypeError, ValueError):
                raise ValidationError("'monto' debe ser numérico")
            if monto_f <= 0:
                raise ValidationError("'monto' debe ser mayor que cero")
            result['monto'] = round(monto_f, 2)

    if 'categoria' in data:
        cat = _require_str(data.get('categoria'), 'categoria', MAX_CATEGORIA)
        if cat not in CATEGORIAS_VALIDAS:
            raise ValidationError(
                f"'categoria' inválida. Valores permitidos: {sorted(CATEGORIAS_VALIDAS)}"
            )
        result['categoria'] = cat
    elif not partial:
        result['categoria'] = 'Otros'

    if 'id' in data and data['id'] is not None:
        try:
            result['id'] = int(data['id'])
            if result['id'] <= 0:
                raise ValidationError("'id' debe ser un entero positivo")
        except (TypeError, ValueError):
            raise ValidationError("'id' debe ser un entero válido")

    return result
