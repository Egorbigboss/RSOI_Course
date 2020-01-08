from celery import Celery

app = Celery(
    'cqueue',
    broker = 'redis://user:test@localhost:6379/0',
    include = ['GatewayApp.cel_queue.tasks']
)

if __name__ == "__main__":
    app.start()