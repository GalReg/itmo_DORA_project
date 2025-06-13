import time
import psutil
from fastapi import Response, Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

REQUESTS = Counter(
    'purchase_requests_total',
    'Total number of requests to the Purchase API',
    ['endpoint', 'method']
)

REQUEST_TIME = Histogram(
    'purchase_request_duration_seconds',
    'Time spent processing request',
    ['endpoint', 'method']
)

STATUS_CODES = Counter(
    'purchase_response_status_total',
    'Total number of responses by status code',
    ['status_code', 'endpoint', 'method']
)

MODEL_USAGE = Counter(
    'purchase_model_usage_total',
    'Total number of model invocations',
    ['model_name']
)

CPU_USAGE = Gauge(
    'purchase_cpu_usage_percent',
    'CPU usage in percent'
)

MEMORY_USAGE = Gauge(
    'purchase_memory_usage_bytes',
    'Memory usage in bytes'
)

MEMORY_PERCENT = Gauge(
    'purchase_memory_usage_percent',
    'Memory usage in percent'
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        method = request.method
        REQUESTS.labels(endpoint=endpoint, method=method).inc()
        
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        REQUEST_TIME.labels(endpoint=endpoint, method=method).observe(duration)
        
        status_code = str(response.status_code)
        STATUS_CODES.labels(status_code=status_code, endpoint=endpoint, method=method).inc()
        
        return response

def collect_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
    mem = psutil.virtual_memory()
    MEMORY_USAGE.set(mem.used)
    MEMORY_PERCENT.set(mem.percent)

def setup_metrics(app):
    app.add_middleware(PrometheusMiddleware)
    
    @app.get("/metrics")
    def metrics():
        collect_system_metrics()
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )