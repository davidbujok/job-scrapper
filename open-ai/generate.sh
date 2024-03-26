#!/bin/bash

echo 'Job ID:'
read input

url=$(echo -e "$input" | python generate_personal_statement.py)

echo `firefox-developer-edition $url` &

