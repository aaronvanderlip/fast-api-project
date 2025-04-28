import logging
import os
from typing import Annotated, Literal
from uuid import UUID

import markdown
import redis
from fastapi import Body, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, conint

from app.worker import celery as celery_app
from app.worker import fib, sleepy

logger = logging.getLogger(__name__)


app = FastAPI()
origins = [
    "http://127.0.0.1:8888",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


redis_client = redis.StrictRedis(host="redis", port=6379, db=0)


class TaskResult(BaseModel):
    id: UUID
    state: str
    result: str | None


class TaskResultDetail(BaseModel):
    id: UUID
    state: str
    result: str | None
    date: str | None


class SortParams(BaseModel):
    order: Literal["DESC", "ASC"] = "DESC"
    sort: Literal["date", "id", "result", "state"] = "date"


class SleepyTaskModel(BaseModel):
    seconds: Annotated[int, conint(gt=0, lt=3600)]


@app.get("/")
def render_markdown(request: Request):  # pragma no cover
    filename = "README.md"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.dirname(script_dir)
    file_path = os.path.join(grandparent_dir, filename)

    if not os.path.isfile(file_path):
        print(f"File '{filename}' not found in directory '{grandparent_dir}'")
        return None
    with open(filename, "r") as file:
        content = file.read()

    html_content = markdown.markdown(content)

    return HTMLResponse(content=html_content)


@app.post("/tasks/sleepy", status_code=201)
def sleepy_task(task: SleepyTaskModel) -> TaskResult:
    """
    Create a new task to simulate a delayed operation that sleeps for a specified number of seconds.

    This endpoint triggers a background "sleepy" task using Celery, which will sleep for the
    number of seconds specified in the request. The task is run asynchronously, and the response
    includes the task's unique ID, current state, and result status.

    Args:
        task (SleepyTaskModel): A model containing the number of seconds for the task to sleep.
        It includes the following field:
            - seconds (int): The number of seconds to delay the task.

    Returns:
        dict: A dictionary containing the task's details:
            - id (str): The unique identifier of the created task.
            - state (str): The current state of the task (e.g., "PENDING", "STARTED").
            - result (Any): The result of the task (initially None if not completed).

    Example Request Body:
        {
            "seconds": 10
        }

    Status Code:
        201 Created: The task has been successfully created and queued.
    """
    task_result = sleepy.apply_async((task.seconds,), countdown=task.seconds)
    result = {
        "id": task_result.id,
        "state": task_result.state,
        "result": task_result.result,
    }
    return result


@app.post("/tasks/fib", status_code=201)
def fib_task(nthNumber: int = Body(embed=True)) -> TaskResult:
    """
    Create a new task to compute the nth Fibonacci number asynchronously.

    This endpoint triggers a background task to calculate the nth Fibonacci number
    using Celery. The task will run asynchronously, and the response contains the
    task's unique ID, current state, and initial result status.

    Args:
        nthNumber (int): The position in the Fibonacci sequence to compute. This is
        passed in the request body.

    Returns:
        dict: A dictionary with the task's information:
            - id (str): The unique identifier for the created task.
            - state (str): The current state of the task (e.g., "PENDING", "STARTED").
            - result (Any): The result of the task (initially None if not completed).

    Example Request Body:
        {
            "nthNumber": 10
        }

    Status Code:
        201 Created: The task has been successfully created and queued.
    """
    task_result = fib.delay(nthNumber)
    result = {
        "id": task_result.id,
        "state": task_result.state,
        "result": task_result.result,
    }
    return result


@app.get("/tasks/{task_id}")
def get_one(task_id: UUID) -> TaskResultDetail:
    """
    Retrieve the status and result of a specific task by its UUID.

    This endpoint fetches the status of a task from the Celery backend using its UUID.
    The returned information includes the task's current state, result (if available),
    and the date the task was completed.

    Args:
        task_id (UUID): The UUID of the task to retrieve.

    Returns:
        dict: A dictionary containing the task's:
            - id (UUID): The task's UUID.
            - state (str): The current state of the task (e.g., "PENDING", "SUCCESS").
            - result (str): The result of the task if completed, otherwise an empty string.
            - date (str): The timestamp when the task was completed, or None if not available.

    Example:
        /tasks/123e4567-e89b-12d3-a456-426614174000
    """
    task_result = celery_app.AsyncResult(str(task_id))
    result = {
        "id": task_id,
        "state": task_result.state,
        "result": str(task_result.result),
        "date": str(task_result.date_done),
    }
    return result


@app.get("/tasks")
def get_all(sort_query: Annotated[SortParams, Query()]) -> list[TaskResultDetail]:
    """
    Fetch all completed tasks from the Redis results backend and return them sorted.

    This endpoint retrieves all tasks stored in the Redis backend with keys prefixed
    by "celery-task-meta-*". The tasks can be sorted based on a specified field and
    order provided via query parameters.

    Args:
        sort_query (SortParams): Sorting parameters provided via query, which include:
            - sort: The field to sort the tasks by (e.g., "id", "status").
            - order: The order of sorting ("ASC" for ascending, "DESC" for descending).

    Returns:
        List[dict]: A list of task results fetched from Redis, sorted according to the
        specified sort field and order.

    Example Query:
        /tasks?sort=id&order=DESC
    """

    def _get_sort_key(item):
        return item.get(sort_query.sort, "")

    reverse = sort_query.order == "DESC"
    tasks = []
    keys = redis_client.keys("celery-task-meta-*")
    for key in keys:
        task_id = key.decode().split("celery-task-meta-")[-1]
        task_result = get_one(task_id)
        tasks.append(task_result)
    tasks.sort(key=_get_sort_key, reverse=reverse)
    return tasks
