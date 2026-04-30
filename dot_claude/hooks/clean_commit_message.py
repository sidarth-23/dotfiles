#!/usr/bin/env python3
"""
Commit Message Filter Hook

Blocks:
- Any Co-authored-by trailer in any form
- Common AI-generated commit signatures
- Commit messages that do not follow basic Conventional Commit rules

Allowed:
- Subject/header longer than the usual commitlint max length
"""

import json
import re
import shlex
import sys
from pathlib import Path


ALLOWED_TYPES = {
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
}


AI_SIGNATURE_PATTERNS = [
    # Claude / Anthropic
    r"generated\s+with\s+.*claude",
    r"claude\s+code",
    r"anthropic",
    r"noreply@anthropic\.com",

    # OpenAI / ChatGPT / Codex
    r"generated\s+with\s+.*chatgpt",
    r"generated\s+with\s+.*openai",
    r"chatgpt",
    r"openai",
    r"codex",
    r"gpt-[0-9a-z.\-]+",
    r"o[0-9]+(?:-[a-z0-9]+)?",

    # Cursor / Copilot / other coding agents
    r"github\s+copilot",
    r"copilot",
    r"cursor",
    r"windsurf",
    r"codeium",
    r"tabnine",
    r"sourcegraph\s+cody",
    r"\bcody\b",
    r"replit\s+agent",
    r"devin",

    # Generic AI wording
    r"ai[-\s]?generated",
    r"generated\s+by\s+ai",
    r"generated\s+with\s+ai",
    r"written\s+by\s+ai",
]


CO_AUTHOR_PATTERN = re.compile(
    r"(^|\n)\s*co-authored-by\s*:",
    re.IGNORECASE,
)


CONVENTIONAL_HEADER_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)"
    r"(?:\([a-z0-9._/-]+\))?"
    r"(?P<breaking>!)?"
    r": "
    r"(?P<subject>.+)$"
)


def fail(message: str) -> None:
    print(f"❌ {message}", file=sys.stderr)
    sys.exit(2)


def is_git_commit_command(command: str) -> bool:
    return bool(re.search(r"(^|\s)git\s+commit(\s|$)", command))


def extract_commit_message_from_command(command: str) -> str | None:
    """
    Extract commit message from common git commit forms:
    - git commit -m "message"
    - git commit --message "message"
    - git commit -m "header" -m "body"
    - git commit -F file
    - git commit --file file

    Returns None when the message cannot be determined.
    """

    try:
        args = shlex.split(command)
    except ValueError:
        # Fallback: inspect raw command directly if shell parsing fails.
        return command

    try:
        git_index = args.index("git")
    except ValueError:
        return None

    git_args = args[git_index:]

    if len(git_args) < 2 or git_args[1] != "commit":
        return None

    messages: list[str] = []

    i = 2
    while i < len(git_args):
        arg = git_args[i]

        if arg in ("-m", "--message"):
            if i + 1 >= len(git_args):
                fail("git commit message flag was provided without a message")
            messages.append(git_args[i + 1])
            i += 2
            continue

        if arg.startswith("--message="):
            messages.append(arg.split("=", 1)[1])
            i += 1
            continue

        if arg in ("-F", "--file"):
            if i + 1 >= len(git_args):
                fail("git commit file flag was provided without a file path")

            file_path = Path(git_args[i + 1])
            try:
                messages.append(file_path.read_text(encoding="utf-8"))
            except Exception as exc:
                fail(f"Could not read commit message file: {file_path}. Error: {exc}")

            i += 2
            continue

        if arg.startswith("--file="):
            file_path = Path(arg.split("=", 1)[1])
            try:
                messages.append(file_path.read_text(encoding="utf-8"))
            except Exception as exc:
                fail(f"Could not read commit message file: {file_path}. Error: {exc}")

            i += 1
            continue

        i += 1

    if messages:
        return "\n\n".join(messages)

    return None


def remove_comment_lines(message: str) -> str:
    """
    Ignore git commit template comments.
    """
    lines = message.splitlines()
    return "\n".join(line for line in lines if not line.lstrip().startswith("#")).strip()


def check_no_co_authors(message: str) -> None:
    if CO_AUTHOR_PATTERN.search(message):
        fail("Co-authoring is prohibited in commit messages. Remove all Co-authored-by trailers.")


def check_no_ai_signature(message: str) -> None:
    for pattern in AI_SIGNATURE_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE | re.MULTILINE):
            fail(
                "Commit message contains an AI-generated identifier or signature. "
                "Use a clean custom commit message."
            )


def check_basic_commitlint(message: str) -> None:
    cleaned = remove_comment_lines(message)

    if not cleaned:
        fail("Commit message cannot be empty")

    lines = cleaned.splitlines()
    header = lines[0].strip()

    match = CONVENTIONAL_HEADER_PATTERN.match(header)
    if not match:
        fail(
            "Commit message must follow Conventional Commit format: "
            "type(scope optional): subject. Example: feat(auth): add login flow"
        )

    commit_type = match.group("type")
    subject = match.group("subject").strip()

    if commit_type not in ALLOWED_TYPES:
        fail(
            "Invalid commit type. Allowed types: "
            + ", ".join(sorted(ALLOWED_TYPES))
        )

    if not subject:
        fail("Commit subject cannot be empty")

    if subject.endswith("."):
        fail("Commit subject should not end with a period")

    if subject[0].isupper():
        fail("Commit subject should start with lowercase text")

    # Intentionally NOT enforcing subject/header max length.


def check_commit_message(command: str) -> None:
    if not is_git_commit_command(command):
        return

    message = extract_commit_message_from_command(command)

    if message is None:
        fail(
            "Could not inspect commit message. Use git commit -m or git commit -F "
            "so the message can be validated."
        )

    check_no_co_authors(message)
    check_no_ai_signature(message)
    check_basic_commitlint(message)


def main() -> None:
    try:
        tool_use_json = sys.stdin.read()
        tool_use = json.loads(tool_use_json)
    except json.JSONDecodeError as exc:
        fail(f"Invalid hook input JSON: {exc}")

    if tool_use.get("tool_name") != "Bash":
        sys.exit(0)

    command = tool_use.get("tool_input", {}).get("command", "")
    check_commit_message(command)

    sys.exit(0)


if __name__ == "__main__":
    main()