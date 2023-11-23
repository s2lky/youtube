from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv(verbose=True)
    
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')


def insert_db(df, table_name):
    db_connection = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(db_connection)
    df.to_sql(table_name, engine, if_exists='append', index=False)
    
if __name__ == "__main__":
    print(dbname)