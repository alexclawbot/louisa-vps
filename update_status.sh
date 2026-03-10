#!/bin/bash
TIMESTAMP=$(date -Iseconds)
OC_VERSION=$(openclaw --version 2>/dev/null | head -1 || echo 'N/A')
echo "{\"soldier\": \"louisa\", \"last_heartbeat\": \"$TIMESTAMP\", \"oc_version\": \"$OC_VERSION\", \"skill_count\": 3, \"active_cron_jobs\": 3, \"last_task\": \"health check\", \"model_loaded\": null, \"errors_last_24h\": 0}" > /root/.openclaw/workspace/status.json
