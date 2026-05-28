from gasto_repository import GastoRepository
from validators import ValidationError, validate_gasto_payload


class GastoService:
    def __init__(self, repository: GastoRepository):
        self._repo = repository

    def list_all(self) -> list[dict]:
        return self._repo.list_all()

    def get_by_id(self, gasto_id: int) -> dict | None:
        return self._repo.get_by_id(gasto_id)

    def create(self, raw_data: dict | None) -> dict:
        data = validate_gasto_payload(raw_data, partial=False)
        explicit_id = data.pop('id', None)
        if explicit_id is not None and self._repo.exists(explicit_id):
            raise ValidationError(
                f"Ya existe un gasto con id {explicit_id}", status_code=409
            )
        return self._repo.create(
            descripcion=data['descripcion'],
            monto=data['monto'],
            categoria=data.get('categoria', 'Otros'),
            gasto_id=explicit_id,
        )

    def update(self, gasto_id: int, raw_data: dict | None) -> dict:
        if not self._repo.exists(gasto_id):
            raise ValidationError('Gasto no encontrado', status_code=404)
        data = validate_gasto_payload(raw_data, partial=True)
        if not data:
            raise ValidationError('No hay campos válidos para actualizar')
        new_id = data.pop('id', None)
        if new_id is not None and new_id != gasto_id and self._repo.exists(new_id):
            raise ValidationError(
                f"Ya existe un gasto con id {new_id}", status_code=409
            )
        updated = self._repo.update(gasto_id, data)
        if updated is None:
            raise ValidationError('Gasto no encontrado', status_code=404)
        return updated

    def delete(self, gasto_id: int) -> dict:
        removed = self._repo.delete(gasto_id)
        if removed is None:
            raise ValidationError('Gasto no encontrado', status_code=404)
        return removed
