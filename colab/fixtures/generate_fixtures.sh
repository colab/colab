#!/bin/bash

python ../manage.py dumpdata --indent=2 auth.user super_archives > sample_data.json
