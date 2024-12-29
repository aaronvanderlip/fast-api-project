import os

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")

result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

task_track_started = True
