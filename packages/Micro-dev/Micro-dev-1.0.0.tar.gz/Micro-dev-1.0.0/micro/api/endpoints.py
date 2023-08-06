import os
from celery import Celery

BROKER_URL = os.environ.get("MICRO_BROKER_URL")
QUEUE = os.environ.get("MICRO_QUEUE")

if not BROKER_URL:
    raise RuntimeError("No broker URL set")

if not QUEUE:
    raise RuntimeError("No queue set")

app = Celery("Micro", broker=BROKER_URL, backend="rpc://")


@app.task(name="Micro.plugins", queue=QUEUE)
def plugins():
    pass


@app.task(name="Micro.info", queue=QUEUE)
def info(name):
    pass


@app.task(name="Micro.help", queue=QUEUE)
def help(name):
    pass


@app.task(name="Micro.run", queue=QUEUE)
def run(plugin_name, **kwargs):
    pass
