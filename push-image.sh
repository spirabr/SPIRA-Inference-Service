#!/bin/bash
docker compose stop
docker compose build inference-service mlflow-server
docker compose push inference-service mlflow-server