from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Woyage Followups API"
    model_name: str = "gpt-4o-mini"
    max_output_questions: int = 3

    class Config:
        env_file = ".env"

settings = Settings()
