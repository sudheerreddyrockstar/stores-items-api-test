from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.models.user import UserModel
from starter_code.tests.base_test import BaseTest
import json


class Itemtest(BaseTest):
    def setUp(self):
        super(Itemtest, self).setUp()  #invoking the setUp method of the parent class of ItemTest.
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_request.data)['access_token']
                self.access = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers={'Authorization': self.access})
                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/item/test', headers={'Authorization': self.access})
                self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.delete('/item/test')
                self.assertEqual(response.status_code, 200)

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.post('/item/test', data=json.dumps({'price': 19.99, 'store_id': 1}),
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', data=json.dumps({'price': 19.99, 'store_id': 1}),
                            headers={'Content-Type': 'application/json'})
                response = client.post('/item/test', data=json.dumps({'price': 19.99, 'store_id': 1}),
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 400)

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.put('/item/test', data=json.dumps({'price': 19.99, 'store_id': 1}),
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price,19.99)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                response = client.put('/item/test', data=json.dumps({'price': 19.99, 'store_id': 1}),
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price,19.99)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                resp = client.get('/items')
                self.assertDictEqual({'items': [{'name': 'test', 'price': 5.99}]}, json.loads(resp.data))
