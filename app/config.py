from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str

    class Config:
        env_prefix = ''
        env_file = "app/.env"
        env_file_encoding = 'utf-8'


settings = Settings()
