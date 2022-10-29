#!/bin/bash
docker compose stop
docker compose build inference-service
docker compose push inference-service