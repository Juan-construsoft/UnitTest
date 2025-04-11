import unittest
from ..services.user_service import UserService
from ..models.user import User

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()
        # Clean up any test users from previous runs
        self.clean_test_users()

    def clean_test_users(self):
        conn = self.user_service.db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username LIKE 'test_user%'")
        conn.commit()
        conn.close()

    def test_register_user(self):
        # Test user registration
        user_id = self.user_service.register_user(
            'test_user1',
            'test1@example.com',
            'password123'
        )
        self.assertIsNotNone(user_id)

        # Verify user was created
        user = self.user_service.get_user_by_username('test_user1')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'test_user1')
        self.assertEqual(user.email, 'test1@example.com')

    def test_get_user_by_username(self):
        # Create a test user
        self.user_service.register_user(
            'test_user2',
            'test2@example.com',
            'password123'
        )

        # Test getting existing user
        user = self.user_service.get_user_by_username('test_user2')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'test_user2')
        self.assertEqual(user.email, 'test2@example.com')

        # Test getting non-existent user
        user = self.user_service.get_user_by_username('nonexistent_user')
        self.assertIsNone(user)

    def test_login(self):
        # Create a test user
        self.user_service.register_user(
            'test_user3',
            'test3@example.com',
            'password123'
        )

        # Test successful login
        self.assertTrue(self.user_service.login('test_user3', 'password123'))

        # Test failed login - wrong password
        self.assertFalse(self.user_service.login('test_user3', 'wrongpassword'))

        # Test failed login - non-existent user
        self.assertFalse(self.user_service.login('nonexistent_user', 'password123'))

    def test_get_all_users(self):
        # Create multiple test users
        test_users = [
            ('test_user4', 'test4@example.com', 'password123'),
            ('test_user5', 'test5@example.com', 'password123')
        ]
        for username, email, password in test_users:
            self.user_service.register_user(username, email, password)

        # Test getting all users
        users = self.user_service.get_all_users()
        self.assertIsNotNone(users)
        self.assertIsInstance(users, list)
        
        # Verify test users are in the list
        test_usernames = [user[0] for user in test_users]
        found_users = [user for user in users if user.username in test_usernames]
        self.assertEqual(len(found_users), len(test_users))

    def tearDown(self):
        # Clean up test users
        self.clean_test_users()

if __name__ == '__main__':
    unittest.main()