from unittest.mock import patch

from app.worker import fib, sleepy


@patch("app.worker.celery.task")  # Mock the celery.task decorator
def test_sleepy(mock_celery_task):
    # Test the 'sleepy' task without using Celery
    result = sleepy(5)
    assert result == "Slept for 5 second(s)"


@patch("app.worker.celery.task")
@patch("time.sleep", return_value=None)  # Mock time.sleep to avoid delays in testing
def test_fib_large_number(mock_time_sleep, mock_celery_task):
    # Test the Fibonacci task without the actual 1-second delays
    result = fib(10)  # Call the task directly
    assert result == 55  # 10th Fibonacci number is 55
