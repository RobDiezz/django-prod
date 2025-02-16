from pathlib import Path
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parent.parent.joinpath(".env")
print(env_path)

class Settings(BaseSettings):
    secret_key_django: str | None = None
    loglevel: str | None = None
    django_debug: str | None = None
    allowed_hosts: Annotated[str, Field(default="localhost")]
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding='utf-8')


settings = Settings()