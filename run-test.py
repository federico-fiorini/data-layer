#!.env/bin/python
from app import app
import unittest

headers = {
    'Authorization': 'Bearer ' + app.config['AUTHORIZATION_KEY']
}


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        """ Test without Authorization header """
        response = tester.get('/', content_type='application/json')
        self.assertEqual(response.status_code, 403)

        """ Test with Authorization header """
        response = tester.get('/', content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()