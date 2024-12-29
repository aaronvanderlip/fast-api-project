# Application overview

This application stack consist of the following notable technologies

- [FastAPI](https://fastapi.tiangolo.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Redis](https://redis.io)
- [React Admin](https://marmelab.com/react-admin/)
- [Schemathesis](https://schemathesis.readthedocs.io/en/stable/)

## Starting the application

Unzip the provide file and ensure you have a Docker daemon running. Running Docker Desktop should be sufficient.

In the directory run the following command

`docker compose up --build`

Once the application is built you can begin exploring the application.

<http://127.0.0.1:8004> -> The FastAPI App (contains a rendered copy of this markdown file).

<http://127.0.0.1:8004/docs> -> OpenAPI doc view for the application, built into FastAPI.

<http://127.0.0.1:8004/redoc> -> Redoc rendering of the OpenAPI spec, built into FastAPI.

<http://127.0.0.1:8888/#/tasks> The React Admin based front end for view tasks and task details. This will be blank when the
application starts ups so lets fix that.

## Adding some task

You can interact with the API using <http://127.0.0.1:8004/docs>

There are two task endpoints enabled for this app

[Sleepy, a task that will uses Celery functionality for a set number of seconds](http://127.0.0.1:8004/docs#/default/sleepy_task_tasks_sleepy_post)

and

[Fib, a purposely slow Fibonacci function](http://127.0.0.1:8004/docs#/default/fib_task_tasks_fib_post)

Using the UI, select the 'Try it Out' button for the respective endpoint.
You will then be prompted with an interface detailing the request and response definitions for the endpoint.
Selecting the 'Execute' button will submit a request to the running application and return a response.

After executing the request you will be provided an equivalent `curl` command if you wish to interact with the API using the command line.

`curl -X 'POST' 
  'http://127.0.0.1:8004/tasks/fib' 
  -H 'accept: application/json' 
  -H 'Content-Type: application/json' 
  -d '{
  "nthNumber": 0
}'`

Once you have added a number of tasks it is time to check on tasks.

## Inspecting tasks

There are several way to inspect a task's state.

[Using the endpoint directly to fetch a task by UUID](http://127.0.0.1:8004/docs#/default/get_one_tasks__task_id__get)

[Using the endpoint directly to view a list of completed tasks](http://127.0.0.1:8004/docs#/default/get_all_tasks_get)

### [Or use the dashboard](http://127.0.0.1:8888/#/tasks)

The dashboard provides a means for sorting by field and changing the sort order. Pagination is not supported, see Caveats.

Clicking on an row will bring you to a detailed view of the task.

## Testing

The current application has 90% test coverage for the API. There are no tests for the front end, see Caveats.

With the Docker containers running, start another terminal session to interact with the application.

Determine the name of the
`web` container

`docker ps`

and using the name returned issue a command that is similar to this

`docker exec -it fast-api-web-1   pytest --cov=app`

replacing `fast-api-web-1` with the name of you container.

This will run a suite of tests and provide a coverage report.

You might be interested in viewing the terminal that is running the docker containers when the [Schemathesis](https://schemathesis.readthedocs.io/en/stable/) test are running.

If something errors out during testing you can run the tests suite to drop into the Python debugger using the following command

`docker exec -it fast-api-web-1 pytest --cov=app --pdb`

Test coverage is below 100% because I really wanted to have this Markdown file rendered as part of the app.

Python code is formatted with `ruff` using the default settings.