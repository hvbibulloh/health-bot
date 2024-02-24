import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                           port=DB_PORT)
        self.cursor = self.connection.cursor()

    def create_user(self, phone_number, full_name, date_of_birth, city, information, languages):
        try:
            self.cursor.execute(
                "INSERT INTO health_user(phone_number, full_name, date_of_birth, city, information, languages) VALUES(%s, %s, %s, %s, %s, %s)",
                (phone_number, full_name, date_of_birth, city, information, languages)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Client Error: {e}")
