import os
import time
from typing import Tuple

import prometheus_client
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    multiprocess as prom_mp,
)
from prometheus_client.multiprocess import MultiProcessCollector
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp, Message, Receive, Scope, Send

DEFAULT_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.125,
    0.15,
    0.175,
    0.2,
    0.25,
    0.3,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    float('+inf'),
)


def register() -> prometheus_client.CollectorRegistry:
    registry = prometheus_client.CollectorRegistry()
    prom_mp.MultiProcessCollector(registry)
    return registry


REQUESTS = Counter(
    'sirius_starlette_requests_total',
    'Total count of requests by method and path.',
    ['method', 'path_template'],
)

RESPONSES = Counter(
    'sirius_starlette_responses_total',
    'Total count of responses by method, path and status codes.',
    ['method', 'path_template', 'status_code'],
)
REQUESTS_PROCESSING_TIME = Histogram(
    'sirius_starlette_requests_processing_time_seconds',
    'Histogram of requests processing time by path (in seconds)',
    ['method', 'path_template'],
    buckets=DEFAULT_BUCKETS,
)
EXCEPTIONS = Counter(
    'sirius_starlette_exceptions_total',
    'Total count of exceptions raised by path and exception type',
    ['method', 'path_template', 'exception_type'],
)
REQUESTS_IN_PROGRESS = Gauge(
    'sirius_starlette_requests_in_progress',
    'Gauge of requests by method and path currently being processed',
    ['method', 'path_template'],
)
DEPS_LATENCY = prometheus_client.Histogram(
    'sirius_deps_latency_seconds',
    '',
    ['endpoint'],
    buckets=DEFAULT_BUCKETS,
)
SENT_TO_KAFKA = Counter(
    'sirius_sent_to_kafka_total',
    'Total count of sent messages to kafka topic per client',
    ['topic', 'client_id'],
)


class PrometheusMiddleware:
    def __init__(self, app: ASGIApp, filter_unhandled_paths: bool = False) -> None:
        self.app = app
        self.filter_unhandled_paths = filter_unhandled_paths

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] not in ('http', 'websocket'):
            await self.app(scope, receive, send)
            return

        status_code = None

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code, send
            if message['type'] == 'http.response.start':
                status_code = message['status']
            await send(message)

        conn = HTTPConnection(scope)
        method = scope['method']
        path_template, is_handled_path = self.get_path_template(conn, scope)

        if self._is_path_filtered(is_handled_path):
            await self.app(scope, receive, send)
            return

        REQUESTS_IN_PROGRESS.labels(method=method, path_template=path_template).inc()
        REQUESTS.labels(method=method, path_template=path_template).inc()
        before_time = time.perf_counter()
        try:
            await self.app(scope, receive, send_wrapper)
        except BaseException as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            EXCEPTIONS.labels(
                method=method,
                path_template=path_template,
                exception_type=type(e).__name__,
            ).inc()
            raise e from None
        else:
            after_time = time.perf_counter()
            REQUESTS_PROCESSING_TIME.labels(method=method, path_template=path_template).observe(
                after_time - before_time
            )
        finally:
            RESPONSES.labels(method=method, path_template=path_template, status_code=status_code).inc()
            REQUESTS_IN_PROGRESS.labels(method=method, path_template=path_template).dec()

    @staticmethod
    def get_path_template(conn: HTTPConnection, scope: Scope) -> Tuple[str, bool]:
        for route in scope['app'].routes:
            match, child_scope = route.matches(scope)
            if match == Match.FULL:
                return route.path, True

        return conn.url.path, False

    def _is_path_filtered(self, is_handled_path: bool) -> bool:
        return self.filter_unhandled_paths and not is_handled_path


def metrics(request: Request) -> Response:
    if 'prometheus_multiproc_dir' in os.environ:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    return Response(generate_latest(registry), headers={'Content-Type': CONTENT_TYPE_LATEST})
