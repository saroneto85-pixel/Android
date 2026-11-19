#!/usr/bin/env python3
"""Add independent Maven Central mirrors to generated Capacitor Gradle files."""
from pathlib import Path

root = Path("android")
targets = [root / "build.gradle", root / "settings.gradle", root / "build.gradle.kts", root / "settings.gradle.kts"]

def add_repo(text, token, repo, kotlin):
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
    # Remove Aliyun mirrors after prior HTTP 502 errors.
    for repo in ["https://maven.aliyun.com/repository/central", "https://maven.aliyun.com/repository/google"]:
        text = text.replace(f"maven {{ url '{repo}' }}", "")
        text = text.replace(f'maven {{ url "{repo}" }}', "")
    # Use independent mirrors before the standard repositories.
    for token in ["mavenCentral()", "google()"]:
        text = add_repo(text, token, "https://repo.huaweicloud.com/repository/maven/", path.suffix == ".kts")
        text = add_repo(text, token, "https://maven-central.storage-download.googleapis.com/maven2/", path.suffix == ".kts")
    path.write_text(text)

if not found:
    raise SystemExit("Tidak ditemukan file Gradle hasil generate Capacitor di folder android/")
print("Mirror Huawei dan Google-hosted Maven Central ditambahkan; repositori resmi tetap dipertahankan.")
