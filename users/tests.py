from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, Game
from users.csv_utils import get_csv_path
import csv

class UserAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Seed test user & game
        self.user = User.objects.create(
            user_id=1,
            user_name="Ronnica",
            country="El Salvador",
            u_age=69,
            pincode="95413",
            city="Camiri",
            passwords="9791"
        )
        self.game = Game.objects.create(
            game_id=1,
            user_id=1,
            game_name="Viva",
            game_type="Opela",
            age_rest=13,
            rate=8913
        )

    def test_01_home_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Digital video game distribution')
        self.assertContains(resp, 'User Database')
        self.assertContains(resp, 'Life is a game!')

    def test_02_insert_user_and_csv_sync(self):
        data = {
            'user_id': '101',
            'user_name': 'trial',
            'country': 'india',
            'u_age': '19',
            'pincode': '382007',
            'city': 'gandhinagar',
            'passwords': '2828'
        }
        resp = self.client.post('/Insertuser', data)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'User trial is insert successfully !')
        self.assertTrue(User.objects.filter(user_id=101).exists())

        # Check CSV
        with open(get_csv_path(), 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('101,trial,india,19,382007,gandhinagar,2828', content)

    def test_03_duplicate_user_id(self):
        data = {
            'user_id': '1',
            'user_name': 'duplicate',
            'country': 'india',
            'u_age': '20',
            'pincode': '123456',
            'city': 'delhi',
            'passwords': 'pass'
        }
        resp = self.client.post('/Insertuser', data)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'User ID 1 already exists!')

    def test_04_show_user(self):
        resp = self.client.get('/showuser')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Show User Details')
        self.assertContains(resp, 'Ronnica')

    def test_05_sort_user(self):
        resp = self.client.get('/sortuser?sort_by=Country')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Show User Data - Sorted')
        self.assertContains(resp, 'Ronnica')

    def test_06_edit_user(self):
        resp = self.client.get('/edituser/1')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Edit User Records')
        self.assertContains(resp, 'Ronnica')

    def test_07_update_user_and_csv_sync(self):
        update_data = {
            'user_name': 'Ronnica_Updated',
            'country': 'El Salvador',
            'u_age': '70',
            'pincode': '95413',
            'city': 'Camiri',
            'passwords': '9791'
        }
        resp = self.client.post('/updateuser/1', update_data)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Record updated successfully!!')
        u = User.objects.get(user_id=1)
        self.assertEqual(u.user_name, 'Ronnica_Updated')

        # Check CSV
        with open(get_csv_path(), 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('1,Ronnica_Updated,El Salvador,70,95413,Camiri,9791', content)

    def test_08_delete_user_and_csv_sync(self):
        resp = self.client.get('/Deluser/1')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Deleted Successfully')
        self.assertFalse(User.objects.filter(user_id=1).exists())

        # Check CSV
        with open(get_csv_path(), 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertNotIn('1,Ronnica', content)

    def test_09_query_natural_join(self):
        query = 'select * from "User" natural join "Game"'
        resp = self.client.post('/ProcessCustomQuery/', {'query': query})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'game_name')
        self.assertContains(resp, 'Viva')

    def test_10_query_single_column(self):
        query = 'select "user_name" from "User"'
        resp = self.client.post('/ProcessCustomQuery/', {'query': query})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'user_name')
        self.assertContains(resp, 'Ronnica')

    def test_11_query_security_rejection(self):
        bad_query = 'DROP TABLE "User"'
        resp = self.client.post('/ProcessCustomQuery/', {'query': bad_query})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Security restriction')

    def test_12_export_csv(self):
        resp = self.client.get('/export_csv')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="users.csv"', resp['Content-Disposition'])
        resp.close()

    def test_13_ajax_insert_returns_json_and_syncs_csv(self):
        data = {
            'user_id': '102',
            'user_name': 'ajax-user',
            'country': 'india',
            'u_age': '21',
            'pincode': '110001',
            'city': 'delhi',
            'passwords': '1234'
        }
        resp = self.client.post('/Insertuser', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['success'])
        self.assertTrue(User.objects.filter(user_id=102).exists())

    def test_14_query_page_contains_prepared_queries(self):
        resp = self.client.get('/runQueryuser')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Choose a prepared query')
        self.assertContains(resp, 'Users ordered by age')

    def test_15_query_insert_update_delete(self):
        insert = self.client.post('/ProcessCustomQuery/', {
            'query': 'INSERT INTO "User" (user_id, user_name, country, u_age, pincode, city, passwords) VALUES (999999, \'Query User\', \'India\', 25, \'000000\', \'Query City\', \'demo\')'
        })
        self.assertContains(insert, 'INSERT completed successfully')
        self.assertTrue(User.objects.filter(user_id=999999).exists())

        update = self.client.post('/ProcessCustomQuery/', {
            'query': 'UPDATE "User" SET city = \'Updated City\' WHERE user_id = 999999'
        })
        self.assertContains(update, 'UPDATE completed successfully')
        self.assertEqual(User.objects.get(user_id=999999).city, 'Updated City')

        delete = self.client.post('/ProcessCustomQuery/', {
            'query': 'DELETE FROM "User" WHERE user_id = 999999'
        })
        self.assertContains(delete, 'DELETE completed successfully')
        self.assertFalse(User.objects.filter(user_id=999999).exists())

    def test_16_query_blocks_schema_changes_and_multiple_statements(self):
        for query in ('DROP TABLE "User"', 'SELECT * FROM "User"; DELETE FROM "User"'):
            resp = self.client.post('/ProcessCustomQuery/', {'query': query})
            self.assertContains(resp, 'Security restriction')
