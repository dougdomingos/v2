#!/bin/bash
# 
# Automatically push any existent changes to the blog repository.
# Authors: @dougdomingos

readonly COMMIT_AUTHOR='github-actions[bot] <github-actions[bot]@users.noreply.github.com>'

git diff --quiet
change_status=$?

if [ $change_status -ne 0 ]; then
    git add ./data/projects.yaml
    git commit -m "chore(actions): update project list" --author="$COMMIT_AUTHOR"
    git push
else
    echo "No changes detected. Nothing to commit."
fi
