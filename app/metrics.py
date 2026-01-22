"""
Prometheus metrics for monitoring
"""

from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
requests_total = Counter(
    'chatbot_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

responses_total = Counter(
    'chatbot_responses_total',
    'Total number of chat responses generated'
)

errors_total = Counter(
    'chatbot_errors_total',
    'Total number of errors',
    ['error_type']
)

# Performance metrics
request_duration = Histogram(
    'chatbot_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

active_requests = Gauge(
    'chatbot_active_requests',
    'Number of active requests'
)

# Token usage metrics
tokens_used = Histogram(
    'chatbot_tokens_used',
    'Number of tokens used per request',
    buckets=[10, 50, 100, 500, 1000, 2000, 5000]
)

# Redis metrics
redis_operations = Counter(
    'chatbot_redis_operations_total',
    'Total Redis operations',
    ['operation']
)

redis_errors = Counter(
    'chatbot_redis_errors_total',
    'Total Redis errors'
)

# Session metrics
active_sessions = Gauge(
    'chatbot_active_sessions',
    'Number of active sessions'
)
