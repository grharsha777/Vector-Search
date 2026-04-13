#!/usr/bin/env python3
"""Patch files in repo to replace hardcoded API keys with env lookups.
Usage: python scripts/fix_notebook_secrets.py /path/to/repo
"""
import re
import sys
from pathlib import Path

PATTERNS = [
    re.compile(r"GEMINI_API_KEY\s*=\s*[\"'][^\"']+[\"']"),
    re.compile(r"OPENAI_API_KEY\s*=\s*[\"'][^\"']+[\"']"),
    re.compile(r"PINECONE_API_KEY\s*=\s*[\"'][^\"']+[\"']"),
    re.compile(r"AIza[0-9A-Za-z\-_]{35}")
]

REPLACEMENT = {
    'GEMINI_API_KEY': "GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')",
    'OPENAI_API_KEY': "OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')",
    'PINECONE_API_KEY': "PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')",
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: fix_notebook_secrets.py /path/to/repo')
        sys.exit(1)
    root = Path(sys.argv[1])
    if not root.exists():
        print('Path not found:', root)
        sys.exit(1)

    for p in root.rglob('*.py'):
        text = p.read_text(encoding='utf-8')
        new = text
        for pat in PATTERNS:
            new = pat.sub(lambda m: "# SECRET REMOVED - LOAD FROM ENV", new)
        if new != text:
            p.write_text(new, encoding='utf-8')
            print('Patched', p)
    print('Done')
