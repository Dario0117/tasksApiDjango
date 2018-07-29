from django.test import TestCase, Client

from utils import getDict

class TasksTestCase(TestCase):

    def createUser(self, user):
        return self.makeRequest.post(
            path = self.registerPath, 
            content_type = self.contentType,
            data = user
        )

    def loginUser(self, user):
        return self.makeRequest.post(
            path = self.loginPath, 
            content_type = self.contentType,
            data = user
        )

    def createTask(self, token, task):
        return self.makeRequest.post(
            path = self.tasksPath, 
            content_type = self.contentType,
            data = task,
            HTTP_AUTHORIZATION = token,
        )

    def setUp(self):
        self.makeRequest = Client()
        self.registerPath = '/register'
        self.loginPath = '/login'
        self.tasksPath = '/tasks'
        self.contentType = 'application/json'
        self.user = {
            'email': 'e@mail.com',
            'name': 'Dario0117',
            'password': 'Pa55w0rD',
        }

    def test_requests_must_have_correct_http_verb(self):
        requests = {
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
        registerRequests = requests['register']
        self.assertEqual(registerRequests['GET'].status_code, 404)
        self.assertEqual(registerRequests['PUT'].status_code, 404)
        self.assertEqual(registerRequests['PATCH'].status_code, 404)
        self.assertEqual(registerRequests['POST'].status_code, 200)

        loginRequests = requests['login']
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
        newUser = self.createUser(self.user)
        response = getDict(newUser.content)
        self.assertEqual(response['error'], '')
        self.assertIsNot(response['token'], '')
        self.assertIsNotNone(response['token'])

    def test_should_login_with_email_and_password(self):
        newUser = self.createUser(self.user)
        sessionUser = self.loginUser(self.user)
        response = getDict(sessionUser.content)
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
            },
            { # no email
                'password': 'password'
            },
            { # no password
                'email': 'a@mail.com',
            }
        ]
        
        for user in badUsers:
            badRequestLogin = self.loginUser(user)
            self.assertEqual(badRequestLogin.status_code, 400)

    def test_should_throw_error_on_accessing_tasks_without_login(self):
        unauthenticatedRequests = [
            self.makeRequest.get( # /tasks GET
                path = self.tasksPath,
                content_type = self.contentType,
            ),
            self.makeRequest.post( # /tasks POST
                path = self.tasksPath,
                content_type = self.contentType,
            ),
            self.makeRequest.get( # /tasks/:id GET
                path = self.tasksPath + '/1',
                content_type = self.contentType,
            ),
            self.makeRequest.patch( # /tasks/:id PATCH
                path = self.tasksPath + '/1',
                content_type = self.contentType,
            ),
            self.makeRequest.delete( # /tasks/:id DELETE
                path = self.tasksPath + '/1',
                content_type = self.contentType,
            )
        ]
        
        for response in unauthenticatedRequests:
            self.assertEqual(response.status_code, 403)

    def test_should_create_task_with_authorized_request(self):
        newUser = self.createUser(self.user)
        responseUser = getDict(newUser.content)

        newTask = self.createTask(
            token = responseUser['token'],
            task = {
                'title': 'Title task',
                'content':'Content task',
            }
        )
        responseTask = getDict(newTask.content)
        self.assertEqual(newTask.status_code, 201)
        self.assertEqual(responseTask['error'], '')
        self.assertIsNot(responseTask['id_task'], '')

    def test_should_throw_error_on_create_task_with_wrong_parametters(self):
        newUser = self.createUser(self.user)
        responseUser = getDict(newUser.content)
        badTasks = [
            { # empty

            },
            { # no title
                'content': 'no title'
            },
            { # no content
                'title': 'no content',
            }
        ]
        
        for task in badTasks:
            newTask = self.createTask(
                token = responseUser['token'],
                task = task,
            )
            self.assertEqual(newTask.status_code, 400)

    def test_should_get_all_tasks_with_authorized_request(self):

        newUser = self.createUser(self.user)
        responseUser = getDict(newUser.content)

        Tasks = [
            { 
                'title': 'Task title 1',
                'content': 'Task content'
            },
            { 
                'title': 'Task title 2',
                'content': 'Task content'
            },
            { 
                'title': 'Task title 3',
                'content': 'Task content'
            },
            { 
                'title': 'Task title 4',
                'content': 'Task content'
            },
            { 
                'title': 'Task title 5',
                'content': 'Task content'
            },
        ]
        
        for task in Tasks:
            newTask = self.createTask(
                token = responseUser['token'],
                task = task,
            )

        allTasks = self.makeRequest.get(
            path = self.tasksPath, 
            content_type = self.contentType,
            HTTP_AUTHORIZATION = responseUser['token'],
        )

        response = getDict(allTasks.content)
        self.assertEqual(allTasks.status_code, 200)
        self.assertEqual(response['error'], '')
        self.assertIsInstance(response['tasks'], list)

    def test_should_get_specific_task_with_authorized_request(self):
        newUser = self.createUser(self.user)
        responseUser = getDict(newUser.content)

        Tasks = [
            { 
                'title': 'Task title 1',
                'content': 'Task content'
            },
            { 
                'title': 'Task title 2',
                'content': 'Task content'
            },
            { 
                'title': 'Task title 3',
                'content': 'Task content'
            },
            { 
                'title': 'Task title 4',
                'content': 'Task content'
            },
            { 
                'title': 'Task title 5',
                'content': 'Task content'
            },
        ]
        
        for task in Tasks:
            newTask = self.createTask(
                token = responseUser['token'],
                task = task,
            )

        task = self.makeRequest.get(
            path = self.tasksPath + '/3', 
            content_type = self.contentType,
            HTTP_AUTHORIZATION = responseUser['token'],
        )

        response = getDict(task.content)
        self.assertEqual(task.status_code, 200)
        self.assertEqual(response['error'], '')
        self.assertIsNot(response['task'], '')

    def test_should_throw_error_on_get_inexistent_task(self):
        newUser = self.createUser(self.user)
        responseUser = getDict(newUser.content)

        task = self.makeRequest.get(
            path = self.tasksPath + '/1', 
            content_type = self.contentType,
            HTTP_AUTHORIZATION = responseUser['token'],
        )

        response = getDict(task.content)
        self.assertEqual(task.status_code, 404)
        self.assertIsNot(response['error'], '')
        self.assertEqual(response['task'], '')