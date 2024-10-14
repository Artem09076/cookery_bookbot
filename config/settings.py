from pydantic_settings import  BaseSettings, SettingsConfigDict

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

settings = Settings()
