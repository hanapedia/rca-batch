from application.use_cases import GatherMetricsUseCase
from infrastructure.kubernetes_adapter import KubernetesAdapter
from infrastructure.prometheus_adapter import PrometheusAdapter
from infrastructure.s3_adapter import S3Adapter

def main():
    gather_metrics = GatherMetricsUseCase(
        KubernetesAdapter('your-namespace'),
        PrometheusAdapter('http://localhost:9090'),
        S3Adapter('your-bucket')
    )
    gather_metrics.execute()

if __name__ == "__main__":
    main()
