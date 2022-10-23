#!/bin/bash
chmod +x ./model_register_server/wait-for-it.sh
docker compose --profile production --env-file envs/mlflow/mlflow.env up 