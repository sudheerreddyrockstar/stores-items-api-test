from starter_code.models.user import UserModel
from starter_code.tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                data = {'username': 'test', 'password': '1234'}
                json_data = json.dumps(data)
                headers = {'Content-Type': 'application/json'}
                request = client.post('/register', data=json_data, headers=headers)
                self.assertEqual(request.status_code,  201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'user created successfully.'},
                                     json.loads(request.data))

    def test_register_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register',
                            data=json.dumps({'username': 'test', 'password': '1234'}),
                            headers={'Content-Type': 'application/json'})
                auth_req = client.post('/auth',
                                       data=json.dumps({'username': 'test', 'password': '1234'}),
                                       headers={'Content-Type': 'application/json'})
                response_data = json.loads(auth_req.data)
                print("Response Data:", response_data)
                self.assertIn('access_token', response_data.keys())

    def test_register_duplicate(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register',
                            data=json.dumps({'username': 'test', 'password': '1234'}),
                            headers={'Content-Type': 'application/json'})
                response = client.post('/register', data=json.dumps({'username': 'test', 'password': '1234'}),
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with username already exists'}, json.loads(response.data))

