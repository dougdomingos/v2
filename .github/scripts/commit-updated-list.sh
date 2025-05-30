#!/bin/bash
# 
# Automatically push any existent changes to the blog repository.
# Authors: @dougdomingos

git diff --quiet
change_status=$?

if [ $change_status -ne 0 ]; then
    git add ./data/projects.yaml
    git commit -m "chore(actions): update project list"
    git push
else
    echo "No changes detected. Nothing to commit."
fi
