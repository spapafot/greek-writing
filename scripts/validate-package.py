#!/usr/bin/env python3
"""Validate the Greek Writing package without external dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = ROOT / "SKILL.md"
README_PATH = ROOT / "README.md"
PLUGIN_PATH = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".claude-plugin" / "marketplace.json"
OPENAI_PATH = ROOT / "agents" / "openai.yaml"


def fail(message: str) -> None:
    raise SystemExit(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        fail(f"{path.relative_to(ROOT)} is not valid UTF-8: {error}")


for required_path in (
    SKILL_PATH,
    README_PATH,
    PLUGIN_PATH,
    MARKETPLACE_PATH,
    OPENAI_PATH,
    ROOT / "AGENTS.md",
    ROOT / "LICENSE",
):
    require(required_path.is_file(), f"Missing required file: {required_path.relative_to(ROOT)}")

skill = read_text(SKILL_PATH)
readme = read_text(README_PATH)
openai_yaml = read_text(OPENAI_PATH)
plugin = json.loads(read_text(PLUGIN_PATH))
marketplace = json.loads(read_text(MARKETPLACE_PATH))

frontmatter_match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
require(frontmatter_match is not None, "SKILL.md must start with YAML frontmatter")
frontmatter = frontmatter_match.group(1)
frontmatter_keys = re.findall(r"(?m)^([a-z][a-z0-9_-]*):", frontmatter)
require(
    frontmatter_keys == ["name", "description"],
    f"SKILL.md frontmatter must contain only name and description, found {frontmatter_keys}",
)

skill_name_match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", frontmatter)
require(skill_name_match is not None, "SKILL.md name is missing or invalid")
skill_name = skill_name_match.group(1)
require(skill_name == "greek-writing", f"Unexpected skill name: {skill_name}")

description_match = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
require(description_match is not None, "SKILL.md description is missing")
require(len(description_match.group(1).strip()) >= 80, "SKILL.md description is too short")

pattern_numbers = [
    int(number) for number in re.findall(r"(?m)^### ([0-9]+)\. ", skill)
]
require(
    pattern_numbers == list(range(1, 38)),
    f"Expected patterns 1-37 in SKILL.md, found {pattern_numbers}",
)

pattern_matches = list(re.finditer(r"(?m)^### ([0-9]+)\. ", skill))
for index, pattern_match in enumerate(pattern_matches):
    block_start = pattern_match.start()
    block_end = (
        pattern_matches[index + 1].start()
        if index + 1 < len(pattern_matches)
        else skill.find("\n## ", pattern_match.end())
    )
    if block_end == -1:
        block_end = len(skill)
    block = skill[block_start:block_end]
    number = pattern_match.group(1)
    before_marker = "\nΠριν:\n>"
    after_marker = "\nΜετά:\n>"
    require(block.count(before_marker) == 1, f"Pattern {number} must have one Πριν example")
    require(block.count(after_marker) == 1, f"Pattern {number} must have one Μετά example")
    require(block.index(before_marker) < block.index(after_marker), f"Pattern {number} examples are out of order")

readme_numbers = {
    int(number) for number in re.findall(r"(?m)^\|\s*([0-9]+)\s*\|", readme)
}
require(
    readme_numbers == set(range(1, 38)),
    "README pattern table must contain patterns 1-37",
)

require(len(skill.splitlines()) <= 500, "SKILL.md exceeds the 500-line portability budget")
require(
    "[blader's Humanizer](https://github.com/blader/humanizer)" in readme,
    "README must credit and link to blader/humanizer",
)
require(
    "https://github.com/spapafot/greek-writing" in readme,
    "README installation commands must use the package repository",
)
require(not (ROOT / "humanizer-el.md").exists(), "Remove the legacy humanizer-el.md file")

version_match = re.search(r"(?m)^- \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*", readme)
require(version_match is not None, "README version history is missing")
readme_version = version_match.group(1)
plugin_version = str(plugin.get("version", ""))
require(readme_version == plugin_version, "README and plugin versions do not match")

require(plugin.get("name") == skill_name, "Plugin and skill names do not match")
require(plugin.get("repository") == "https://github.com/spapafot/greek-writing", "Plugin repository is incorrect")
require(marketplace.get("name") == skill_name, "Marketplace and skill names do not match")
plugins = marketplace.get("plugins")
require(isinstance(plugins, list) and len(plugins) == 1, "Marketplace must expose one plugin")
require(plugins[0].get("name") == skill_name, "Marketplace plugin and skill names do not match")
require(("$" + skill_name) in openai_yaml, "agents/openai.yaml default prompt must name the skill")

print(f"Greek Writing package v{plugin_version} is valid")
