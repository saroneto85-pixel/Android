#!/usr/bin/env python3
"""Configure stable official Maven repositories plus a Maven Central fallback."""
from pathlib import Path

root = Path("android")
targets = [
    root / "build.gradle",
    root / "settings.gradle",
    root / "build.gradle.kts",
    root / "settings.gradle.kts",
]

def add_repo(text: str, token: str, repo: str, kotlin: bool) -> str:
    if repo in text:
        return text
    if kotlin:
        addition = f'maven {{ url = uri("{repo}") }}' + "\n        " + token
    else:
        addition = f"maven {{ url '{repo}' }}" + "\n        " + token
    return text.replace(token, addition)

found = False
for path in targets:
    if not path.exists():
        continue
    found = True
    text = path.read_text()
    # Remove Aliyun mirrors: the previous Actions run showed HTTP 502.
    text = text.replace(
        'maven { url "https://maven.aliyun.com/repository/central" }', ""
    ).replace(
        "maven { url 'https://maven.aliyun.com/repository/central' }", ""
    ).replace(
        'maven { url "https://maven.aliyun.com/repository/google" }', ""
    ).replace(
        "maven { url 'https://maven.aliyun.com/repository/google' }", ""
    )
    # Keep official Google Maven and Maven Central; repo1 is a Central fallback.
    text = add_repo(
        text, "mavenCentral()", "https://repo1.maven.org/maven2/",
        path.suffix == ".kts"
    )
    path.write_text(text)

if not found:
    raise SystemExit("Tidak ditemukan file Gradle hasil generate Capacitor di folder android/")
print("Google Maven dan Maven Central resmi aktif; repo1 disiapkan sebagai fallback.")
