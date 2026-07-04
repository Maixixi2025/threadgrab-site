#!/usr/bin/env python3
"""
threadgrab 3-lang article builder for shadowbroker-mcp-osint-social-creators-2026
Generated: 2026-07-03
Topic: Daily briefing 2026-07-03 ⭐ #1 (threadgrab) - Shadowbroker MCP OSINT dashboard
Archetype: news-hook (platform/protocol change with concrete creator action)
"""
import json, os, re, hashlib
from datetime import date

SLUG = "shadowbroker-mcp-osint-social-creators-2026"
DATE = "2026-07-03"
SITE = "/root/threadgrab-site"

# Source files (already written)
EN_FILE = f"{SITE}/en/blog/{SLUG}.html"
PT_FILE = f"{SITE}/pt/blog/{SLUG}.html"
ID_FILE = f"{SITE}/id/blog/{SLUG}.html"

# Verify code block identity
print("=== Code block identity check ===")
hashes = {}
for lang, path in [('en', EN_FILE), ('pt', PT_FILE), ('id', ID_FILE)]:
    with open(path) as f:
        html = f.read()
    blocks = re.findall(r'<pre><code>(.*?)</code></pre>', html, re.DOTALL)
    hashes[lang] = [hashlib.md5(b.encode()).hexdigest()[:8] for b in blocks]
    print(f"  {lang}: {len(blocks)} blocks, hashes: {hashes[lang]}")

en_h = hashes['en']
if all(hashes[l] == en_h for l in ['pt', 'id']):
    print("  ✅ All 3 langs byte-identical")
else:
    print("  ❌ Mismatch detected")
    raise SystemExit(1)

# Verify verifier passes
import subprocess
r = subprocess.run(
    ['python3', '/root/.hermes/skills/ilang-content/scripts/threadgrab-3lang-verify.py', SITE, SLUG],
    capture_output=True, text=True, timeout=30
)
print(f"\n=== Verifier: exit {r.returncode} ===")
print(r.stdout)
if r.returncode != 0:
    print("❌ Verifier failed")
    raise SystemExit(1)
print("✅ ALL CHECKS PASSED")
