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

LINE_BUDGET = 600


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


def find_labels(block: str, label: str) -> list[int]:
    """Positions of a `Πριν:` / `Μετά:` style label, tolerating bold and spacing."""
    return [match.start() for match in re.finditer(rf"(?m)^[ \t*_]*{label}[ \t*_]*:", block)]


def has_quote_after(block: str, position: int) -> bool:
    """A blockquote follows the label, ignoring any blank lines in between."""
    for line in block[position:].splitlines()[1:]:
        if line.strip():
            return line.lstrip().startswith(">")
    return False


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
for required_key in ("name", "description"):
    require(
        required_key in frontmatter_keys,
        f"SKILL.md frontmatter must define {required_key}, found {frontmatter_keys}",
    )

skill_name_match = re.search(r"""(?m)^name:\s*["']?([a-z0-9-]+)["']?\s*$""", frontmatter)
require(skill_name_match is not None, "SKILL.md name is missing or invalid")
skill_name = skill_name_match.group(1)

description_match = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
require(description_match is not None, "SKILL.md description is missing")
description = description_match.group(1).strip().strip("\"'")
require(len(description) >= 60, f"SKILL.md description is too short ({len(description)} chars)")

pattern_matches = list(re.finditer(r"(?m)^#{2,4} *([0-9]+)[.)] ", skill))
pattern_numbers = [int(match.group(1)) for match in pattern_matches]
pattern_count = len(pattern_numbers)
require(pattern_count > 0, "SKILL.md contains no numbered patterns")
require(
    pattern_numbers == list(range(1, pattern_count + 1)),
    f"SKILL.md patterns must be numbered 1-{pattern_count} without gaps, found {pattern_numbers}",
)

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
    before_positions = find_labels(block, "Πριν")
    after_positions = find_labels(block, "Μετά")
    require(before_positions, f"Pattern {number} must have a Πριν example")
    require(after_positions, f"Pattern {number} must have a Μετά example")
    require(
        len(before_positions) == len(after_positions),
        f"Pattern {number} has {len(before_positions)} Πριν and {len(after_positions)} Μετά examples",
    )
    require(
        all(before < after for before, after in zip(before_positions, after_positions)),
        f"Pattern {number} examples are out of order",
    )
    for label, positions in (("Πριν", before_positions), ("Μετά", after_positions)):
        require(
            all(has_quote_after(block, position) for position in positions),
            f"Pattern {number} {label} example must be followed by a > blockquote",
        )

readme_numbers = {
    int(number) for number in re.findall(r"(?m)^\|\s*\**\s*([0-9]+)\s*\**\s*\|", readme)
}
require(
    readme_numbers == set(pattern_numbers),
    f"README pattern table must list patterns 1-{pattern_count}, "
    f"missing {sorted(set(pattern_numbers) - readme_numbers)}, "
    f"unexpected {sorted(readme_numbers - set(pattern_numbers))}",
)

skill_lines = len(skill.splitlines())
require(skill_lines <= LINE_BUDGET, f"SKILL.md is {skill_lines} lines, over the {LINE_BUDGET}-line portability budget")
require(
    re.search(r"github\.com/blader/humanizer", readme) is not None,
    "README must credit and link to blader/humanizer",
)
require(not (ROOT / "humanizer-el.md").exists(), "Remove the legacy humanizer-el.md file")

version_match = re.search(r"(?m)^\s*[-*#]+\s*\**([0-9]+\.[0-9]+\.[0-9]+)\**", readme)
require(version_match is not None, "README version history is missing")
readme_version = version_match.group(1)
plugin_version = str(plugin.get("version", ""))
require(readme_version == plugin_version, f"README version {readme_version} != plugin version {plugin_version}")

require(plugin.get("name") == skill_name, "Plugin and skill names do not match")
repository = str(plugin.get("repository", "")).rstrip("/")
require(
    re.fullmatch(r"https://github\.com/[\w.-]+/[\w.-]+", repository) is not None,
    f"Plugin repository must be a GitHub URL, found {repository!r}",
)
require(repository in readme, f"README installation commands must reference {repository}")
require(marketplace.get("name") == skill_name, "Marketplace and skill names do not match")
plugins = marketplace.get("plugins")
require(isinstance(plugins, list) and len(plugins) == 1, "Marketplace must expose one plugin")
require(plugins[0].get("name") == skill_name, "Marketplace plugin and skill names do not match")
require(("$" + skill_name) in openai_yaml, "agents/openai.yaml default prompt must name the skill")

print(f"Greek Writing package v{plugin_version} is valid")
