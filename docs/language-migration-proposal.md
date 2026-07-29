# Proposal: make German the default language at `/`

**Status: not implemented. For owner review only.**

## Why this is being proposed

Search Console data (last 3 months, `sc-domain:meilenguru.ch`):

- Switzerland accounts for 2,451 of 4,570 impressions (54%) and 44 of 55 clicks (80%).
- Searches driving those impressions are overwhelmingly German-language
  (`willkommensbonus schweiz`, `kreditkarten bonusprogramm`, `meilen sammeln schweiz`,
  `miles and more credit card swiss`, etc.).
- Google's own index currently favours English pages: a `site:meilenguru.ch` check
  surfaces only 4 pages, all English, zero German — despite German pages having
  comparable or better content in several cases.
- Yet the site defaults to English at `/`, `<html lang="en">`, and every hub/nav
  structure treats English as primary and German as the "translated" variant
  (`/index-de`, `/blog-de`, `/tools-de`, etc.).

The traffic and intent data both point the same direction: the audience is
Swiss and searches in German, but the site's information architecture is
English-first. That's a structural mismatch, not a content problem.

## What the migration would involve

This is a URL migration, which Google Search Central treats as one of the
highest-risk categories of SEO change — it can cause a temporary (sometimes
multi-week) ranking and traffic dip even when done correctly, because every
indexed URL's signals have to be reconsolidated onto a new URL.

### 1. New URL structure

Move German pages to root and English pages to a `/en/` prefix (or similar):

| Current | Proposed |
|---|---|
| `/` (English) | `/en/` |
| `/index-de` | `/` |
| `/strategies` | `/en/strategies` |
| `/strategien` | `/strategien` |
| `/beste-kreditkarte-meilen-schweiz` | `/beste-kreditkarte-meilen-schweiz` (unchanged) |
| `/meilenguru-strategy-best-swiss-credit-cards-miles` | `/en/best-swiss-credit-cards-miles` |
| ...all 29 pairs, same pattern | |

The English-slug pages that currently have no clean short slug
(`meilenguru-strategy-*`, `meilenguru-blog-*`) would also need shortening while
we're touching their URLs — leaving them as-is under `/en/` would just carry
the same awkward naming forward.

### 2. Redirect map

All 29 current URLs (58 with both languages) need 301s to their new location.
Given the `.html` redirect work in Phase 1 already proved that Netlify's
`netlify.toml` splat redirects don't reliably fire, this would need to be 58
explicit `_redirects` rules, verified individually post-deploy — same approach
as Phase 1, just a second full pass.

### 3. hreflang and sitemap

Every hreflang pair and sitemap entry from Phase 4 would need regenerating
against the new URLs. Mechanically straightforward once the redirect map
exists, since the pair-map script from Phase 4 already exists and just needs
new slugs fed in.

### 4. Internal links

Every internal link site-wide (247 at last count) currently points at the
current URLs. All of them would need updating in the same change, or the
site would round-trip through redirects on almost every click — workable,
but doubles down on the "reclaim crawl budget" work from Phase 1c only to
reintroduce a redirect on every internal link.

### 5. External references

- Google Search Console property and any saved reports reference current URLs.
- Anything already linking to the site externally (currently: nothing, per
  the 0-backlink finding — this is the one silver lining that makes this
  migration lower-risk than it would be for a site with real backlink equity).
- Any bookmarks, saved links, or the referral-partner codes on `/referrals`
  and `/empfehlungen` that might be shared externally.
- Social media bios/posts (Instagram, TikTok, Facebook) if they link directly
  to specific pages rather than just the domain.

## Risk assessment

**Risk: Medium-High, reward: Uncertain but plausibly significant.**

- The GSC data suggests Google is already somewhat confused about which
  version of this site is canonical (only 4 pages indexed at all, all
  English, despite German being the higher-intent language) — a clean
  migration *might* resolve that confusion in German's favour. But it might
  also just reset the indexing clock and cost weeks of crawl budget while
  Google re-evaluates.
- This site has zero backlinks and a short indexing history (first pages
  seen mid-May 2026), which lowers the downside — there's little existing
  authority to lose — but it also means there's no signal yet to prove the
  current structure isn't just still "warming up."
- The alternative already implemented in this pass (Phases 1–4: fixing the
  `.html` duplication, adding the missing schema, correcting hreflang so
  `x-default` points to German for Swiss-intent pages) addresses the same
  underlying signal-confusion problem without touching a single URL. It's
  reasonable to let that settle for a full crawl cycle (Search Console
  reporting suggests 4–8 weeks for a site this size) before deciding whether
  a full URL migration is still worth the risk.

## Recommendation

**Do not migrate now.** Ship Phases 1–4 as they stand, resubmit the sitemap,
and revisit this proposal after a full reporting cycle once there's data on
whether the non-destructive fixes moved the needle. If German pages are still
absent from Google's index after that, this migration becomes a much
stronger case — supported by evidence that the softer fix wasn't enough,
rather than a guess made without it.

If and when this does move forward, it should be its own isolated piece of
work with a rollback plan, not bundled with anything else.
