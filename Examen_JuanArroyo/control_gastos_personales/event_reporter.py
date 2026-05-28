import requests
from loguru import logger

from config import get_settings

QUERY_ACTIONS = {'READ_ALL', 'READ_ONE'}


class EventReporter:
    def __init__(self) -> None:
        self._settings = get_settings()

    def report(
        self,
        action: str,
        title: str,
        description: str,
        payload: dict | None = None,
    ) -> None:
        normalized = action.upper()
        if normalized in QUERY_ACTIONS:
            normalized = 'QUERY'

        event_data = {
            'source': 'control_gastos_personales',
            'entity': 'gasto',
            'action': normalized,
            'title': title[:200],
            'description': (description or '')[:500],
            'payload': payload or {},
        }

        try:
            response = requests.post(
                self._settings.event_manager_url,
                json=event_data,
                timeout=5,
            )
            if response.status_code not in (200, 201):
                logger.warning(
                    'Event Manager rechazó evento {}: {}',
                    normalized,
                    response.text,
                )
            else:
                logger.info('Evento {} registrado en Event Manager', normalized)
        except requests.RequestException as exc:
            logger.error('No se pudo conectar al Event Manager: {}', exc)
