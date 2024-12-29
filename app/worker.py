import time

from celery import Celery

celery = Celery(__name__)
celery.config_from_object("celeryconfig")


@celery.task(name="sleepy_task", bind=True)
def sleepy(self, seconds):
    """
    Simulate a long-running task by sleeping for a specified number of seconds.

    This Celery task puts the worker to sleep for the specified duration, simulating a
    long-running or delayed operation. After the sleep period, it returns a message
    indicating the number of seconds slept.

    Args:
        self: The task instance, automatically passed by Celery when `bind=True`.
        seconds (int): The number of seconds the task should sleep.

    Returns:
        str: A message indicating how long the task slept, e.g., "Slept for X second(s)".

    Example:
        sleepy.delay(10)  # Task will sleep for 10 seconds.
    """
    return f"Slept for {seconds} second(s)"


@celery.task(name="fib_task", bind=True)
def fib(self, nthNumber):
    """
    Calculate the nth Fibonacci number, with a 1-second delay between each iteration to simulate a long-running task.

    Args:
        self: The task instance (if used in a Celery task with `bind=True`).
        nthNumber (int): The position in the Fibonacci sequence to calculate.

    Returns:
        int: The Fibonacci number at the given position `nthNumber`.

    Example:
        fib(5)  # Returns the 5th Fibonacci number, which is 5, after simulating a delay.

    Notes:
        This function introduces an artificial delay of 1 second per iteration, making it suitable for use cases
        where a long-running task is desired for testing or simulation purposes.
    """
    a, b = 1, 1
    for i in range(1, nthNumber):
        time.sleep(1)
        a, b = b, a + b
    return a
