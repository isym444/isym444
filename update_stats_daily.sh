#!/bin/sh

# Navigate to the repository directory
cd /home/iym444/Desktop/anki-vocab-totals-transfer-to-linux/isym444

git pull

# Optional: Add all changes to staging
git add *
git add .
git add -A

# Optional: Commit changes with a generic message
git commit -m "Updated stats"

# Push changes to the remote repository
git push
