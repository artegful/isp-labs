#!/bin/bash

export PYTHONPATH="."

pytest --cov=custom_json --cov=custom_pickle --cov=custom_yaml --cov=serializer/utility tests/*tests.py