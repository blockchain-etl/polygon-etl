#!/usr/bin/env bash

gcloud deployment-manager deployments create matic-etl-pubsub-0 --template deployment_manager_pubsub_matic.py
