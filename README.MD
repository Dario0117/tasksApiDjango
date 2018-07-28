# Tasks Api Django

## Use cases

### Sign up and login

    - Description: User gain access to service
    - Constraints: Can not create multiple accounts with same email
    - Routes:
        - /register [POST] : IN {email, name, password}, OUT {token}
        - /login [POST]: IN {email, password}, OUT {token}

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