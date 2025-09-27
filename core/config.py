from pydantic_settings import BaseSettings
from pydantic import Field
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # App
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Mongo (từ .env)
    MONGO_HOST: str = Field(default="localhost")
    MONGO_PORT: int = Field(default=27017)
    MONGO_DB: str = Field(default="face_recognition")
    MONGO_USER: str = Field(default="")
    MONGO_PASSWORD: str = Field(default="")
    MONGO_AUTH_SOURCE: str = Field(default="admin")  # đổi nếu bạn tạo user ở DB khác

    @property
    def MONGO_URI(self) -> str:
        if self.MONGO_USER and self.MONGO_PASSWORD:
            user = quote_plus(self.MONGO_USER)
            pwd = quote_plus(self.MONGO_PASSWORD)
            return (
                f"mongodb://{user}:{pwd}@{self.MONGO_HOST}:{self.MONGO_PORT}/"
                f"{self.MONGO_DB}?authSource={self.MONGO_AUTH_SOURCE}"
            )
        # no auth
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"

    class Config:
        env_file = ".env"

settings = Settings()