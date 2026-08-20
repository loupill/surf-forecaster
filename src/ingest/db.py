import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def get_engine():
    """
    Create a SQLAlchemy engine from the environment variables
    """

    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    db = os.environ["POSTGRES_DB"]

    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(connection_string, future=True)


def write_dataframe(df, table_name, schema, engine, if_exists = 'append'):
    """
    Write a DataFrame to a Postgres table.
    """

    df.to_sql(
        table_name,
        con = engine,
        schema = schema,
        if_exists = if_exists,
        index = False
    )