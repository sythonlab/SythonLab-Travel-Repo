#!/usr/bin/env python3
import re
import subprocess
import sys
from pathlib import Path

SETUP_FILE = Path(__file__).parent / "setup.py"


def get_current_version() -> str:
    content = SETUP_FILE.read_text()
    match = re.search(r'version="(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        print("ERROR: version not found in setup.py")
        sys.exit(1)
    return match.group(0).replace('version=', '').strip('"'), match.groups()


def bump_version(parts: tuple, part: str) -> str:
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def main():
    part = sys.argv[1] if len(sys.argv) > 1 else "patch"
    if part not in ("major", "minor", "patch"):
        print("Usage: python publish.py [major|minor|patch]")
        sys.exit(1)

    _, parts = get_current_version()
    old_version = ".".join(parts)
    new_version = bump_version(parts, part)

    content = SETUP_FILE.read_text()
    SETUP_FILE.write_text(content.replace(f'version="{old_version}"', f'version="{new_version}"'))
    print(f"Version: {old_version} → {new_version}")

    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "build", "twine"], check=True)
    subprocess.run([sys.executable, "-m", "build"], check=True)
    subprocess.run(["twine", "upload", "dist/*"], check=True)


if __name__ == "__main__":
    main()
