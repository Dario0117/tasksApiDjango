from django.test import TestCase, Client

class AuthTestCase(TestCase):

    def setUp(self):
        self.makeRequest = Client()
        self.registerPath = '/register'
        self.loginPath = '/login'
        self.contentType = 'application/json'
        
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
                    content_type = self.contentType
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
                    content_type = self.contentType
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
        registerRequests = self.requests['register']
        badRequestRegister = self.makeRequest.post(
            path = self.registerPath, 
            content_type = 'text/plain'
        )
        self.assertEqual(registerRequests['POST'].status_code, 200)
        self.assertEqual(badRequestRegister.status_code, 400)

        loginRequests = self.requests['login']
        badRequestLogin = self.makeRequest.post(
            path = self.loginPath, 
            content_type = 'text/plain'
        )
        self.assertEqual(loginRequests['POST'].status_code, 200)
        self.assertEqual(badRequestLogin.status_code, 400)
        