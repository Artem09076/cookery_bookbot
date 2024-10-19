from pydantic_settings import  BaseSettings, SettingsConfigDict
from src.logger import logger


class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    BOT_WEBHOOK_URL: str
    @property
    def db_url(self):
        return  f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='config/.env', env_file_encoding='utf-8')

try:
    settings = Settings()
    logger.info('Настройки успешно загружены')
except Exception as e:
    logger.error(f'Ошибка загрузки настроек: {e}')
