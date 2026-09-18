# Meilenguru

Static HTML site for Swiss-based frequent-flyer advice — earning Miles & More and
Flying Blue miles from everyday CHF spending, and redeeming them for business and
first class. Deployed on Netlify at **meilenguru.ch**. Bilingual: English pages and
German pages exist as separate files.

## Working here efficiently

This repo is ~114 hand-written HTML pages. Reading one costs roughly 6,000–15,000
tokens, so how a task is approached matters more than usual.

- **Never read the whole site.** Use `grep`/`rg` to find the pages that matter, then
  read only those. `rg -l "Bundle & Go" *.html` beats opening files to look.
- **For a change across many pages, write a script** (`sed -i`, or a short Python
  read-modify-write) instead of opening each page. A script never loads page content
  into context. `scripts/seo_check.py` is an existing example.
- **Edit, don't rewrite.** Targeted string replacements cost a fraction of re-emitting
  a whole page.
- **Styling changes usually belong in `assets/`, not in a page** — see below.
- Prefer one task per session. Files read earlier stay in context and are re-sent on
  every subsequent turn.

## Layout

```
*.html              ~114 pages, flat in the repo root
assets/site.css     shared base styles
assets/site-media.css  shared responsive styles
cookie-consent.js   the only page script
docs/               working notes (SEO report, language-migration proposal)
scripts/            seo_check.py
netlify.toml        redirects + security headers
_redirects          URL redirects
sitemap.xml, robots.txt, llms.txt
```

Page naming is not fully consistent — the same article can exist as
`meilenguru-strategy-<topic>.html` (EN) and `<thema>-schweiz.html` (DE), and some
older pages use other patterns. Grep for the headline rather than guessing a filename.

## CSS architecture

Styles load in three stages, and the order is load-bearing:

1. `assets/site.css` — rules that were byte-identical on every page using them
2. the page's own `<style>` — anything specific to that page
3. `assets/site-media.css` — shared `@media` rules, which must come *after* the
   page's `<style>` so base rules never override breakpoints

Some pages add a second `<style>` after step 3 for their own media queries.

Rules when touching CSS:

- A change that should apply site-wide goes in `assets/site.css`. One edit, not 114.
- A rule that differs on even one page stayed inline on purpose — the shared files
  only hold rules that were identical everywhere, because a page-level override
  cannot un-set a property the shared rule adds.
- **Keep a selector's media queries together.** If `.foo` has both a `@768` and a
  `@480` rule, both live in the same place. Splitting them between `site-media.css`
  and a page's `<style>` inverts the breakpoints.
- Design tokens are CSS custom properties on `:root`. `:root` is *not* shared —
  several pages define extra variables — so a new global token must be added to
  each page that needs it, or promoted into `site.css` only if every page agrees.

## Design system

| Variable | Value |
|---|---|
| `--black` | `#0a0a0a` |
| `--white` | `#faf9f7` |
| `--warm-white` | `#f5f3ef` |
| `--gold` | `#b8962e` |
| `--gold-light` | `#d4ae4e` |
| `--muted` | `#888580` |
| `--font-display` | Cormorant Garamond (serif) |
| `--font-body` | DM Sans (sans-serif) |

Fonts load from Google Fonts. No build step, no framework, no bundler.

## Content style rules

- Never use en-dashes (`–`) in page content. For ranges, compound words and route
  pairs ("Zürich-Cancún", "2-3 years") use a plain hyphen (`-`).
- Em-dashes (`—`) are fine and used deliberately for asides.

## Deployment

Netlify serves the files directly; no build command. Pushing to `main` on GitHub
deploys automatically.

```bash
git add <changed-files>
git commit -m "description of change"
git push origin main
```

Because there is no build step, a broken CSS edit ships as-is. After a change that
touches shared styles, check a page at desktop and mobile width before pushing.

## Recurring tasks

A weekly audit runs on its own — a macOS `launchd` LaunchAgent
(`com.meilenguru.weeklyaudit`, plist at
`~/Library/LaunchAgents/com.meilenguru.weeklyaudit.plist`) fires
`~/.claude/meilenguru-weekly-audit.sh` at every login and daily at 9:07am; the
script gates actual execution to roughly once every 7 days. It runs `claude -p`
headlessly against `~/.claude/referral-audit-prompt.md`, which covers the whole
site — welcome-bonus figures, `referrals.html` / `empfehlungen.html` and every
card's dedicated review page (the on-site page is called "Card offers";
"referrals"/`empfehlungen` is a legacy filename left over from when the site ran
referral links, which it no longer does), the monthly Flying Blue Promo Awards
post, the availability radar, and the homepage ticker — and commits + pushes any
fixes directly. Logs at `~/.claude/logs/meilenguru-audit.log`.

This is OS-level automation: it runs regardless of whether you're working here
via Claude Code (terminal) or Claude Desktop, and needs no re-arming or
session-start action. Full audit instructions live in
`~/.claude/referral-audit-prompt.md`, not in this repo. Don't set up a second
recurring job for this (local cron or a Cowork scheduled routine) — this is the
only one, and it already covers the full card-offers scope.
