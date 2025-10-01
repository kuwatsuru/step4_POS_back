from pydantic import BaseModel
import os

class Settings(BaseModel):
    DATABASE_URL: str
    TAX_RATE: float = 0.1


def load_settings() -> Settings:
    # .env を使う場合は python-dotenv を利用します
    from dotenv import load_dotenv
    load_dotenv()
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL", "mysql+pymysql://user:pass@localhost:3306/pos_db"),
        TAX_RATE=float(os.getenv("TAX_RATE", "0.1")),
    )

settings = load_settings() 