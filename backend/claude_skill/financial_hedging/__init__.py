"""Financial hedging Claude skill (skill definition + tool scripts)."""

import os

SKILL_DIR = os.path.dirname(__file__)
SKILL_MD_PATH = os.path.join(SKILL_DIR, "SKILL.md")


def load_skill_md() -> str:
    """Read SKILL.md from disk. Used as the system prompt for the agent."""
    with open(SKILL_MD_PATH, "r", encoding="utf-8") as fh:
        return fh.read()
