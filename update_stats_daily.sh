#!/bin/sh

# Navigate to the repository directory
cd /Users/samir/Desktop/GithubReadme/isym444

# Optional: Add all changes to staging
git add *
git add .
git add -A

# Optional: Commit changes with a generic message
git commit -m "Updated stats"

# Push changes to the remote repository
git push
