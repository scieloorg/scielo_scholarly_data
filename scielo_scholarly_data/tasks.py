import logging

from celery import Celery

from app.configuration import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND_URL,
    REGISTER_ROW_QUEUE,
)

from app import std_sponsor


app = Celery('tasks', backend=CELERY_RESULT_BACKEND_URL, broker=CELERY_BROKER_URL)

LOGGER = logging.getLogger(__name__)


def _handle_result(task_name, result, get_result):
    if get_result:
        return result.get()


###########################################

def get_sponsor_names(
        name,
        standard_name_and_acron_items,
        method,
        get_result=True,
        ):
    res = task_get_sponsor_names.apply_async(
        queue=REGISTER_ROW_QUEUE,
        args=(
            name,
            standard_name_and_acron_items,
            method,
        ),
    )
    return _handle_result("task get_sponsor_names", res, get_result)


@app.task()
def task_get_sponsor_names(
        name,
        standard_name_and_acron_items,
        method,
        ):
    return std_sponsor.get_sponsor_names(
        name,
        standard_name_and_acron_items,
        method,
    )
