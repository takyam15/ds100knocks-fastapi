from dotenv import dotenv_values
import pandas as pd
from sqlalchemy import create_engine, URL


def register_data(file, conn):
    df = pd.read_csv(f'data/{file}.csv')
    df.to_sql(file, conn, if_exists='replace', index=False)


if __name__ == '__main__':
    config = dotenv_values('postgres/.env.dev')
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

    register_data('category', engine)
    register_data('customer', engine)
    register_data('geocode', engine)
    register_data('product', engine)
    register_data('receipt', engine)
    register_data('store', engine)
