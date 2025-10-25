import logging
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_logging():
    return logger


# Métriques Prometheus existantes
query_counter = Counter('rag_queries_total', 'Total queries processed', ['provider', 'status'])
response_time_histogram = Histogram('rag_response_time_seconds', 'Response time distribution')
accuracy_gauge = Gauge('rag_accuracy_score', 'Current accuracy score')
cache_hit_counter = Counter('rag_cache_hits_total', 'Total cache hits', ['cache_type'])

# Nouvelles métriques Prometheus pour API/RAG/Cache
api_requests_total = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
api_responses_total = Counter('api_responses_total', 'Total API responses', ['method', 'endpoint', 'status_code'])
api_errors_total = Counter('api_errors_total', 'Total API errors', ['method', 'endpoint', 'status_code'])
api_response_time_seconds = Histogram('api_response_time_seconds', 'API response time in seconds', ['method', 'endpoint', 'status_code'])
rag_processing_time_seconds = Histogram('rag_processing_time_seconds', 'RAG processing time in seconds', ['endpoint', 'status'])
cache_operations_total = Counter('cache_operations_total', 'Total cache operations', ['status', 'endpoint'])
