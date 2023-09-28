from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.tests.base_test import BaseTest


class Storetest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')
        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(store.find_by_name('test'))
            store.save_to_db()
            self.assertIsNotNone(store.find_by_name('test'))
            store.delete_from_db()
            self.assertIsNone(store.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.9, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')
            # It fetches the first item in database and checks it equal or not

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test',
                'items': [{'name': 'test_item', 'price': 19.99}]
            }

            self.assertDictEqual(store.json(), expected)