# Page Update — Full Content Audit & Sync

You are doing a full content audit of meilenguru.ch. Your job is to check whether card-specific data shown across the site is still accurate, update any pages that are wrong, commit and push all changes, then report what changed.

Work through the steps below in order.

---

## Step 1 — Fetch current data from issuer websites

Use WebFetch on each URL. If a page is JavaScript-heavy and returns little useful content, fall back to WebSearch (e.g. "Cornèrcard Miles More Platinum annual fee 2026") and use the most credible recent result.

Extract for each card:
- Welcome bonus (miles / MR points / CHF value)
- Annual fee (first year if discounted separately)
- Earn rate (miles or points per CHF spent)
- Any active promotional offer with expiry date
- Any discontinued offer that may still appear on the site

**Cards to check:**

1. **Cornèrcard M&M Platinum + Diners** — https://www.cornercard.ch/en/credit-cards/cornercard-miles-more-kombi-angebot-platinum/
2. **Cornèrcard M&M Gold + Diners** — https://www.cornercard.ch/en/credit-cards/cornercard-miles-more-kombi-angebot-gold/
3. **Cornèrcard M&M Classic + Diners** — https://www.cornercard.ch/en/credit-cards/cornercard-miles-more-kombi-angebot/
4. **Amex Platinum (Swisscard)** — https://www.americanexpress.ch/en/cards/private-customers-cards/platinum-card
5. **Amex Gold (Swisscard)** — https://www.americanexpress.ch/en/cards/private-customers-cards/gold-card
6. **SWISS M&M Platinum Duo (Swisscard)** — https://www.miles-and-more-cards.ch/en/private-customers/credit-cards/platinum
7. **Alpian Amex Platinum** — https://www.alpian.com/bank/american-express
8. **Revolut Metal/Premium transfer partners** — WebSearch for "Revolut transfer partners Flying Blue Miles More 2026" to confirm transfer ratios are still 1:1

Compile a clean data table before moving to Step 2. Do not start comparing until you have fetched all sources.

---

## Step 2 — Read the site HTML files

Read these files and note every card-specific data point (bonus numbers, fees, earn rates, expiry text, badge classes):

**Primary (referral + promo pages) — highest priority:**
- `/Users/sampenfold/Desktop/meilenguru/referrals.html`
- `/Users/sampenfold/Desktop/meilenguru/empfehlungen.html`

**Strategy / comparison pages — check card stats blocks:**
- `/Users/sampenfold/Desktop/meilenguru/meilenguru-strategy-best-swiss-credit-cards-miles.html`
- `/Users/sampenfold/Desktop/meilenguru/beste-kreditkarte-meilen-schweiz.html`
- `/Users/sampenfold/Desktop/meilenguru/meilenguru-revolut-amex-miles.html`
- `/Users/sampenfold/Desktop/meilenguru/revolut-amex-meilen-schweiz.html`
- `/Users/sampenfold/Desktop/meilenguru/meilenguru-business-miles-switzerland.html`
- `/Users/sampenfold/Desktop/meilenguru/business-meilen-schweiz.html`
- `/Users/sampenfold/Desktop/meilenguru/meilenguru-grenzgaenger-miles.html`
- `/Users/sampenfold/Desktop/meilenguru/grenzgaenger-meilen-schweiz.html`

**Also scan these for any card data that may have drifted:**
- `/Users/sampenfold/Desktop/meilenguru/strategies-amex.html`
- `/Users/sampenfold/Desktop/meilenguru/strategien-amex.html`
- `/Users/sampenfold/Desktop/meilenguru/strategies-miles-more.html`
- `/Users/sampenfold/Desktop/meilenguru/strategien-miles-more.html`
- `/Users/sampenfold/Desktop/meilenguru/strategies.html`
- `/Users/sampenfold/Desktop/meilenguru/strategien.html`
- `/Users/sampenfold/Desktop/meilenguru/index.html`
- `/Users/sampenfold/Desktop/meilenguru/index-de.html`

---

## Step 3 — Compare and flag discrepancies

For every piece of card data found in Step 2, compare it against the issuer data from Step 1. Flag:

- **Wrong numbers** — bonus, fee, earn rate no longer matches issuer
- **Expired promos** — shown as active but no longer on issuer page
- **New promos** — available on issuer page but not reflected on site
- **Stale expiry dates** — date shown has passed
- **DE/EN sync issues** — English and German pages show different data for the same card

Group flags by page so you know exactly what to edit.

---

## Step 4 — Update all affected files

Edit every file where data is wrong. Rules:

- Keep the existing HTML structure — update numbers, descriptions, badge classes, expiry text only
- **German pages** use Swiss number formatting: apostrophe thousands separator (40'000 not 40,000), German card names and labels
- **Badge classes**: `badge-hot` = active promo, `badge-exp` = expiring soon, `badge-std` = standard offer; `promo-card hot` = highlighted, `promo-card plain` = standard
- Always update BOTH the English and German versions of any page
- If a promo has expired and there is no replacement, remove the promo block rather than leaving stale content
- Update the `<lastmod>` date in `sitemap.xml` for every file you edit (use today's date: 2026-05-31)

If everything is accurate, skip this step.

---

## Step 5 — Commit and push if changes were made

Stage only the files you actually edited:

```bash
cd /Users/sampenfold/Desktop/meilenguru
git add <list of changed files> sitemap.xml
git commit -m "Page update: sync card offer data with issuer sources [auto]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin main
```

---

## Step 6 — Report

Print a concise summary:

```
## Page update complete — <date>

### Sources checked
- Cornèrcard Platinum: [what you found]
- Cornèrcard Gold: ...
- Amex Platinum: ...
- Amex Gold: ...
- SWISS M&M Platinum: ...
- Alpian Amex Platinum: ...
- Revolut transfer ratios: ...

### Changes made
- referrals.html: [what changed]
- beste-kreditkarte-meilen-schweiz.html: [what changed]
- ... (or "No changes needed — all data accurate")

### Pushed to GitHub
[commit hash or "No commit (nothing changed)"]
```
