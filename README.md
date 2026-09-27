# Reading Room

A private, GitHub Pages–hosted reading site for Ray Arcadio's stories, built with Jekyll.

Live at: https://rayarcadio.github.io/reading-room/

This site is **unlisted, not secured** — the URL isn't linked anywhere public and
`robots.txt` / `noindex` keep it out of search engines, but anyone with the exact link
can open it. See the "Adding a new story" section below for how to publish new work.

## Structure

- `_data/series.yml` — the list of series/universes shown on the home page.
- `_data/stories.yml` — one entry per story: title, series, description, cover, status.
- `_stories/` — the actual story text. One file per chapter, named `<story-id>-<NN>.md`.
- `assets/covers/` — cover images (placeholder SVGs for now — swap in real art anytime).
- `_layouts/`, `assets/css`, `assets/js` — site templates, styling, dark-mode + "continue
  reading" behavior.

## Adding a new story

1. Pick a short lowercase `story_id` (e.g. `jude`).
2. Add an entry to `_data/stories.yml`:
   ```yaml
   jude:
     title: JUDE
     subtitle: Jude's Story
     series: gunhead-universe
     order: 6
     status: First Draft
     description: "A one-sentence hook, no spoilers."
     cover: /assets/covers/jude.svg
   ```
3. Drop a cover image into `assets/covers/jude.svg` (or `.jpg`/`.png` — just update the
   `cover:` path to match).
4. Create `_stories/jude-01.md`:
   ```markdown
   ---
   layout: chapter
   story_id: jude
   chapter: 1
   permalink: /read/jude/1/
   ---

   Your story text starts here.
   ```
5. For a multi-chapter story, add `jude-02.md`, `jude-03.md`, etc., bumping `chapter:`
   and `permalink:` each time (`/read/jude/2/`, `/read/jude/3/`...). Previous/Next
   chapter links appear automatically once a story has more than one chapter file.
6. Commit and push. GitHub rebuilds the site automatically — no other steps needed.

## Local preview (optional)

Requires Ruby + Bundler installed once:

```bash
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000/reading-room/ in a browser.
