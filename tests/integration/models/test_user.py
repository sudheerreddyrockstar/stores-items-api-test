from starter_code.models.user import UserModel
from starter_code.tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'abcd')
            self.assertIsNone(user.find_by_username('test'))
            self.assertIsNone(user.find_by_id(1))

            user.save_to_db()
            self.assertIsNotNone(user.find_by_username('test'))
            self.assertIsNotNone(user.find_by_id(1))

