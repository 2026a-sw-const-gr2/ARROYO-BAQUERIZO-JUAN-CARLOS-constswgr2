import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv('.env_config')
load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_port: int
    fis_api_key: str
    event_manager_url: str
    log_level: str
    log_file: str
    db_path: str


def get_settings() -> Settings:
    return Settings(
        app_port=int(os.getenv('APP_PORT', '5000')),
        fis_api_key=os.getenv('FIS_API_KEY', ''),
        event_manager_url=os.getenv(
            'EVENT_MANAGER_URL', 'http://localhost:3000/events'
        ),
        log_level=os.getenv('LOG_LEVEL', 'INFO'),
        log_file=os.getenv('LOG_FILE', 'logs/audit.log'),
        db_path=os.getenv('DB_DATABASE', 'db/gastos.sqlite'),
    )
