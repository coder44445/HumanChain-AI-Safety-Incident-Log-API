import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text 


def create_database_if_not_exists():

    """Create the database if it doesn't exist"""

    try:
        # Create engine without database
        engine = create_engine(f"mysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/")
        
        # Create database if it doesn't exist
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}"))
            conn.commit()

    except Exception as e:
        print(f"Error creating database: {str(e)}")
        raise


if __name__ == '__main__':
    load_dotenv()