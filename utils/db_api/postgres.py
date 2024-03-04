import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                           port=DB_PORT)
        self.cursor = self.connection.cursor()

    def create_user(self, telegram_id, phone_number, full_name, date_of_birth, city, information, languages, tajriba):
        try:
            self.cursor.execute(
                "INSERT INTO health_user(telegram_id,phone_number, full_name, date_of_birth, city, information, languages, tajriba , created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, NOW())",
                (telegram_id, phone_number, full_name, date_of_birth, city, information, languages, tajriba)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Client Error: {e}")

    def get_ball(self, telegram_id, ball):
        try:
            ball_str = str(ball)

            self.cursor.execute(
                "UPDATE health_user SET ball = %s WHERE telegram_id = %s",
                (ball_str, telegram_id)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error updating ball: {e}")

    async def get_vakansiya(self, name):
        try:
            self.cursor.execute(
                "SELECT * FROM health_vakansiya WHERE name=%s",
                (name,)
            )
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(f"Database Error: {e}")

    async def get_vakansiyaru(self, name):
        try:
            self.cursor.execute(
                "SELECT * FROM health_vakansiyaru WHERE name=%s",
                (name,)
            )
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(f"Database Error: {e}")

    async def get_vakansiya_key(self):
        try:
            self.cursor.execute(
                "SELECT * FROM health_vakansiya"
            )
            result = self.cursor.fetchall()
            return result if result else []
        except Exception as e:
            print(f"Database Error: {e}")

    async def get_vakansiya_keyru(self):
        try:
            self.cursor.execute(
                "SELECT * FROM health_vakansiyaru"
            )
            result = self.cursor.fetchall()
            return result if result else []
        except Exception as e:
            print(f"Database Error: {e}")

    async def get_user(self, telegram_id):
        try:
            self.cursor.execute(
                "SELECT * FROM health_user WHERE telegram_id=%s",
                (telegram_id,)
            )
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(f"Database Error: {e}")

    async def get_media(self):
        try:
            self.cursor.execute(
                "SELECT * FROM health_media "
            )
            result = self.cursor.fetchone()
            return result if result else []
        except Exception as e:
            print(f"Database Error: {e}")

    async def okompaniya(self):
        try:
            self.cursor.execute(
                "SELECT * FROM health_bizhaqimizda "
            )
            result = self.cursor.fetchone()
            return result if result else []
        except Exception as e:
            print(f"Database Error: {e}")


    async def okompaniyaru(self):
        try:
            self.cursor.execute(
                "SELECT * FROM health_bizhaqimizdaru "
            )
            result = self.cursor.fetchone()
            return result if result else []
        except Exception as e:
            print(f"Database Error: {e}")

    def create_shikoyat(self, telegram_id, nickname, phone_number, about):
        try:
            self.cursor.execute(
                "INSERT INTO health_taklif(telegram_id, nickname, phone_number, about, created_at) VALUES(%s, %s, %s, %s, NOW())",
                (telegram_id, nickname, phone_number, about)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Client Error: {e}")
