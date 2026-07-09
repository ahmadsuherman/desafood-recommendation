from sqlalchemy import create_engine
from app.core.config import *

print("DB_HOST =", repr(DB_HOST))
print("DB_PORT =", repr(DB_PORT))
print("DB_DATABASE =", repr(DB_DATABASE))
print("DB_USERNAME =", repr(DB_USERNAME))
print("DB_PASSWORD =", "***" if DB_PASSWORD else None)

DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

print("DATABASE_URL =", DATABASE_URL)

engine = create_engine(DATABASE_URL)