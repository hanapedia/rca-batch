# RCA Batch jobs
Batch jobs required for running rca experiments.

The job consists of following steps:
1. Query Prometheus API for metrics such as CPU usage, memory usage, and network latency.
2. Format queried metrics into Pandas Dataframe.
3. Save the Dataframe to S3 bucket or localfile.

## Usage
### Run Locally
Prerequisite:
- K8s cluster access via kube config.
- AWS credentials in `~/.aws/` (for S3).
- Prometheus API access (defaults at `http://localhost:9090`).

Prepare env file:
```sh
    cp .env.example .env
    vi .env # fill the environmental variables as needed.
```

Run:
```sh
    make install
    make start
```

### Run in Kubernetes
Prerequisite:
- K8s cluster access via kube config.
- AWS credentials in `~/.aws/` (for S3).
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) controller installed in cluster and cli installed locally.

Prepare env file:
```sh
    cp .env.example k8s/overlays/development/.env.k8s
    vi k8s/overlays/development/.env.k8s # fill the environmental variables as needed.
```

Build Image if needed:
```sh
    make ship
```

Deploy:
```sh
    make deploy NAMESPACE=[namespace to deploy to]
```
