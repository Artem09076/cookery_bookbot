from pydantic_settings import  BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5555
    DB_NAME: str = 'postgres'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = '123'

    @property
    def db_url(self):
        return  f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='config/.env', env_file_encoding='utf-8')


settings = Settings()