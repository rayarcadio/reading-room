#!/bin/bash
# Convert one story from gunhead-universe/stories/ into this site's Jekyll
# format, commit it, and push. Safe to run by hand any time:
#   ./sync-story.sh /path/to/gunhead-universe/stories/GUNHEAD-v10.md
#
# Also invoked automatically by gunhead-universe's post-commit hook whenever a
# story version-bump commit lands (see gunhead-universe/.githooks/post-commit).
set -euo pipefail

SRC="${1:?usage: sync-story.sh <path-to-source-story.md>}"
cd "$(dirname "${BASH_SOURCE[0]}")"

python3 scripts/sync_story.py "$SRC"

CHANGED=$(git status --porcelain _stories/)
if [ -z "$CHANGED" ]; then
  echo "sync-story.sh: no changes to sync for $SRC (site already up to date)"
  exit 0
fi

STORY_FILE=$(git status --porcelain _stories/ | awk '{print $2}')
git add "$STORY_FILE"
git commit -m "Sync $(basename "$SRC") to reading room"
git push
echo "sync-story.sh: pushed $STORY_FILE — https://rayarcadio.github.io/reading-room/"
