# backend/services/user_service.py

from ..db.database import Database
from ..models.user import User

class UserService:
    def __init__(self):
        self.db = Database()

    def register_user(self, username, email, password):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, password))
        conn.commit()
        return cursor.lastrowid

    def get_user_by_username(self, username):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, email, password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return User(*row)
        return None

    def login(self, username, password):
        """
        Retorna True si el usuario existe y coincide la contraseña, False si no.
        """
        user = self.get_user_by_username(username)
        if user and user.password == password:
            return True
        return False

    def get_all_users(self):
        conn = None
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, email, password FROM users")
            rows = cursor.fetchall()
            if not rows:
                print("No users found in database")
                return []
            users = [User(*row) for row in rows]
            print(f"Successfully fetched {len(users)} users from database")
            return users
        except Exception as e:
            print(f"Error fetching users: {str(e)}")
            raise e
        finally:
            if conn:
                conn.close()
