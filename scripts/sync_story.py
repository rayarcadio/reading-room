#!/usr/bin/env python3
"""
Convert a finished story manuscript from gunhead-universe/stories/ into this
site's Jekyll chapter format and write it into _stories/.

Usage: sync_story.py /path/to/gunhead-universe/stories/GUNHEAD-v10.md
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DST_DIR = REPO_ROOT / "_stories"

# Substring (case-insensitive) match against the source filename -> story_id
# used in _data/stories.yml. Add an entry here when a new story is added.
STORY_ID_MAP = {
    "gunhead": "gunhead",
    "calamari": "calamari",
    "tic_tac": "tictac",
    "tictac": "tictac",
    "nightingale": "nightingale",
    "rosie": "rosie",
}


def resolve_story_id(filename: str) -> str:
    stem = filename.lower()
    for needle, story_id in STORY_ID_MAP.items():
        if needle in stem:
            return story_id
    raise SystemExit(
        f"sync_story.py: don't know which story_id '{filename}' belongs to. "
        f"Add it to STORY_ID_MAP in {__file__}."
    )


def strip_title_block(lines: list[str]) -> list[str]:
    """Strip a leading '# Title' metadata block (through its first '---'
    divider, if any within the first 15 lines) so the Jekyll layout's own
    title header isn't duplicated in the chapter body."""
    if not lines or not lines[0].startswith("#"):
        return lines

    for i, line in enumerate(lines[:15]):
        if line.strip() == "---":
            return lines[i + 1 :]

    # No title-block divider found (e.g. Tic Tac's format) -> just drop line 1
    return lines[1:]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: sync_story.py <path-to-source-story.md>")

    src_path = Path(sys.argv[1]).resolve()
    if not src_path.is_file():
        raise SystemExit(f"sync_story.py: no such file: {src_path}")

    story_id = resolve_story_id(src_path.name)

    lines = src_path.read_text(encoding="utf-8").splitlines(keepends=True)
    body_lines = strip_title_block(lines)
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)
    body = "".join(body_lines)

    front_matter = (
        "---\n"
        "layout: chapter\n"
        f"story_id: {story_id}\n"
        "chapter: 1\n"
        f"permalink: /read/{story_id}/1/\n"
        "---\n\n"
    )

    dst_path = DST_DIR / f"{story_id}-01.md"
    dst_path.write_text(front_matter + body, encoding="utf-8")
    print(f"synced {src_path.name} -> {dst_path.relative_to(REPO_ROOT)}  ({story_id})")


if __name__ == "__main__":
    main()
