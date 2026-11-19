#!/usr/bin/env python3
"""Add reliable Maven mirrors to the generated Capacitor Android Gradle project."""
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
        addition = f'maven {{ url = uri("{repo}") }}\\n        {token}'
    else:
        addition = f"maven {{ url '{repo}' }}\\n        {token}"
    return text.replace(token, addition)

found = False
for path in targets:
    if not path.exists():
        continue
    found = True
    text = path.read_text()
    kotlin = path.suffix == ".kts"
    text = add_repo(text, "mavenCentral()", "https://maven.aliyun.com/repository/central", kotlin)
    text = add_repo(text, "mavenCentral()", "https://repo1.maven.org/maven2/", kotlin)
    text = add_repo(text, "google()", "https://maven.aliyun.com/repository/google", kotlin)
    path.write_text(text)

if not found:
    raise SystemExit("Tidak ditemukan file Gradle hasil generate Capacitor di folder android/")
print("Maven Central dan Google mirror telah ditambahkan ke konfigurasi Gradle.")
