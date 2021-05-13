#!/bin/bash

cp ./tests/*tests.py .
pytest --cov=serializer ./*tests.py
rm ./*tests.py