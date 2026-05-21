# Meilenguru

A static HTML website for Swiss-based frequent flyer mile earning and redemption advice. The site targets Swiss residents who want to accumulate Miles & More and Flying Blue miles from everyday CHF spending in order to book business/first class flights. It is deployed on Netlify at **meilenguru.ch**.

## What the site covers

- Strategies for earning miles via Swiss credit cards (Amex, etc.) and partner programmes
- Flying Blue and Miles & More programme guides
- Real trip reports (blog posts) showing award redemptions
- A paid 30-minute consultation offering (CHF 79)
- Referral links and tools pages

## File structure

All files live flat in the project root — there are no subdirectories beyond `.git`.

### Pages

| File | Purpose |
|------|---------|
| `index.html` | Homepage — overview, hero, value proposition |
| `blog.html` | Blog index listing all trip reports and strategy articles |
| `strategies.html` | Overview of earning strategies |
| `strategies-flying-blue.html` | Flying Blue-specific strategy guide |
| `strategies-miles-more.html` | Miles & More-specific strategy guide |
| `strategies-amex.html` | American Express earning strategy |
| `strategies-benchmark.html` | Benchmark / comparison page |
| `about.html` | About page |
| `consultation.html` | Consultation booking page |
| `referrals.html` | Referral links page |
| `tools.html` | Tools and calculators page |

### Blog / article pages

| File | Topic |
|------|-------|
| `meilenguru-blog-perth-singapore-zurich-sq-swiss.html` | Trip report: Perth → Singapore → Zurich on SQ (Swiss miles) |
| `meilenguru-blog-perth-zurich-oman-air.html` | Trip report: Perth → Zurich on Oman Air |
| `meilenguru-blog-singapore-zurich-sq346.html` | Trip report: Singapore → Zurich on SQ346 |
| `meilenguru-blog-singapore-amsterdam-klm.html` | Trip report: Singapore → Amsterdam on KLM |
| `meilenguru-blog-zurich-cancun-tap.html` | Trip report: Zurich → Cancun on TAP |
| `meilenguru-blog-lh-first-class-sin-bsl.html` | Trip report: Lufthansa First Class Singapore → Basel |
| `meilenguru-strategy-flying-blue-promo-awards.html` | Strategy: Flying Blue promo awards |
| `meilenguru-strategy-100k-miles-without-flying.html` | Strategy: earning 100k miles without flying |
| `meilenguru-strategy-best-swiss-credit-cards-miles.html` | Strategy: best Swiss credit cards for miles |
| `meilenguru-flying-blue-promo-may-2026.html` | Flying Blue May 2026 promo awards |
| `meilen-sammeln-ohne-fliegen-schweiz.html` | DE: earning miles without flying (Switzerland) |
| `flying-blue-promo-awards-schweiz.html` | DE: Flying Blue promo awards (Switzerland) |
| `beste-kreditkarte-meilen-schweiz.html` | DE: best credit cards for miles (Switzerland) |

### Assets

| File | Purpose |
|------|---------|
| `logo-fb.png` | Flying Blue logo |
| `logo-mm.png` | Miles & More logo |
| `logo-amex.png` | American Express logo |
| `logo_flyingblue-RVB_couleur_1.png` | Flying Blue full colour logo |
| `Miles-More-Logo-500x281.png` | Miles & More banner logo |
| `Miles_&_More_Lufthansa_Logo.svg.png` | Lufthansa / M&M combined logo |
| `American Express.png` | Amex card image |
| `Flying-Blue-1024x538-18.jpg` | Flying Blue hero image |
| `Oman_Air.jpeg` | Oman Air cabin photo |
| `Oman_Air_Food.jpeg` | Oman Air food photo |
| `Thai_Business.jpeg` | Thai Airways business class photo |
| `pexels-davegarcia-32641818.jpg` | Stock travel photo |

### Config / meta

| File | Purpose |
|------|---------|
| `netlify.toml` | Netlify deployment config — redirects netlify.app → meilenguru.ch, sets security headers |
| `sitemap.xml` | XML sitemap for search engines |

## Tech stack

Pure static HTML/CSS — no build step, no framework, no JavaScript bundler. Styles are written inline inside `<style>` tags in each HTML file. Fonts are loaded from Google Fonts (Cormorant Garamond + DM Sans).

## Design system

Defined as CSS custom properties at the top of each page:

| Variable | Value |
|----------|-------|
| `--black` | `#0a0a0a` |
| `--white` | `#faf9f7` |
| `--warm-white` | `#f5f3ef` |
| `--gold` | `#b8962e` |
| `--gold-light` | `#d4ae4e` |
| `--muted` | `#888580` |
| `--font-display` | Cormorant Garamond (serif) |
| `--font-body` | DM Sans (sans-serif) |

## Deployment

The site is hosted on **Netlify**. Pushes to the `main` branch on GitHub trigger an automatic deploy. No build command is needed — Netlify serves the files directly.

## Workflow

After making any changes, commit and push to GitHub so the site deploys automatically:

```bash
git add <changed-files>
git commit -m "description of change"
git push origin main
```
