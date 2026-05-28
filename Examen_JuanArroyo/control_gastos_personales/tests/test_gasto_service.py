import pytest

from gasto_repository import GastoRepository
from gasto_service import GastoService
from validators import ValidationError


@pytest.fixture
def service(tmp_path):
    db_file = tmp_path / 'test_gastos.sqlite'
    return GastoService(GastoRepository(str(db_file)))


def test_create_gasto_asigna_id_automatico(service):
    gasto = service.create(
        {'descripcion': 'Almuerzo', 'monto': 12.5, 'categoria': 'Comida'}
    )
    assert gasto['id'] == 1
    assert gasto['monto'] == 12.5


def test_create_rechaza_id_duplicado(service):
    service.create(
        {
            'id': 10,
            'descripcion': 'Primero',
            'monto': 5,
            'categoria': 'Otros',
        }
    )
    with pytest.raises(ValidationError) as exc:
        service.create(
            {
                'id': 10,
                'descripcion': 'Duplicado',
                'monto': 8,
                'categoria': 'Otros',
            }
        )
    assert exc.value.status_code == 409


def test_create_rechaza_monto_negativo(service):
    with pytest.raises(ValidationError):
        service.create(
            {'descripcion': 'Inválido', 'monto': -1, 'categoria': 'Otros'}
        )


def test_update_sin_json_no_rompe_servicio(service):
    creado = service.create(
        {'descripcion': 'Base', 'monto': 10, 'categoria': 'Otros'}
    )
    with pytest.raises(ValidationError):
        service.update(creado['id'], None)


def test_delete_gasto_inexistente(service):
    with pytest.raises(ValidationError) as exc:
        service.delete(999)
    assert exc.value.status_code == 404


def test_datos_persisten_en_sqlite(tmp_path):
    db_file = str(tmp_path / 'persist.sqlite')
    svc1 = GastoService(GastoRepository(db_file))
    svc1.create(
        {'descripcion': 'Persistente', 'monto': 99, 'categoria': 'Otros'}
    )
    svc2 = GastoService(GastoRepository(db_file))
    gastos = svc2.list_all()
    assert len(gastos) == 1
    assert gastos[0]['descripcion'] == 'Persistente'
