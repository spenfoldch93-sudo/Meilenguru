# SEO Implementation Report

Implementing the SEO remediation plan derived from the Google Search Console
+ live-site audit. 9 commits, direct to `main` (by owner's choice — no PR
workflow exists on this repo; see CLAUDE.md). All changes verified live
after each push, not just locally.

Commits, in order: `5361404` → `329ddfe`.

---

## 1. What was done, by phase

### Phase 1 — Critical technical fixes (`5361404`)
- Added `robots.txt` (was 404) and `/llms.txt` (new).
- The `.html` → clean-URL redirect was the single highest-priority item.
  `netlify.toml` already had a `force = true` rule for this, but it silently
  didn't work in production (`/about.html` was returning 200, not 301).
  Replaced with 58 explicit `_redirects` rules, verified individually —
  all now return 301 with no redirect loop.
- Fixed the "Duplicate without user-selected canonical" GSC flag on
  `/meilenguru-flying-blue-promo-may-2026` — it had no canonical tag at
  all, and turned out to be genuinely distinct content (a dated promo
  breakdown, not a duplicate of the evergreen guide), so added the missing
  canonical rather than redirecting real content away.
- Fixed the dead footer language switcher (FR linked to `#`, removed
  entirely; DE on the German homepage also linked to `#` instead of
  marking itself current).
- Regenerated `sitemap.xml`: real git-derived `lastmod`, dropped
  `priority`/`changefreq`, added reciprocal hreflang alternates.
- Confirmed already-correct, no fix needed: `/de/` and `/fr/` return clean
  404s, http→https redirects correctly.

### Phase 2 — Performance (`a38e8c2`, extended in `c8c7396`)
- Homepage was 909-928KB, of which 835KB was 6 base64-encoded photos
  inline in the CSS. Extracted to WebP, both homepages now 74KB (92%
  reduction) — already well under the &lt;100KB target from this alone.
- Added width/height to all logo `<img>` tags, lazy-loading on below-fold
  images.
- Added long-cache immutable headers for image assets in `netlify.toml`.
- **Extended scope**: the verification script (Phase 9) surfaced the same
  problem at much larger scale — `blog.html` was 1.5MB, and several
  individual trip-report pages were 200KB-1MB each. Site-wide scan found
  18 unique embedded images across all pages; extracted the 12 not already
  handled, replaced all 36 occurrences. **Every page on the site is now
  under 100KB** (was up to 1.5MB for the worst offender).
- Deliberately not done: extracting the ~20KB of inline `<style>`/`<script>`
  per page into external files, and self-hosting Google Fonts. The stated
  target was already met by the image work; these are lower-value,
  higher-risk changes given how many pages share slightly different inline
  style blocks.

### Phase 3 — Structured data (`ce28cd2`)
- 24 pages had zero JSON-LD. Added Organization + WebSite schema
  site-wide, FAQPage (built from the real 11 on-page Q&A pairs) on the FAQ
  pages, Service+Offer (CHF 79) on the consultation pages, Person on the
  About pages, WebApplication on the tools pages, Article on 6 strategy
  pages that had none.
- Found and fixed 2 pages with genuinely invalid JSON-LD: an unescaped
  HTML anchor tag inside a JSON string field broke the parser (matches
  GSC's exact "Missing ',' or '}'" error). While fixing it, also found the
  German version's structured data was describing the page in English —
  fixed the language too.
- 58/58 pages now carry valid JSON-LD (verified with `json.loads()` on
  every block), 78 blocks total.

### Phase 4 — hreflang (`39f5e85`)
- Rebuilt hreflang across all 58 pages from one verified 29-pair EN/DE
  map: exactly 3 tags, fully reciprocal, absolute clean URLs.
- **x-default now points to German** for the 23 Swiss-intent pairs
  (strategy guides, tools, FAQ, referrals, about, consultation) — 89% of
  impressions are Swiss and search in German. Kept English as x-default
  for the 6 trip-report pairs, which GSC shows pulling real
  Singapore/Netherlands traffic.
- Fixed `lang="de"` → `lang="de-CH"` on 26 pages.
- Wrote `docs/language-migration-proposal.md`: a full write-up for making
  German the default at `/`, with redirect map and risk assessment —
  **not implemented**, per the plan's own instruction to defer it.

### Phase 5 — Titles, meta descriptions, whitespace bugs (`3c8ee97`, `9610b3f`)
- Found and fixed 184 instances (57 files) of a heading concatenation
  bug — `<br>` with no space before it, so the *rendered* page looks fine
  but the raw `textContent` (what search engines parse) reads words fused
  together, e.g. "Kreditkartenfür" instead of "Kreditkarten für". The 4
  bugs named in the audit were confirmed instances of this exact pattern;
  found 180 more.
- Rewrote titles/descriptions for the 12 flagged pages, prioritising the
  two CTR disasters (`/empfehlungen`: 706 impressions/2 clicks/0.28% CTR;
  `/tools-de`: 400 impressions/2 clicks/0.50% CTR). Left
  `/meilen-sammeln-ohne-fliegen-schweiz` (8.7% CTR, the best on the site)
  trimmed for length only, not rewritten.
- Fixed the small number of `ß` instances in German body copy to `ss`
  (Swiss orthography).
- Added `<meta name="robots" content="max-snippet:-1, max-image-preview:large">`
  site-wide.

### Phase 6 — German content parity (`bec0286`)
- `/beste-kreditkarte-meilen-schweiz`: the audit said the FAQ section was
  "missing entirely" — on inspection, the FAQ *content* was already there
  and properly translated (4 matching Q&A pairs), it just had no section
  heading above it, unlike every other section on the page. Added the
  heading.
- Checked the "JS-generated links" theory for `/strategies-benchmark` —
  doesn't hold. The inbound links are plain `<a href>` in raw HTML. The
  more likely cause (`.html`/clean-URL fragmentation) was already fixed
  in Phase 1.
- Reviewed the revolut-amex and business-miles page pairs: not thin by
  any reasonable bar (460-990 words), already have unique
  titles/descriptions/schema. Didn't expand further — no new factual
  material to add without either padding or inventing figures, both
  prohibited by the plan's own ground rules.

### Phase 8 — Internal linking (`329ddfe`)
- Zero orphan pages found site-wide (verified via the script) — every
  sitemap URL already has an inbound internal link. No fix needed there.
- Added visible breadcrumbs (Home › Blog › Article) + matching
  BreadcrumbList schema to all 12 trip-report pages.
- **Not done**: breadcrumbs/related-links on the other 46 pages. 8
  distinct page templates with materially different markup make a single
  scripted rollout unsafe; doing it well by hand per-template is a
  substantial separate piece of work. See "Deferred" below.

### Phase 9 — Verification script
Built `scripts/seo_check.py` (standalone Python, no dependencies, no CI
wiring — per your call not to introduce a Node/npm toolchain into a repo
that's never had one). Checks: sitemap integrity, titles/descriptions
length and uniqueness, H1 count, whitespace-bug regex, canonical
correctness, hreflang reciprocity, `lang` attributes, JSON-LD validity,
image alt/width/height, page weight (HTML/inline-block/data-URI size
budgets), orphan detection, dead `href="#"` links.

Run it any time with:
```
python3 scripts/seo_check.py
python3 scripts/seo_check.py --base-url https://meilenguru.ch   # also checks live status codes
```

This script is what actually caught the Phase 2 extension (the 1.5MB
`blog.html`) and the duplicate EN/DE title bug — it paid for itself
within the same session it was built.

### Phase 7 — New pages: **not built, see "Deferred" below**

### Phase 10 — Commits/deploy
Direct to `main`, 9 commits, each verified live via `curl`/rendered
checks before moving to the next phase (your call, matching how the rest
of this project has worked — no PR review step exists here).

---

## 2. Redirect table

All 58 `.html` URLs → their clean equivalent, 301, via `_redirects`
(replacing the non-functioning `netlify.toml` rule):

| From | To |
|---|---|
| `/index.html` | `/` |
| `/about.html` | `/about` |
| `/blog.html` | `/blog` |
| `/consultation.html` | `/consultation` |
| ...and 54 more, one per page | same pattern |

Full list is in `_redirects` at the repo root (generated, not hand-maintained
— regenerate it if new top-level `.html` files are added).

No other redirects were added or changed.

---

## 3. Before / after

| Metric | Before | After |
|---|---|---|
| Homepage (`/`) weight | 928 KB | 74 KB |
| `/index-de` weight | 927 KB | 73 KB |
| `blog.html` weight | 1,521 KB | 58 KB |
| Largest single page | ~1,521 KB (`blog.html`) | 76 KB (`index.html`) |
| Pages with valid JSON-LD | 4 of 21 checked | 58 of 58 |
| Pages with zero JSON-LD | 17 | 0 |
| Invalid/unparsable JSON-LD blocks | 2 (the GSC-flagged parse error) | 0 |
| `.html` URLs returning 200 instead of 301 | 58 | 0 |
| Sitemap duplicate URLs | 2 (`/tools`, `/tools-de`) | 0 |
| Sitemap `.html` entries | 0 | 0 (unchanged, already clean) |
| Heading whitespace/concatenation bugs | 4 confirmed, unknown total | 0 (184 found and fixed) |
| Titles over 60 chars (12 flagged pages) | up to 73 | all rewritten to 44-60 |
| Descriptions over 160 chars (12 flagged pages) | up to 244 | all rewritten to 137-163 |
| Pages with `robots` meta tag | 0 | 58 |
| hreflang tag count per page | 3-6, often duplicated | exactly 3, always |
| `x-default` pointing at German (Swiss-intent pages) | 0 | 23 |
| `lang="de"` vs `lang="de-CH"` | 26 pages said `de` | 0 (all `de-CH`) |
| Orphan sitemap pages (no inbound link) | not measured pre-session | 0 |
| Pages with visible breadcrumbs | 0 | 12 (trip reports) |

Lighthouse before/after scores were not captured — no Lighthouse/CI
tooling exists in this environment and installing one was out of scope
given the "no new toolchain" decision. The page-weight numbers above are
measured directly (`curl` + byte count against the live site), which is
the input Lighthouse's performance score is most sensitive to for a
static site like this.

---

## 4. `TODO(owner)` placeholders

**None.** No new factual claims — bonus amounts, fees, transfer ratios,
dates — were introduced anywhere this session. Every number that appears
in new or changed copy was already published on the page it came from
(e.g. the CHF 79 consultation price, reused verbatim into the new Service
schema). Phase 7's new pages, which *would* have needed several, were not
built — see below.

---

## 5. What wasn't done, and why

1. **Phase 7 (6 new pages)** — not built. Two of the target queries
   (`nachträgliche Meilengutschrift`, `Bundle & Go`) need real,
   currently-accurate policy detail (claim windows, processing times,
   exact Bundle & Go pricing) that isn't published anywhere on this site
   for me to draw from — writing them would mean either fabricating
   numbers (explicitly prohibited) or shipping pages that are mostly
   `TODO(owner)` placeholders, which isn't a real page. Instead, here's
   what's needed to build each one for real:

   | Page | Target query | What's needed from you |
   |---|---|---|
   | `/nachtraegliche-meilengutschrift-miles-and-more` | breakout | Claim window (days), required documents, typical processing time, what happens on rejection |
   | `/bundle-and-go-miles-and-more-schweiz` | breakout | Current Bundle & Go pricing tiers/cost-per-mile |
   | `/miles-and-more-kreditkarte-schweiz` | +350% | None — this can be built from content already on `/beste-kreditkarte-meilen-schweiz`, mostly a hub-page restructure |
   | `/meilenrechner` (dedicated landing) | high-intent, low-CTR on `/tools-de` | None — restructuring `/tools-de` around the calculator as primary H1 is a design/copy task, not a facts one |
   | `/marriott-bonvoy-punkte-meilen-schweiz` | +300% | Current Bonvoy→Miles&More / Bonvoy→Flying Blue transfer ratios |
   | `/milesandmore-login-hilfe` | +300%, navigational | Marked optional/low-priority in the plan itself — recommend skipping |

   Once you have the facts for the first two and the transfer ratio for
   the fifth, these are straightforward to write — happy to do it in a
   follow-up session.

2. **Breadcrumbs/related-links on the other 46 pages** — done for the 12
   trip reports (most template-uniform, clearest win). The remaining
   pages span 8 different templates; a good version of this is a real
   piece of work, not a quick follow-on to what's already built.

3. **Lighthouse CI / GitHub Actions** — per your call, skipped in favour
   of the standalone Python script. If you want automated enforcement on
   every push later, this is the natural next step, but it's a real
   infrastructure addition (dependencies, CI minutes) to a repo that's
   deliberately had none.

4. **Language migration (Phase 4d)** — deliberately deferred, exactly as
   the plan itself instructed. Full proposal is in
   `docs/language-migration-proposal.md`. Recommendation: wait for a full
   crawl cycle (4-8 weeks) after this session's fixes before deciding
   whether it's still needed.

---

## 6. Search Console follow-up checklist

- [ ] Resubmit `https://meilenguru.ch/sitemap.xml` in Search Console
      (regenerated with hreflang alternates and clean lastmod dates)
- [ ] **Wait until this deploy is confirmed live** before clicking any
      Validate Fix button — a failed validation triggers a cooldown
- [ ] Run **Validate Fix** on:
  - Unparsable structured data (the parse error — fixed in Phase 3)
  - Alternative page with proper canonical tag (18 URLs — fixed in Phase 1)
  - Duplicate without user-selected canonical (1 URL — fixed in Phase 1)
  - Crawled – currently not indexed (6 URLs — content/schema/hreflang all
    touched across Phases 3-6; can't force reindexing, only remove the
    reasons Google had to skip them)
- [ ] Re-inspect the six URLs that already had indexing requested
      manually
- [ ] Check the Core Web Vitals report in ~4 weeks once there's enough
      field data — the homepage alone went from 928KB to 74KB, this
      should move LCP substantially
- [ ] **Begin genuine link acquisition.** Zero external backlinks is the
      biggest remaining ceiling on this site, and nothing in this session
      fixes that — it's not a code problem. Realistic angles: Swiss
      personal-finance forums/communities, Swiss travel blogs, offering
      to be a source for Swiss consumer-finance journalists, and your
      existing Instagram/TikTok/Facebook audiences. Not attempted here —
      outreach and account activity are yours to run, not something to
      automate.

---

## 7. How to verify any of this yourself

```bash
python3 scripts/seo_check.py                              # local checks
python3 scripts/seo_check.py --base-url https://meilenguru.ch  # + live status codes
curl -sI https://meilenguru.ch/about.html                 # should be 301 -> /about
curl -sI https://meilenguru.ch/about                      # should be 200
```
