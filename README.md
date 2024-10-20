### Graph Authorization Example 1

This is a Django based example for working with Neo4J data and authorization in Django.

We allow users to retrieve data through REST endpoints but provide only data from a limited subgraph where a user has access, based on department.
Users can see their own department data, and users in the 'Audit' group can see all data.

The REST endpoint `/project_tasks` will query Neo4J with data that is only relevant for the scope that they are allowed to see. The REST endpoint `/own_project_tasks` does the same and filters on the tasks assigned to the given user.
For this example there is a simple front-end to login for the users and show the different results.

#### Technologies

* Neo4J
* Django
* neomodel library
* Docker Compose
* Poetry

#### Demo data

The Django application uses a custom command to setup some demo data. A superuser is created with the `start_django.sh` script in the entrypoint before it starts Django.
It will create Django users in Finance and Sales departments, and 'Audit', that can see data of all departments. Then it will create demo data in Neo4J.
In Neo4J projects, project tasks and workers are created, where workers' names are equal to some usernames.

Users:
* Finance
  * shaniqua / shaniqua
  * tyrone / tyrone
* Sales
  * loraine / loraine
  * chen / chen
* Audit (see all)
  * devon / devon
* Superadmin (can login to Django's /admin/)
  * jenny / (see environment variable)

<br>

#### Functional testing

Go to the [demo](http://localhost:8000) webapp and login with the usernames above.
Depending on the NEO4J_* groups they are a member of, they can see a certain part or all of the data.

Verify users/groups with superadmin jenny in [Django Admin](http://localhost:8000/admin/)

<br>

### Setup

Essentially we start up a Django application and a Neo4J instance using Docker/Podman compose.
Because on Podman, the depends_on property is not supported, django waits for 15 seconds to make sure Neo4J is online before it creates demo data and starts the application.

#### environment variables

the demo `.env` has been included with demo passwords

```
DJANGO_SUPERUSER_PASSWORD=R3placeMePlease!
NEO4J_PW=R3placeMePlease!
NEO4J_HOST=graphpartition_neo4j_1
```


#### run

```
[docker|podman] compose up -d
```

Wait for the instances to complete and for Django to generate demo data 15 seconds after starting.

