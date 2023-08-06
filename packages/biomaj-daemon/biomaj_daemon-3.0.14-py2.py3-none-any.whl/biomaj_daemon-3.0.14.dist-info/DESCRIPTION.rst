# About

Microservice to manage biomaj, acts as a frontend to receive biomaj-cli commands and execute operations

Needs mongo and redis



# Development

    flake8 --ignore E501 biomaj_daemon


# Run

## Message consumer:

    export BIOMAJ_CONFIG=path_to_config.yml
    python bin/biomaj_daemon_consumer.py

## Web server

If package is installed via pip, you need a file named *gunicorn_conf.py* containing somehwhere on local server:

    def worker_exit(server, worker):
        from prometheus_client import multiprocess
        multiprocess.mark_process_dead(worker.pid)

If you cloned the repository and installed it via python setup.py install, just refer to the *gunicorn_conf.py* in the cloned repository.

    export BIOMAJ_CONFIG=path_to_config.yml
    rm -rf ..path_to/prometheus-multiproc
    mkdir -p ..path_to/prometheus-multiproc
    export prometheus_multiproc_dir=..path_to/prometheus-multiproc
    gunicorn -c ../path_to/gunicorn_conf.py biomaj_daemon.daemon.biomaj_daemon_web:app

Web processes should be behind a proxy/load balancer, API base url /api/daemon

## API

For authentication, add api key to HTTP header X-API-KEY

For admin only, operations, add to config.yml

    general:
      admin:
        - admin_user_id



TO use API, some operations are limited to 


3.0.14:
  Fake version for Pypi re-upload
3.0.13:
  Allow per service local_endpoint definition
  Add --stats option
  Modify --version option to get all module details
  Add REST API to daemon (/api/daemon/...)

3.0.12:
  Add biomaj_daemon_consumer.py to python scripts for install with package
3.0.11:
  Disable daemon web service logging
3.0.10:
  Fix tail endpoint syntax
3.0.9:
  Fix #1 remove debug log
  Fix #2 log dir not removed with --remove-all if proxy option not set
3.0.8:
  Fix #78, for multiple banks update in monolithic config, if one fails, next banks are not updated
  Add /api/daemon/bank/x/log[/y] endpoint to get last bank session log file
3.0.7:
  Add whatsup support for non proxy config
  Skip bank config with errors
3.0.6:
  Fix logging for monolithic setup
  Add whatsup option
  Fix prometheus stats
3.0.5:
  Fix for python 2.x
3.0.4:
  Fix status page with other services
  Add missing README in package
3.0.3:
  Fix missing parameters
3.0.2:
  Move options to management to utils for reuse
  Fix --about-me
3.0.1:
  Micro service to manage biomaj updates


