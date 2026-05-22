from django.test import TestCase, Client
from django.urls import reverse
import json

class TweetsAppTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_index_view(self):
        """
        Verify the index page renders successfully and displays the templates.
        """
        response = self.client.get(reverse('tweets:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweets/index.html')
        self.assertIn('dev_latency', response.context)
        self.assertIn('dev_status', response.context)

    def test_fetch_tweets_api_validation(self):
        """
        Verify the fetch tweets AJAX view returns 400 when username is missing.
        """
        response = self.client.get(reverse('tweets:fetch_tweets_api'))
        self.assertEqual(response.status_code, 400)
        
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Username is required')

    def test_fetch_tweets_api_success_mock(self):
        """
        Verify that fetch tweets API returns 5 tweets in mock mode.
        """
        response = self.client.get(reverse('tweets:fetch_tweets_api'), {'username': 'nasa'})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['mode'], 'developer_mock')
        self.assertEqual(data['user']['username'].lower(), 'nasa')
        self.assertEqual(len(data['tweets']), 5)

    def test_update_dev_settings_api(self):
        """
        Verify the developer controls API updates configurations in session.
        """
        response = self.client.post(
            reverse('tweets:update_credentials_api'),
            data=json.dumps({'latency': 2.0, 'status_code': '429'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['dev_latency'], 2.0)
        self.assertEqual(data['dev_status'], '429')
        
        # Verify it is in the session
        self.assertEqual(self.client.session['dev_latency'], 2.0)
        self.assertEqual(self.client.session['dev_status'], '429')

    def test_fetch_tweets_api_simulated_errors(self):
        """
        Verify that API fetch correctly returns simulated status errors (404 and 429).
        """
        # 1. Test 404 User Not Found simulation
        session = self.client.session
        session['dev_status'] = '404'
        session['dev_latency'] = 0.0
        session.save()
        
        response = self.client.get(reverse('tweets:fetch_tweets_api'), {'username': 'nonexistent_user'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())
        
        # 2. Test 429 Rate Limit simulation
        session['dev_status'] = '429'
        session.save()
        
        response = self.client.get(reverse('tweets:fetch_tweets_api'), {'username': 'elonmusk'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())
        self.assertIn('rate limit', response.json()['error'].lower())
