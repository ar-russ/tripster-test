from pydantic import BaseModel


class Auth(BaseModel):
    SECRET: str = "SECRET"


class Postgres(BaseModel):
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = ""
    PASSWORD: str = ""
    DB: str = ""

    def build_url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"


class Settings(BaseModel):
    AUTH: Auth = Auth()
    POSTGRES: Postgres = Postgres()
    HOST: str = "localhost"
    PORT: int = 8080


settings = Settings()
