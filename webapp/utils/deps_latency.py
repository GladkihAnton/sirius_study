import time
from functools import wraps

from webapp import metrics


def time_it(function):
    @wraps(function)
    async def wrapper(*arg, **kwargs):
        start_time = time.time()

        response = await function(*arg, **kwargs)

        run_time = time.time() - start_time

        metrics.DEPS_LATENCY.labels(endpoint=function.__name__).observe(run_time)

        return response

    return wrapper