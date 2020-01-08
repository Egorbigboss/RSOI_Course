from .celery import app
from .Jobs import Job
from celery import Task
from requests.exceptions import RequestException

# celery -A cqueue worker -l info -P gevent


class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f'{task_id} failed: {exc}')

    def on_success(self, retval, task_id, args, kwargs):
        print(f'{task_id} returned code : *{retval}*')


JREQ = Job()

@app.task(base=CustomTask, autoretry_for=(RequestException,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def post_task(url: str, data : dict):
    return JREQ.post(url, data)


@app.task(bind = True, base=CustomTask, autoretry_for=(RequestException,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def patch_task(url: str, data : dict):
    print("hmm",url,data)
    return JREQ.patch(url, data)
