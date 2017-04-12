#!.env/bin/python
from app import app
import unittest
import json

headers = {
    'Authorization': 'Bearer ' + app.config['AUTHORIZATION_KEY']
}


class BasicTestCase(unittest.TestCase):

    expected_apis = {
        "addresses": "/api/v1.0/addresses",
        "cleaners": "/api/v1.0/cleaners",
        "coverages": "/api/v1.0/coverages",
        "order_reference": "/api/v1.0/order/reference/REFERENCE_NUMBER",
        "orders": "/api/v1.0/orders",
        "potential_users": "/api/v1.0/potential_users",
        "schedules": "/api/v1.0/schedules",
        "services": "/api/v1.0/services",
        "user_authentication": "/api/v1.0/user/authentication",
        "users": "/api/v1.0/users"
    }

    def test_index(self):
        tester = app.test_client(self)

        # Test without Authorization header
        response = tester.get('/', content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # Test with wrong methods
        response = tester.post('/', content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 405)

        response = tester.put('/', content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 405)

        response = tester.delete('/', content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 405)

        # Test with Authorization header
        response = tester.get('/', content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 200)

        actual = json.loads(response.data)
        self.assertIn("apis", actual)

        for api in self.expected_apis:
            self.assertIn(api, actual['apis'])

    def test_services(self):
        tester = app.test_client(self)
        # Test without Authorization header
        response = tester.get(self.expected_apis["services"], content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # Test with wrong methods
        response = tester.post(self.expected_apis["services"], content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 405)

        response = tester.put(self.expected_apis["services"], content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 405)

        response = tester.delete(self.expected_apis["services"], content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 405)

        # Test with Authorization header
        response = tester.get(self.expected_apis["services"], content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 200)

        actual = json.loads(response.data)
        self.assertIn("services", actual)

    def test_users(self):
        tester = app.test_client(self)
        user_api = self.expected_apis["users"]

        # Test without Authorization header
        response = tester.get(user_api, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # Test with wrong methods
        response = tester.put(user_api, content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 405)

        response = tester.delete(user_api, content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 405)

        # Test with Authorization header
        response = tester.get(user_api, content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 200)

        actual = json.loads(response.data)
        self.assertIn("users", actual)

        # Test create new user
        test_user = {
            "name": "User",
            "lastname": "Test",
            "password": "testpassword",
            "email": "test@mail.com"
        }

        response = tester.post(user_api, content_type='application/json', headers=headers, data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)

        # Get and modify new user
        new_user = json.loads(response.data)

        response = tester.get(new_user['user']['url'], content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 200)

        response = tester.get(new_user['user']['url'] + "FAKE_ID", content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 404)

        response = tester.put(
            new_user['user']['url'],
            data=json.dumps(dict(name="NewName")),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['user']['name'], "NewName")

        # Test login
        response = tester.post(
            self.expected_apis["user_authentication"],
            data=json.dumps(dict(email="test@mail.com", password="testpassword")),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)

        response = tester.post(
            self.expected_apis["user_authentication"],
            data=json.dumps(dict(email="notexisting@mail.com", password="testpassword")),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 404)

        response = tester.post(
            self.expected_apis["user_authentication"],
            data=json.dumps(dict(email="test@mail.com", password="wrongpassword")),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 400)

        # Test delete new user
        response = tester.delete(new_user['user']['url'], content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()