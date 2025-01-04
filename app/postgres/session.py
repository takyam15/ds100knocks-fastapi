from dotenv import dotenv_values
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker


config = dotenv_values('app/postgres/.env.dev')

url_object = URL.create(
    "postgresql+psycopg",
    username=config["POSTGRES_USER"],
    password=config["POSTGRES_PASSWORD"],  # plain (unescaped) text
    host=config.get("POSTGRES_HOST", "postgres"),
    port=config.get("POSTGRES_PORT", "5432"),
    database=config.get("POSTGRES_DB", "postgres"),
    query={"options": f"-c search_path={config.get('POSTGRES_SCHEMA', 'public')}"},
)

engine = create_engine(url_object)

SessionLocal = sessionmaker(engine)
