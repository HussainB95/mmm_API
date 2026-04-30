DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

print("DATABASE_URL =", DATABASE_URL)