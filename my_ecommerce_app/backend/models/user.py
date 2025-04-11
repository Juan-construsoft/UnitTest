# backend/models/user.py

class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password  # En un sistema real, ¡debería ir encriptada!

    def __repr__(self):
        return f"<User {self.user_id}: {self.username} ({self.email})>"