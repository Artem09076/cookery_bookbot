from pydantic_settings import  BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str = '7932967993:AAE1rN1mEKhOzPci7VQhQM9GchEgWgtor-A'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5555
    DB_NAME: str = 'postgres'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = '123'
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    @property
    def db_url(self):
        return  f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='config/.env', env_file_encoding='utf-8')


settings = Settings()