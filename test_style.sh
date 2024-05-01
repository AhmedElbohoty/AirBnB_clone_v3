#!/usr/bin/env bash

find . -type f -name "*.py" | grep -v "./airbnb_venv/" | while read -r file_path; do
    pycodestyle "$file_path"
done