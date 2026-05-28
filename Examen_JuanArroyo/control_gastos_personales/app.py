import os

from flask import Flask, jsonify, render_template, request
from loguru import logger

from config import get_settings
from event_reporter import EventReporter
from gasto_repository import GastoRepository
from gasto_service import GastoService
from logging_config import setup_logging
from validators import ValidationError

FIS_HEADER = 'X-FIS-EPN-KEY'


def create_app() -> Flask:
    setup_logging()
    settings = get_settings()
    repository = GastoRepository(settings.db_path)
    gasto_service = GastoService(repository)
    event_reporter = EventReporter()
    app = Flask(__name__)

    @app.before_request
    def require_fis_api_key():
        if request.path in ('/', '/health') or request.path.startswith('/static'):
            return None
        if request.method == 'OPTIONS':
            return None

        provided = request.headers.get(FIS_HEADER)
        if not settings.fis_api_key:
            logger.error('FIS_API_KEY no configurada en el entorno')
            return jsonify({'error': 'Servidor mal configurado'}), 500
        if provided != settings.fis_api_key:
            logger.warning(
                'Acceso denegado: API key inválida o ausente en {}',
                request.path,
            )
            return jsonify({'error': 'No autorizado: API key inválida'}), 401
        return None

    @app.route('/')
    def index():
        return render_template('index.html', fis_api_key=settings.fis_api_key)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'service': 'control_gastos_personales'})

    @app.route('/gastos', methods=['GET'])
    def get_gastos():
        try:
            data = gasto_service.list_all()
            event_reporter.report(
                'READ_ALL',
                'Consulta de Gastos',
                'El usuario consultó la lista completa de gastos',
            )
            logger.info('Listado de gastos: {} registros', len(data))
            return jsonify(data)
        except Exception as exc:
            logger.error('Error en GET /gastos: {}', exc)
            return jsonify({'error': 'Error interno del servidor'}), 500

    @app.route('/gastos/<int:gasto_id>', methods=['GET'])
    def get_gasto(gasto_id: int):
        try:
            gasto = gasto_service.get_by_id(gasto_id)
            if not gasto:
                logger.warning('Gasto no encontrado: id={}', gasto_id)
                return jsonify({'error': 'Gasto no encontrado'}), 404
            event_reporter.report(
                'READ_ONE',
                'Consulta de Gasto',
                f'Consulta del gasto con ID {gasto_id}',
                payload=gasto,
            )
            logger.info('Consulta de gasto id={}', gasto_id)
            return jsonify(gasto)
        except Exception as exc:
            logger.error('Error en GET /gastos/{}: {}', gasto_id, exc)
            return jsonify({'error': 'Error interno del servidor'}), 500

    @app.route('/gastos', methods=['POST'])
    def create_gasto():
        try:
            nuevo = gasto_service.create(request.get_json(silent=True))
            event_reporter.report(
                'CREATE',
                'Nuevo Gasto Registrado',
                f"Se creó un nuevo gasto: {nuevo['descripcion']}",
                payload=nuevo,
            )
            logger.info('Gasto creado id={}', nuevo['id'])
            return jsonify(nuevo), 201
        except ValidationError as err:
            logger.warning('Validación POST /gastos: {}', err.message)
            return jsonify({'error': err.message}), err.status_code
        except Exception as exc:
            logger.error('Error en POST /gastos: {}', exc)
            return jsonify({'error': 'Error interno del servidor'}), 500

    @app.route('/gastos/<int:gasto_id>', methods=['PUT'])
    def update_gasto(gasto_id: int):
        try:
            gasto = gasto_service.update(gasto_id, request.get_json(silent=True))
            event_reporter.report(
                'UPDATE',
                'Gasto Actualizado',
                f'Se actualizó el gasto con ID {gasto_id}',
                payload=gasto,
            )
            logger.info('Gasto actualizado id={}', gasto_id)
            return jsonify(gasto)
        except ValidationError as err:
            logger.warning(
                'Validación PUT /gastos/{}: {}', gasto_id, err.message
            )
            return jsonify({'error': err.message}), err.status_code
        except Exception as exc:
            logger.error('Error en PUT /gastos/{}: {}', gasto_id, exc)
            return jsonify({'error': 'Error interno del servidor'}), 500

    @app.route('/gastos/<int:gasto_id>', methods=['DELETE'])
    def delete_gasto(gasto_id: int):
        try:
            gasto_service.delete(gasto_id)
            event_reporter.report(
                'DELETE',
                'Gasto Eliminado',
                f'Se eliminó el gasto con ID {gasto_id}',
                payload={'id': gasto_id},
            )
            logger.info('Gasto eliminado id={}', gasto_id)
            return jsonify({'message': 'Gasto eliminado correctamente'})
        except ValidationError as err:
            logger.warning(
                'Validación DELETE /gastos/{}: {}', gasto_id, err.message
            )
            return jsonify({'error': err.message}), err.status_code
        except Exception as exc:
            logger.error('Error en DELETE /gastos/{}: {}', gasto_id, exc)
            return jsonify({'error': 'Error interno del servidor'}), 500

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', '5000'))
    logger.info('Servidor de Control de Gastos en puerto {}', port)
    app.run(port=port)
