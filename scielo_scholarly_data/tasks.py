import logging

from celery import Celery

from app.configuration import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND_URL,
    QUEUE_ADD_SCORE,
    QUEUE_GET_BEST_SCORE,

)

from operator import itemgetter
from app import std_sponsor


app = Celery('tasks', backend=CELERY_RESULT_BACKEND_URL, broker=CELERY_BROKER_URL)

LOGGER = logging.getLogger(__name__)


def _handle_result(task_name, result, get_result):
    if get_result:
        return result.get()


###########################################

def get_sponsor_names_with_score(
        name,
        standard_name_and_acron_items,
        method,
        get_result=False,
        ):
    res = task_get_sponsor_names_with_score.apply_async(
        queue=QUEUE_ADD_SCORE,
        args=(
            name,
            standard_name_and_acron_items,
            method,
        ),
    )
    return _handle_result("task get_sponsor_names_with_score", res, get_result)


@app.task()
def task_get_sponsor_names_with_score(
        name,
        standard_name_and_acron_items,
        method,
        ):
    return std_sponsor.get_sponsor_names_with_score(
        name,
        standard_name_and_acron_items,
        method,
    )


##############################
def get_standardized_sponsor_name(name, standard_names, method, get_result=False):
    res = task_get_standardized_sponsor_name.apply_async(
        queue=QUEUE_GET_BEST_SCORE,
        args=(
            name,
            standard_name_and_acron_items,
            method,
        ),
    )
    return _handle_result("task standardized_sponsor_name", res, get_result)


@app.task()
def task_get_standardized_sponsor_name(name, standard_names, method):
    temp = []
    try:
        for standard_name in standard_names:
            std_name, std_acron = standard_name.split(",")
            sponsor_standardized = get_sponsor_names_with_score(
                name,
                std_sponsor.make_standard_sponsor(std_name, std_acron),
                method=method,
                get_result=True,
            )
            if sponsor_standardized != None:
                temp.append(sponsor_standardized[0])

        temp = sorted(temp, key=itemgetter('score'))
        return temp[-1]
    except:
        return
