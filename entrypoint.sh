#!/bin/bash

echo "============================"

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${INPUT_EMAIL}"
git config --global --add safe.directory /github/workspace

git pull origin main
python3 /usr/bin/rss.py
git add -A && git commit -m "Update Feed"
git push origin main

echo "============================"
