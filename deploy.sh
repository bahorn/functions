#!/bin/sh
gcloud functions deploy calendar_req \
    --source ./functions/ics-2-ical  \
    --runtime python38 \
    --trigger-http \
    --allow-unauthenticated
