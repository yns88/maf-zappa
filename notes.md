# REFERENCE NOTES

- https://github.com/Miserlou/zappa
- https://github.com/Miserlou/django-zappa


- init: manage.py deploy dev
- deploy: manage.py update dev
- remote commands: manage.py invoke dev
    - does not work for shell, dbshell, migrate

## Setup steps
- make django project
- install django-zappa, add to INSTALLED_APPS and MIDDLEWARE
- add ZAPPA_SETTINGS to settings.py
- manage.py deploy dev

## Static assets
- install django-storages
- set DEFAULT_FILE_STORAGE = 'libs.storages.S3Storage.S3Storage'
- set STATIC_URL to your S3 bucket and add settings params for AWS credentials
- run manage.py collectstatic

## Database setup
- setup RDS instance
- configure lambda function to run on same VPC as the database
- punch hole in VPC to allow local connections to database
- manage.py migrate from localhost
- manage.py update dev

## General Lambda issues
- python 2.7 is all that's supported by default
- shipping precompiled binaries for dependencies is tricky

## Django-Zappa issues
- could only use us-east-1, trying us-west-2 caused problems
- cannot manage.py shell/dbshell/migrate inside the lambda function
- cannot have egg-links in site-packages (zappa auto-packages your virtualenv)
- deploys sometimes include outdated pycs (need to do your own pyc cleanup before deploying)
- django redirect responses did not respect the `/dev` SCRIPT_NAME
- keep_warm doesn't do anything, need to add your own "keep warm" event schedule to Amazon
- zappa moves settings.py into BASE_DIR, which can break the BASE_DIR calculation
- failed deploys leave junk zipfiles in repo root

## Billing breakdown (small-scale deployment)
- Lambda: Free for 1M monthly requests or 400,000 RAM GB-seconds of CPU time
- Postgres: Free t2.micro for 12 months, then ~$13/month
    - Seems worthy to migrate to DynamoDB for a long-term free offering and better bang:buck ratio
- S3: Free for 12 months, then ~$0.50/month to serve basic static assets (CSS/JS)
- VPC: ~$30/month if using a NAT gateway to make outbound calls from inside a lambda in a VPC
    - Alternatively, one could move the lambda out of the VPC and take risks with exposing the RDS instance
- API Gateway: Free for 12 months, then ~$4.00/month to serve 1M API requests
- Total costs: $0/mo for 12 months, then ~$18/mo for a small app (or $5/mo if using DynamoDB)
