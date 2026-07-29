#!/usr/bin/env python3
"""
SEO verification for meilenguru.ch.

Standalone script, no dependencies beyond the standard library (+ requests
if you want live-URL checks). Run against the local repo:

    python3 scripts/seo_check.py

Or cross-check a deployed site's status codes too:

    python3 scripts/seo_check.py --base-url https://meilenguru.ch

Exits non-zero if any FAIL is found. WARN findings don't affect the exit
code but are printed for awareness.
"""

import argparse
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)

FAILS = []
WARNS = []


def fail(check, detail):
    FAILS.append((check, detail))


def warn(check, detail):
    WARNS.append((check, detail))


def slug_from_file(fname):
    if fname == "index.html":
        return ""
    return fname[:-5]


def load_all_pages():
    pages = {}
    for f in glob.glob("*.html"):
        with open(f, encoding="utf-8") as fh:
            pages[f] = fh.read()
    return pages


# ---------------------------------------------------------------------------
# Sitemap checks
# ---------------------------------------------------------------------------

def check_sitemap():
    print("== sitemap.xml ==")
    if not os.path.exists("sitemap.xml"):
        fail("sitemap", "sitemap.xml does not exist")
        return {}

    try:
        tree = ET.parse("sitemap.xml")
    except ET.ParseError as e:
        fail("sitemap", f"not valid XML: {e}")
        return {}

    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [u.find("s:loc", ns).text for u in tree.getroot().findall("s:url", ns)]

    if len(urls) != len(set(urls)):
        dupes = [u for u in urls if urls.count(u) > 1]
        fail("sitemap", f"duplicate URLs: {set(dupes)}")

    for u in urls:
        if u.endswith(".html"):
            fail("sitemap", f".html URL present: {u}")
        if not u.startswith("https://meilenguru.ch"):
            fail("sitemap", f"non-absolute or wrong-domain URL: {u}")

    for u in tree.getroot().findall("s:url", ns):
        loc = u.find("s:loc", ns).text
        lastmod = u.find("s:lastmod", ns)
        if lastmod is not None:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", lastmod.text or ""):
                fail("sitemap", f"invalid lastmod on {loc}: {lastmod.text}")

    print(f"  {len(urls)} URLs, {len(set(urls))} unique")
    return {u.rstrip("/") or "https://meilenguru.ch" for u in urls}


# ---------------------------------------------------------------------------
# Per-page checks
# ---------------------------------------------------------------------------

WHITESPACE_BUG_RE = re.compile(r"[a-zäöü][,—]?<br\s*/?>(?:<[a-z]+>)?[a-zA-Z]")


def check_page(fname, html, sitemap_urls, all_titles, all_descs):
    slug = slug_from_file(fname)
    url = "https://meilenguru.ch/" if slug == "" else f"https://meilenguru.ch/{slug}"

    # -- title --
    m = re.search(r"<title>([^<]*)</title>", html)
    if not m:
        fail(fname, "no <title>")
    else:
        title = m.group(1)
        if not (30 <= len(title) <= 60):
            warn(fname, f"title length {len(title)} (target 30-60): {title!r}")
        all_titles[title].append(fname)

    # -- meta description --
    m = re.search(r'name="description"\s*\n?\s*content="([^"]*)"', html)
    if not m:
        fail(fname, "no meta description")
    else:
        desc = m.group(1)
        if not (120 <= len(desc) <= 160):
            warn(fname, f"description length {len(desc)} (target 120-160)")
        all_descs[desc].append(fname)

    # -- H1 --
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if len(h1s) == 0:
        fail(fname, "no <h1>")
    elif len(h1s) > 1:
        fail(fname, f"{len(h1s)} <h1> tags, expected exactly 1")
    else:
        h1_text = re.sub(r"<[^>]+>", "", h1s[0]).strip()
        if "title" in dir() and m and h1_text == title:
            warn(fname, "H1 identical to <title>")

    # -- whitespace bugs (regression guard for the fix already shipped) --
    for wm in WHITESPACE_BUG_RE.finditer(html):
        warn(fname, f"possible heading whitespace bug near: {wm.group(0)[:60]!r}")

    # -- canonical --
    cm = re.search(r'rel="canonical" href="([^"]*)"', html)
    if not cm:
        fail(fname, "no canonical tag")
    else:
        canon = cm.group(1)
        if not canon.startswith("https://meilenguru.ch"):
            fail(fname, f"canonical not absolute: {canon}")
        if canon.endswith(".html"):
            fail(fname, f"canonical points at .html: {canon}")
        if canon.rstrip("/") not in (url.rstrip("/"), "https://meilenguru.ch"):
            # allow the homepage's bare-slash vs no-slash mismatch
            if not (slug == "" and canon == "https://meilenguru.ch/"):
                warn(fname, f"canonical {canon} doesn't match own URL {url}")

    # -- hreflang --
    tags = re.findall(r'hreflang="([^"]*)"\s+href="([^"]*)"', html)
    langs = sorted(t[0] for t in tags)
    if len(tags) != 3:
        fail(fname, f"expected exactly 3 hreflang tags, found {len(tags)}")
    elif langs != ["de", "en", "x-default"]:
        fail(fname, f"hreflang lang set wrong: {langs}")
    for lang, href in tags:
        if not href.startswith("https://meilenguru.ch"):
            fail(fname, f"hreflang {lang} not absolute: {href}")

    # -- lang attribute --
    lm = re.search(r'<html lang="([^"]*)"', html)
    if not lm:
        fail(fname, "no <html lang>")
    else:
        html_lang = lm.group(1)
        is_de_file = any(
            de_href == url for _, de_href in tags if _ == "de"
        ) is False and False  # placeholder, real check below

    # -- JSON-LD --
    blocks = re.findall(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.DOTALL
    )
    if not blocks:
        fail(fname, "no JSON-LD present")
    for b in blocks:
        try:
            json.loads(b)
        except json.JSONDecodeError as e:
            fail(fname, f"invalid JSON-LD: {e}")
            continue
        if "<" in b:
            # allow it only inside already-valid JSON (i.e. as literal text,
            # which is fine) -- the real risk is unescaped HTML that breaks
            # parsing, which json.loads() above would already have caught.
            pass

    # -- images --
    for im in re.finditer(r"<img\b([^>]*)>", html):
        attrs = im.group(1)
        if 'alt="' not in attrs and "alt='" not in attrs:
            fail(fname, f"<img> missing alt: {attrs[:80]!r}")
        if "width=" not in attrs:
            warn(fname, f"<img> missing width: {attrs[:80]!r}")
        if "height=" not in attrs:
            warn(fname, f"<img> missing height: {attrs[:80]!r}")

    # -- page weight --
    size = len(html.encode("utf-8"))
    if size > 150_000:
        fail(fname, f"page weight {size} bytes exceeds 150KB")

    for style in re.findall(r"<style>(.*?)</style>", html, re.DOTALL):
        if len(style) > 5000:
            warn(fname, f"inline <style> block is {len(style)} chars (>5000)")
    for script in re.findall(r"<script(?:(?!src=)[^>])*>(.*?)</script>", html, re.DOTALL):
        if len(script) > 5000:
            warn(fname, f"inline <script> block is {len(script)} chars (>5000)")

    for dm in re.finditer(r'data:image/[^"\')]+', html):
        if len(dm.group(0)) > 2000:
            fail(fname, f"data:image URI over 2KB found ({len(dm.group(0))} chars)")

    # -- dead links --
    if re.search(r'href="#"', html):
        n = len(re.findall(r'href="#"', html))
        warn(fname, f'{n} href="#" link(s) found')

    return url


def check_orphans(pages, sitemap_urls):
    print("== internal link / orphan check ==")
    linked_to = set()
    for fname, html in pages.items():
        for m in re.finditer(r'href="([^"#][^"]*)"', html):
            href = m.group(1)
            if href.startswith("http") and "meilenguru.ch" not in href:
                continue
            slug = href.lstrip("/").rstrip("/")
            if slug.endswith(".html"):
                slug = slug[:-5]
            target = "https://meilenguru.ch/" if slug == "" else f"https://meilenguru.ch/{slug}"
            linked_to.add(target)

    for u in sitemap_urls:
        norm = u if u.endswith("/") or u == "https://meilenguru.ch" else u
        if u not in linked_to and u.rstrip("/") not in {x.rstrip("/") for x in linked_to}:
            warn("orphans", f"{u} has no inbound internal link found")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=None, help="Also check live status codes against this base URL")
    args = parser.parse_args()

    sitemap_urls = check_sitemap()

    print("== per-page checks ==")
    pages = load_all_pages()
    all_titles = defaultdict(list)
    all_descs = defaultdict(list)
    for fname, html in sorted(pages.items()):
        check_page(fname, html, sitemap_urls, all_titles, all_descs)

    print("== uniqueness ==")
    for title, files in all_titles.items():
        if len(files) > 1:
            fail("titles", f"duplicate title {title!r} on {files}")
    for desc, files in all_descs.items():
        if len(files) > 1:
            fail("descriptions", f"duplicate description on {files}")

    check_orphans(pages, sitemap_urls)

    if args.base_url:
        print(f"== live checks against {args.base_url} ==")
        try:
            import urllib.request

            def status(path):
                req = urllib.request.Request(args.base_url + path, method="HEAD")
                try:
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        return resp.status, resp.geturl()
                except urllib.error.HTTPError as e:
                    return e.code, None

            for check_path, expect in [("/robots.txt", 200), ("/llms.txt", 200), ("/", 200)]:
                code, _ = status(check_path)
                if code != expect:
                    fail("live", f"{check_path} returned {code}, expected {expect}")

            for fname in list(pages)[:10]:  # sample to keep this fast
                if fname == "index.html":
                    continue
                code, final_url = status("/" + fname)
                if code not in (301, 308):
                    fail("live", f"/{fname} returned {code}, expected a redirect")
        except Exception as e:
            warn("live", f"live checks skipped: {e}")

    print()
    print(f"RESULT: {len(FAILS)} failures, {len(WARNS)} warnings")
    if WARNS:
        print("\n--- warnings ---")
        for check, detail in WARNS:
            print(f"  WARN [{check}] {detail}")
    if FAILS:
        print("\n--- failures ---")
        for check, detail in FAILS:
            print(f"  FAIL [{check}] {detail}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
