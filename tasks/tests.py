from django.test import TestCase, Client

from utils import getDict

class TasksTestCase(TestCase):

    def setUp(self):
        self.makeRequest = Client()
        self.registerPath = '/register'
        self.loginPath = '/login'
        self.contentType = 'application/json'
        self.user = {
            'email': 'e@mail.com',
            'name': 'Dario0117',
            'password': 'Pa55w0rD',
        }
        
        # Ideal case requests
        # This requests should ALWAYS work
        self.requests = {
            'register': {
                'GET': self.makeRequest.get(
                    path = self.registerPath, 
                    content_type = self.contentType
                ),
                'PUT': self.makeRequest.put(
                    path = self.registerPath, 
                    content_type = self.contentType
                ),
                'PATCH': self.makeRequest.patch(
                    path = self.registerPath, 
                    content_type = self.contentType
                ),
                'POST': self.makeRequest.post(
                    path = self.registerPath, 
                    content_type = self.contentType,
                    data = self.user
                ),
            },
            'login': {
                'GET': self.makeRequest.get(
                    path = self.loginPath, 
                    content_type = self.contentType
                ),
                'PUT': self.makeRequest.put(
                    path = self.loginPath, 
                    content_type = self.contentType
                ),
                'PATCH': self.makeRequest.patch(
                    path = self.loginPath, 
                    content_type = self.contentType
                ),
                'POST': self.makeRequest.post(
                    path = self.loginPath, 
                    content_type = self.contentType,
                    data = self.user
                ),
            }
        }

    def test_requests_must_have_correct_http_verb(self):
        registerRequests = self.requests['register']
        self.assertEqual(registerRequests['GET'].status_code, 404)
        self.assertEqual(registerRequests['PUT'].status_code, 404)
        self.assertEqual(registerRequests['PATCH'].status_code, 404)
        self.assertEqual(registerRequests['POST'].status_code, 200)

        loginRequests = self.requests['login']
        self.assertEqual(loginRequests['GET'].status_code, 404)
        self.assertEqual(loginRequests['PUT'].status_code, 404)
        self.assertEqual(loginRequests['PATCH'].status_code, 404)
        self.assertEqual(loginRequests['POST'].status_code, 200)
    
    def test_requests_must_have_correct_content_type(self):
        badRequestRegister = self.makeRequest.post(
            path = self.registerPath, 
            content_type = 'text/plain'
        )
        self.assertEqual(badRequestRegister.status_code, 400)

        badRequestLogin = self.makeRequest.post(
            path = self.loginPath, 
            content_type = 'text/plain'
        )
        self.assertEqual(badRequestLogin.status_code, 400)
        
    def test_request_must_have_correct_params(self):
        badUsers = [
            { # empty

            },
            { # no name
                'email': 'b@mail.com',
                'password': 'Pa55w0rD',
            },
            { # no email
                'name': 'Dario0117',
                'password': 'Pa55w0rD',
            },
            { # no password
                'email': 'c@mail.com',
                'name': 'Dario0117',
            }
        ]

        for user in badUsers:
            badRequestRegister = self.makeRequest.post(
                path = self.registerPath, 
                content_type = self.contentType,
                data = user
            )
            self.assertEqual(badRequestRegister.status_code, 400)

        badUsers = [
            { # empty

            },
            { # no email
                'password': 'Pa55w0rD',
            },
            { # no password
                'email': 'c@mail.com',
            }
        ]
        
        for user in badUsers:
            badRequestLogin = self.makeRequest.post(
                path = self.loginPath, 
                content_type = self.contentType,
                data = user
            )
            self.assertEqual(badRequestLogin.status_code, 400)

    def test_should_register_users_and_send_token(self):
        registerRequests = self.requests['register']
        response = getDict(registerRequests['POST'].content)
        self.assertEqual(response['error'], '')
        self.assertIsNot(response['token'], '')
        self.assertIsNotNone(response['token'])

    def test_should_login_with_email_and_password(self):
        loginRequests = self.requests['login']
        response = getDict(loginRequests['POST'].content)
        self.assertEqual(response['error'], '')
        self.assertIsNot(response['token'], '')
        self.assertIsNotNone(response['token'])

    def test_should_throw_error_on_wrong_email_and_password(self):
        badUsers = [
            { # wrong password
                'email': 'e@mail.com',
                'password': 'wrong_password'
            },
            { # email unregistred
                'email': 'a@mail.com',
                'password': 'password'
            }
        ]
        
        for user in badUsers:
            badRequestLogin = self.makeRequest.post(
                path = self.loginPath, 
                content_type = self.contentType,
                data = user
            )
            self.assertEqual(badRequestLogin.status_code, 400)

