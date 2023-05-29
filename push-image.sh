#!/bin/bash
docker compose stop
docker compose build inference-service mlflow-server k8s-test-image
docker compose push inference-service mlflow-server k8s-test-image