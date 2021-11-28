#!/bin/bash

#gunicornCmd="gunicorn --workers=2 --bind=127.0.0.1:9001 test_flask:app"
gunicornCmd="gunicorn --workers=2 --bind=127.0.0.1:9001 metric_reporter:flask_app()"

$gunicornCmd