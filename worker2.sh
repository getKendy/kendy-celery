#!/bin/bash

celery -A src worker --loglevel=INFO -Q barometer