from django.test import TestCase, Client
import json
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
            data = json.dumps(user)
        )

    def createTask(self, token, task):
        return self.makeRequest.post(
            path = self.tasksPath, 
            content_type = self.contentType,
            data = task,
            HTTP_AUTHORIZATION = 'Bearer ' + token,
        )

    def setUp(self):
        self.makeRequest = Client()
        self.registerPath = '/register/'
        self.loginPath = '/login/'
        self.tasksPath = '/tasks/'
        self.contentType = 'application/json'
        self.user = {
            'email': 'a@mail.com',
            'username': 'dario0117',
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
                'POST': self.createUser(self.user),
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
                    data = json.dumps(self.user),
                ),
            }
        }
        registerRequests = requests['register']
        self.assertEqual(registerRequests['GET'].status_code, 404)
        self.assertEqual(registerRequests['PUT'].status_code, 404)
        self.assertEqual(registerRequests['PATCH'].status_code, 404)
        self.assertEqual(registerRequests['POST'].status_code, 201)

        loginRequests = requests['login']
        self.assertEqual(loginRequests['GET'].status_code, 405)
        self.assertEqual(loginRequests['PUT'].status_code, 405)
        self.assertEqual(loginRequests['PATCH'].status_code, 405)
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
        self.assertEqual(badRequestLogin.status_code, 415)
        
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

    def test_should_login_with_email_and_password(self):
        newUser = self.createUser(self.user)
        sessionUser = self.loginUser(self.user)
        response = getDict(sessionUser.content)
        self.assertIsNot(response['access'], '')
        self.assertIsNot(response['refresh'], '')

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
                path = self.tasksPath + '/1/',
                content_type = self.contentType,
            ),
            self.makeRequest.patch( # /tasks/:id PATCH
                path = self.tasksPath + '/1/',
                content_type = self.contentType,
            ),
            self.makeRequest.delete( # /tasks/:id DELETE
                path = self.tasksPath + '/1/',
                content_type = self.contentType,
            )
        ]

        possibleCodes = {
            404: True,
            401: True,
        }
        
        for response in unauthenticatedRequests:
            self.assertEqual(possibleCodes[response.status_code], True)

    def test_should_create_task_with_authorized_request(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)
        newTask = self.createTask(
            token = response['access'],
            task = json.dumps({
                'title': 'Title task',
                'content':'Content task',
            })
        )
        responseTask = getDict(newTask.content)
        self.assertEqual(newTask.status_code, 201)

    def test_should_throw_error_on_create_task_with_wrong_parametters(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)
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
                token = response['access'],
                task = task,
            )
            self.assertEqual(newTask.status_code, 400)

    def test_should_get_all_tasks_with_authorized_request(self):

        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

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
                token = response['access'],
                task = json.dumps(task),
            )
            self.assertEqual(newTask.status_code, 201)

        allTasks = self.makeRequest.get(
            path = self.tasksPath, 
            content_type = self.contentType,
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )

        response = getDict(allTasks.content)
        self.assertEqual(allTasks.status_code, 200)
        self.assertIsInstance(response, list)

    def test_should_get_specific_task_with_authorized_request(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

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
                token = response['access'],
                task = json.dumps(task),
            )

        task = self.makeRequest.get(
            path = self.tasksPath + '3/', 
            content_type = self.contentType,
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )

        self.assertEqual(task.status_code, 200)

    def test_should_throw_error_on_get_inexistent_task(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

        task = self.makeRequest.get(
            path = self.tasksPath + '1/', 
            content_type = self.contentType,
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )
        self.assertEqual(task.status_code, 404)

    def test_should_be_allowed_to_update_tasks(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

        oldTitle = 'Title task'
        oldContent = 'Content task'
        newTitle = 'Title updated'
        newContent = 'Content updated'

        newTask = self.createTask(
            token = response['access'],
            task = json.dumps({
                'title': oldTitle,
                'content': oldContent,
            })
        )
        responseTask = getDict(newTask.content)
        taskID = 1

        # Send empty data
        updatedTaskEmpty = self.makeRequest.patch(
            path = self.tasksPath + str(taskID) +'/', 
            content_type = self.contentType,
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )
        responseTaskEmpty = getDict(updatedTaskEmpty.content)
        self.assertEqual(updatedTaskEmpty.status_code, 200)
        self.assertEqual(responseTaskEmpty['content'], oldContent)
        self.assertEqual(responseTaskEmpty['title'], oldTitle)

        # Update only title
        updatedTaskTitle = self.makeRequest.patch(
            path = self.tasksPath + str(taskID) + '/', 
            content_type = self.contentType,
            data = json.dumps({
                'title': newTitle
            }),
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )
        responseTaskTitle = getDict(updatedTaskTitle.content)
        self.assertEqual(updatedTaskTitle.status_code, 200)
        self.assertEqual(responseTaskTitle['title'], newTitle)

        # Update only content
        updatedTaskContent = self.makeRequest.patch(
            path = self.tasksPath + str(taskID) + '/', 
            content_type = self.contentType,
            data = json.dumps({
                'content': newContent
            }),
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )
        responseTaskContent = getDict(updatedTaskContent.content)
        self.assertEqual(updatedTaskContent.status_code, 200)
        self.assertEqual(responseTaskContent['content'], newContent)

        # Update both
        updatedTask = self.makeRequest.patch(
            path = self.tasksPath + str(taskID) + '/', 
            content_type = self.contentType,
            data = json.dumps({
                'content': oldContent,
                'title': oldTitle,
            }),
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )
        responseTaskBoth = getDict(updatedTask.content)
        self.assertEqual(updatedTask.status_code, 200)
        self.assertEqual(responseTaskBoth['content'], oldContent)
        self.assertEqual(responseTaskBoth['title'], oldTitle)

    def test_should_throw_error_on_update_tasks_without_login(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

        newTask = self.createTask(
            token = response['access'],
            task = json.dumps({
                'title': 'Title task',
                'content': 'Content task',
            }),
        )
        taskID = 1

        updatedTask = self.makeRequest.patch(
            path = self.tasksPath + str(taskID)+ '/', 
            content_type = self.contentType,
            data = {
                'content': 'new content',
                'title': 'new title',
            }
        )

        self.assertEqual(updatedTask.status_code, 401)
    
    def test_should_throw_error_on_update_inexistent_task(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

        newTask = self.createTask(
            token = response['access'],
            task = json.dumps({
                'title': 'Title task',
                'content': 'Content task',
            }),
        )
        taskID = 1

        updatedTask = self.makeRequest.patch(
            path = self.tasksPath + str(taskID + 1) + '/', 
            content_type = self.contentType,
            data = json.dumps({
                'content': 'new content',
                'title': 'new title',
            }),
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )

        self.assertEqual(updatedTask.status_code, 404)

    def test_should_be_allowed_to_delete_tasks(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

        newTask = self.createTask(
            token = response['access'],
            task = json.dumps({
                'title': 'Title',
                'content': 'Content',
            }),
        )
        taskID = 1

        # Remove task
        deletedTask = self.makeRequest.delete(
            path = self.tasksPath + str(taskID) + '/',
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )
        self.assertEqual(deletedTask.status_code, 200)

        # Try to find task with id that doesn't exists anymore
        # And should throw error 404
        task = self.makeRequest.get(
            path = self.tasksPath + str(taskID) + '/',
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )

        self.assertEqual(task.status_code, 404)

    def test_should_throw_error_on_delete_tasks_without_login(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

        newTask = self.createTask(
            token = response['access'],
            task = json.dumps({
                'title': 'Title task',
                'content': 'Content task',
            }),
        )
        taskID = 1

        deletedTask = self.makeRequest.delete(
            path = self.tasksPath + str(taskID) + '/', 
            content_type = self.contentType,
        )

        self.assertEqual(deletedTask.status_code, 401)
    
    def test_should_throw_error_on_delete_inexistent_task(self):
        newUser = self.createUser(self.user)
        newUserLogin = self.loginUser(self.user)
        response = getDict(newUserLogin.content)

        newTask = self.createTask(
            token = response['access'],
            task = {
                'title': 'Title task',
                'content': 'Content task',
            }
        )
        taskID = 1

        deletedTask = self.makeRequest.patch(
            path = self.tasksPath + str(taskID + 1) + '/', 
            content_type = self.contentType,
            HTTP_AUTHORIZATION = 'Bearer ' + response['access'],
        )

        self.assertEqual(deletedTask.status_code, 404)

        