# Tasks Api Django

> **Python: 3.5.5**

> **Django: 2.0.7**

> **PyJWT: 1.6.4**

## Instructions

- `git clone https://github.com/Dario0117/tasksApiDjango && cd tasksApiDjango`
- `docker run -it --name tasksApiDjango -p 8000:8000 -v $PWD:/code python:3.5.5-stretch bash`
- `cd code`
- `pip install -r requirements.txt`
- `python manage.py migrate`
- `python manage.py runserver 0:8000`

**Test:** `python manage.py test`

## Use cases

### Sign up and login

    - Description: User gain access to service
    - Constraints: Can not create multiple accounts with same email
    - Routes:
        - /register [POST] : IN {email, username, password}, OUT {token}
        - /login [POST]: IN {username, password}, OUT {token}

### Create tasks

    - Description: User can create tasks and assign it to his account
    - Routes:
        - /tasks [POST]: HEAD {token}, IN {title, content}, OUT {id_task}

### Retrieve tasks

    - Description: User can get all tasks associated with his account
    - Routes:
        - /tasks [GET]: HEAD {token}, IN {}, OUT {[task]}
        - /tasks/:id [GET]: HEAD {token}, IN {}, OUT {task}

### Update tasks

    - Description: User can set title and/or content of his tasks
    - Routes:
        - /tasks/:id [PATCH]: HEAD {token}, IN {title, content}, OUT {task}

### Delete tasks

    - Description: User can remove tasks from his account
    - Routes:
        - /tasks/:id [DELETE]: HEAD {token}, IN {}, OUT {}