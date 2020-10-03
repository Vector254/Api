import unittest
import os
import json
from app import create_app, db

class QuotesTestCase(unittest.TestCase):
    """This class represents the quotes test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.quotes = {'title': 'Happiness'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_quote_creation(self):
        """Test API can create a quote (POST request)"""
        res = self.client().post('/quotes/', data=self.quote)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Happiness', str(res.data))

    def test_api_can_get_all_quotes(self):
        """Test API can get a quote (GET request)."""
        res = self.client().post('/quotes/', data=self.quote)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/quotes/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Happiness', str(res.data))

    def test_api_can_get_quote_by_id(self):
        """Test API can get a single quote by using it's id."""
        rv = self.client().post('/quotes/', data=self.quote)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/quotes/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Happiness', str(result.data))

    def test_quotes_can_be_updated(self):
        """Test API can update an existing quote. (PUT request)"""
        rv = self.client().post(
            '/quotes/',
            data={'title': 'Never give up'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/quotes/1',
            data={
                "title": "You only live once)"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/quotes/1')
        self.assertIn('You only live once', str(results.data))

    def test_quote_deletion(self):
        """Test API can delete an existing quote. (DELETE request)."""
        rv = self.client().post(
            '/quotes/',
            data={'title': 'Never give up'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/quotes/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/quotes/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
