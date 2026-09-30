
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

password = quote_plus("password@123")  # Automatically converts '@' to '%40'
db_url = f"postgresql://postgres:{password}@localhost:5432/fastapidemo"

engine = create_engine(db_url);
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


