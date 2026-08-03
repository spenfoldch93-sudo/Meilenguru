# Weekly Audit Diagnosis — August 2026

## What was missed and why

The July 29 automated audit logged "all other figures checked out" while multiple stale figures and two active referral codes remained across the site. This document explains why.

---

## Root cause: the audit only reads two files

The prompt (`~/.claude/referral-audit-prompt.md`) instructs the audit to:

> Step 2 — Read referrals.html and empfehlungen.html [only these two files]

The referral codes and stale bonus figures that needed cleaning were spread across **six additional files**:

| File | What was stale |
|------|---------------|
| `meilenguru-strategy-best-swiss-credit-cards-miles.html` | Amex referral-box (FA5DFTFMC), Alpian fee row, Alpian references in FAQ/picker |
| `beste-kreditkarte-meilen-schweiz.html` | Same in German + comparison table |
| `meilenguru-strategy-100k-miles-without-flying.html` | M&M referral-box (FM1GZ454U), Amex referral-box, Alpian intro, stale running totals |
| `meilen-sammeln-ohne-fliegen-schweiz.html` | Same in German |
| `meilenguru-miles-and-more-credit-card-switzerland.html` | "Enter referral code FM1GZ454U" hint |
| `miles-and-more-kreditkarte-schweiz.html` | Same in German |

The audit never looked at any of these files.

---

## Secondary issue: Alpian mis-reported as "still active"

The July 29 log says the Alpian Amex Platinum offer was "still active." The audit fetches `alpian.com/bank/american-express` (Step 1, item 6), but the Amex card was removed from Alpian's product range. The page at that URL either no longer exists or no longer references the card. The audit appears to have interpreted a non-error response as confirmation of activity rather than checking for the actual card details.

---

## What the audit currently does well

- Catches figure changes on `referrals.html` and `empfehlungen.html` promptly (it caught the 75k summer promo expiry on July 29)
- Commits and pushes without human intervention
- Notifies via macOS notification on success/failure

---

## Options to consider (do not act until reviewed)

**Option A — Expand the file list in the prompt**  
Add the six article files to Step 2 so the audit checks them too. Low effort. Risk: longer runs, more tokens per audit.

**Option B — Centralise figures in one place**  
Keep all bonus figures in a single "source of truth" include/snippet, and have articles reference it. Eliminates drift entirely, but requires a build step (the site is currently pure static HTML).

**Option C — Periodic manual sweep**  
Keep the automated audit scoped to the referrals pages (its sweet spot) and do a manual quarterly sweep of the article files. The article files change less frequently and have fewer time-sensitive figures.

**Recommendation:** Option A is the lowest-friction fix. Append the six file paths to Step 2 of `~/.claude/referral-audit-prompt.md` and add a note about what to check in each (figures, not prose).
